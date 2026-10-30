#!/usr/bin/env python3
"""Validate and capture a locally served Academic Pages site.

Usage:
  python3 scripts/preview_site.py --url http://127.0.0.1:4000
  python3 scripts/preview_site.py --browser /usr/bin/google-chrome

Start Jekyll separately. Screenshots and report.json are written to --output-dir.
GIFs and videos are frozen at frame zero for captures; autoplay is checked
separately on freshly loaded pages without calling play().
"""

import argparse
from datetime import datetime, timezone
from io import BytesIO
import json
from pathlib import Path
from urllib.parse import urldefrag, urljoin, urlsplit
from urllib.request import urlopen

from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
PAGES = ("/", "/publications/", "/cv/")
VIEWPORTS = {"desktop": (1440, 1050), "tablet": (768, 1024), "mobile": (390, 844)}


def freeze_videos(page):
    """Capture a deterministic decoded frame, without changing the live site."""
    page.wait_for_function(
        "Array.from(document.querySelectorAll('video')).every(video => video.readyState >= 2)"
    )
    page.locator("video").evaluate_all("""async videos => {
        await Promise.all(videos.map(async video => {
            video.pause();
            if (video.currentTime !== 0) {
                await new Promise(resolve => {
                    video.addEventListener('seeked', resolve, {once: true});
                    video.currentTime = 0;
                });
            }
        }));
    }""")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default="http://127.0.0.1:4000")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "tmp/previews")
    parser.add_argument("--browser", help="Path to an installed Chromium executable")
    args = parser.parse_args()
    if urlsplit(args.url).hostname not in ("127.0.0.1", "localhost", "::1"):
        parser.error("Use a local preview URL.")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    origin = args.url.rstrip("/")
    report = {
        "url": origin,
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "viewports": VIEWPORTS,
        "gif_frame": 0,
        "video_frame": 0,
        "pages": [],
        "screenshots": [],
        "videos": [],
        "cancelled_media_requests": [],
        "errors": [],
    }

    def freeze_gif(route):
        with urlopen(route.request.url) as response:
            with Image.open(BytesIO(response.read())) as image:
                output = BytesIO()
                image.seek(0)
                image.convert("RGBA").save(output, format="PNG")
        route.fulfill(body=output.getvalue(), content_type="image/png")

    def request_failed(request):
        # Navigating or seeking cancels buffered media ranges. Actual media
        # availability and autoplay are validated separately below.
        if request.resource_type == "media" and request.failure == "net::ERR_ABORTED":
            report["cancelled_media_requests"].append(request.url)
        else:
            report["errors"].append(f"Request failed: {request.url}: {request.failure}")

    with sync_playwright() as playwright:
        launch = {"headless": True}
        if args.browser:
            launch["executable_path"] = args.browser
        browser = playwright.chromium.launch(**launch)
        report["browser_version"] = browser.version
        context = browser.new_context(
            viewport={"width": 1440, "height": 1050},
            device_scale_factor=1,
            reduced_motion="reduce",
            color_scheme="light",
            locale="en-US",
            timezone_id="America/New_York",
        )
        context.route("**/*.gif", freeze_gif)
        page = context.new_page()
        page.on("pageerror", lambda error: report["errors"].append(str(error)))
        page.on("console", lambda message: report["errors"].append(message.text)
                if message.type == "error" else None)
        page.on("requestfailed", request_failed)
        page.on("response", lambda response: report["errors"].append(
            f"HTTP {response.status}: {response.url}"
        ) if response.status >= 400 else None)
        try:
            pending = [urljoin(origin, path) for path in (*PAGES, "/sitemap/")]
            visited, resources = set(), set()
            while pending:
                address = pending.pop(0)
                if address in visited:
                    continue
                visited.add(address)
                response = page.goto(address, wait_until="networkidle")
                assert response and response.ok, f"Page failed: {address}"
                page.locator("img").evaluate_all("""async nodes => {
                    await Promise.all(nodes.map(async image => {
                        image.loading = 'eager';
                        await image.decode();
                    }));
                }""")
                assert page.locator("h1").count() == 1, f"Expected one title: {address}"
                text = page.locator("body").inner_text()
                for unwanted in (
                    "Your Name", "Your Sidebar Name", "Blog Posts",
                    "Benchmarking State Estimation Algorithms",
                ):
                    assert unwanted not in text, f"Unexpected content: {unwanted}"
                nav = page.locator("#site-nav").inner_text()
                assert all(label not in nav for label in ("Talks", "Teaching", "Projects"))
                assert page.locator("video").evaluate_all("""videos => videos.every(video =>
                    !video.controls && video.autoplay && video.muted && video.loop &&
                    video.playsInline && video.disablePictureInPicture &&
                    video.disableRemotePlayback
                )"""), f"Video should autoplay silently without controls: {address}"
                if urlsplit(address).path.startswith("/publications/") and urlsplit(address).path != "/publications/":
                    assert page.locator(".page__date, meta[itemprop='datePublished'], meta[property='article:published_time']").count() == 0, (
                        f"Generated file date shown as publication date: {address}"
                    )
                for href in page.locator("a[href]").evaluate_all(
                    "(nodes) => nodes.map(n => n.href)"
                ):
                    target = urldefrag(href).url
                    if urlsplit(target).netloc == urlsplit(origin).netloc:
                        path = urlsplit(target).path
                        if path.endswith("/") or path.endswith(".html"):
                            if target not in visited:
                                pending.append(target)
                        else:
                            resources.add(target)
                for source in page.locator("img[src], source[src], video[poster]").evaluate_all(
                    "(nodes) => nodes.map(n => n.poster || n.src)"
                ):
                    resources.add(source)
                broken = page.locator("img").evaluate_all(
                    "(nodes) => nodes.filter(n => !n.complete || !n.naturalWidth).map(n => n.src)"
                )
                assert not broken, f"Broken images: {broken}"
                report["pages"].append(address)

            for address in sorted(resources):
                response = context.request.head(address)
                assert response.ok, f"Resource failed: {address}"
            report["resources_checked"] = len(resources)

            for device, (width, height) in VIEWPORTS.items():
                page.set_viewport_size({"width": width, "height": height})
                for path in PAGES:
                    page.goto(origin + path, wait_until="networkidle")
                    page.locator("img").evaluate_all("""async nodes => {
                        await Promise.all(nodes.map(async image => {
                            image.loading = 'eager';
                            await image.decode();
                        }));
                    }""")
                    page.evaluate("document.fonts.ready")
                    overflow = page.evaluate(
                        "document.documentElement.scrollWidth > window.innerWidth + 1"
                    )
                    name = path.strip("/").replace("/", "-") or "about"
                    screenshot = args.output_dir / f"{name}-{device}.png"
                    freeze_videos(page)
                    page.screenshot(path=str(screenshot), full_page=True, animations="disabled")
                    report["screenshots"].append(str(screenshot))
                    assert not overflow, f"Horizontal overflow at {width}px: {path}"
                    avatar = page.locator(".author__avatar img").first
                    shape = avatar.evaluate("""img => ({
                        width: img.getBoundingClientRect().width,
                        height: img.getBoundingClientRect().height,
                        radius: getComputedStyle(img).borderRadius,
                        naturalWidth: img.naturalWidth,
                        naturalHeight: img.naturalHeight
                    })""")
                    assert abs(shape["width"] - shape["height"]) < 1, shape
                    assert shape["radius"] == "50%", shape
                    assert shape["naturalWidth"] == shape["naturalHeight"] == 800, shape
                    for video in page.locator("video").all():
                        shape = video.evaluate("""video => ({
                            width: video.getBoundingClientRect().width,
                            height: video.getBoundingClientRect().height,
                            ratio: Number(video.width) / Number(video.height)
                        })""")
                        assert abs(shape["height"] - shape["width"] / shape["ratio"]) < 1, (
                            f"Video frame proportions changed at {width}px: {path}", shape
                        )

            page.set_viewport_size({"width": 390, "height": 844})
            page.goto(origin, wait_until="networkidle")
            menu = page.get_by_role("button", name="More pages")
            if menu.is_visible():
                menu.click()
                assert menu.get_attribute("aria-expanded") == "true"
                page.locator("#more-pages a").last.click()
                assert page.url != origin + "/"
            page.goto(origin, wait_until="networkidle")
            contact = page.get_by_role("button", name="Contact", exact=True)
            if contact.is_visible():
                contact.click()
                page.locator("#author-links").wait_for(state="visible")
                assert contact.get_attribute("aria-expanded") == "true"
            theme = page.get_by_role("button", name="Toggle dark mode")
            theme.focus()
            page.keyboard.press("Enter")
            assert page.locator("html").get_attribute("data-theme") == "dark"
            freeze_videos(page)
            page.screenshot(
                path=str(args.output_dir / "about-mobile-dark.png"),
                full_page=True, animations="disabled",
            )
            page.reload(wait_until="networkidle")
            assert page.locator("html").get_attribute("data-theme") == "dark"
            page.get_by_role("button", name="Toggle dark mode").click()

            page.set_viewport_size({"width": 1440, "height": 1050})
            for path in ("/publications/hulk/", "/publications/whole-body-dexterity/",
                         "/publications/hydroshear/", "/publications/bimanual-manipulation/"):
                page.goto(origin + path, wait_until="networkidle")
                for video in page.locator("video").all():
                    video.scroll_into_view_if_needed()
                    page.wait_for_function(
                        "video => !video.paused && video.currentTime > 0 && video.readyState >= 2",
                        arg=video.element_handle(),
                    )
                    details = video.evaluate("""async video => {
                        const start = video.currentTime;
                        await new Promise(resolve => setTimeout(resolve, 400));
                        if (video.paused || video.currentTime === start)
                            throw new Error("Video did not autoplay: " + video.currentSrc);
                        if (!video.videoWidth || !video.videoHeight || video.error)
                            throw new Error("Video failed to decode: " + video.currentSrc);
                        return {src: video.currentSrc, width: video.videoWidth,
                            height: video.videoHeight, duration: video.duration,
                            autoplay: video.autoplay, controls: video.controls};
                    }""")
                    if path == "/publications/bimanual-manipulation/":
                        assert (details["width"], details["height"]) == (948, 774), details
                        assert abs(details["duration"] - 7.5) < 0.05, details
                    if urlsplit(details["src"]).path == "/videos/hulk-power-clean.mp4":
                        assert abs(details["duration"] - 11) < 0.05, details
                    report["videos"].append(details)
                page.reload(wait_until="networkidle")
                name = path.strip("/").replace("/", "-")
                freeze_videos(page)
                page.screenshot(
                    path=str(args.output_dir / f"{name}-desktop.png"),
                    full_page=True, animations="disabled",
                )
            assert len(visited) >= 10, f"Missing pages: {visited}"
            assert not report["errors"], report["errors"]
            report["result"] = "passed"
        except Exception as error:
            report["result"] = "failed"
            report["errors"].append(str(error))
            page.screenshot(path=str(args.output_dir / "failure.png"), full_page=True)
            raise
        finally:
            (args.output_dir / "report.json").write_text(json.dumps(report, indent=2) + "\n")
            browser.close()
    print(f"Passed: {len(report['pages'])} pages, {report['resources_checked']} resources, "
          f"{len(report['videos'])} videos, desktop/tablet/mobile checks.")
    print(f"Previews: {args.output_dir}")


if __name__ == "__main__":
    main()

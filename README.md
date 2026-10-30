# An Dang's academic website

Website template yoinked from [Academic Pages](https://academicpages.github.io/).
Built with Jekyll. Navigation contains About, Publications, and CV. Talks, Teaching,
Blog Posts, and Projects have no pages or collections.

## Local preview

Use Ruby 3.3 (see `.ruby-version`), Bundler, and Node.js 24:

```sh
bundle install
npm ci
npm run build
bundle exec jekyll serve --host 127.0.0.1
```

Open `http://127.0.0.1:4000`. The homepage is authored in `index.md`;
Jekyll produces `_site/index.html`. Source pages need a Jekyll build.

For a production build:

```sh
JEKYLL_ENV=production bundle exec jekyll build
```

## Editing content

- `index.md`: biography, dated news, and selected research.
- `_config.yml`: author sidebar, contact links, and site settings.
- `_data/navigation.yml`: top navigation.
- `_publications/*.md`: one file per publication. Set `featured: true` to show
  an entry on the homepage; `order` controls listing order.
- `_pages/cv.md`: education and work experience. The publication list is
  generated from the same collection as the Publications page.
- `_sass/_custom.scss`: local additions to the Academic Pages styling.

The CV follows the compact education, date-first experience, and publication
lists of [Miquel Oller's CV](https://mr-mikmik.github.io/cv/).
Publication dates and education details incorporate the owner's corrections.

## Browser checks and screenshots

The maintained `scripts/preview_site.py` command checks local pages, links,
images, the circular profile crop, navigation, dark mode, and video playback.
It writes desktop, tablet, and mobile screenshots:

```sh
python3 -m pip install -r scripts/requirements-preview.txt
python3 -m playwright install chromium
python3 scripts/preview_site.py --url http://127.0.0.1:4000 --output-dir tmp/previews
```

Use `--browser /path/to/chrome` for an already installed Chromium browser.
Screenshot provenance and results are written to `report.json`.
GIFs and videos are frozen at their first frame for repeatable captures.
Autoplay is checked separately without calling `play()`. Browser and font
versions can still affect rendering.

## Research media

Publication demonstrations are stored locally and autoplay silently in a loop,
with no playback controls. Source URLs and SHA-256
checksums for downloaded assets are in `media-sources.json`. The cart and
Whole-Body Dexterity clips are unmodified copies. HydroShear's complete title
video is compressed for the web with its framing, duration, and speed preserved.
The HULK power-clean preview uses the first 11 seconds at the original speed.

```sh
python3 scripts/fetch_media.py
python3 scripts/fetch_media.py --verify
```

To reproduce HydroShear's web video and poster (requires FFmpeg):

```sh
python3 scripts/prepare_video.py
```

The large original lives in ignored `media/sources/`; it can be downloaded
again with `fetch_media.py`. The maintained preparation script writes the
encoding commands, tool version, and output hashes to `media/hydroshear.json`.

To reproduce the power-clean clip, place the supplied
`DJI_20261027160719_0475_D (1).MP4` at `media/sources/hulk-power-clean.MP4`, then:

```sh
python3 scripts/prepare_video.py \
  --source media/sources/hulk-power-clean.MP4 \
  --output videos/hulk-power-clean.mp4 \
  --poster images/hulk-power-clean.jpg \
  --report media/hulk-power-clean.json \
  --duration 11 \
  --poster-time 4
```

When intentionally adding a new source, use `--record-hashes` once to record
its checksum. See `CONTENT_SOURCES.md` for content provenance.

### Bimanual Dual Limit Surfaces preview

The publication uses the right-hand simulation from the supplied
[YouTube video](https://www.youtube.com/watch?v=sUok_EjFdDU), through 2:46.
The requested range begins at 2:30 with a black transition; the prepared clip
starts at 2:31, when the simulation is visible. Its 948 × 774 crop removes the
comparison panel, title text, and black borders without stretching the image.
It plays at 2× speed, making the 15-second source excerpt 7.5 seconds long.

Download the original 1080p video stream (prepared with `yt-dlp==2026.10.26`):

```sh
yt-dlp --no-playlist --format 137 \
  --output 'media/sources/bimanual-dual-limit-surfaces.%(ext)s' \
  'https://www.youtube.com/watch?v=sUok_EjFdDU'
```

Inspect source frames and reproduce the clip and poster:

```sh
python3 scripts/prepare_video.py \
  --source media/sources/bimanual-dual-limit-surfaces.mp4 \
  --inspect-at 150 151 154 158 162 165.9 \
  --inspect-dir tmp/dual-limit-source

python3 scripts/prepare_video.py \
  --source media/sources/bimanual-dual-limit-surfaces.mp4 \
  --source-url 'https://www.youtube.com/watch?v=sUok_EjFdDU' \
  --start 151 --duration 15 --crop 948 774 966 252 --mute --speed 2 \
  --poster-time 1.5 \
  --output videos/bimanual-dual-limit-surfaces.mp4 \
  --poster images/bimanual-dual-limit-surfaces.jpg \
  --report media/bimanual-dual-limit-surfaces.json
```

The preparation report records source/output hashes, crop, timestamps, and
encoding commands. The original remains in ignored `media/sources/`.
The browser workflow verifies clip decoding, duration, and display proportions.

## GitHub Pages

`.github/workflows/pages.yml` builds pull requests and deploys pushes to `main`.
Select **GitHub Actions** under **Settings → Pages → Build and deployment → Source**
to use only this workflow and avoid running the legacy branch build alongside it.

## Profile photo

`images/sources/an-dang-speaking.png` is the supplied `linkedin-square.png`
reference (800 × 800 pixels). Its zoom and position are preserved exactly.
Academic Pages applies the circular mask in the sidebar.

```sh
python3 -m pip install Pillow==12.3.0
python3 scripts/crop_profile.py
```

Add `--preview /tmp/an-dang-profile-circle.png` for a standalone 192-pixel
circular preview. The sidebar uses the theme's own responsive display size.
Source images and tooling are excluded from the generated site.

See `THIRD_PARTY.md` and `LICENSE` for template provenance and licensing.

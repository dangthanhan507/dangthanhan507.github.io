#!/usr/bin/env python3
"""Prepare a web video and poster, or inspect source frames before cropping.

Default input is HydroShear's title video, downloaded with fetch_media.py.
Requires ffmpeg and ffprobe. Outputs and encoding provenance are reproducible
with the same ffmpeg version. By default, framing and duration are preserved.

Examples:
  python3 scripts/prepare_video.py
  python3 scripts/prepare_video.py --source input.mp4 --inspect-at 150 158 165
  python3 scripts/prepare_video.py --source input.mp4 --start 150 --duration 16 \\
      --crop 940 700 970 190 --mute --output videos/demo.mp4 \\
      --poster images/demo.jpg --report media/demo.json

Crop coordinates are WIDTH HEIGHT X Y in source pixels, before scaling.
--duration always refers to source time; --speed changes playback speed.
Poster timestamps are relative to the prepared clip. Inspection timestamps
are relative to the source, and --inspect-at only extracts inspection frames.
"""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def metadata(path):
    return json.loads(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries",
        "stream=codec_name,codec_type,width,height:format=duration,size",
        "-of", "json", str(path),
    ]))


def record_command(command):
    return [part.replace(str(ROOT) + "/", "") for part in command]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=ROOT / "media/sources/hydroshear-title.mp4")
    parser.add_argument("--output", type=Path, default=ROOT / "videos/hydroshear.mp4")
    parser.add_argument("--poster", type=Path, default=ROOT / "images/hydroshear.jpg")
    parser.add_argument("--report", type=Path, default=ROOT / "media/hydroshear.json")
    parser.add_argument("--width", type=int, default=1280, help="Maximum output width; no upscaling")
    parser.add_argument("--crf", type=int, default=24, help="H.264 quality (0–51, lower is higher quality)")
    parser.add_argument("--poster-time", type=float, default=1.0, help="Poster timestamp in seconds")
    parser.add_argument("--start", type=float, default=0, help="Clip start in source seconds")
    parser.add_argument("--duration", type=float, help="Clip duration in seconds; default is to the end")
    parser.add_argument("--speed", type=float, default=1.0,
                        help="Playback speed from 0.5 to 2; 2 makes the clip twice as fast")
    parser.add_argument("--crop", nargs=4, type=int, metavar=("WIDTH", "HEIGHT", "X", "Y"),
                        help="Crop rectangle in source pixels before scaling")
    parser.add_argument("--mute", action="store_true", help="Omit audio from the prepared clip")
    parser.add_argument("--source-url", help="Original public source URL for the provenance report")
    parser.add_argument("--inspect-at", nargs="+", type=float, metavar="SECONDS",
                        help="Extract source frames at these times and exit without encoding")
    parser.add_argument("--inspect-dir", type=Path, default=ROOT / "tmp/video-inspection",
                        help="Directory for inspection frames and their provenance")
    args = parser.parse_args()
    if args.width < 2 or not 0 <= args.crf <= 51 or args.poster_time < 0:
        parser.error("Invalid width, CRF, or poster timestamp")
    if not 0.5 <= args.speed <= 2:
        parser.error("Playback speed must be between 0.5 and 2")
    source_metadata = metadata(args.source)
    source_video = next(stream for stream in source_metadata["streams"]
                        if stream["codec_type"] == "video")
    source_duration = float(source_metadata["format"]["duration"])
    ffmpeg_version = subprocess.check_output(["ffmpeg", "-version"], text=True).splitlines()[0]
    if args.inspect_at is not None:
        if any(not 0 <= time < source_duration for time in args.inspect_at):
            parser.error("Inspection timestamps must be within the source duration")
        args.inspect_dir.mkdir(parents=True, exist_ok=True)
        frames = []
        for time in args.inspect_at:
            output = args.inspect_dir / f"frame-{time:010.3f}.jpg"
            command = [
                "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                "-ss", str(time), "-i", str(args.source),
                "-frames:v", "1", "-q:v", "2", "-threads", "1", str(output),
            ]
            subprocess.run(command, check=True)
            frames.append({"time": time, "command": record_command(command),
                           "sha256": digest(output)})
        (args.inspect_dir / "report.json").write_text(json.dumps({
            "source_sha256": digest(args.source), "source_url": args.source_url,
            "ffmpeg": ffmpeg_version, "source_metadata": source_metadata, "frames": frames,
        }, indent=2) + "\n")
        print(f"Inspected {len(frames)} source frames in {args.inspect_dir}")
        return
    if not 0 <= args.start < source_duration:
        parser.error("Clip start must be within the source duration")
    clip_duration = args.duration if args.duration is not None else source_duration - args.start
    if clip_duration <= 0 or args.start + clip_duration > source_duration + 0.05:
        parser.error("Clip duration must be positive and within the source duration")
    output_duration = clip_duration / args.speed
    if args.poster_time >= output_duration:
        parser.error("Poster timestamp must be within the prepared clip")
    outputs = [args.source, args.output, args.poster, args.report]
    if len({path.resolve() for path in outputs}) != len(outputs):
        parser.error("Source, output, poster, and report paths must differ")
    filters = []
    if args.speed != 1:
        filters += [f"trim=duration={clip_duration}",
                    f"setpts=(PTS-STARTPTS)/{args.speed}"]
    if args.crop:
        width, height, x, y = args.crop
        if (width < 2 or height < 2 or x < 0 or y < 0
                or x + width > source_video["width"]
                or y + height > source_video["height"]
                or any(value % 2 for value in args.crop)):
            parser.error("Crop must use even coordinates and fit within the source frame")
        filters.append(f"crop={width}:{height}:{x}:{y}")
    filters.append(f"scale='min({args.width},iw)':-2")
    for output in (args.output, args.poster, args.report):
        output.parent.mkdir(parents=True, exist_ok=True)
    encode = [
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-ss", str(args.start), "-i", str(args.source),
    ]
    if args.duration is not None or args.speed != 1:
        encode += ["-t", str(output_duration)]
    encode += ["-map", "0:v:0"]
    if args.mute:
        encode += ["-an"]
    else:
        encode += ["-map", "0:a?", "-c:a", "aac", "-b:a", "128k"]
        if args.speed != 1 and any(stream["codec_type"] == "audio"
                                   for stream in source_metadata["streams"]):
            encode += ["-af", f"atrim=duration={clip_duration},"
                       f"asetpts=PTS-STARTPTS,atempo={args.speed}"]
    encode += [
        "-vf", ",".join(filters),
        "-c:v", "libx264", "-preset", "medium", "-crf", str(args.crf),
        "-pix_fmt", "yuv420p", "-threads", "1",
        "-map_metadata", "-1", "-movflags", "+faststart", str(args.output),
    ]
    poster = [
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-ss", str(args.poster_time), "-i", str(args.output),
        "-frames:v", "1", "-q:v", "2", "-threads", "1", str(args.poster),
    ]
    subprocess.run(encode, check=True)
    subprocess.run(poster, check=True)
    args.report.write_text(json.dumps({
        "source_sha256": digest(args.source),
        "source_url": args.source_url,
        "source_metadata": source_metadata,
        "output_sha256": digest(args.output),
        "poster_sha256": digest(args.poster),
        "ffmpeg": ffmpeg_version,
        "edit": {"start": args.start, "duration": clip_duration,
                 "speed": args.speed, "output_duration": output_duration,
                 "crop": args.crop, "mute": args.mute, "poster_time": args.poster_time},
        "encode_command": record_command(encode),
        "poster_command": record_command(poster),
        "metadata": metadata(args.output),
    }, indent=2) + "\n")
    print(f"Prepared {args.output} ({args.output.stat().st_size:,} bytes)")
    print(f"Poster: {args.poster}; provenance: {args.report}")


if __name__ == "__main__":
    main()

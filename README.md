# Video cutter

Simple video cutter using a timestamp input text file an ffmpeg to cut the video

```shell
cutVideo.py video_file timestamp
```

The timestamp file have to follow thins syntax

```csv
time;title
```

The script auto add a numeration before the title on the timestamp file.
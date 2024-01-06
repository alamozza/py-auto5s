# auto5s-photo-movie

## functions

- move the files info a directory whose name is the file creation date.
- In the cases of `.jpg`, `.jpeg`, use exif info.
- In the cases of `.mp4`, use ffmpeg info.
- In the other cases, use file creation date info.

## env

- linux
- python3.11

## how to run

```
$ git clone 
$ cd 
# edit srcpath(source path) and tgtpath(target directory) in auto5s.py
$ python3 auto5s.py
```

## remarks

- the date information for directory name is 8 digits, YYYYmmdd.
- if there's already a directory on the target directory whose name 
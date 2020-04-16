# Photo Finder

Trawls through a given directory tree and sorts things out, from something like this:

```
messyFolder
├ file1.png
├ folder1
| ├ file3.png
| └ innerfolder
|   └ file2.png
├ folder2
| ├ file5.png
| └ document.pdf
└ folder3
  ├ file6.png
  ├ file7.png
  └ folder4
    └ file4.png
```

Into something like this:

```
neatFolder
├ photos
| ├ 2015
| | └ 01-January
| |   ├ 03
| |   | ├ file1.png
| |   | └ file2.png
| |   └ 25
| |     └ file3.png
| └ 2016
|   ├ 05-May
|   | └ 28
|   |   ├ file4.png
|   |   └ file5.png
|   └ 12-December
|     └ 25
|       ├ file6.png
|       └ file7.png
└ documents
  └ 2018
    └ 10-October
      └ 23
        └ document.pdf
```

It does this based on either the exif `photo taken` date or the `created date` metadata read from the files.

## How Do?

just run `python main.py` and it'll ask where you want to move from and to.

- It uses a mapping defined in `fileTypeMapping.json` to work out what folders to put each file type into
  - eg. group `.png`, `.jpg` and `.bmp` files as images, group `.mkv` and `.mp4` as movies, etc.)
  - modify `fileTypeMapping.json` to organise file types how you want
  - any file types not mapped will be treated as `unknown`
- Any files that encounter errors when moving will have the details logged to `error.log`
 
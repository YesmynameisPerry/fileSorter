# Photo Finder

trawls through a given directory tree and sorts things out, from something like this:

```
root
├ file1.png
├ folder1
| ├ file3.png
| └ innerfolder
|   └ file2.png
├ folder2
| └ file5.png
└ folder3
  ├ file6.png
  ├ file7.png
  └ folder4
    └ file4.png
```

to something like this:

```
photos
├ year1
| ├ file1.png
| ├ file2.png
| └ file3.png
└ year2
  ├ file4.png
  ├ file5.png
  ├ file6.png
  └ file7.png
```

based on the `created date` metadata that is part of the files.

## Features 

 - Can sort into years or years/months.
 - User defined file type mapping (eg. treat `.png`, `.jpg` and `.bmp` files as the same 'image' type, treat `.mov` and `.mp4` as 'movies', etc.)
 - User defined 'search' and 'output' folders (enables easy running on the leftovers of a previous run to inlcude more filetypes)
 - Can either keep filenames the same, filenames are the path, filenames are the created date with or without a random string appended (to deal with duplicates)
 
 ## To do
 
  - User defined save file input and output (skip changing settings)
  - Make the settings actually do what they should
  - Cleanup & refactor
  - Maybe multi thread if I can be bothered
  - Public?

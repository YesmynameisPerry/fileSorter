# Photo Finder

Trawls through a given directory tree and sorts things out, from something like this:

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

Into something like this:

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

It does this based on the `created date` metadata read from the files.

## How Do?

`python main.py` and then have fun (make sure you're using python 3 because lordy there are lots of hint types which will break python 2)

## Features 

- User defined file type mapping (eg. treat `.png`, `.jpg` and `.bmp` files as the same 'image' type, treat `.mov` and `.mp4` as 'movies', etc.)
- User defined 'input' and 'output' folders (enables easy running on the leftovers of a previous run to inlcude more filetypes)
- Logs any errors to a helpful lil file
 
## To do

- Remove the folder tree once all files are gone
- Can either keep filenames the same, filenames are the path, filenames are the created date with or without a random string appended (to deal with duplicates)
- Can sort into years or years/months (make it an editable setting).
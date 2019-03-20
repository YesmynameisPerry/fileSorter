# Settings

# File types (add new file extensions here to map them to the correct folder)

SETTING_MAPPING = {
    "documets": [
        "doc",
        "docx",
        "xls",
        "xlsx",
        "ppt",
        "pptx",
        "pdf",
        "csv",
        "odt"
    ],
    "photos": [
        "png",
        "jpg",
        "jpeg",
        "bmp",
        "gif"
    ],
    "videos": [
        "mov",
        "mp4",
        "m4a",
        "flv",
        "avi",
        "wmv",
        "mkv"
    ]
}

# Divide photos in "year" folders into "month" folders.

SETTING_MONTHS = True

# Change the filename settings
# Has to be a number between 0 and 3:
# 0 -> do not change file names
# 1 -> change the filename to be the full original path of the file
# 2 -> change the filename to the "created date" of the file
# 3 -> change the filename to the "created date" and a random string of characters (in case of duplicates)

SETTING_RENAME = 0

# Automatically start sorting through files once the number of files is known
# Has to be either True or False

SETTING_AUTOSTART = True
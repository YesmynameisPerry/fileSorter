# rename file settings

CONST_RENAME_NO_TOUCH = "not change the filename"
CONST_RENAME_FULL_PATH = "include the original full path in the filename"
CONST_RENAME_CREATED_DATE = "become the created date of the file"
CONST_RENAME_CREATED_DATE_WITH_RANDOM = "become the created date of the file and a random 5 character word"

CONST_RENAME_LIST = [
  CONST_RENAME_NO_TOUCH,
  CONST_RENAME_FULL_PATH,
  CONST_RENAME_CREATED_DATE,
  CONST_RENAME_CREATED_DATE_WITH_RANDOM
]

# settings file strings
CONST_SETTING_STRING_1 = "# Settings\n\n# File types (add new file extensions here to map them to the correct folder)\n\nSETTING_MAPPING = "
CONST_SETTING_STRING_2 = "\n\n# Divide photos in \"year\" folders into \"month\" folders.\n\nSETTING_MONTHS = "
CONST_SETTING_STRING_3 = "\n\n# Change the filename settings\n# Has to be a number between 0 and 3:\n# 0 -> do not change file names\n# 1 -> change the filename to be the full original path of the file\n# 2 -> change the filename to the \"created date\" of the file\n# 3 -> change the filename to the \"created date\" and a random string of characters (in case of duplicates)\n\nSETTING_RENAME = "
CONST_SETTING_STRING_4 = "\n\n# Copy or move the files from the source to the destination\n# Has to be either CONST_MOVE or CONST_COPY\n\nSETTING_COPY_OR_MOVE = "

# internal logic constants
CONST_NOT_KNOWN = "unknown command or value yay"
CONST_ADD = "add"
CONST_DELETE = "delete"
CONST_YES = "yis"
CONST_NO = "nope"

# user shown constants
CONST_UNKNOWN_OPERATION = "hey so i don't know what you want from that"
CONST_CURRENT_MAPPING_OK = "Is the current file mapping ok?"

# move or copy constants
CONST_MOVE = "move"
CONST_COPY = "copy"
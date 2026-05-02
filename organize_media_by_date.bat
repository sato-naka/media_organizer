@echo off

set SRC=.\Camera
set OUT=output

exiftool -P -r ^
 "-Directory<DateTimeOriginal" -d %OUT%/%%Y/%%m ^
 "-Directory<ModifyDate" -d %OUT%/%%Y/%%m ^
 "-Directory<FileModifyDate" -d %OUT%/%%Y/%%m ^
 -o . ^
 %SRC%

echo Done!
pause
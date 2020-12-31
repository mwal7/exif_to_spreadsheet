# exif_to_spreadsheet
A script that parses output from the command line tool ExifTool, and writes it to a spreadsheet. 

This script requires ExifTool to function. The script provides a single function - exif_to_sheet() - that accepts a directory path and file name. The script runs ExifTool on each file and adds the output as a row to the supplied csv file. If the file already exists new data will be appended, otherwise a new file will be created. See ExifTool documentation for information on installation and supported file types.

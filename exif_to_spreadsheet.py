import subprocess
import re
from os import listdir
from os.path import isfile, join
import pandas as pd
import sys

# run cli tool exiftool to extract metadata from images, videos, and other files
# make the returned data tabular, and write it to a spreadsheet
# turn code into a function that accepts a folder location, use python to generate a list
# of files in the folder. iterate through all the files and add data from each to a spreadsheet

def exif_to_sheet(in_directory, out_file):
    """
    Accepts a directory name and output file name. File type should be csv.

    Extracts exif data from files in given directory, and outputs data to output file in tabular form.
    """
    dir = in_directory
    files = None
    try:
        files = [file for file in listdir(dir) if isfile(join(dir, file))]
        if len(files) == 0:
            print("There are no files in this directory.")
            sys.exit("Exiting program.")
        if files == None:
            print("There was an issue finding the directory.")
    except FileNotFoundError as e:
        print("in_directory should be an absolute path, or relative to the directory from which this script is executed.")

    for file in files:
        dict = {}
        try:
            exif_output = subprocess.run(["exiftool",
                                    join(dir,file)], check=True, stdout=subprocess.PIPE).stdout

            string_data = exif_output.decode("utf-8") # convert bytes to utf-8 encoded string
            key_values = re.split("\n", string_data) # split string at newline to create list of key-value pairs delineated by ' : '

            for pair in key_values:
                try:
                    key, value = re.split("\s{1,}:\s{1,}", pair) # split key-value pairs
                    dict[key] = value
                except Exception as e:
                    pass

            if isfile(out_file) == False: # if outfile doesn't exist already, create it + write file data
                new_df = pd.DataFrame(dict, index=[0]) # create DF from key-value pairs (col headers and values)
                new_df.to_csv(out_file, sep=',', mode='w', index=True) # create file and write data
                print("Creating new file. Writing 1st row.")
            elif isfile(out_file):
                in_file = pd.read_csv(out_file) # if outfile exists, read it in
                next_row = in_file.index[-1] + 1 # get index number for next row to write
                print('Writing row {}'.format(next_row))
                new_df = pd.DataFrame(dict, index=[next_row]) # prepare row to write
                new_out_file = in_file.append(new_df, sort=True) # append row to existing records
                # concated = pd.concat([in_file, new_df], axis=1, join='outer')
                new_out_file.to_csv(out_file, sep=',', mode='w') # overwrite file with new data added
        except Exception as e:
            print(e)


if __name__ == "__main__":
    i = input("Input directory: ")
    o = input("Output file name (should be a CSV): ")
    exif_to_sheet(i,o)

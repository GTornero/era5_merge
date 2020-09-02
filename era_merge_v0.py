"""era_merge - a script to merge the monthly .csv output files from the ERA5 CDS - by Guillermo Tornero 01/09/2020."""

import csv
import re
import os
from tkinter import filedialog


# Asks the used to select the folder containing the ERA5 csv download files.
directory = filedialog.askdirectory(
    title="Select the folder containing the monthly .csv files."
)

# TODO: Create a regular expression for the monthly ERA5 download csv files. They all start with ERA5_ then some numbers and finished with .netcdf.csv
era_regex = re.compile(r"^(ERA5_)(\d{4})(\d{1,2})\.netcdf.csv$")

# TODO: Loop through files within the selected directory and save the file names that match the era5 regular expression.
# The regular expression should have groups so that we can isolate the part of the file name with the year and month to organise the files in order of olders to recent.

# Initiating an empty list which will store all of the filenames containing the era5 CDS data
era_files = []
# Looping through all the files within the selected directory
for filename in os.listdir(directory):
    # If the filename matches the regular expression, append the filename to the list of era5 filenames.
    if era_regex.search(filename):
        era_files.append(filename)
        continue


# TODO: Need to sort the list of era5 filenames in chronological order (year and then month)
# Sorting the list first based on year and then month using a custom lambda function
era_files.sort(
    key=lambda x: (int(era_regex.search(x).group(2)), int(era_regex.search(x).group(3)))
)

# TODO: Loop through the era5 files in chronological order and append them to the final output csv file
# Create the output .csv file
with open(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), "ERA_Wave_output.csv"),
    "w",
    newline="",
) as output_file:
    # Create the writer object for the final output file
    csv_writer = csv.writer(output_file)

    # TODO: Need to create the header, this can be done only in the first pass through the file loop.
    for counter, filename in enumerate(era_files):
        # Open the corresponding monthyly era5 csv file
        with open(os.path.join(directory, filename), "r", newline="") as monthly_file:
            # Create the reader object for the monthly era5 data file
            csv_reader = csv.reader(monthly_file)
            # Create header of the output csv file only on the first iteration of the for loop
            if counter == 0:
                csv_writer.writerows(csv_reader)
            else:
                next(csv_reader)
                for row in csv_reader:
                    csv_writer.writerow(row)
        print(
            f"Progress: {int(float(counter + 1) / float(len(era_files)) * 100)}%",
            end="\r",
        )

print("End of file creation.")

import csv
import re

# Function to replace special characters with spaces
def replace_special_characters(text):
    # Replace special characters with a space
    return re.sub(r'[^\w\s]', ' ', text)

# Input and output file paths
input_file = "/Users/nitish/Downloads/SFL_DAILER_DATA_12_NOV_2024.csv"  # Change to your input CSV file
output_file = "/Users/nitish/Downloads/output6.csv"  # Output CSV file with cleaned data

# Process CSV file
with open(input_file, mode='r', newline='', encoding='utf-8', errors='replace') as infile, \
     open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    for row in reader:
        # Replace special characters in each cell
        cleaned_row = [replace_special_characters(cell) for cell in row]
        writer.writerow(cleaned_row)

print(f"Special characters replaced and data saved to '{output_file}'.")

def remove_extra_spaces(text):
    return re.sub(r'\s+', ' ', text).strip()  # Replace multiple spaces with one and strip leading/trailing spaces

# Input and output file paths
input_file = "/Users/nitish/Downloads/output6.csv"  # Replace with your input CSV file path
output_file = "/Users/nitish/Downloads/output7.csv"  # Path for the cleaned CSV file

# Process CSV file
with open(input_file, mode='r', newline='', encoding='utf-8', errors='replace') as infile, \
     open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    for row in reader:
        # Clean each cell in the row by removing extra spaces
        cleaned_row = [remove_extra_spaces(cell) for cell in row]
        writer.writerow(cleaned_row)

print(f"Cleaned data saved to '{output_file}' with extra spaces removed.")


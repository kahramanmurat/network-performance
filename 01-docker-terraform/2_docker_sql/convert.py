import os
import gzip
import csv

def decompress_gzip(input_gzip_file, output_csv_file):
    with gzip.open(input_gzip_file, 'rt') as gzipped_file:
        with open(output_csv_file, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            for line in csv.reader(gzipped_file):
                csv_writer.writerow(line)

def decompress_gzip_files_in_folder_recursive(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.gz'):
                input_gzip_file = os.path.join(root, file)
                output_csv_file = os.path.join(root, file[:-3])  # Remove the .gz extension
                decompress_gzip(input_gzip_file, output_csv_file)

                print(f"Decompressed {input_gzip_file} to {output_csv_file}")

# Example usage
folder_path = 'data/'
decompress_gzip_files_in_folder_recursive(folder_path)

import os
import json
from tqdm import tqdm
import json
import PyPDF2
import os
from tqdm import tqdm

def count_pdf_pages(pdf_file_path):
    try:
        with open(pdf_file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            num_pages = len(pdf_reader.pages)
            return num_pages
    except FileNotFoundError:
        print(f"File not found: {pdf_file_path}")
        return None
    except:
        print(f"Error reading PDF file: {pdf_file_path}")
        return None

data = {}  # Dictionary to store statistics
fail_count = 0
ls_fail = []
for year in tqdm(sorted(os.listdir('/mnt/HDFS/patidarritesh/pdf_extr'))):
    year_path = os.path.join('/mnt/HDFS/patidarritesh/pdf_extr', year)
    data[year] = {}  # Create a sub-dictionary for the year

    for month in tqdm(sorted(os.listdir(year_path))):
        if(month == 'json_files'):
            continue
        month_path = os.path.join(year_path, month)
        data[year][month] = {}  # Create a sub-dictionary for the month
        data[year][month]['lst_num_pages'] = []  # Initialize the total count for the month
        
        for path in tqdm(sorted(os.listdir(month_path))):
            pdf_file_path = os.path.join(month_path, path)

            num_pages = count_pdf_pages(pdf_file_path)
            if num_pages is not None:
                # Store the number of pages in the dictionary
                data[year][month]['lst_num_pages'].append(num_pages)
            else:
                print(f'Error could not read PDF file {pdf_file_path}.')
                fail_count += 1
                ls_fail.append(pdf_file_path)

        # Store the total count for the month
        data[year][month]['total_pages'] = sum(data[year][month]['lst_num_pages'])
        data[year][month]['total_pdf'] = len(data[year][month]['lst_num_pages'])
# Save the data to a JSON file
output_file_path = '/mnt/HDFS/patidarritesh/husain/final_statistics.json'
with open(output_file_path, 'w') as json_file:
    json.dump(data, json_file, indent=2)

print(f"Statistics saved to {output_file_path}")

print(f"Failed to read {fail_count} PDF files.")

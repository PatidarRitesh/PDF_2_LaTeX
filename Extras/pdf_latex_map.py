# import os
# import subprocess



# latex_base_names =[]
# latex_base_names.append(os.listdir("/mnt/NFS/patidarritesh/test_path"))



# def copy_pdf():
    
# # Replace these paths with your actual paths

#     pdf_directory = '/mnt/HDFS/patidarritesh/pdf_extr'
#     destination_directory = '/mnt/HDFS/patidarritesh/test_pdf'

#     # Create the destination directory if it doesn't exist
#     if not os.path.exists(destination_directory):
#         os.makedirs(destination_directory)

#     # Iterate through the base names
#     for file in latex_base_names[0]:
#         try:
#             # Construct the paths for LaTeX and PDF files
#             # latex_file = os.path.join('/mnt/NFS/patidarritesh/test_path', file)
#             if len(file.split('.')) == 3:
                
#                 yymm = file.split('.')[0]
#                 year, month = int(yymm[:2]), int(yymm[2:])
#                 year_ = f'200{year}' if year < 10 else f'20{year}'
#                 month_ = f'{year_[2:]}0{month}' if month < 10 else f'{year_[2:]}{month}'

#             else:
#                 month_ = file[-11:-7]
#                 year = int(month_[:2])
#                 year_ = f'200{year}' if year < 10 else f'20{year}'
#                 # print(year_, month_)

#             pdf_path = os.path.join(pdf_directory, str(year_), str(month_))
#             # print(pdf_path)
#             # copy file.pdf to destination folder
#             pdf_file = file[:-4] + '.pdf'
#             subprocess.run(['cp', os.path.join(pdf_path, pdf_file), destination_directory])
#             # for pdf_file in os.listdir(pdf_directory):
#         except Exception as e:
#             print(e)
#             # print("file", file, "pdf", pdf_file) 
#             print(pdf_file) 
          

        


    


# copy_pdf()

# print("Copy operation completed.")





# import os
# import subprocess
# import datetime
# from tqdm import tqdm

# latex_base_names = os.listdir("/mnt/NFS/patidarritesh/test_path")


# def copy_pdf():
#     # Replace these paths with your actual paths
#     pdf_directory = '/mnt/HDFS/patidarritesh/pdf_extr'
#     destination_directory = '/mnt/HDFS/patidarritesh/test_pdf2'

#     # Create the destination directory if it doesn't exist
#     if not os.path.exists(destination_directory):
#         os.makedirs(destination_directory)

#     # Create a log file to store errors
#     log_file_path = 'error_log.txt'

#     # Open the log file in append mode
#     with open(log_file_path, 'a') as log_file:
#         # Iterate through the base names
#         for file in tqdm(latex_base_names):
#             try:
#                 # Construct the paths for LaTeX and PDF files
#                 if len(file.split('.')) == 3:
#                     yymm = file.split('.')[0]
#                     year, month = int(yymm[:2]), int(yymm[2:])
#                     year_ = f'200{year}' if year < 10 else f'20{year}'
#                     month_ = f'{year_[2:]}0{month}' if month < 10 else f'{year_[2:]}{month}'
#                 else:
#                     month_ = file[-11:-7]
#                     year = int(month_[:2])
#                     year_ = f'200{year}' if year < 10 else f'20{year}'

#                 pdf_path = os.path.join(pdf_directory, str(year_), str(month_))
#                 pdf_file = file[:-4] + '.pdf'

#                 # Check if the PDF file exists
#                 pdf_file_path = os.path.join(pdf_path, pdf_file)
#                 if os.path.exists(pdf_file_path):
#                     # Copy the PDF file to the destination directory
#                     subprocess.run(['cp', pdf_file_path, destination_directory])
#                     # print(f"Copied {pdf_file_path} to {destination_directory}")
#                 else:
#                     # If PDF file doesn't exist, log an error
#                     error_message = f"PDF file not found for {pdf_file_path}\n"
#                     log_file.write(error_message)
#                     print(error_message)
#             except Exception as e:
#                 # Log any other exceptions
#                 error_message = f"Error processing {file}: {e}\n"
#                 log_file.write(error_message)
#                 print(error_message)

#     print("Copy operation completed. Check the error log for any issues.")


# copy_pdf()





import os
import subprocess
import datetime
from tqdm import tqdm
import re
pattern = r"\d{4}\.\d{5}"
pattern2= r"\d{4}\.\d{4}"

pdf_base_names = os.listdir("/mnt/NAS/patidarritesh/5_page_pdfs")

new_folder = '/mnt/NAS/patidarritesh/ExtraPdf_5_page'
if not os.path.exists(new_folder):
        os.makedirs(new_folder)

def copy_latex():
    # Replace these paths with your actual paths
    latex_directory = '/mnt/NAS/patidarritesh/preprocess_2'
    destination_directory = '/mnt/NAS/patidarritesh/latex_files'

    # Create the destination directory if it doesn't exist
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)

    # Create a log file to store errors
    log_file_path = 'error_log.txt'

    # Open the log file in append mode
    with open(log_file_path, 'a') as log_file:
        # Iterate through the base names
        for pdf_file in tqdm(pdf_base_names):
            try:
                # Construct the paths for LaTeX and PDF files
                # if len(file.split('.')) == 3:
                #     yymm = file.split('.')[0]
                #     year, month = int(yymm[:2]), int(yymm[2:])
                #     year_ = f'200{year}' if year < 10 else f'20{year}'
                #     month_ = f'{year_[2:]}0{month}' if month < 10 else f'{year_[2:]}{month}'
                # else:
                #     month_ = file[-11:-7]
                #     year = int(month_[:2])
                #     year_ = f'200{year}' if year < 10 else f'20{year}'
                if re.search(pattern, pdf_file):
                    # continue
                    years = str(int(pdf_file[:2]))
                    # # print(years)

                    month = pdf_file[:4]
                elif re.search(pattern2, pdf_file):
                    # continue
                    years = str(int(pdf_file[:2]))
                    # print(years)
                    month = pdf_file[:4]
                else:
                    
                    years = str(int(pdf_file[-11:-9]))  # Corrected the slicing indices
                    month =  pdf_file[-11:-7]    # Corrected the slicing indices
                latex_file = pdf_file[:-4] + '.tex'
                latex_path = os.path.join(latex_directory, years, month)

                # latex_path = os.path.join(latex_directory, str(year_), str(month_))
               

                # Check if the PDF file exists
                latex_file_path = os.path.join(latex_path, latex_file)
                if os.path.exists(latex_file_path):
                    # Copy the PDF file to the destination directory
                    subprocess.run(['cp', latex_file_path, destination_directory])
                    # print(f"Copied {pdf_file_path} to {destination_directory}")
                else:
                    # If PDF file doesn't exist, log an error
                    subprocess.run(['mv', os.path.join('/mnt/NAS/patidarritesh/5_page_pdfs', pdf_file), new_folder])
                    error_message = f"latex file not found for {latex_file_path}\n"
                    log_file.write(error_message)
                    print(error_message)
            except Exception as e:
                # Log any other exceptions
                error_message = f"Error processing {pdf_file}: {e}\n"
                log_file.write(error_message)
                print(error_message)

    print("Copy operation completed. Check the error log for any issues.")


copy_latex()

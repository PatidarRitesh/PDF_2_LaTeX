import os
import subprocess
from tqdm import tqdm


# html_filenames = []
# html_filenames.append(os.listdir('/home/patidarritesh/Nougat/nougat/html_files_2'))

# def html_2_pdf_map():
#     # print(html_filenames)

#     pdf_directory = '/mnt/NAS/patidarritesh/pdf_test/test_pdf2'
#     ritesh = '/mnt/NAS/patidarritesh/ritesh'
#     sid='/mnt/NAS/patidarritesh/sid'
#     ankit='/mnt/NAS/patidarritesh/ankit'
#     husain='/mnt/NAS/patidarritesh/husain'
#     os.makedirs(ritesh, exist_ok=True)
#     os.makedirs(sid, exist_ok=True)
#     os.makedirs(ankit, exist_ok=True)
#     os.makedirs(husain, exist_ok=True)


#     log_file_path = 'error_log_pdf_html.txt'
#     # Iterate through the base names
#     count=0
#     with open(log_file_path, 'w') as log_file:
#         for file in tqdm(html_filenames[0]):
#             try:
#                 pdf_path=pdf_directory
                
#                 pdf_file = file[:-5] + '.pdf'
                

                
#                 pdf_file_path = os.path.join(pdf_path, pdf_file)
#                 if os.path.exists(pdf_file_path):
#                     if count<37000:
#                         subprocess.run(['cp', pdf_file_path, ritesh])

#                     elif count>37000 and count<74000:
#                         subprocess.run(['cp', pdf_file_path, sid])

#                     elif count>74000 and count<111000:
#                         subprocess.run(['cp', pdf_file_path, ankit])

#                     elif count>111000 :
#                         subprocess.run(['cp', pdf_file_path, husain])
                    
#                 else:
#                     # If PDF file doesn't exist, log an error
#                     error_message = f"PDF file not found for {pdf_file_path}\n"
#                     log_file.write(error_message)
#                     print(error_message)
#             except Exception as e:
#                 error_message = f"Error processing {file}: {e}\n"
#                 log_file.write(error_message)
#                 print(error_message)  

#             count+=1     
        
# html_2_pdf_map()
# print("copied successfully")











pdf_filenames = []
pdf_filenames.append(os.listdir('/mnt/NAS/patidarritesh/final_pdf'))

def pdf_2_html_map():

    html_directory = '/home/patidarritesh/Nougat/nougat/html_files_2'
    destination_directory = '/mnt/NAS/patidarritesh/path/html/root'

    log_file_path = 'error_log_pdf_html_2.txt'
    # Iterate through the base names
    with open(log_file_path, 'w') as log_file:
        for file in tqdm(pdf_filenames[0]):
            try:
                html_path=html_directory
                
                html_file = file[:-4] + '.html'
                

                
                html_file_path = os.path.join(html_path, html_file)
                if os.path.exists(html_file_path):
                    subprocess.run(['cp', html_file_path, destination_directory])
                    
                else:
                    # If PDF file doesn't exist, log an error
                    error_message = f"HTML file not found for {html_file_path}\n"
                    log_file.write(error_message)
                    print(error_message)
            except Exception as e:
                error_message = f"Error processing {file}: {e}\n"
                log_file.write(error_message)
                print(error_message)


pdf_2_html_map()
print("copied successfully")
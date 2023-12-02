import os
import re
from tqdm import tqdm

# -----------------------------------------------------------
pattern1 = r"((?<!\\)%.*)"
pattern2 = r"\\iffalse"
pattern3 = r"\\fi"
pattern4 = r"\\begin{comment}"
pattern5 = r"\\end{comment}"
pattern6 = r"\\usepackage.*"

# -----------------------------------------------------------
def remove_comments(data, start_pattern, end_pattern):
    matches = re.finditer(start_pattern, data)
    if matches:
        new_data = ""
        prev_end = 0
        for match in matches:
            start = match.start()
            end = re.search(end_pattern, data[start:]).end()
            new_data += data[prev_end:start]
            prev_end = start + end
        new_data = new_data + data[prev_end:]
        return new_data
    return data


for year in range(2000,2024):
    try:
        year = str(year)
        input_folder_path = f"/mnt/NFS/patidarritesh/PDF_2_TEX/{year}/final_merged"
        output_folder_path = f"/mnt/NFS/patidarritesh/PDF_2_TEX/{year}/preprocessing_1"


        err_count = 0
        for i in tqdm(range(1,13)):
            folder = year[-2:]+str(i).zfill(2)
            input_folder_path2 = os.path.join(input_folder_path,folder)
            output_folder_path2 = os.path.join(output_folder_path,folder)
            # create folder if not exist
            if not os.path.exists(output_folder_path2):
                os.makedirs(output_folder_path2)

            files = os.listdir(input_folder_path2)
            for file in tqdm(files):
                try:
                    data = ""
                    with open(input_folder_path2 + "/" + file, "rb") as f:
                        data = f.read()
                        try:
                            data = data.decode("utf-8")  # Ignore non-UTF-8 characters
                        except:
                            data = data.decode("latin-1", errors="ignore")

                        #__________________________________________________________________________________
                        # In[1]: remove all the comments
                        # ---------------------------------------------------------------------------
                        data = re.sub(pattern1, "", data)
                        #__________________________________________________________________________________
                        # In[2]: remove all the text between \begin{comment} and \end{comment}
                        data = remove_comments(data, pattern2, pattern3)
                        #__________________________________________________________________________________
                        # In[3]: remove all the text between \begin{comment} and \end{comment}
                        data = remove_comments(data, pattern4, pattern5)
                        #__________________________________________________________________________________

                        # In[4]: remove all the usepackage 
                        data = re.sub(pattern6, "", data)
                        # In[]: write back the data
                        data = re.sub('\n+','\n',data)         # remove all the multiple new line character

                        file_path = output_folder_path2 + "/" + file
                        # Use 'w' mode to create a new file (or overwrite an existing one)
                        with open(file_path, "w") as f:
                            pass  # Using 'pass' to indicate that we're not writing any content to the file

                        print(f"Created a new file: {file_path}")
                        # with open(output_folder_path2 + "/" + file, "wb") as f:
                        with open(output_folder_path2 + "/" + file, "wb") as f:
                            try:
                                data1 = data.encode("utf-8")  # Ignore non-UTF-8 characters
                            except:
                                data1 = data.encode("latin-1", errors="ignore")
                            f.write(data1)
                except Exception as e:
                    err_count += 1
                    print(e)

        print(f"Number of errors in {year}: ", err_count)
    except Exception as e:
        print(e)






                
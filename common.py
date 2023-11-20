import os

def read_text_files_from_folder(folder_path):
    # Get a list of files in the folder
    files = os.listdir(folder_path)

    # Filter only text files
    text_files = [file for file in files if file.endswith(".txt")]

    # Initialize an array to store the contents of the text files
    text_data = []

    # Read each text file and append its content to the array
    for file_name in text_files:
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'rb') as file:
            file_content = file.read()
            text_data.append(file_content)

    return text_data
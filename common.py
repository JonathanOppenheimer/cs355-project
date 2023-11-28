import hashlib
import numpy as np
import os


def get_file_paths(folder_path):
    file_paths = []
    
    # Walk through the directory and get all file paths
    for foldername, subfolders, filenames in os.walk(folder_path):
        for filename in filenames:
            file_paths.append(os.path.join(foldername, filename))
    
    return file_paths

def exor(v1, v2):
    a = np.frombuffer(v1, dtype = np.uint8)
    b = np.frombuffer(v2, dtype = np.uint8)
    re=(a^b).tobytes()
    return(re)

def sha256_hash(data):
    sha256 = hashlib.sha256()
    sha256.update(data)
    return sha256.digest()

def calculate_ed2k_hash(file_path):
    chunk_size = 9728000

    with open(file_path, 'rb') as file:
        file_size = os.path.getsize(file_path)
        hash_list = []

        if file_size <= chunk_size:
            # For files with one chunk or less
            file_data = file.read()
            return sha256_hash(file_data)

        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break

            hash_list.append(sha256_hash(chunk))

        if file_size % chunk_size == 0:
            # If file size is a multiple of chunk size, add hash of null
            hash_list.append(sha256_hash(b''))

        # Concatenate the hash values and calculate the final SHA-256 hash
        concatenated_hash = b''.join(hash_list)
        ed2k_hash = sha256_hash(concatenated_hash)

        return ed2k_hash



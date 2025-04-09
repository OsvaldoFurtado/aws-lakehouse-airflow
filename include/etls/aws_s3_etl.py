
from include.utils.constants import AWS_ACCESS_KEY, AWS_SECRET_KEY
import s3fs
import os

def connect_to_s3():

    try:
        s3 = s3fs.S3FileSystem(anon=False,
                               key= AWS_ACCESS_KEY,
                               secret=AWS_SECRET_KEY)
        return s3
    except Exception as e:
        print(e)



def upload_to_s3(s3: s3fs.S3FileSystem, local_path: str, target_s3_path: str):
    
    try:
        
        print("Verifying if the files exist locally ")
        if not os.path.exists(local_path):
            raise FileNotFoundError(f"Path not found: {local_path}")

        print(f"Initiating upload from {local_path} to {target_s3_path}")

        for file_name in os.listdir(local_path):
            file_path = os.path.join(local_path, file_name)
            if os.path.isfile(file_path):  
                s3_target_path = f"{target_s3_path}{file_name}" 
                if s3.exists(s3_target_path):
                    print(f"File {file_name} already exists. Skipping upload.")
                    continue

                print(f"Sending {file_path} to {s3_target_path}")
                s3.put(file_path, s3_target_path)

        print('Files uploaded to s3')

    except Exception as e:
        print(f"Error occured during the upload: {str(e)}")
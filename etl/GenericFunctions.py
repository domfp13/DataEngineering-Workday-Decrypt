# -*- coding: utf-8 -*-
# Luis Enrique Fuentes Plata

from typing import Optional
from pathlib import Path

def moveFilesFromFTP(host_name:str, user_name:str, password:str)->list:
    """Moves and deletes files from remote FTP server, the files are downloaded to
    the local "out" directory, once they are move, they are deleted from the 
    remote server.

    Args:
        host_name (str): Host name of the remote server
        user_name (str): User name of the remote server
        password (str): Password of the remote server

    Returns:
        list: [description]
    """
    import paramiko
    from os import getcwd

    try:
        # Starting Paramikio client
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=host_name, username=user_name, password=password)

        # Transfering object to FTP
        with ssh_client.open_sftp() as ftp:
            
            files_out = []
            
            for file in ftp.listdir():
                local_file = Path(getcwd(),'out',file)
                ftp.get(f'/Home/QlikFFIprod/{file}', local_file) # remote path, local path
                files_out.append(local_file)
                #ftp.remove(file)
            
            ftp.close() # sometimes with does not close the connection, therefore connection is explicitly closed
        
        return files_out

    except Exception as e:
        e
    finally:
        ssh_client.close()

def uploadToS3(file_obj:Path)->None:
    """Uploads object to an S3 bucket, file is uploaded with a datetime prefix
    with the current day.

    Args:
        file_obj (Path): pathlib Path
    """

    from os.path import basename
    from datetime import datetime
    import boto3
    
    bucket = 'domfp13-s3-bucket' # Add your bucket here
    
    #s3_client = boto3.client('s3')
    s3_client = boto3.client('s3', aws_access_key_id='', aws_secret_access_key='')
    
    prefix  = 'hr_bk_files/' # Add your prefix here
    object_name = "{prefix}{time}_{name}".format(prefix=prefix, time=datetime.now().strftime('%Y%m%d'), name=basename(file_obj))
    
    with open(file_obj, "rb") as f:
        s3_client.upload_fileobj(f, bucket, object_name)

def decrypt(filein:Path)->Path:
    """Uses the GPG.exe file in order to decrypt the current file (filein)

    Args:
        filein (Path): Host path for the file that is being decryted.

    Returns:
        Path: Host path for the encrypted file.
    """

    from os.path import exists
    from os import remove, system, getcwd
    from time import sleep
    
    try:
        base_name = "{base}_decrypted.csv".format(base=filein.stem)
        fileout = Path(getcwd(), 'out', base_name)

        if exists(fileout):
            remove(fileout)
        
        #Decrypting
        gpg = Path(getcwd(), 'gpg', 'bin', 'gpg.exe').absolute().as_posix()
        system(f'{gpg} -d -o {fileout} {filein}')
        sleep(5)
        
        return Path(getcwd(), 'out', base_name)

    except Exception as e:
        pass
    finally:
        # Kill gpg.exe process if still running
        system(f'taskkill /IM gpg.exe /f')

def dataframeTransformation(filein:Path)->None:
    """Uses Pandas Dataframe to perform a trasformation based on Date.

    Args:
        filein (Path): Host path for the file that is being decryted.
    """

    import pandas as pd

    # Using Dataframe to clean the file
    data_test = pd.read_csv(filein, encoding="utf-8", nrows=2)
    cols = list(data_test.columns)
    date_cols = [x for x in cols if ('Date' in x and x != 'CFI - ServiceNow Manager Email As of Hire Date') or x == 'Last Day of Work']
    data = pd.read_csv(filein, encoding="utf-8",
                    parse_dates=date_cols,
                    infer_datetime_format=True,
                    error_bad_lines=False,
                    low_memory=False)
    
    # Converting to CSV 
    data.to_csv(filein, index=False)

def copyFileToAnotherLocalDestination():
    pass # Todo
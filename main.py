# -*- coding: utf-8 -*-
# Luis Enrique Fuentes Plata

#External Libs
from typing import Optional
from functools import partial
from os import getcwd
from pathlib import Path
import logging

# Local functions
from etl.GenericFunctions import (moveFilesFromFTP, 
                                  uploadToS3, decrypt, dataframeTransformation,
                                  copyFileToAnotherLocalDestination)

LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
loggin_file_path = str(Path('{path}/LOGGER.log'.format(path = getcwd())))
logging.basicConfig(filename = loggin_file_path,
                    level = logging.DEBUG,
                    format = LOG_FORMAT,
                    filemode = 'w')

logger = logging.getLogger()

if __name__ == '__main__':

    try:

        logger.info("01. Dowload files from FTP")

        host_name = "" # Add hostname
        user_name = "" # Add username
        password = ""  # Add password
        
        local_files = moveFilesFromFTP(host_name, user_name, password)

        if len(local_files)>0:

            logger.info("02. Upload Encrypted files to s3")
            list(map(partial(uploadToS3, prefix='hr_bk_files'), local_files)) # In python 3 map is lazy evaluation: each value is only computed when it's needed

            logger.info("03. Extracting files")
            final_paths = list(map(decrypt, local_files))

            logger.info("04. Data Transfomation")
            list(map(dataframeTransformation, final_paths))

            logger.info("05. Upload Encrypted files to s3")
            list(map(partial(uploadToS3, prefix='hr_files'), final_paths)) # In python 3 map is lazy evaluation: each value is only computed when it's needed
            
            logger.info("06. Copies files in output to other local destination")
            list(map(copyFileToAnotherLocalDestination, final_paths))

    except Exception as e:
        print(e)
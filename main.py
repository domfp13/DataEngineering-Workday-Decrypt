# -*- coding: utf-8 -*-
# Luis Enrique Fuentes Plata

#External Libs
from typing import Optional
from os import getcwd
from pathlib import Path
import logging

# Local functions
from etl.GenericFunctions import moveFilesFromFTP, uploadToS3, extractAndDecrypt

LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
loggin_file_path = str(Path('{path}/LOGGER.log'.format(path = getcwd())))
logging.basicConfig(filename = loggin_file_path,
                    level = logging.DEBUG,
                    format = LOG_FORMAT,
                    filemode = 'w')

logger = logging.getLogger()

if __name__ == '__main__':

    logger.info("Begin")
    logger.info("01. Dowload files from FTP")

    host_name = "" # Add hostname
    user_name = "" # Add username
    password = "" # Add password
    
    local_files = moveFilesFromFTP(host_name, user_name, password)
    
    logger.info("02. Upload files to s3")
    #for element in local_files:
    #   uploadToS3(element)

    logger.info("03. Extracting files")
    extractAndDecrypt(local_files)

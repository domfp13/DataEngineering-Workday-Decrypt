# DataEngineering-Workday-Decrypt
DataEngineering-Workday-Decrypt is a process that decrypts information from source systems to our local environments; this process takes specific GPG files and decrypts them as a CSV.

The process takes files from an FTP server and transfer them locally, after that we send a copy to our archive prefix on a AWS S3 bucket, the dataflow continues as the files are decrypted, the decrypted files are also send to an S3 Bucket once they have been decrypted, the last step of the process is to move the .csv files to another location within the server. 

This repo is part of a project that is decouple in two different scripts “DataEngineering-Workday-Decrypt” & “DataEngineering-Workday-Transfer”, here is the BPMB and its component diagram.

### BPMB
![](resources/img/bpmb.PNG)

### Components Diagram
![](resources/img/components.PNG)

### Tech
DataEngineering-Workday-Decrypt uses a number of open source projects to work properly:

* Python 3.7
* Windows 7+

### Local Testing

Requires [Python](https://docs.conda.io/en/latest/miniconda.html) v3.7+ to run.

Install the dependencies

```sh
$ cd DataEngineering-Workday-Decrypt
$ conda create -n workday-decrypt python=3.7
$ conda activate workday-decrypt
$ pip install --upgrade -r requirements.txt
$ # Add FTP credentials and AWS credentials
$ python main.py
```

#### Building for source
if new lib added to the project update requirements.txt
```sh
$ pip freeze --local > requirements.txt
```

### Docker

```sh
FROM python:3
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD [ "python", "./your-daemon-or-script.py" ]
```


## Authors
* **Luis Fuentes** - *2020-07-14*
* **Daniel Steinemann**
* **Angel Angel**
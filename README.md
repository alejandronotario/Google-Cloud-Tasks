# Google-Cloud-Tasks
# Import & Export Manual

This manual belongs to Ei Analytics project. It describes some procedrues to data management at Google Cloud

<br>
<hr>


## Overview
There are several data resources in this project and they must be integrated at Google Cloud in an automatically way. For thos target it is needed to use cron tabs. In this notebooks is is described the code to include.

## Prerequisites

## Links and sources
https://cloud.google.com/sdk/gcloud/reference/

## Steps

__Data from EI Database__

__Steps__

- Create instance at SQL Cloud
```console
anotarioei@cloudshell:~ (ei-ga-datastreaming)$ gcloud sql instances create [INSTANCE_NAME] --tier=[MACHINE_TYPE] --region=[REGION]
anotarioei@cloudshell:~ (ei-ga-datastreaming)$ gcloud sql instances create [INSTANCE_NAME] --tier=db-n1-standard-1 --region=europe-west1 #standard instance
```
- Create a database at SQL Cloud
```
anotarioei@cloudshell:~ (ei-ga-datastreaming)$ gcloud sql databases create [DATABASE_NAME] --instance=[INSTANCE_NAME]
```
- Unzip file if needed, it cold be either .zip or .sql
- Upload dump to Google Storage
```console
server@administrator:~$ gsutil cp -r ~/[FOLDER_NAME] gs://[BUCKET_NAME] #if it is to upload a folder
server@administrator:~$ gsutil cp ~/[DUMP_FILE_NAME] gs://[BUCKET_NAME]/[FOLDER_NAME]
```
- Make a directory at GC console
- Copy the dump file in the created directory
```console
anotarioei@cloudshell:~ (ei-ga-datastreaming)$ gsutil cp gs://[BUCKET_NAME]/[FOLDER_NAME]/[DUMP_FILE_NAME] ~/[DIRECTORY_NAME]
```
- Upload the dump file to SQL Cloud
```console
anotarioei@cloudshell:~ (ei-ga-datastreaming)$ gcloud sql connect [INSTANCE_NAME] --user root < [DUMP_FILE_NAME]
```
- Export tables in .csv format to Google Storage. The idea is to code all the required queries in one shell script to run every period
```
anotarioei@cloudshell:~ (ei-ga-datastreaming)$ gcloud sql export csv [INSTANCE_NAME] gs://[BUCKET_NAME]/[FOLDER_NAME]/[CSV_FILE_NAME] --query='select*from [TABLE_NAME]' --database=[DATABASE_NAME]
```


- Export data tables with header. This is an example and it works

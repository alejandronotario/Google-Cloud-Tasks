# Import & Export Manual at Cloud Sql sevice

This manual describes some procedures to data management at Google Cloud Sql service

<br>
<hr>


## Overview
There are several data resources in every project and they must be integrated at Google Cloud in an automatically way. For this target it is needed to use cron tabs. Here it is described some code to include.

__Workflow__

Database dump at some server -> Import dump to Google Cloud Storage -> Import dump to Google Cloud SQL -> Export csv to Google Cloud Storage

## Prerequisites

- A Google Cloud Account

## Links and sources

https://cloud.google.com/sdk/gcloud/reference/

## Steps

- Generating a name and a password to call the cloud sql instance. It is necessary to create new name and password each instance because Google Cloud does not allow to repeat recently used names to call them. First it is generated the current date and then it is added to "instance" and "pass" for example

```bash
today="$(date + "%Y%m%d")"
number=0
while test -e "$today$suffix.txt"; do
	(( ++number ))
	suffix="$(printf -- '-%02d' "number" )"
done
instanceName="instance$today$suffix"
password="pass$today$suffix"

```

- Creating instance at SQL Cloud
```console
user@cloudshell:~ ([PROJECT_ID])$ gcloud sql instances create [INSTANCE_NAME] --tier=[MACHINE_TYPE] --region=[REGION]
user@cloudshell:~ ([PROJECT_ID])$ gcloud sql instances create [INSTANCE_NAME] --tier=db-n1-standard-1 --region=europe-west1 #standard instance
```
- Setting up the password

```
gcloud sql users set-password root % --instance $instanceName --password=$password

```

- Creating a database at SQL Cloud
```console
user@cloudshell:~ ([PROJECT_ID])$ gcloud sql databases create [DATABASE_NAME] --instance=[INSTANCE_NAME]
```
- Unzip file if needed, it could be either .zip or .sql  
- Upload dump to Google Storage
```console
server@administrator:~$ gsutil cp -r ~/[FOLDER_NAME] gs://[BUCKET_NAME] #if it is to upload a folder
server@administrator:~$ gsutil cp ~/[DUMP_FILE_NAME] gs://[BUCKET_NAME]/[FOLDER_NAME] 
```
- Making a directory at GC console (just the first time)
```console
user@cloudshell:~ ([PROJECT_ID])$ mkdir [DIRECTORY_NAME]
```
- Copying the dump file in the created directory:
```console
user@cloudshell:~ ([PROJECT_ID])$ gsutil cp gs://[BUCKET_NAME]/[FOLDER_NAME]/[DUMP_FILE_NAME] ~/[DIRECTORY_NAME]
```
- Uploading the dump file to SQL Cloud:
```console
user@cloudshell:~ ([PROJECT_ID])$ gcloud sql connect [INSTANCE_NAME] --user root < [DUMP_FILE_NAME]
```

- Giving credentials. Is is necessary to give credentials to SQL Cloud to allow it to export data. Server account can be found at SQL Cloud overview. For this:

- 1. Create a text file with instance description in which it can be found the service account address:

```console
$ gcloud sql instances describe [INSTANCE_NAME] > [FILE_NAME].txt

```

- 2. Extract service account address:

```console
$ grep -o ' .*gserviceaccount.com' account.txt > accountAddress.txt

```
- 3. Remove the first space:

```console
$ tr -d ' ' < accountAddress.txt > no-spaces.txt

```

- 4. Assign the variable:

```console
$ value=$(<no-spaces.txt)
``` 
- 5. Giving the writer role: 

```console
$ gsutil acl ch -u $value:W gs://[BUCKET_NAME]
```


- Exporting tables in .csv format to Google Storage. This way does not give any header:
```console
$ user@cloudshell:~ ([PROJECT_ID])$ gcloud sql export csv [INSTANCE_NAME] gs://[BUCKET_NAME]/[FOLDER_NAME]/[CSV_FILE_NAME] --query='SELECT*FROM [TABLE_NAME]' --database=[DATABASE_NAME]
```

- Exporting data tables with header. The example below is to a 3 columns table:

```console
$ gcloud sql export csv $instanceName gs://[BUCKET_NAME]/[FILE_NAME].csv --query="SELECT '[column_name1]','[column_name2]','[column_name3]' UNION ALL SELECT column_name1,column_name2,column_name3 FROM [TABLE_NAME]" --database=[DATABASE_NAME]
```


- Delete the sql instance. First yes is to force at the prompt 

```console
$ yes | gcloud sql instances delete [INSTANCE_NAME]
```
	

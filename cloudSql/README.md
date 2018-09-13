# Import & Export at Cloud SQL sevice



<br>
<hr>


## Overview
This manual describes some procedures to data management at Google Cloud Sql service. There are several data resources in every project and they must be integrated at Google Cloud in an automatically way. For this target it is needed to use cron tabs. Here it is described some code to include.

__Workflow__

Database dump at some server -> Importing dump to Google Cloud Storage -> Creating a Cloud SQL instance -> Importing dump to Cloud SQL instance -> Exporting .csv tables to Storage -> Deleting the Cloud SQL instance

## Prerequisites

- A Google Cloud Account

## Links and sources

https://cloud.google.com/sdk/gcloud/reference/

## Steps

- Uploading dump to Google Storage:

```console
server@administrator:~$ gsutil cp -r ~/[FOLDER_NAME] gs://[BUCKET_NAME] #if it is to upload a folder
server@administrator:~$ gsutil cp ~/[DUMP_FILE_NAME] gs://[BUCKET_NAME]/[FOLDER_NAME]
```
- Unzip file if needed, it could be either .zip or .sql.

- Generating a name to call the cloud sql instance. It is necessary to create new name and password each instance because Google Cloud does not allow to repeat recently used names to call them. First it is generated the current date and then it is added to "instance" for example:

```bash
#!bin/bash
today="$(date + "%Y%m%d")"
number=0
while test -e "$today$suffix.txt"; do
	(( ++number ))
	suffix="$(printf -- '-%02d' "number" )"
done
instanceName="instance$today$suffix"
password="pass$today$suffix"

```

- Creating instance at SQL Cloud:

```console
user@cloudshell:~ ([PROJECT_ID])$ gcloud sql instances create $instanceName --tier=[MACHINE_TYPE] --region=[REGION]
user@cloudshell:~ ([PROJECT_ID])$ gcloud sql instances create $instanceName --tier=db-n1-standard-1 --region=europe-west1 #standard instance
```

- Creating a database at SQL Cloud:

```console
user@cloudshell:~ ([PROJECT_ID])$ gcloud sql databases create [DATABASE_NAME] --instance=$instanceName
```
- Giving credentials. Is is necessary to give credentials to SQL Cloud to allow it to import and export data. Server account can be found at SQL Cloud overview. For this:

- 1. Creating a text file with instance description in which it can be found the service account address:

```console
user@cloudshell:~ ([PROJECT_ID])$ gcloud sql instances describe [INSTANCE_NAME] > [FILE_NAME].txt

```

- 2. Extracting service account address:

```console
user@cloudshell:~ ([PROJECT_ID])$ grep -o ' .*gserviceaccount.com' account.txt > accountAddress.txt

```
- 3. Removing the first space:

```console
user@cloudshell:~ ([PROJECT_ID])$ tr -d ' ' < accountAddress.txt > no-spaces.txt

```
- 4. Assigning the variable:

```console
user@cloudshell:~ ([PROJECT_ID])$ value=$(<no-spaces.txt)
```
- 5. Giving reader and writer roles. If it is a file to import it must be included the complete path to the file and give credentials to READ:

```console
user@cloudshell:~ ([PROJECT_ID])$ gsutil acl ch -u $value:R gs://[BUCKET_NAME]/[FOLDER_NAME]/[DUMP_FILE_NAME] 
user@cloudshell:~ ([PROJECT_ID])$ gsutil acl ch -u $value:W gs://[BUCKET_NAME]
```

- Uploading the dump file to SQL Cloud. Yes pipe is to answer automatically the prompt:

```console
user@cloudshell:~ ([PROJECT_ID])$ yes | gcloud sql import sql $instanceName gs://[BUCKET_NAME]/[FOLDER_NAME]/[DUMP_FILE_NAME] --database=[DATABASE_NAME]
```


- Exporting tables in .csv format to Google Storage. This way does not give any header:
```console
$ user@cloudshell:~ ([PROJECT_ID])$ gcloud sql export csv [INSTANCE_NAME] gs://[BUCKET_NAME]/[FOLDER_NAME]/[CSV_FILE_NAME] --query='SELECT*FROM [TABLE_NAME]' --database=[DATABASE_NAME]
```

- Exporting data tables with header. The example below is to a 3 columns table:

```console
user@cloudshell:~ ([PROJECT_ID])$ gcloud sql export csv $instanceName gs://[BUCKET_NAME]/[FILE_NAME].csv --query="SELECT '[column_name1]','[column_name2]','[column_name3]' UNION ALL SELECT column_name1,column_name2,column_name3 FROM [TABLE_NAME]" --database=[DATABASE_NAME]
```


- Deleting the sql instance.  

```console
user@cloudshell:~ ([PROJECT_ID])$ yes | gcloud sql instances delete [INSTANCE_NAME]
```
	

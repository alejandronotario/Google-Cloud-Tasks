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

- Generating a name and a password to call the cloud sql instance. It is necessary to create new name and password each instance because Google Cloud does not allow to repeat recently used names to call them. First it is generated the current date and then it is added to "instance" and "pass" for example

```
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
anotarioei@cloudshell:~ (ei-ga-datastreaming)$ gcloud sql instances create [INSTANCE_NAME] --tier=[MACHINE_TYPE] --region=[REGION]
anotarioei@cloudshell:~ (ei-ga-datastreaming)$ gcloud sql instances create [INSTANCE_NAME] --tier=db-n1-standard-1 --region=europe-west1 #standard instance
```
- Setting up the password

```
gcloud sql users set-password root % --instance $instanceName --password=$password

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

```
gcloud sql export csv ei4 gs://ei-db/apply_suscription_user.csv --query="select 'id_apply_suscription_user','id_apply_suscription','id_user
','token','activation_date','insertion_date','update_date'union all select id_apply_suscription_user,id_apply_suscription,id_user,token,activation_date,insertion_date,update_date from ap
ply_suscription_user" --database=db_ei
```
- Giving credentials. Is is necessary to give credentials to SQL Cloud. Server account can be found at SQL Cloud overview

```
gsutil acl ch -u "[SERVER_ACCOUNT]":W gs://[BUCKET_NAME]
```

# Create a text file with instance description in which it can be found the service account address

```
gcloud sql instances describe [INSTANCE_NAME] > [FILE_NAME].txt

```

# Extract service account address

```
grep -o ' .*gserviceaccount.com' account.txt > accountAddress.txt

```

# Remove the first space

```
tr -d ' ' < accountAddress.txt > no-spaces.txt

```

# Assign the variable

```
value=$(<no-spaces.txt)
``` 

# Delete the sql instance. First yes is to force at the prompt 

```
yes | gcloud sql instances delete [INSTANCE_NAME]
```
	

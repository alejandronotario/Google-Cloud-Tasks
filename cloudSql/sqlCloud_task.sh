#!/bin/bash
#Filename: sqlCloud_task.sh

# Upload dump to Google Storage

server@administrator:~$ gsutil cp -r ~/[FOLDER_NAME] gs://[BUCKET_NAME] #if it is to upload a folder
server@administrator:~$ gsutil cp ~/[DUMP_FILE_NAME] gs://[BUCKET_NAME]/[FOLDER_NAME] 

#  Generating a name and a password to call the cloud sql instance. It is necessary to create new name and password each instance because Google Cloud does not allow to repeat recently used names to call them. First it is generated the current date and then it is added to "instance" and "pass" for example

today="$(date + "%Y%m%d")"
number=0
while test -e "$today$suffix.txt"; do
        (( ++number ))
        suffix="$(printf -- '-%02d' "number" )"
done
instanceName="instance$today$suffix"
password="pass$today$suffix"

# Creating instance at SQL Cloud
# gcloud sql instances create $instanceName --tier=[MACHINE_TYPE] --region=[REGION]

gcloud sql instances create $instanceName --tier=db-n1-standard-1 --region=europe-west1 #standard instance

# Creating  a database at SQL Cloud

gcloud sql databases create [DATABASE_NAME] --instance=$instanceName

# Giving credentials. Is is necessary to give credentials to SQL Cloud. Server account can be found at SQL Cloud overview

# Create a text file with instance description in which it can be found the service account address

gcloud sql instances describe $instanceName > [FILE_NAME].txt

# Extract service account address

grep -o ' .*gserviceaccount.com' [FILE_NAME].txt > accountAddress.txt

# Remove the first space

tr -d ' ' < accountAddress.txt > no-spaces.txt

# Assign the variable

value=$(<no-spaces.txt)

# Give credentials

gsutil acl ch -u $value:R gs://[BUCKET_NAME]/[FOLDER_NAME]/[DUMP_FILE_NAME]
gsutil acl ch -u $value:W gs://[BUCKET_NAME]

# Upload the dump file to SQL Cloud. Yes pipe is to answer automatically the prompt

yes | gcloud sql import sql $instanceName gs://[BUCKET_NAME]/[FOLDER_NAME]/[DUMP_FILE_NAME] --database=[DATABASE_NAME]

# Export tables in .csv format to Google Storage. The idea is to code all the required queries in one shell script to run every period

gs://[BUCKET_NAME]/[FILE_NAME].csv --query="SELECT '[column_name1]','[column_name2]','[column_name3]' UNION ALL SELECT column_name1,column_name2,column_name3 FROM [TABLE_NAME]" --database=[DATABASE_NAME]

# Deleting the instance

yes | gcloud sql instances delete $instanceName





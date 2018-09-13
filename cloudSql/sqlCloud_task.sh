#!/bin/bash
#Filename: sqlCloud_task.sh

# 1. Generating a name and a password to call the cloud sql instance. It is necessary to create new name and password each instance because Google Cloud does not allow to repeat recently used names to call them. First it is generated the current date and then it is added to "instance" and "pass" for example

today="$(date + "%Y%m%d")"
number=0
while test -e "$today$suffix.txt"; do
        (( ++number ))
        suffix="$(printf -- '-%02d' "number" )"
done
instanceName="instance$today$suffix"
password="pass$today$suffix"

# 2. Creating instance at SQL Cloud
# gcloud sql instances create [INSTANCE_NAME] --tier=[MACHINE_TYPE] --region=[REGION]

gcloud sql instances create $instanceName --tier=db-n1-standard-1 --region=europe-west1 #standard instance

# 3. Setting up the password

gcloud sql users set-password root % --instance $instanceName --password=$password

# 4. Create a database at SQL Cloud

gcloud sql databases create [DATABASE_NAME] --instance=$instanceName

# 5. Upload dump to Google Storage

gsutil cp ~/[DUMP_FILE_NAME] gs://[BUCKET_NAME]/[FOLDER_NAME]

# 6. Make a directory at GC console. This task could be done before and only one time

# 7. Copy the dump file in the created directory

gsutil cp gs://[BUCKET_NAME]/[FOLDER_NAME]/[DUMP_FILE_NAME] ~/[DIRECTORY_NAME]

# 8. Upload the dump file to SQL Cloud

gcloud sql connect $instanceName --user root < [DUMP_FILE_NAME]

# 9. Giving credentials. Is is necessary to give credentials to SQL Cloud. Server account can be found at SQL Cloud overview

# 9.1. Create a text file with instance description in which it can be found the service account address

gcloud sql instances describe $instanceName > [FILE_NAME].txt

# 9.2. Extract service account address

grep -o ' .*gserviceaccount.com' [FILE_NAME].txt > accountAddress.txt

# 9.3. Remove the first space

tr -d ' ' < accountAddress.txt > no-spaces.txt

# 9.4. Assign the variable

value=$(<no-spaces.txt)

# 9.5. Give credentials

gsutil acl ch -u $value:W gs://[BUCKET_NAME]

# 10. Export tables in .csv format to Google Storage. The idea is to code all the required queries in one shell script to run every period

gs://[BUCKET_NAME]/[FILE_NAME].csv --query="SELECT '[column_name1]','[column_name2]','[column_name3]' UNION ALL SELECT column_name1,column_name2,column_name3 FROM [TABLE_NAME]" --database=[DATABASE_NAME]


# 11. Deleting the instance

yes | gcloud sql instances delete $instanceName




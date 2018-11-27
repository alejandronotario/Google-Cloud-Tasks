#!usr/bin/bash

#Script to connect to the remote server to run Datalab and work with Spark

PROJECT=ei-ga-datastreaming
CLUSTER_NAME=ei-spark
REGION=europe-north1
ZONE=europe-north1-c
HOSTNAME=ei-spark-m
PORT=1080

export PROJECT=$PROJECT
export CLUSTER_NAME=$CLUSTER_NAME
export ZONE=$ZONE
export REGION=$REGION
export HOSTNAME=$HOSTNAME
export PORT=$PORT


#-D specifies dynamic application-level port forwarding
#-N instructs gcloud not to open a remote shell

gcloud compute ssh $HOSTNAME --project=$PROJECT --zone=$ZONE --\
	-D $PORT -N 





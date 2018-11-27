#!bin/bash

#Script to create cluster with scopes to use datalab with Spark

#Links:
#https://cloud.google.com/sdk/gcloud/reference/dataproc/clusters/create

#Command variables to export to fill
PROJECT=ei-ga-datastreaming
CLUSTER_NAME=ei-spark
REGION=europe-north1



export PROJECT=$PROJECT 
export CLUSTER_NAME=$CLUSTER_NAME
export REGION=$REGION

gcloud dataproc clusters create $CLUSTER_NAME --num-workers=2 --worker-machine-type=n1-standard-2 \
	--region=$REGION --initialization-actions gs://dataproc-initialization-actions/jupyter/jupyter.sh




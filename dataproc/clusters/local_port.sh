#!usr/bin/bash


#script to access Web application UIs running on your master instance with SSH local port forwarding, which forwards the master's port to a local port. For example, the following command lets you access localhost:1080 to reach cluster-name-m:8088

PORT=8123
HOSTNAME=ei-spark-m
PROJECT=ei-ga-datastreaming

export PORT=$PORT
export HOSTNAME=$HOSTNAME
export PROJECT=$PROJECT


gcloud compute ssh $HOSTNAME \
    --project=$PROJECT -- \
    -L $PORT:$HOSTNAME-m:8088 -N -n


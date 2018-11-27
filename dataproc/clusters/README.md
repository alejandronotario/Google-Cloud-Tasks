# Dataproc Cluster Creation and Configuration. 

Dataproc cluster creation with jupyter notebooks service to code pySpark

<br>
<hr>


## Overview
This task takes 4 steps:

- Cluster creation
- SSH tunnel
- proxy to open jupyter in the web browser
- local port to access

## Prerequisites

- Google Cloud Account

## Links

- https://cloud.google.com/sdk/gcloud/reference/dataproc/clusters

__Creating cluster with scopes to use datalab with Spark__

```bash

PROJECT=[PROJECT-NAME]
CLUSTER_NAME=[CLUSTER-NAME]
REGION=[REGION]


export PROJECT=$PROJECT
export CLUSTER_NAME=$CLUSTER_NAME
export REGION=$REGION

gcloud dataproc clusters create $CLUSTER_NAME --num-workers=2 --worker-machine-type=n1-standard-2 \
        --region=$REGION --initialization-actions gs://dataproc-initialization-actions/jupyter/jupyter.sh

```

__SSH. Connecting to the remote server to run Datalab and work with Spark__

```bash

PROJECT=[PROJECT-NAME]
CLUSTER_NAME=[CLUSTER-NAME]
REGION=[REGION]
ZONE=[ZONE]
HOSTNAME=[CLUSTER-NAME + m]
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
```

__Proxy. Browser configuration with proxy server parameters__

```bash
PORT=1080
HOSTNAME=ei-spark-m

export PORT=$PORT
export HOSTNAME=$HOSTNAME

/usr/bin/google-chrome --proxy-server="socks5://localhost:$PORT" \
        --user-data-dir=/tmp/$HOSTNAME

```

__Local Port__

Accessing Web application UIs running on your master instance with SSH local port forwarding, which forwards the master's port to a local port. For example, the following command lets you access localhost:8123 to reach cluster-name-m:8088

```bash
PORT=8123
HOSTNAME=[CLUSTER-NAME + m]
PROJECT=[PROJECT-NAME]

export PORT=$PORT
export HOSTNAME=$HOSTNAME
export PROJECT=$PROJECT


gcloud compute ssh $HOSTNAME \
    --project=$PROJECT -- \
    -L $PORT:$HOSTNAME-m:8088 -N -n

```


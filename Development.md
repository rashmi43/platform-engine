Where to begin:

## Prerequisites:

Postgres database server version 10.5
- Graphql
- Python 3.6 or above.
- Kubernetes 1.9 or above
- storyscript - (pip install storyscript)

## Steps:
Install all the above prerequisites.
Clone your forked version of platform-engine.
Configure platform-engine to talk to your Kubernetes.
Update asyncy/Config.py with your cluster CLUSTER_AUTH_TOKEN, CLUSTER_CERT and CLUSTER_HOST.
You can retrieve the CLUSTER_AUTH_TOKEN and CLUSTER_CERT using the below commands:
kubectl -n default get secrets  |grep default
kubectl -n default edit secret default-token-dq8ck
This will contain ca.crt and token values which can be decoded using base64 and updated in your Config.py.

## Run:
Follow this document and create your first app.
Use storyscript compile -j to compile your story.
Update app_public.releases table with the payload generated with the above command.
Run asyncy-server start and this will now deploy the story whose payload was uploaded to your  to your local Kubernetes. 

You can now use this environment to do your development.

# Links for ubuntu 16.04:
https://tecadmin.net/install-postgresql-server-on-ubuntu/
https://www.edureka.co/blog/install-kubernetes-on-ubuntu
https://docs.python-guide.org/starting/install3/linux/






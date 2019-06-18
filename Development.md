## Prerequisites:

- Postgres database server version 10.5
- Python 3.6 or above.
- Kubernetes 1.9 or above
- storyscript - (pip install storyscript)
- Graphql

## Steps:
1. Install all the above prerequisites.
2. Clone your forked version of platform-engine.
3. Configure platform-engine to talk to your Kubernetes.
4. Update asyncy/Config.py with your cluster CLUSTER_AUTH_TOKEN, CLUSTER_CERT and CLUSTER_HOST.
5. You can retrieve the CLUSTER_AUTH_TOKEN and CLUSTER_CERT using the below commands:
   kubectl -n default get secrets  |grep default
   kubectl -n default edit secret default-token-dq8ck
8. This will contain ca.crt and token values which can be decoded using base64 and updated in your Config.py.

## Run:
1. Follow this document and create your first app.
2. Use storyscript compile -j to compile your story.
3. Update app_public.releases table with the payload generated with the above command.
4. Run asyncy-server start and this will now deploy the story whose payload was uploaded to your  to your local Kubernetes. 

You can now use this environment to do your development.

# Links for ubuntu 16.04:
- https://tecadmin.net/install-postgresql-server-on-ubuntu/
- https://www.edureka.co/blog/install-kubernetes-on-ubuntu
- https://docs.python-guide.org/starting/install3/linux/






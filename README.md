# ProjectSet API

## Env variables


```
export JWT_SECRET_KEY=
export X_API_KEY=
export JWT_EXP=31536000
export JWT_HEADER="JWT"
export ADMIN_DISABLE="n"
export ADMIN_PASSWD=
export PWORKERS=1
export PWORKERS_SLEEP=15
export APP_CONF=./app.yaml

```

### App config 

app.yaml

```
envs:
  test-ocp-cluster:
    description: Dev repo for dev/preprod clusters
    url: https://github.com/migrx-io/projectset-crds.git
    branch: main
    token: ghp_Osa...
    conf_file: projectsets.yaml
  prod-ocp-cluster:
    description: Prod repo for production clusters
    url: https://github.com/migrx-io/projectset-crds.git
    branch: main  
    token: ghp_Osa...
    conf_file: projectsets.yaml

roles:
  user:
    projectset:
      edit:
        - labels
        - annotations
        - namespace
        - template
  admin:
    projectset:
      edit:
        - labels
        - annotations
        - namespace
        - template
    projectsettemplate:
      edit:
        - labels
        - annotations
        - namespace


```

### Deployment 

```

kubectl create ns projectset-api-system

kubectl create secret generic app-conf --from-file=app.yaml=app.yaml --namespace projectset-api-system

kubectl apply -f ./deploy/manifests.yaml
  
```


## Development

### Run locally

```
LOGLEVEL=DEBUG PYENV=/opt/homebrew/bin/ make run

```

### Run tests

```
LOGLEVEL=DEBUG PYENV=/opt/homebrew/bin/ make tests
```

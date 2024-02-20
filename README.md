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
export APP_CONF=./repos.yaml

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

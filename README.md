# ProjectSet API

## Env variables


```
export JWT_SECRET_KEY="secret"
export X_API_KEY="secret_api"
export JWT_EXP=31536000
export JWT_HEADER="JWT"
export ADMIN_DISABLE="n"
export ADMIN_PASSWD="super"
export PWORKERS=1
export PWORKERS_SLEEP=15

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

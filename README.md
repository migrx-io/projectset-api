# ProjectSet API

## Env variables


```
export JWT_SECRET_KEY="secret"
export JWT_EXP=31536000
export JWT_HEADER="JWT"
export ADMIN_PASSWD="super"
export ADMIN_DISABLE="n"
export PWORKERS=2
export PWORKERS_SLEEP=10

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

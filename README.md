### Run localstack (example)
```
LAMBDA_REMOTE_DOCKER=0 \
    LAMBDA_DOCKER_FLAGS='-p 19891:19891' \
    DEBUG=1 localstack start
```

### Create virutalenv (optional)
```
python -m venv .venv
source .venv/bin/activate
```

### Install dependecies
```
pip install poetry
poetry install
```

### Generate requirements
This step is only necessery if `pyproject.toml` or `poetry.lock` has changed.
```
poetry export --without-hashes --format=requirements.txt > requirements.txt
```

### Deploy lambda
Create sqs
```
awslocal sqs create-queue --queue-name fastapi-queue
```
Deploy lambda
```
chalice-local deploy --stage local
```

### Trigger lambda
Start rest server
```
uvicorn rest_app:app --reload
```
Call endpoint that sends message to sqs
```
curl "localhost:8000/send?title=test"
```

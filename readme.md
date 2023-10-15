# Test project
Project contains following tools:

upload_to_s3_script - downloads zipped file from web and uploads unzipped files to S3 bucket

## Prerequirements
* Install [docker-compose](https://docs.docker.com/compose/install/)
* Set environment variables to file .env
```
AWS_KEY=<key>
AWS_SECRET_KEY=<secret>
S3_BUCKET_NAME=<name>
```
## Usage

Run command
```
docker-compose build
docker-compose run --rm /bin/bash "python cli.py upload_to_s3_script <URL>"
```

Run tests
```
make tests/up-compose
make tests/pytest
```

Run checks
```
make tests/up-compose
make tests/all
```

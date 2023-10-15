#!/usr/bin/env bash

set -e

awslocal s3 mb s3://$S3_BUCKET_NAME
awslocal s3api put-bucket-acl --bucket $S3_BUCKET_NAME --acl public-read

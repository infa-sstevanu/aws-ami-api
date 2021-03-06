# AWS AMI REST-API

This API will return a AWS AMI ID based on regions, tags, and other filters

## Requirements

### AWS Access
Make sure you have AWS EC2ReadOnly access in ~/.aws/credentials
or using AWS environment variable

```bash
export AWS_ACCESS_KEY_ID=xxx
export AWS_SECRET_ACCESS_KEY=xxx
export AWS_REGION=<aws_region>
```

### GCP Access
Need to add/setup the application_default_credentials.json in the $HOME folder using below command
```bash
$ gcloud auth application-default login
```

### Azure Access
Follow this link to setup the Azure access for the API to be able to list the images
https://docs.microsoft.com/en-us/azure/developer/python/configure-local-development-environment?tabs=cmd

## Manual Installation

### Clone the repo

```bash
$ git clone https://github.com/infa-sstevanu/aws-ami-api
$ cd aws-ami-api
```

### Start a virtual environment

```bash
$ virtualenv .venv
$ source .venv/bin/activate
```

### Install the required pip modules

```bash
$ pip install -r requirements
```

### Set at least one cloud_enabled environment variable

To enable the AWS set below env:
```bash
$ export AWS_ENABLED=true
```

To enable GCP
```bash
$ export GCP_ENABLED=true
```

To enable Azure
```bash
$ export AZURE_ENABLED=true
```

### Unit Test (Optional)

After setup the virtualenv and install the pip modules
```bash
$ pytest -v .
```

### Run the application (for Development env)

```bash
$ export FLASK_APP=ami_api
$ export FLASK_ENV=development
$ flask run --port 8080
```

### Run the application (for Production)

```bash
$ gunicorn -w 4 -b 0.0.0.0:8080 "ami_api:create_app()"
```

Visit http://127.0.0.1:8080 in a browser to test if the installation works properly

OR

## Docker Installation

You can use docker to run the api (with this you don't need to start a virtualenv and pip install)

```bash
$ git clone https://github.com/infa-sstevanu/aws-ami-api
$ cd aws-ami-api
$ docker build -t ami_api .
$ docker run -v ~/.aws:/home/apiuser/.aws -p 8080:8080 -d ami_api
```

Visit http://127.0.0.1:8080 in a browser to test if the installation works properly

## API Usage

Check the healthy status of the API
```bash
$ curl "http://API_URL/health
```

Get the list of all available images on AWS_REGION=us-west-2 (default region)
```bash
$ curl "http://API_URL/ami"
```

Basic Usage
```bash
$ curl "http://API_URL/ami?provider=<aws|gcp|azure>&release=<Rxx.x>&os=<rhel|redhat|centos>&type=<infa|iics|cdie>&limit=<int>"
```

URL query parameters

(Mandatory)
```bash
provider
release
os
```

(Optional)
```bash
type
limit
```

### Example

Get all ami ids of AWS, R36 and RHEL(RedHat)
```bash
$ curl "http://API_URL/ami?provider=aws&release=R36&os=rhel"
```

Get all ami ids of AWS/R36/RedHat(RHEL)
```bash
$ curl "http://API_URL/ami?provider=aws&release=R36&os=redhat"
```

Get the last 3 ami ids of AWS/R36/RHEL
```bash
$ curl "http://API_URL/ami?provider=aws&release=R36&os=rhel&limit=3"
```

Get the last 10 ami ids of AWS/R36/Centos
```bash
$ curl "http://API_URL/ami?provider=aws&release=R36&os=centos&limit=10"
```

Get the last 5 ami ids of AWS/R36/RedHat/CDIE
```bash
$ curl "http://API_URL/ami?provider=aws&release=R36&os=Redhat&type=CDIE&limit=5"
```

Get the last ami id of AWS/R36.2/RHEL
```bash
$ curl "http://API_URL/ami?provider=aws&release=r36.2&os=Rhel&limit=1"
```

Get the last ami id of AWS/R36.2/RHEL/CDIE
```bash
$ curl "http://API_URL/ami?provider=aws&release=r36.2&os=Rhel&type=cdie&limit=1"
```

Note: The URL query parameter values are case-insensitive, ex: 'rhel' will yield the same result as 'RHEL' or 'Rhel'

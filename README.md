# AWS AMI REST-API

This API will return a AWS AMI ID based on regions, tags, and other filters

## Requirements
Make sure you have AWS EC2ReadOnly access in ~/.aws/credentials
or using AWS environment variable

```bash
export AWS_ACCESS_KEY_ID=xxx
export AWS_SECRET_ACCESS_KEY=xxx
export AWS_REGION=<aws_region>
```

## Installation

### Clone the repo

```bash
$> git clone https://github.com/infa-sstevanu/aws-ami-api
$> cd aws-ami-api
```

### Start a virtual environment

```bash
$> virtualenv .venv
$> source .venv/bin/activate
```

### Install the required pip modules

```bash
$> pip install -r requirements
```

### Run the application

```bash
$> export FLASK_APP=ami-api
$> export FLASK_ENV=development
$> flask run
```

Visit http://127.0.0.1:5000/ami in a browser and you should see all available images in region us-west-2

Note: Still on development, it is just a prototype 

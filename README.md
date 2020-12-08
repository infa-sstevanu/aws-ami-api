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

### Run the application

```bash
$ export FLASK_APP=ami_api
$ export FLASK_ENV=development
$ flask run
```

Visit http://127.0.0.1:5000 in a browser to test if the installation works properly

OR

## Docker Installation

You can use docker to run the api (with this you don't need to start a virtualenv and pip install)

```bash
$ git clone https://github.com/infa-sstevanu/aws-ami-api
$ cd aws-ami-api
$ docker build -t ami_api .
$ docker run -v ~/.aws:/home/ami-api/.aws -p 5000:5000 -d ami_api
```

Visit http://127.0.0.1:5000 in a browser to test if the installation works properly

## API Usage

Check the healthy status of the API
```bash
$ curl "http://127.0.0.1:5000/health
```

Get the list of all available images on AWS_REGION=us-west-2 (default region)
```bash
$ curl "http://127.0.0.1:5000/ami"
```

Retrieve the list of all available images on AWS_REGION=us-west-1
```bash
$ curl "http://127.0.0.1:5000/ami?region=us-west-1"
```

Get the list of all available images with specific tags filter `Key= tag:SERVICENAME, Values=[CLOUDAGENT]`
```bash
$ curl "http://127.0.0.1:5000/ami?region=us-west-2&tags=SERVICENAME:CLOUDAGENT"
```

Even you can combine tags to filter specific result (separated by `;`):
```bash
$ curl "http://127.0.0.1:5000/ami?region=us-west-2&tags=SERVICENAME:CLOUDAGENT;VERSION:v0.1"
```

Return the latest image-id using argument `latest`
```bash
$ curl "http://127.0.0.1:5000/ami?region=us-west-2&latest=true"
```

Lastly, combining arguments `tags`, `latest`
```bash
$ curl "http://127.0.0.1:5000/ami?region=us-west-2&tags=SERVICENAME:CLOUDAGENT;VERSION:v0.1&latest=true"
```

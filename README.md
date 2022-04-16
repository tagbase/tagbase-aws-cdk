# Tagbase AWS CDK

## Introduction

This project leverages the [AWS Cloud Development Kit](https://aws.amazon.com/cdk/) (CDK) to facilitate 
the configuration, deployment, operation and maintenance of 
[tagbase-server](https://github.com/tagbase/tagbase-server/) in AWS.

This project was born out of the need to 
[implement cloud-based persistent storage for PostgreSQL data](https://github.com/tagbase/tagbase-server/issues/80);
essentially eTUFF data stored in TagbaseDB.

Without going any further, it will benefit you to 
[learn about AWS CDK](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html)

The project is modularized such that you can develop, test, deploy and maintain individual subsystems independently.
In AWS language, each module is referred to as a [Stack](https://docs.aws.amazon.com/cdk/v2/guide/stacks.html).
For example, the TagbaseDB Stack manages resources such as a 
[PostgreSQL-backed AWS RDS](https://aws.amazon.com/rds/postgresql/) deployment and 
associated resources such as a security groups, inbound and outbound rules, etc.

# Prerequisites

* [Python 3.6](https://www.python.org/); or later including `pip` and `virtualenv`
* [NodeJS](https://nodejs.org/en/); long term support (LTS)
* [AWS CDK](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html#getting_started_prerequisites);
follow the tutorial thoroughly... it will way off.

# Configuration

Define the following global environment variables
* `TAGBASE_AWS_ACCOUNT`: The AWS account number to use for the deployment 
* `TAGBASE_DEFAULT_REGION`: The target [AWS region](https://aws.amazon.com/about-aws/global-infrastructure/regions_az/)

# High-level Guide

The `cdk.json` file tells the CDK Toolkit how to execute the app.

This project is set up like a standard Python project. The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

To deactivate the vurtualenv, do this:

```
% deactivate
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

Bootstrap the CDK deployment

```
% cdk bootstrap
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

N.B. If you are warned about runtime issues due to your node version not being supported, 
then you should upgrade to a supported node version as indicated in the warnings.

To add additional dependencies, for example other CDK libraries, just add
them to the `setup.py` file and rerun the `pip install -r requirements.txt`
command.

# Deploying

There are a few options for deploying.

## Deploying the entire stack

This deploys both the VPC and PostgreSQL stacks.
```
% cdk deploy --all
```

## Deploying the PostgreSQL DB into an existing VPC

Assumes that you already have a host VPC and wish to deploy the TagbaseDB stack into it.

```
% cdk deploy tagbase-db-stack
```
# Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!

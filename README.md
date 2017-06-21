# Lambda Static Blog Article Generator

This lambda function is used to generate HTML from markdown, along with syntax highlighting via

## Overview

This lambda function is meant to take markdown files and convert them to HTML with syntax highlighting. As it is meant to address my own needs there will most likely be lots of hard coded/non-generic code going down. If you want to tailor it to your own needs I recommend forking. The overall process is:

1. Setup CodePipeline with the GitHub repository that contains your markdown (currently this must be in a `sources/` directory)
2. Next, setup a Lambda function Invoke in the `Build` step which accepts the CodePipeline artifact as input
3. Commit some files to your repo that contain markdown
4. CodePipeline will proc from the commit
5. It will then take the code in question and make a ZIP file with it (called an artifact)
6. CodePipeline then invokes the blog generator lambda with JSON containing the artifact S3 location and other info
7. Lambda takes this JSON and behind the scenes converts it to a python dictionary
8. `lambda_handler` receives this data
9. It obtains the zip data from S3 into bytes
10. These bytes are converted to a BytesIO object to act as a file pointer
11. This is passed onto the `zipfile` module to open
12. The zip file is checked to see if any of the files are in the `sources/` directory ( bailing out early and marking the job complete if no file exists )
13. For each of the files in `sources/`, load them up and output to HTML in a string
14. Once all the HTML is collected write it out to S3
15. Finally, mark the job as complete
16. ???
17. Profit!

## Requirements

The following is required:

* An AWS account permisison to:
  * Lambda
  * CodePipeline
  * CloudWatch (Optional for Lambda logging)
  * S3
* Python 3.x
* boto3 for local development
* The scroll of delusion

TODO: The markdown and syntax highlighting libraries once I track down something that works

## Setup

First off an IAM role will need to be setup for the Lambda. This allows for the following:

* Reading the CodePipeline S3 ZIP artifact
* Writing the HTML markdown to the S3 bucket (potentially overwriting an existing version)
* Writing logs to CloudWatch
* Setting job state as completed/failed in CodePipeline
* Break dance battling lumberjacks

With that in mind the following IAM permissions are used:

### S3

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "s3:*",
      "Resource": "*"
    }
  ]
}
```

### CodePipeline

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "Stmt1497965040000",
            "Effect": "Allow",
            "Action": [
                "codepipeline:PutJobFailureResult",
                "codepipeline:PutJobSuccessResult"
            ],
            "Resource": [
                "*"
            ]
        }
    ]
}
```

### Logging

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "Stmt1497965473000",
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": [
                "arn:aws:logs:*:*:*"
            ]
        }
    ]
}
```

This are fairly simple based on my particular needs, but I recommend you evaluate how explicit these particular permissions need to be based on use and collaboration.

## Install

TODO: lambda upload script/commands/etc.

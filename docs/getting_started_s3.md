# Validating data on Amazon S3

This is a very short tutorial on using goodtables.io to continuously validate data hosted on [Amazon S3][s3].

## Pre-requisites

* A [GitHub][github] login
* An [Amazon S3][s3] login

## Instructions

### Setting up Amazon S3 bucket and read-only user

1. [Create a bucket on S3][howto-s3bucket] to hold your data
    * Create the bucket on the `us-west-2` region. It's a [current limitation][s3-region-bug] of goodtables.io that we're working to fix.
1. [Create a new IAM user][howto-iamuser]. This user will be used by goodtables.io to read your bucket.
    * Make sure you take note of the AWS Access Key ID, AWS Secret Access Key, and the User ARN.
1. Go to your [bucket's overview page][bucket-overview], click on the `Permissions` tab, and find the `Bucket Policy` link. We need the permissions:
    * _s3:ListBucket_: To list the bucket's contents
    * _s3:GetObject_: To read the bucket's files
    * _s3:GetBucketPolicy_, _s3:PutBucketPolicy_, _s3:GetBucketLocation_, and _s3:PutBucketNotification_: To set up the AWS Lambda functions that notifies goodtables.io when a new file is added.

The final bucket policy should look like:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "statement1",
            "Effect": "Allow",
            "Principal": {
                "AWS": "IAM_USER_ARN"
            },
            "Action": [
                "s3:ListBucket",
                "s3:GetBucketLocation",
                "s3:GetBucketPolicy",
                "s3:PutBucketPolicy",
                "s3:PutBucketNotification"
            ],
            "Resource": "arn:aws:s3:::BUCKET_NAME"
        },
        {
            "Sid": "statement2",
            "Effect": "Allow",
            "Principal": {
                "AWS": "IAM_USER_ARN"
            },
            "Action": ["s3:GetObject"],
            "Resource": "arn:aws:s3:::BUCKET_NAME/*"
        }
    ]
}
```

With your IAM User ARN and Bucket Name substituting the `IAM_USER_ARN` and `BUCKET_NAME`.

### Setting up goodtables.io

1. Login on [goodtables.io][gtio] using your GitHub account.
1. Go to the [Manage Sources][gtio-managesources] page, click on the `Amazon` tab, and on the plus sign on the right of the Filter input.
1. Fill in the `Access Key Id`, `Secret Access Key` and `Bucket Name` with the IAM User and bucket you just created in the previous section.

We're all set. Goodtables will automatically validate whenever a file is added or modified in the bucket. You can now [upload data to your bucket][howto-s3upload] and goodtables will automatically validate any tabular files (CSV, XLS, ODS, ...) and tabular data packages.

## Next steps

* [Write a table schema][gtio-dataschema] to validate the contents of your data
* [Configure which files are validated and how][gtio-configuring]

[gtio]: https://goodtables.io/ "Goodtables.io"
[github]: https://github.com/ "GitHub"
[s3]: https://aws.amazon.com/s3/ "Amazon S3"
[s3-region-bug]: https://github.com/frictionlessdata/goodtables.io/issues/136 "Can't add S3 bucket with other region that Oregon (us-west-2)"
[howto-s3bucket]: https://docs.aws.amazon.com/AmazonS3/latest/user-guide/create-bucket.html "How do I create an S3 Bucket?"
[howto-s3upload]: https://docs.aws.amazon.com/AmazonS3/latest/user-guide/upload-objects.html "How do I upload files and folders to an S3 Bucket?"
[howto-iamuser]: http://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html?icmpid=docs_iam_console "Create an IAM User in your AWS account"
[bucket-overview]: https://s3.console.aws.amazon.com/s3/buckets/ "Amazon S3 Bucket list"
[gh-new-repo]: https://help.github.com/articles/create-a-repo/ "GitHub: Create new repository tutorial"
[gtio-managesources]: https://goodtables.io/settings "Goodtables.io: Manage sources"
[datapackage]: https://frictionlessdata.io/data-packages/ "Data Package"
[gtio-dataschema]: writing_data_schema.html "Writing a data schema"
[gtio-configuring]: configuring.html "Configuring goodtables.io"

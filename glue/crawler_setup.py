import boto3

glue = boto3.client('glue')

response = glue.create_crawler(
    Name='smartcity-crawler',
    Role='arn:aws:iam::<your-account-id>:role/<your-glue-service-role>',
    DatabaseName='smartcity_db',
    Targets={'S3Targets': [{'Path': 's3://sparkstreamingdata/data/'}]},
    TablePrefix='',
    SchemaChangePolicy={
        'UpdateBehavior': 'UPDATE_IN_DATABASE',
        'DeleteBehavior': 'DEPRECATE_IN_DATABASE'
    }
)
glue.start_crawler(Name='smartcity-crawler')

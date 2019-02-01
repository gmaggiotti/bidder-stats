import numpy as np
import boto3

# Create CloudWatch client
cloudwatch = boto3.client('cloudwatch')

# List metrics through the pagination interface
paginator = cloudwatch.get_paginator('list_metrics')
for response in paginator.paginate(Namespace='CloudFront'):
    print(response['Metrics'])
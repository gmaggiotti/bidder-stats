import boto3
from datetime import datetime, timedelta

# Create CloudWatch client
cloudwatch = boto3.client('cloudwatch')

# List metrics through the pagination interface
# paginator = cloudwatch.get_paginator('list_metrics')
# for response in paginator.paginate(Dimensions=[{'Name': 'QPSType'}],
#                                    MetricName='QPS',
#                                    Namespace='RTB'):
#     print(response['Metrics'])


response = cloudwatch.get_metric_data(
    MetricDataQueries=[
        {
            'Id': 'qps',
            'MetricStat': {
                'Metric': {
                    'Namespace': 'RTB',
                    'MetricName': 'QPS',
                    'Dimensions': [
                        # {
                        #     u'Name': 'InstanceName',
                        #     u'Value': 'Safiro RTB 27'
                        # },
                        # {
                        #     u'Name': 'InstanceRegion',
                        #     u'Value': 'us-east-2'
                        # },
                        {
                            u'Name': 'QPSType',
                            u'Value': 'eff'
                        }
                    ],
                },
                'Period': 300,
                'Stat': 'Average',
                'Unit': 'Count/Second'
            },
            'ReturnData': True
        },
    ],
    StartTime=datetime(2018, 11, 12),
    EndTime=datetime(2018, 12, 22),
    ScanBy='TimestampDescending',
    MaxDatapoints=123)

print response

# paginator = cloudwatch.get_paginator('describe_alarms')
# for response in paginator.paginate(StateValue='INSUFFICIENT_DATA'):
#     print(response['MetricAlarms'])



CLOUDWATCH_METRICS=[
    {
        'namespace': 'RTB',
        'metricname': 'QPS'
    },
    {
        'namespace': 'RTB',
        'metricname': 'QPS',
        'dimensions': [
            {
                u'Name': 'QPSType',
                u'Value': 'eff'
            }
        ]
    },
]

CLOUDWATCH_PERIOD=300


for metric in CLOUDWATCH_METRICS:
    print 'INFO: Reading metric %s from namespace %s' % (metric['metricname'], metric['namespace'])
    response = None
    if 'dimensions' in metric.keys():
        response = cloudwatch.get_metric_statistics(
            Namespace=metric['namespace'],
            MetricName=metric['metricname'],
            Dimensions=metric['dimensions'],
            StartTime=datetime(2018, 12, 26),
            EndTime=datetime.utcnow(),
            Period=CLOUDWATCH_PERIOD,
            Statistics=['Average', 'Minimum', 'Maximum'],
            Unit='Count/Second'
        )
    else:
        response = cloudwatch.get_metric_statistics(
            Namespace=metric['namespace'],
            MetricName=metric['metricname'],
            StartTime=datetime(2018, 12, 26),
            EndTime=datetime.utcnow(),
            Period=CLOUDWATCH_PERIOD,
            Statistics=['Average', 'Minimum', 'Maximum'],
            Unit='Count/Second')
    print response
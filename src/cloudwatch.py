import boto3
from datetime import datetime, timedelta
from stats_util import get_cloudwatch_eff_histogram

# Create CloudWatch client
cloudwatch = boto3.client('cloudwatch',region_name='ap-southeast-1')

# List metrics through the pagination interface
# paginator = cloudwatch.get_paginator('list_metrics')
# for response in paginator.paginate(Dimensions=[{'Name': 'QPSType'}],
#                                    MetricName='QPS',
#                                    Namespace='RTB'):
#     print(response['Metrics'])


# response = cloudwatch.get_metric_data(
#     MetricDataQueries=[
#         {
#             'Id': 'qps',
#             'MetricStat': {
#                 'Metric': {
#                     'Namespace': 'RTB',
#                     'MetricName': 'QPS',
#                     'Dimensions': [
#                         {
#                             u'Name': 'QPSType',
#                             u'Value': 'eff'
#                         }
#                     ],
#                 },
#                 'Period': 300,
#                 'Stat': 'Average',
#                 'Unit': 'Count/Second'
#             },
#             'ReturnData': True
#         },
#     ],
#     StartTime=datetime(2018, 11, 12),
#     EndTime=datetime(2018, 12, 22),
#     ScanBy='TimestampDescending',
#     MaxDatapoints=123)
#
# print response

# paginator = cloudwatch.get_paginator('describe_alarms')
# for response in paginator.paginate(StateValue='INSUFFICIENT_DATA'):
#     print(response['MetricAlarms'])



CLOUDWATCH_METRICS=[
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

CLOUDWATCH_PERIOD=1800


# for metric in CLOUDWATCH_METRICS:
#     print 'INFO: Reading metric %s from namespace %s' % (metric['metricname'], metric['namespace'])
#     response = cloudwatch.get_metric_statistics(
#         Namespace=metric['namespace'],
#         MetricName=metric['metricname'],
#         Dimensions=metric['dimensions'],
#         StartTime=datetime(2018, 12, 1),
#         EndTime=datetime.utcnow(),
#         Period=CLOUDWATCH_PERIOD,
#         Statistics=['Average'],
#         Unit='Count/Second'
#     )
#
#     eff_list =sorted( [ (eff['Timestamp'],eff['Average']) for eff in response['Datapoints']] )

time, freq = get_cloudwatch_eff_histogram(datetime(2018, 12, 1),datetime(2018, 12, 27),'ap-southeast-1')
print freq
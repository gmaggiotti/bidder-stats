from pyhive import presto
import pandas as pd
import numpy as np
import boto3
from datetime import datetime

def enum(**enums):
    return type('Enum', (), enums)


Type = enum(qps_cap=1, qps_eff=2, avg_lat=3, max_lat=4, timeouts=5, bids=6)

def get_norm_dist(mu, sigma):
    return mu + sigma * np.random.randn(10000)

#
#  time,qps_cap,qps_eff,avg_lat,max_lat,timeouts,bids
#
def get_serie(dataset, type, date_from, date_to):
    fn = dataset[:, type]
    return fn

def get_presto_bidrate_histogram(beans, date_from, date_to, region):
    query = """
     select numeric_histogram("""+str(beans)+""", cant) as hist, max(cant) as max, min(cant) as min, count(cant) as total 
     from (  
             select date_trunc('second', from_iso8601_timestamp(created)), count(*) as cant 
             from hive.aleph.bids_daily 
             where day >= '""" + date_from + """' and day <= '""" + date_to + """' and region = '"""+region+"""'
             group by 1)
    """

    cursor = presto.connect(host='emr-prd-queries.jampp.com', username='gmaggiotti', port=8889).cursor()
    cursor.execute(query)
    cursor.close()
    hst = cursor.fetchall()
    df = pd.DataFrame(hst)

    hist, max_, min_, cant = df.iloc[0].values
    hist = sorted([(round(float(k), 2),int(v)) for k,v in hist.items()])
    xvals = [int(x[0]) for x in hist]
    yvals = [x[1] for x in hist]
    return xvals, yvals


def get_stats(x, y):
    n = np.sum(y)
    mean = np.dot(x, y) / float(n)
    standard_dsviation = np.sqrt(np.sum((x - mean) ** 2 * np.array(y)) / float(n))
    return mean, standard_dsviation


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


def get_cloudwatch_eff_histogram(date_from, date_to, region):
    # Create CloudWatch client
    cloudwatch = boto3.client('cloudwatch',region_name=region)
    for metric in CLOUDWATCH_METRICS:
        response = cloudwatch.get_metric_statistics(
            Namespace=metric['namespace'],
            MetricName=metric['metricname'],
            Dimensions=metric['dimensions'],
            StartTime=date_from,
            EndTime=date_to,
            Period=CLOUDWATCH_PERIOD,
            Statistics=['Average'],
            Unit='Count/Second'
        )

    eff_list =sorted( [ (eff['Timestamp'],eff['Average']) for eff in response['Datapoints']] )
    timestamp = [x[0] for x in eff_list]
    freq = [x[1] for x in eff_list]
    return timestamp,freq





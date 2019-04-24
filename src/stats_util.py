# from pyhive import presto
import numpy as np
import boto3

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
     select numeric_histogram({0}, cant) as hist, max(cant) as max, min(cant) as min, count(cant) as total 
     from (  
             select date_trunc('second', from_iso8601_timestamp(created)), count(*) as cant 
             from hive.aleph.bids_daily 
             where day >= '{1}' and day <= '{2}' and region = '{3}'
             group by 1)
    """.format(beans,date_to,date_to,region)

    cursor = presto.connect(host='emr-prd-queries.jampp.com', username='gmaggiotti', port=8889).cursor()
    cursor.execute(query)
    cursor.close()
    hst = cursor.fetchall()

    hist = sorted([(round(float(k), 2), int(v)) for k, v in hst[0][0].items()])
    xvals = [int(x[0]) for x in hist]
    yvals = [x[1] for x in hist]
    return xvals, yvals


def get_stats(x, y):
    n = np.sum(y)
    mean = np.dot(x, y) / float(n)
    standard_dsviation = np.sqrt(np.sum((x - mean) ** 2 * np.array(y)) / float(n))
    return mean, standard_dsviation


CLOUDWATCH_METRICS = {
    'namespace': 'RTB',
    'metricname': 'QPS',
    'dimensions': [
        {
            u'Name': 'QPSType',
            u'Value': 'cap'
        },
    ]
}

CLOUDWATCH_METRICS_1 = {
    'namespace': 'CloudFront',
    'metricname': 'Requests',
    'dimensions': [
        {
            u'Name': 'Distributionid',
            u'Value': 'E317LTNGG1QQ5K'
        },
    ]
}


CLOUDWATCH_PERIOD = 60


def get_cloudwatch_times_serie(date_from, date_to, region, metric, stats):
    # Create CloudWatch client
    CLOUDWATCH_METRICS['dimensions'][0]['Value'] = metric
    #CLOUDWATCH_METRICS = CLOUDWATCH_METRICS_1
    cloudwatch = boto3.client('cloudwatch', region_name=region)
    response = cloudwatch.get_metric_statistics(
        Namespace=CLOUDWATCH_METRICS['namespace'],
        MetricName=CLOUDWATCH_METRICS['metricname'],
        Dimensions=CLOUDWATCH_METRICS['dimensions'],
        StartTime=date_from,
        EndTime=date_to,
        Period=CLOUDWATCH_PERIOD,
        Statistics=[stats],
        Unit='Count/Second'
        )

    eff_list = sorted([(eff['Timestamp'], eff[stats]) for eff in response['Datapoints']])
    timestamp = [x[0] for x in eff_list]
    freq = [x[1] for x in eff_list]
    return timestamp, freq

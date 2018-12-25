from pyhive import presto
import pandas as pd
import numpy as np

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

def get_presto_bidrate_histogram(beans, date_from, date_to):
    query = """
     select numeric_histogram("""+str(beans)+""", cant) as hist, max(cant) as max, min(cant) as min, count(cant) as total 
     from (  
             select date_trunc('second', from_iso8601_timestamp(created)), count(*) as cant 
             from hive.aleph.bids_daily 
             where day >= '""" + date_from + """' and day <= '""" + date_to + """' and region = 'ap-southeast-1'
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

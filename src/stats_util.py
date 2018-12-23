from pyhive import presto
import pandas as pd

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

def get_presto_bidrate_histogram(beans, year, month, day):
    query = """
     select numeric_histogram("""+str(beans)+""", cant) as hist, max(cant) as max, min(cant) as min, count(cant) as total 
     from (  
             select date_trunc('second', from_iso8601_timestamp(created)), count(*) as cant 
             from hive.aleph.bids_daily 
             where day = {} and region = 'ap-southeast-1' 
             group by 1)
    """.format("'{:04d}{:02d}{:02d}'".format(year,month,day))

    cursor = presto.connect(host='emr-prd-queries.jampp.com', username='gmaggiotti', port=8889).cursor()
    cursor.execute(query)
    cursor.close()
    hst = cursor.fetchall()
    df = pd.DataFrame(hst)

    hist, max_, min_, cant = df.iloc[0].values
    return  sorted([(round(float(k), 2),int(v)) for k,v in hist.items()])

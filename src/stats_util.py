def enum(**enums):
    return type('Enum', (), enums)


Type = enum(qps_cap=2, qps_eff=3, avg_lat=4, max_lat=5, timeouts=6, bids=7)


#  time,qps_cap,qps_eff,avg_lat,max_lat,timeouts,bids
#
def get_serie(dataset, type, date_from, date_to):
    fn = dataset[:, type]
    return fn

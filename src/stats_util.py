def enum(**enums):
    return type('Enum', (), enums)


Type = enum(qps_cap=1, qps_eff=2, avg_lat=3, max_lat=4, timeouts=5, bids=6)

#
#  time,qps_cap,qps_eff,avg_lat,max_lat,timeouts,bids
#
def get_serie(dataset, type, date_from, date_to):
    fn = dataset[:, type]
    return fn

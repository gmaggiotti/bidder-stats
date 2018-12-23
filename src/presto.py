from stats_util import get_presto_bidrate_histogram

hist = get_presto_bidrate_histogram(24,2018,12,10)

print(hist)

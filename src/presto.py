from stats_util import get_presto_bidrate_histogram

hist = get_presto_bidrate_histogram(24,"20181210","20181210")

print(hist)

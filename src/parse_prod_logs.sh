#!/bin/bash
cat ../data/$1.log | fgrep qps |fgrep -v 'DEBUG'| awk -F " " '{ printf("%s%s,%s,%s,%s,%s,%s%s\n",$1,$2,$6,$9,$12,$15,$19,$29) }' | sed 's/INFO:rtb:threadpool:worker:// ; s/s// ; s/-//g ; s/://g ' > ../data/$1.csv
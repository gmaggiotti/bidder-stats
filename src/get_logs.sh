#!/bin/bash
# $1. Is the IP
# $2. Is the number of lines to fetch
# $3. Is the name of the output log file

ssh ec2-user@$1 "tail -$2 /var/log/gunicorn/safirortb.log| fgrep qps" > ../data/$3.log
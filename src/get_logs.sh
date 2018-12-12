#!/bin/bash
ssh ec2-user@$1 "tail -$2 /var/log/gunicorn/safirortb.log| grep qps" > ../data/$3.log
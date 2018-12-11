#!/bin/bash
ssh ec2-user@172.17.13.230 "tail -$1 /var/log/gunicorn/safirortb.log| grep qps" > ../data/safirortb.log
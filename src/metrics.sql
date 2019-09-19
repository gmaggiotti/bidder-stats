WITH
bids AS (
  SELECT
    trans_id,
    instance_id,
    DATE_TRUNC('{granularity}', from_iso8601_timestamp(created)) as time_stamp,
    price as price
  FROM hive.aleph.bids_daily
  WHERE instance_id IN ('{benchmark_id}', '{canary_id}')
    AND day BETWEEN '{start_date:%Y%m%d}' AND '{end_date:%Y%m%d}'
  AND created BETWEEN '{start_date:%Y-%m-%dT%H:%M:%S}' AND '{end_date:%Y-%m-%dT%H:%M:%S}'
),
impressions AS (
  SELECT
    trans_id,
    DATE_TRUNC('{granularity}', from_iso8601_timestamp(created)) as time_stamp
  FROM hive.aleph.impressions_daily
  WHERE day BETWEEN '{start_date:%Y%m%d}' AND '{end_date:%Y%m%d}'
  AND created BETWEEN '{start_date:%Y-%m-%dT%H:%M:%S}' AND '{end_date:%Y-%m-%dT%H:%M:%S}'
),
clicks AS (
  SELECT
    trans_id,
    DATE_TRUNC('{granularity}', from_iso8601_timestamp(created)) as time_stamp
  FROM hive.aleph.clicks_daily
  WHERE day BETWEEN '{start_date:%Y%m%d}' AND '{end_date:%Y%m%d}'
  AND created BETWEEN '{start_date:%Y-%m-%dT%H:%M:%S}' AND '{end_date:%Y-%m-%dT%H:%M:%S}'
)
SELECT
  bids.instance_id AS instance_id,
  bids.time_stamp AS time_stamp,
  COUNT(bids.trans_id) AS bid_rate,
  COUNT(impressions.trans_id) AS impression_rate,
  COUNT(clickS.trans_id) AS click_rate,
  AVG(bids.price) AS avg_bid_price,
  CAST(COUNT(impressions.trans_id) AS DOUBLE) / CAST(COUNT(bids.trans_id) AS DOUBLE) AS win_rate,
  CAST(COUNT(clicks.trans_id) AS DOUBLE) / CAST(COUNT(impressions.trans_id) AS DOUBLE) AS ctr
FROM bids
LEFT JOIN impressions
  ON bids.trans_id = impressions.trans_id
LEFT JOIN clicks
  ON impressions.trans_id = clicks.trans_id
GROUP BY 1,2
ORDER BY 1,2

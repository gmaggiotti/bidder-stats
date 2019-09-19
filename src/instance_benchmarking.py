import datetime as dt
import os
import sys

import matplotlib
matplotlib.use('TkAgg')

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import yaml


from datacommon.dbconnectors import PrestoDb
# from ragnar.extractors import CustomExtractor

#   how to run
#   python instance_benchmarking.py i-04834d146c5fbb05a i-087f16d69b8649f9f 2019-09-18T12 2019-09-19T12
#

plt.style.use('seaborn')


class InstanceBenchmarking():

    def __init__(
            self,
            canary_id,
            benchmark_id,
            start_date,
            end_date,
            granularity='minute',
            cred_path='~/.credentials/credentials.yaml',
            cred_dict=None
            ):

        self.start_date = start_date
        self.end_date = end_date
        self.canary_id = canary_id
        self.benchmark_id = benchmark_id
        self.granularity = granularity
        self.df = None
        if os.path.isfile(cred_path):
            with open(os.path.expanduser(cred_path)) as f:
                credentials = yaml.load(f, Loader=yaml.BaseLoader)
        else:
            self.presto = PrestoDb(**cred_dict)

    def extract(self):

        query_params = dict(
            canary_id=self.canary_id,
            benchmark_id=self.benchmark_id,
            start_date=self.start_date,
            end_date=self.end_date,
            granularity=self.granularity
            )
        with open('metrics.sql') as f:
            query_metrics = f.read().format(**query_params)
        self.df = self.presto.to_frame(query_metrics)
        # self.df = CustomExtractor(query_metrics, with_cache=True).to_frame()
        return self.df

    def _generic_plot(self, argument, title, outliers, step=None, save=True):
        save_path = os.path.join(
            'results_{}_vs_{}_{start_date:%Y-%m-%d}'.format(
                self.canary_id,
                self.benchmark_id,
                start_date=self.start_date),
            'figures')
        if not os.path.isdir(save_path) and save:
            os.makedirs(save_path)
        step = step or (outliers[1] - outliers[0]) / 20
        bins = np.arange(outliers[0], outliers[1], step)
        benchmark = self.df.loc[self.df.instance_id == self.benchmark_id]
        canary = self.df.loc[self.df.instance_id == self.canary_id]
        plt.figure(figsize=(10, 6))
        plt.hist(
            canary[argument],
            bins=bins,
            density=True,
            label='Canary')
        plt.hist(
            benchmark[argument],
            bins=bins,
            alpha=0.5,
            label='Benchmark',
            density=True,)
        plt.title(title)
        plt.xlabel(title)
        plt.ylabel('Probability density')
        plt.legend()
        plt.savefig(os.path.join(save_path, argument))
        # plt.show()

    def plot_bid_rate(self, outliers=[200, 1500]):
        self._generic_plot(
            argument='bid_rate',
            title='Bids per {}'.format(self.granularity),
            outliers=outliers)

    def plot_impression_rate(self, outliers=[0, 800]):
        self._generic_plot(
            argument='impression_rate',
            title='Impressions per {}'.format(self.granularity),
            outliers=outliers)

    def plot_ctr(self, outliers=[0, 0.1]):
        self._generic_plot(
            argument='ctr',
            title='CTR (Clicks / Impressions)',
            outliers=outliers)

    def plot_win_rate(self, outliers=[0, 1]):
        self._generic_plot(
            argument='win_rate',
            title='Win rate (Impressions / Bids)',
            outliers=outliers)

    def plot_avg_bid_price(self, outliers=[0.2, 1.5]):
        self._generic_plot(
            argument='avg_bid_price',
            title='Avg bid price per minute',
            outliers=outliers)

    def aggregate_metrics(self, save=True):
        save_path = os.path.join(
            'results_{}_vs_{}_{start_date:%Y-%m-%d}'.format(
                self.canary_id,
                self.benchmark_id,
                start_date=self.start_date),
            'tables')

        if not os.path.isdir(save_path) and save:
            os.makedirs(save_path)

        benchmark = self.df.loc[self.df.instance_id == self.benchmark_id]
        canary = self.df.loc[self.df.instance_id == self.canary_id]

        benchmark.describe().to_csv(
            os.path.join(save_path, 'benchmark_metrics.csv'))
        canary.describe().to_csv(
            os.path.join(save_path, 'canary_metrics.csv'))

        return canary, benchmark


if __name__ == "__main__":

    ib = InstanceBenchmarking(
        canary_id=sys.argv[1],
        benchmark_id=sys.argv[2],
        start_date=dt.datetime.strptime(sys.argv[3], '%Y-%m-%dT%H'),
        end_date=dt.datetime.strptime(sys.argv[4], '%Y-%m-%dT%H'),
        granularity=sys.argv[5] if len(sys.argv) == 6 else 'minute',
        cred_dict={
            'host': 'emr-prd-data.jampp.com',
            'username': 'DEPLOY-TEST',
            'port': 8889})
    ib.extract()
    ib.plot_bid_rate(outliers=[200, 1300])
    ib.plot_impression_rate(outliers=[0, 300])
    ib.plot_win_rate(outliers=[0, 0.5])
    ib.plot_ctr(outliers=[0, 0.1])
    ib.plot_avg_bid_price(outliers=[0.2, 1.5])
    ib.aggregate_metrics(save=True)

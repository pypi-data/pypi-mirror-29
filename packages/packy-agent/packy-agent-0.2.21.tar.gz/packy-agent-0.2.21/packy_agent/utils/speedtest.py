from __future__ import absolute_import

import speedtest


def run_speedtest(server_id):
    speedtest_client = speedtest.Speedtest()
    speedtest_client.get_servers([server_id])
    speedtest_client.get_best_server()
    speedtest_client.download()
    speedtest_client.upload()

    return speedtest_client.results

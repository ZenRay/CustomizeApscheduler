#-*-coding:utf8-*-
"""Test Configuration

"""

from __future__ import absolute_import
import sys
import os

sys.path.append("..")


from Scheduler.core import BackgroundScheduler


class TestScheduler:
    def test_init_none(self):
        scheduler = BackgroundScheduler("Data")


        assert scheduler._jobstores_alias == "Data"


    def test_init_executor(self):
        scheduler = BackgroundScheduler("Data", executor="pool")


        assert scheduler._jobstores_alias == "Data"    

    def test_init_jobstore(self):
        scheduler = BackgroundScheduler("Data", jobstore="redis")


        assert scheduler._jobstores_alias == "Data"    
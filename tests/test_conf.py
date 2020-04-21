#-*-coding:utf8-*-
"""Test Configuration

"""

from __future__ import absolute_import
import sys
import os

sys.path.append("..")


class TestConf:
    def test_mysql(self):
        from Scheduler.conf import _mysql
        conf = {
            "host":"127.0.0.1",
            "port":3306,
            "user":"root",
            "password":None,
            "charset":"utf8mb4",
            "use_unicode":True,
            "db": "hndx_dial_dev",
            "connect_timeout": 35
        }

        assert _mysql.get("table") == "dial_plan_task"
        assert _mysql.get("conf") == conf

    
    def test_mongo(self):
        from Scheduler.conf import _mongodb

        assert _mongodb.get("host") == "127.0.0.1"


    def test_redis(self):
        from Scheduler.conf import _redis

        assert _redis.get("host") == "127.0.0.1"


    def test_scheduler(self):
        from Scheduler.conf import SCHEDULER
        
        assert SCHEDULER.get('jobstores').get('redis').get_string('host') == '127.0.0.1'
#-*-coding:utf8-*-
"""
Description:
    The script is used to parse the configuration:
    * mysql, basic mysql database connection configuration
    * redis, basic redis database connection configuration. It's recommendation
        that use the connection pool 
    * mongodb, basic mongodb database connnection configuration
    * SCHEDULER, it's scheduler configuration about executers and jobstores 
"""
from __future__ import absolute_import

from pyhocon import ConfigFactory
from os import path


_mysql = ConfigFactory.parse_file(path.join(path.dirname(__file__), "_mysql.conf"))
_redis = ConfigFactory.parse_file(path.join(path.dirname(__file__), "_redis.conf"))
_mongodb = ConfigFactory.parse_file(path.join(path.dirname(__file__), "_mongo.conf"))

SCHEDULER = ConfigFactory.parse_file(path.join(path.dirname(__file__), "_scheduler.conf"))

__all__ = ["_mysql", "_redis", "SCHEDULER", "_mongodb"]

del path
del ConfigFactory
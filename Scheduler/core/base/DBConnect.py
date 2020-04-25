#-*-coding:utf8-*-
from __future__ import absolute_import

import pymysql
import logging
from Scheduler.conf import _mysql

MYSQL_CONF = _mysql.get("conf")
MYSQL_TABLE  = _mysql.get("table")


class DBConnector(object):
    @property
    def _logger(self):
        """Logger Property"""
        logger = logging.getLogger(self.__class__.__name__)
        return logging.LoggerAdapter(logger, {"Database": self})
        

    def log(self, message, level=logging.DEBUG, **kwargs):
        """Run logger to display log information"""
        self._logger.log(level, message, **kwargs)
    
    def close(self):
        """Close Connection"""
        if hasattr(self, "connection"):
            self.connection.close()
        elif hasattr(self, "Connection"):
            self.Connection.close()


class MySQLConnect(DBConnector):
    """MySQL Connection Obejct

    Connect the MySQL database with basic configuration, which there is not database
    connected in default configuration. But database can be specified with assign
    a database to property cursor.

    Properties:
        Connection: connect RDBM with default mysql config
        connection: pymysql.connections.Connection object, same with Connection
        cursor: pymyql.cursors object. If object with a db at initialize, there 
            is the object. Otherwise, get a cursor object with assigning a db
        _cursor: a method create a pymysql.cursors
        connect: a method create pymysql.connections.Connection object
    Arguments:
        db: a database name that is used to select database, default None don't 
            use any database

    Examples:
        >>> from ScrapyFrame.utils.base.database import *
        >>> conn = MySQLConnect()
        >>> conn.connection
            <pymysql.connections.Connection at 0x10afcec50>
        >>> conn.cursor
            "Database isn't connected"
        >>> conn.cursor = "hzjy_test"
        >>> conn.cursor
            <pymysql.cursors.Cursor at 0x10a461750>
        >>> conn.cursor.execute("SHOW TABLES;") 
    """


    def __init__(self):
        self.Connection = self.__connect()

    def __connect(self):
        return pymysql.connect(**MYSQL_CONF)


    @property
    def connection(self):
        return self.Connection


    @property
    def cursor(self):
        self.Connection.ping(reconnect=True)
        return self.Connection.cursor()
    

    @cursor.setter
    def cursor(self, db):
        return self._cursor(db)

    
    @cursor.getter
    def cursor(self):
        if self.Connection.db is None:
            return "Database isn't connected"
        else:
            self.log(f"Database {self.Connection.db} is connected", level=logging.INFO)
            return self.Connection.cursor() 


    def _cursor(self, db):
        # connect a new database
        if not self.Connection.db:
            self.Connection.select_db(db)
            self.Connection.db = db
        else:
            logging.info(f"Convert database {self.Connection.db} to {db}")
            self.Connection.select_db(db)
            self.Connection.db = db
        
        return self.Connection.cursor()
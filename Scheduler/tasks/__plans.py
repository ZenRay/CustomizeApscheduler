#-*-coding:utf8-*-
"""
Retrive plan from database
"""
from __future__ import absolute_import

import logging

from Scheduler.core import MySQLConnect, MYSQL_TABLE

DEFAULT_FORMATTER = "%(asctime)s [%(threadName)s] %(levelname)s: %(message)s"
logging.basicConfig(level=logging.INFO,datefmt="%Y/%m/%d %H:%M:%S", format=DEFAULT_FORMATTER)

logger = logging.getLogger(__name__)

FIELDS = ["id", "dial_plan_id", "dial_service_type", "dial_template", 
            "company_id", "plan_start_time"]

class PlanTask:
    def __init__(self):
        self.connection = MySQLConnect()
        self.task_fields =  FIELDS

    
    def _get_plan_task(self, condition="`dial_status` = 0 LIMIT 1"):
        """Query Dial Plan Task

        Query plan task in `dial_plan_task`, and retrive the single task.

        Arguments:
            condition: 

        """
        cursor = self.connection.cursor
        # 查询数据表，获取任务
        _sentence = self.query_sentence(MYSQL_TABLE, self.task_fields, \
            condition=condition)
        query = cursor.execute(_sentence)
        
        # 返回字典
        if query == 1:
            temp = cursor.fetchone()
            result = {key: temp[index] for index, key in enumerate(self.task_fields)}
            logger.log(level=logging.INFO, msg="Get One Task")
        elif query == 0:
            result = None
            logger.log(level=logging.INFO, msg="Task Exhausted")
        return result


    def query_sentence(self, table, fields, condition=None):
        """Create SQL Query Sentence
        Create a insert sentence, like that:
            SELECT (`col1`, `col2`) FROM <table>  VALUES (%s, %s)
        
        If condition exists, use `WHERE` expression:
            SELECT (`col1`, `col2`) FROM <table>  VALUES (%s, %s) WHERE <condition>
        
        Arguments:
            table: string, table name
            fields: list or tuple, fields name
            condition: string, `where` expression, eg: "`id` = 12"
        """
        symbol=r"%s"
        sentence = "SELECT {fieldnames} FROM {tb}"

        fieldnames = "{column}".format(
            column=", ".join("`{}`".format(field) for field in fields)
        )

        values_symbol = ",".join((symbol for i in range(len(fields))))

        sentence = sentence.format(tb=table, fieldnames=fieldnames)

        if not condition:
            return sentence + ";"
        elif isinstance(condition, str):
            return sentence + " WHERE " + condition + ";"
        else:
            raise TypeError(f"condition must be string, but get {type(condition)}")


    def close(self):
        self.connection.close()


    def __call__(self):
        result = self._get_plan_task()
        logger.log(level=logging.INFO, msg=f"Task: {result}")
        print(result)
        return result


# 打包提取任务的类到一个函数
def retrice_task():
    """Combine Plan Task Query"""
    conn = PlanTask()
    result = conn._get_plan_task()
    # print(result)
    conn.connection.close()
    return result


"""
from datetime import datetime, timedelta 
from Scheduler.core import BackgroundScheduler 
from Scheduler.tasks.__plans import PlanTask, get
scheduler = BackgroundScheduler("Query")
scheduler.start()
test = PlanTask()
scheduler.add_job(get, "date", id="test", jobstore="redis", executor="pool", run_date=datetime.now() + timedelta(seconds
   =30))
"""
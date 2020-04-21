# 说明
基于 Apscheduler 进行定制需要的任务调度。

# Requirements
PyHOCON=0.3.54

# 配置说明
相关配置文件在 `conf` 文件夹中，其中 `_scheduler.conf` 是 scheduler 的配置文件（默认配置了 executers 和 jobstores）。所有的配置信息都通过 pyhocon 进行解析。
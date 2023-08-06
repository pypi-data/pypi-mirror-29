Email Job[With Hive Server Query]
=================================

It's a powerful component help us send customer's special detail data through email attachments.

User Guide
==========

1. Ready some configure files
------------------------------

.. code-block::

    # /etc/pythoncfg/hive.ini

    [HiveServer]
    host=127.0.0.1
    port=10000
    user=hive
    db=default

    # /etc/pythoncfg/email.ini

    [EmailServer]
    server=mail.163.com
    port=25
    user=elkan1788@gmail.com
    passwd=xxxxxx
    mode=TSL


> Please replace the secure info of your. Kind like Hive Server host and email SMTP server user password.

2. Ready your job info configure file
--------------------------------------

_**Example:**_
.. code-block::

    [JobInfo]
    title=邮件报表任务测试

    [CSVFolder]
    folder=/opt/csv_files/

    # Please notice that CSVFile,CSVHead,HQLScript must be same length.
    # And suggest that use prefix+number to flag and write.
    [CSVFile]
    file1=省份分组统计
    file2=城市分组统计

    [CSVHead]
    head1=省份,累计
    head2=省份,城市,累计

    [HQLScript]
    script1=select cn_state,count(1) m from ext_act_ja1
    script2=select cn_state,cn_city,count(1) m from ext_act_ja2

    [EmailInfo]
    to=elkan1788@gmail.com;
    cc=2292706174@qq.com;
    # %s it will replace as the start date.
    subject=%s区域抽奖统计[测试]
    body=此邮件由系统自动发送，请勿回复，谢谢！

> Remember that the file's struct doesn't change. You can save it anywhere you like. And append it as parameter to `Python` bin file.
 
3. Start Python Script
-----------------------

Find out where you install this component folder. Run script as below:

.. code-block::

    python -u bin/email_job.py "/etc/emailjob/test_job.ini" "2018-01-01 10:00:00" "2018-01-01 14:00:00"


> Parameters:
> 1. email job configure file path
> 2. start time (no required)
> 3. stop time (no required)

# 4. Success execute output log

.. code-block::

    2018-02-20 16:28:21,561 [INFO] {__main__  } - Now running 邮件报表任务测试 Email Job...
    2018-02-20 16:28:21,561 [INFO] {__main__  } - Start time: 2018-02-22
    2018-02-20 16:28:21,562 [INFO] {__main__  } - Stop time: 2018-02-20
    2018-02-20 16:28:21,691 [INFO] {pyhive.hive} - USE `default`
    2018-02-20 16:28:21,731 [INFO] {ppytools.hive_client} - Hive server connect is ready. Transport open: True
    2018-02-20 16:28:31,957 [INFO] {ppytools.email_client} - Email SMTP server connect ready.
    2018-02-20 16:28:31,957 [INFO] {root      } - File name list:
    2018-02-20 16:28:31,957 [INFO] {root      } - file1: 省份分组统计
    2018-02-20 16:28:31,957 [INFO] {root      } - file2: 城市分组统计
    2018-02-20 16:28:31,957 [INFO] {root      } - CSV file head list:
    2018-02-20 16:28:31,957 [INFO] {root      } - head1: 省份,累计
    2018-02-20 16:28:31,957 [INFO] {root      } - head2: 省份,城市,累计
    2018-02-20 16:28:31,957 [INFO] {root      } - script1: select cn_state,count(1) m from ext_act_ja2
    2018-02-20 16:28:31,958 [INFO] {pyhive.hive} - select cn_state,count(1) m from ext_act_ja2
    2018-02-20 16:29:04,258 [INFO] {ppytools.hive_client} - Hive client query completed. Records found: 31
    2018-02-20 16:29:04,259 [INFO] {ppytools.lang.timer_helper} - Execute <ppytools.hive_client.execQuery> method cost 32.3012499809 seconds.
    2018-02-20 16:29:04,261 [INFO] {ppytools.csv_helper} - Write a CSV file successful. --> /opt/csv_files/省份分组统计_20180223162904.csv
    2018-02-20 16:29:04,262 [INFO] {ppytools.lang.timer_helper} - Execute <ppytools.csv_helper.write> method cost 0.00222992897034 seconds.
    2018-02-20 16:29:04,262 [INFO] {root      } - script2: select cn_state,cn_city,count(1) m from ext_act_ja2
    2018-02-20 16:29:04,262 [INFO] {pyhive.hive} - select cn_state,cn_city,count(1) m from ext_act_ja2
    2018-02-20 16:29:23,462 [INFO] {ppytools.hive_client} - Hive client query completed. Records found: 367
    2018-02-20 16:29:23,463 [INFO] {ppytools.lang.timer_helper} - Execute <ppytools.hive_client.execQuery> method cost 19.2005498409 seconds.
    2018-02-20 16:29:23,465 [INFO] {ppytools.csv_helper} - Write a CSV file successful. --> /opt/csv_files/城市分组统计_20180223162923.csv
    2018-02-20 16:29:23,465 [INFO] {ppytools.lang.timer_helper} - Execute <ppytools.csv_helper.write> method cost 0.00227284431458 seconds.
    2018-02-20 16:29:23,669 [INFO] {ppytools.email_client} - Send email[2018-02-22区域抽奖统计[测试]] success. To users: elkan1788@163.com.
    2018-02-20 16:29:23,669 [INFO] {ppytools.lang.timer_helper} - Execute <ppytools.email_client.send> method cost 0.204078912735 seconds.
    2018-02-20 16:29:23,714 [INFO] {__main__  } - Finished 邮件报表任务测试 Email Job.
    2018-02-20 16:29:23,715 [INFO] {ppytools.lang.timer_helper} - Execute <emailjob.main.run> method cost 62.1566159725 seconds.

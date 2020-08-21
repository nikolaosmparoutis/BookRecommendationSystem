from configurations.LoggerCls import LoggerCls
from TestLogging import TestLoggerToFiles

class TestLoggerToFiles2:
    formatter = '%(name)s - %(levelname)s - Line No. : %(lineno)d - %(message)s'
    logData2 = LoggerCls("log_to_stdout", "TestLoggerToFiles2", "TestFile2.log", "w", formatter, "DEBUG")

TestLoggerToFiles.logData.info("I am in file")
TestLoggerToFiles2.logData2.info("I am in stdout")
TestLoggerToFiles.logData.info("I am file again")
TestLoggerToFiles2.logData2.info("I am in stdout again")

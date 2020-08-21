from configurations.LoggerCls import LoggerCls

class TestLoggerToFiles:

    formatter = '%(name)s - %(levelname)s - Line No. : %(lineno)d - %(message)s'
    logData = LoggerCls("log_to_file", "TestLoggerToFiles", "TestFile1.log", "w", formatter, "INFO")

def log():
    TestLoggerToFiles.logData.info("I am in file 1")





# NCP ELSA Python SDK

## 1. Intro
1. Naver Cloud Platform - ELSA 의 python SDK
2, python 의 logging module 을 이용하여 개발
    - 기존 logging 하는 법과 같다.
    
        ```
        %(name)s            Name of the logger (logging channel)
        %(levelno)s         Numeric logging level for the message (DEBUG, INFO,
                            WARNING, ERROR, CRITICAL)
        %(levelname)s       Text logging level for the message ("DEBUG", "INFO",
                            "WARNING", "ERROR", "CRITICAL")
        %(pathname)s        Full pathname of the source file where the logging
                            call was issued (if available)
        %(filename)s        Filename portion of pathname
        %(module)s          Module (name portion of filename)
        %(lineno)d          Source line number where the logging call was issued
                            (if available)
        %(funcName)s        Function name
        %(created)f         Time when the LogRecord was created (time.time()
                            return value)
        %(asctime)s         Textual time when the LogRecord was created
        %(msecs)d           Millisecond portion of the creation time
        %(relativeCreated)d Time in milliseconds when the LogRecord was created,
                            relative to the time the logging module was loaded
                            (typically at application startup time)
        %(thread)d          Thread ID (if available)
        %(threadName)s      Thread name (if available)
        %(process)d         Process ID (if available)
        %(message)s         The result of record.getMessage(), computed just as
                            the record is emitted
        ```

## 2. Example Usage
1. usage 1 : 일반 Formatter 를 사용하여 log 저장
    ```
    import logging
    from NCP_ELSA.ELSA import ElsaHanlder  
    
    logger = logging.getLogger("test logger")
    logger.setLevel("DEBUG")
    
    elsa_hanlder = ElsaHanlder(projectName="${PROJECT_ID}")
    formatter = logging.Formatter("%(levelno)s %(asctime)s %(message)s")
    elsa_hanlder.setFormatter(formatter)
    elsa_hanlder.setLevel("INFO")
    
    logger.addHandler(elsa_hanlder)
    logger.info("elsa test")
    ```
2. usage 2 : ElsaJsonFormatter 를 사용하여 json 형태로 log 저장
    ```
    import logging
    from NCP_ELSA.ELSA import ElsaHanlder, ElsaJsonFormatter 
    
    logger = logging.getLogger("test logger")
    logger.setLevel("DEBUG")
    
    elsa_hanlder = ElsaHanlder(projectName="${PROJECT_ID}")
    elsa_formatter_temp = ElsaJsonFormatter("%(levelno)s %(asctime)s %(message)s")
    elsa_hanlder.setFormatter(elsa_formatter_temp)
    elsa_hanlder.setLevel("INFO")
    
    logger.addHandler(elsa_hanlder)
    logger.info("elsa test")
    ```
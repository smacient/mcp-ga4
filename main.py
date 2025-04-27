from localserver.logfolder.logger import setup_logging, logger
from localserver.exception.exception import CustomException
import sys

sys.path.append("localserver")



def main():
    setup_logging()
    logger.debug("debug message", extra={"x": "hello"})
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("critical message")
    try:
        1 / 0
    except CustomException as e:
        logger.exception(e)
        # raise CustomException(e, sys)



if __name__ == "__main__":
    main()

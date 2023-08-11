from pythonjsonlogger import jsonlogger
import logging
import os
import job

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
h = logging.StreamHandler()
h.setLevel(logging.DEBUG)
json_fmt = jsonlogger.JsonFormatter(fmt='%(asctime)s %(levelname)s %(filename)s %(lineno)s %(message)s', json_ensure_ascii=False)
h.setFormatter(json_fmt)
logger.addHandler(h)


if __name__ == "__main__":
    logger.info("start program")
    j = job.JobClass()
    j.api_endpoint = os.environ.get('MAWINTER_API_ENDPOINT') # 'http://hogehoge/v2/record/summary/2023'
    j.spreadsheet_url = os.environ.get('SPREADSHEET_URL') # 'https://docs.google.com/spreadsheets/d/XXXXXXXXXXXXXXXX'
    j.jobInterval = os.environ.get("JOB_INTERVAL") # 0
    j.worksheet_name = os.environ.get('WORKSHEET_NAME') # 'FY2023'
    j.Run()

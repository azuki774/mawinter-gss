from pythonjsonlogger import jsonlogger
import logging
import os
import sys
from google.oauth2 import service_account
import gspread
import mawinter
import time
from datetime import datetime
from zoneinfo import ZoneInfo

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
h = logging.StreamHandler()
h.setLevel(logging.DEBUG)
json_fmt = jsonlogger.JsonFormatter(fmt='%(asctime)s %(levelname)s %(filename)s %(lineno)s %(message)s', json_ensure_ascii=False)
h.setFormatter(json_fmt)
logger.addHandler(h)

class JobClass:
    jobInterval = 0 # 何分に1回起動するかを指定。0なら1回起動して終了。
    api_endpoint = '' # ex. http://hogehoge/v2/record/summary/2023
    spreadsheet_url = '' # spreadsheet_url = "https://docs.google.com/spreadsheets/d/XXXXXXXXXXXXXXXXXXX"
    worksheet_name = '' # ex. FY2023
    last_sync_cell = 'P1' # default 'P1'

    # internal use
    spreadsheet = None # spreadsheet = gc.open_by_url(spreadsheet_url)
    worksheet = None
    sheet_fetch_data = [[]]

    def __init__(self):
        pass

    def _auth_worksheet(self):
        scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive', 
             "https://www.googleapis.com/auth/spreadsheets", 
             "https://www.googleapis.com/auth/drive.file"
            ]

        credentials = service_account.Credentials.from_service_account_file(
            '/.secret/credential.json'
        )

        scoped_credentials = credentials.with_scopes(scope)

        gc = gspread.authorize(scoped_credentials)
        self.spreadsheet = gc.open_by_url(self.spreadsheet_url)
        self.worksheet = self.spreadsheet.worksheet(self.worksheet_name)

    def _fetch(self):
        self.sheet_fetch_data = self.worksheet.get_all_values(value_render_option='FORMULA')

    def _write(self, data):
        tokyo = ZoneInfo("Asia/Tokyo") # タイムゾーン情報を取得
        self.worksheet.update('A1', data, raw=False)
        self.worksheet.update(self.last_sync_cell, str(datetime.now(tokyo)))

    def _load_api_json(self, fetch_data):
        # output category_id -> [category_name,4,5,6,7,8,9,10,11,12,1,2,3]
        ret_dict = {}
        for f in fetch_data:
            value = [f['category_name']] + f['price']
            ret_dict[str(f['category_id'])] = value # 後で使うときは文字列なので str にする
        return ret_dict
    
    def _make_write_data(self, api_dict):
        '''
        実際にスプレッドシートに書き込むデータを作成する。
        category_id が一致するものがあればAPIの出力と書き換え、一致するものがなければそのままにする。
        '''

        write_data = []
        for f in self.sheet_fetch_data:
            fkey = f[0]
            if fkey in api_dict:
                # 書き換え
                insert_data = f
                # insert_data[0] is id
                for num in range(13):
                    # category_name と 4月～3月のフィールドを上書き
                    insert_data[num + 1] = api_dict[fkey][num]
                write_data.append(insert_data)
            else:
                # そのまま
                write_data.append(f)
        
        return write_data

    def Run(self):
        logger.info('set auth')
        self._auth_worksheet()

        while True:
            logger.info('api mawinter-api start')

            # source API call
            if self.api_endpoint != 'mock':
                api_fetch_data = mawinter.get(self.api_endpoint)
            else:
                # use mock
                api_fetch_data = mawinter.get_dummy(self.api_endpoint)

            api_dict = self._load_api_json(api_fetch_data)
            logger.info('fetch mawinter-api complete')

            # sheet fetch
            logger.info('fetch spreadsheet start')
            self._fetch()

            write_data = self._make_write_data(api_dict=api_dict)
            logger.info('fetch spreadsheet complete')

            self._write(write_data)
            logger.info('spreadsheet is updated sucessfully')
            if self.jobInterval == 0:
                return

            logger.info('wait for next interval: {0} min'.format(self.jobInterval))
            time.sleep(int(self.jobInterval) * 60)

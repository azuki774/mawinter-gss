from pythonjsonlogger import jsonlogger
import logging
import requests
import json


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
h = logging.StreamHandler()
h.setLevel(logging.DEBUG)
json_fmt = jsonlogger.JsonFormatter(fmt='%(asctime)s %(levelname)s %(filename)s %(lineno)s %(message)s', json_ensure_ascii=False)
h.setFormatter(json_fmt)
logger.addHandler(h)

def get(endpoint):
    response = requests.get(endpoint)
    print(response)
    if response.status_code == 200:
        json_data = response.json()
        logger.info("fetch ok")
        print(json_data)
        return json_data
    else:
        logger.error("unexpected status code: {}".format(response.status_code))
        raise Exception('unexpected status code')

def get_dummy(endpoint):
    '''
    get_dummy は mawinter の連携せずに下のサンプルデータを返す
    '''
    ret = [{"category_id":100,"category_name":"月給","count":3,"price":[0,0,0,825233,0,0,0,0,0,0,0,0],"total":825233},{"category_id":101,"category_name":"ボーナス","count":0,"price":[0,0,0,0,0,0,0,0,0,0,0,0],"total":0},{"category_id":110,"category_name":"雑所得","count":0,"price":[0,0,0,0,0,0,0,0,0,0,0,0],"total":0},{"category_id":200,"category_name":"家賃","count":4,"price":[0,0,85110,255330,0,0,0,0,0,0,0,0],"total":340440},{"category_id":210,"category_name":"食費","count":209,"price":[0,1690,32414,126738,8593,0,0,0,0,0,0,0],"total":169435},{"category_id":220,"category_name":"電気代","count":0,"price":[0,0,0,0,0,0,0,0,0,0,0,0],"total":0},{"category_id":221,"category_name":"ガス代","count":4,"price":[0,0,5638,4794,0,0,0,0,0,0,0,0],"total":10432},{"category_id":222,"category_name":"水道費","count":2,"price":[0,0,0,7684,0,0,0,0,0,0,0,0],"total":7684},{"category_id":230,"category_name":"コンピュータリソース","count":15,"price":[0,268,0,18449,4929,0,0,0,0,0,0,0],"total":23646},{"category_id":231,"category_name":"通信費","count":10,"price":[0,0,1018,7807,990,0,0,0,0,0,0,0],"total":9815},{"category_id":240,"category_name":"生活用品","count":1,"price":[0,4444,0,0,0,0,0,0,0,0,0,0],"total":4444},{"category_id":250,"category_name":"娯楽費","count":1,"price":[0,33,0,0,0,0,0,0,0,0,0,0],"total":33},{"category_id":251,"category_name":"交遊費","count":0,"price":[0,0,0,0,0,0,0,0,0,0,0,0],"total":0},{"category_id":260,"category_name":"書籍・勉強","count":0,"price":[0,0,0,0,0,0,0,0,0,0,0,0],"total":0},{"category_id":270,"category_name":"交通費","count":0,"price":[0,0,0,0,0,0,0,0,0,0,0,0],"total":0},{"category_id":280,"category_name":"衣服等費","count":0,"price":[0,0,0,0,0,0,0,0,0,0,0,0],"total":0},{"category_id":300,"category_name":"保険・税金","count":0,"price":[0,0,0,0,0,0,0,0,0,0,0,0],"total":0},{"category_id":400,"category_name":"医療・衛生","count":0,"price":[0,0,0,0,0,0,0,0,0,0,0,0],"total":0},{"category_id":500,"category_name":"雑費","count":0,"price":[0,0,0,0,0,0,0,0,0,0,0,0],"total":0},{"category_id":600,"category_name":"家賃用貯金","count":1,"price":[0,12300,0,0,0,0,0,0,0,0,0,0],"total":12300},{"category_id":601,"category_name":"PC用貯金","count":0,"price":[0,0,0,0,0,0,0,0,0,0,0,0],"total":0},{"category_id":700,"category_name":"NISA入出金","count":0,"price":[0,0,0,0,0,0,0,0,0,0,0,0],"total":0},{"category_id":701,"category_name":"NISA変動","count":0,"price":[0,0,0,0,0,0,0,0,0,0,0,0],"total":0}]
    return ret

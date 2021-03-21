from django.test import TestCase
from .utils import DJANGO_ENDPOINTS
from django.core.cache import cache
import redis
import json
import requests
import os
import logging


logger = logging.getLogger(__name__)
# Create your tests here.

TEST_DATA = {
    "SEARCH_API": {
        "positive_case_1": {
            "info": "positive Test case if ifsc code is setup",
            "request": DJANGO_ENDPOINTS['SEARCH'],
            "params": {
                "ifsc_code": "ALLA0213615"
            },
            "response": {
                "message": "Successful",
                "results": {
                    "BANK": "ALLAHABAD BANK",
                    "IFSC": "ALLA0213615",
                    "MICR": "0",
                    "BRANCH": "KPK",
                    "ADDRESS": "PALM ROAD, CIVIL LINES, NAGPUR, PIN-440001",
                    "CITY1": "NAGPUR",
                    "CITY 2": "0",
                    "STATE": "MAHARASHTRA",
                    "STD CODE2": 0.0,
                    "PHONE": "2550742"
                }
            },
            "response_code": 200
        },
        "negative_case_1": {
            "info": "testcase if invalid ifsc code is provided",
            "request": DJANGO_ENDPOINTS['SEARCH'],
            "params": {
                "ifsc_code": "ALLA02615"
            },
            "response": {
                "message": "Unsuccessful search - IFSC Not Found or invalid"
            },
            "response_code": 404
        },
        "negative_case_2": {
            "info": "testcase if no ifsc code is provided",
            "request": DJANGO_ENDPOINTS['SEARCH'],
            "params": None,
            "response": {
                "message": "Invalid request : ifsc_code not provided"
            },
            "response_code": 400
        }
    }

}


class SearchApiTestCase(TestCase):
    def test_search_api(self):
        test_data = TEST_DATA['SEARCH_API']
        for testindex, value in test_data.items():
            logger.info("\n\n"+("*"*55)+testindex+("*"*55)+"\n")
            logger.info("starting {} | {}".format(testindex, value['info']))
            response = requests.get(value['request'], params=value['params'])
            logger.info("performed rest api request | url {} | params {}".format
                  (value['request'], value['params']))
            logger.debug("expected status code {} | actual status code {}".format
                  (value['response_code'], response.status_code))
            logger.debug("expected response {} | actual response {}".format
                  (value['response'], response.json()))
            self.assertEqual((response.status_code, response.json()), (value['response_code'], value['response']))


class IFSCCacheTestCase(TestCase):
    redis_obj = redis.Redis(host='localhost', port=6379, db=0)

    def setUp(self):

        self.redis_obj.flushall()
        os.system('python manage.py clearcache')

    def test_cache(self):
        value = TEST_DATA['SEARCH_API']['positive_case_1']
        logger.info("\n\n"+("*"*55)+"IFSCCacheTestCase"+("*"*55)+"\n")
        logger.info("starting {} | {}".format("IFSCCacheTestCase", value['info']))
        response = requests.get(value['request'], params=value['params'])
        logger.info("performed rest api request | url {} | params {}".format
              (value['request'], value['params']))
        logger.debug("response {}".format(response.json()))
        cached_data = cache.get(value['params']['ifsc_code'])
        logger.debug("verify if cache contains IFSC and its data post response | {}".format(cached_data))
        self.assertEqual(cached_data, response.json()['results'])
        expected_ifsc_hit_count = 1
        expected_cache_hit_count = None
        actual_cache_hit_count = json.loads(
            self.redis_obj.get('IFSC_CACHE_HIT_COUNT'))[value['params']['ifsc_code']] if self.redis_obj.get(
            'IFSC_CACHE_HIT_COUNT') else None
        actual_ifsc_hit_count = json.loads(
            self.redis_obj.get('IFSC_HIT_COUNT'))[value['params']['ifsc_code']] if self.redis_obj.get(
            'IFSC_HIT_COUNT') else None
        logger.debug("Verifying cache hit count | actual cache hit count {} | expected cache hit count None".format(str(actual_cache_hit_count)))
        logger.debug("Verifying ifsc hit count | actual ifsc hit count {} | expected ifsc hit count 1".format(actual_ifsc_hit_count))
        self.assertEqual((actual_cache_hit_count, actual_ifsc_hit_count), (expected_cache_hit_count, expected_ifsc_hit_count))
        response = requests.get(value['request'], params=value['params'])
        logger.info("performed rest api second request  | url {} | params {}".format
              (value['request'], value['params']))
        logger.debug("response {}".format(response.json()))
        logger.debug("verify if cache contains IFSC and its data post response")
        expected_ifsc_hit_count = 2
        expected_cache_hit_count = 1
        actual_cache_hit_count = json.loads(self.redis_obj.get('IFSC_CACHE_HIT_COUNT'))[value['params']['ifsc_code']]
        actual_ifsc_hit_count = json.loads(self.redis_obj.get('IFSC_HIT_COUNT'))[value['params']['ifsc_code']]
        logger.debug("Verifying cache hit count | actual cache hit count {} | expected cache hit count 1".format(actual_cache_hit_count))
        logger.debug("Verifying ifsc hit count | actual ifsc hit count {} | expected ifsc hit count 2".format(
            actual_ifsc_hit_count))
        self.assertEqual((actual_cache_hit_count, actual_ifsc_hit_count), (expected_cache_hit_count, expected_ifsc_hit_count))

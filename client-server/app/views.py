import json
import redis
import requests as req
from . import utils
from rest_framework import views, generics, status
from rest_framework.response import Response
from .utils import FLASK_ENDPOINTS
from django.core.cache import cache

r = redis.Redis(host='localhost', port=6379, db=0)

class IFSCSearchView(views.APIView):
    """ Client Connecting to Query Server for the IFSC Search """

    def get(self, request):

        ifsc = self.request.query_params.get('ifsc_code')
        if ifsc:
            cached_data = cache.get(ifsc)
            if cached_data:
                utils.redis_update_hit_count('IFSC_CACHE_HIT_COUNT', ifsc, r)
                utils.redis_update_hit_count('IFSC_HIT_COUNT', ifsc, r)
                return Response({'message': 'Successful', "results": cached_data},
                                status=status.HTTP_200_OK)
            else:
                flask_response = req.get(FLASK_ENDPOINTS["SEARCH"], params={'ifsc_code': str(ifsc)})
                if flask_response.status_code == status.HTTP_200_OK:
                    utils.redis_update_hit_count('IFSC_HIT_COUNT', ifsc, r)
                    utils.redis_update_hit_count('API_HIT_COUNT', FLASK_ENDPOINTS["SEARCH"], r)
                    results = flask_response.json()['results']
                    cache.set(ifsc, results)
                    return Response({"results": results}, status=status.HTTP_200_OK)
                elif flask_response.status_code == status.HTTP_404_NOT_FOUND:
                    return Response({'message': 'Unsuccessful search - IFSC Not Found or invalid'},
                                    status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response({'message': flask_response.json().message}, status=flask_response.status_code)
        else:
            return Response({'message': 'Invalid request : ifsc_code not provided'}, status=status.HTTP_400_BAD_REQUEST)


class BankLeadBoardView(views.APIView):
    """ Client Connecting to Query Server for the Bank Lead Count """

    def get(self, request, *args, **kwargs):
        lead_param_sort = self.request.query_params.get('sortorder')
        lead_fetch_count_param = self.request.query_params.get('fetchcount')
        flask_response = req.get(FLASK_ENDPOINTS["BANKLEAD"], params={'sortorder': lead_param_sort,
                                                                      'fetchcount': lead_fetch_count_param})

        if flask_response.status_code == status.HTTP_200_OK:
            utils.redis_update_hit_count('API_HIT_COUNT', FLASK_ENDPOINTS["BANKLEAD"], r)
            return Response({"results": flask_response.json()['results'],
                             "available_data_count": flask_response.json()['available_data_count']},
                            status=status.HTTP_200_OK)
        else:
            return Response({'message': flask_response.json()['message']}, status=flask_response.status_code)


class StatisticsView(views.APIView):
    """ Client Connecting to Query Server for Statistics for IFSC Search """

    def get(self, request, *args, **kwargs):
        lead_param_sort = self.request.query_params.get('sortorder')
        lead_fetch_count_param = self.request.query_params.get('fetchcount')
        flask_response = req.get(FLASK_ENDPOINTS["STATS"], params={'sortorder': lead_param_sort,
                                                                   'fetchcount': lead_fetch_count_param})

        if flask_response.status_code == status.HTTP_200_OK:
            utils.redis_update_hit_count('API_HIT_COUNT', FLASK_ENDPOINTS["STATS"], r)
            return Response({"results": flask_response.json()['results'],
                             "available_data_count": flask_response.json()['available_data_count']},
                            status=status.HTTP_200_OK)
        else:
            return Response({'message': flask_response.json()['message']}, status=flask_response.status_code)


class CachePr():
    pass

import json
import redis

from datetime import datetime
from itertools import islice
from django.shortcuts import render

# Rest Frame Work Imports
from rest_framework import views, generics, status
from rest_framework.validators import ValidationError
from rest_framework.response import Response
from django.conf import settings
from . import LEAD_COUNT, BANK_DATA_DIR

# flask.
# dict_data = getattr(settings, "BANK_DATA_DIR", None)
# bank_lead = getattr(settings, "LEAD_COUNT", None)

dict_data = BANK_DATA_DIR
bank_lead = LEAD_COUNT

# Configure redis
r = redis.Redis(host='localhost', port=6379, db=0)


class IFSCSerachView(views.APIView):

    def get(self, request, *args, **kwargs):
        ifsc = self.request.query_params.get('ifsc_code')
        if ifsc and dict_data.get(ifsc):
            data = dict_data.get(ifsc)
            stats = r.get('stats')
            now = datetime.now()
            if stats:
                stats = json.loads(stats)
                print("Redis stats", stats)
                stats.append([ifsc, now.strftime("%m/%d/%Y, %H:%M:%S")])
                r.set('stats', json.dumps(stats))
            else:
                d = [[ifsc, now.strftime("%m/%d/%Y, %H:%M:%S")]]
                r.set('stats', json.dumps(d))
            return Response({"results": data}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Unsuccessful - IFSC Not Found'}, status=status.HTTP_404_NOT_FOUND)


class BankLeadBoardView(views.APIView):

    def get(self, request, *args, **kwargs):

        lead_param_sort = self.request.query_params.get('sortorder')
        lead_fetch_count_param = self.request.query_params.get('fetchcount')

        if lead_fetch_count_param:
            try:
                fetch_param = int(lead_fetch_count_param) if lead_fetch_count_param else 10
            except ValueError as e:
                return Response({'message': "Fetch Count Value should be integer (1 -255)"},
                                status=status.HTTP_400_BAD_REQUEST)

        if fetch_param > 255 or fetch_param < 1:
            return Response({'message': 'Fetch Count Value should be between 1 - 255'},
                            status=status.HTTP_400_BAD_REQUEST)
        sort_param = lead_param_sort if lead_param_sort else "DESC"
        available_record = len(bank_lead)
        if sort_param.upper() == 'ASC':
            data = dict(sorted(bank_lead.items(), key=lambda x: x[1]))
        elif sort_param.upper() == 'DESC':
            data = dict(sorted(bank_lead.items(), key=lambda x: x[1], reverse=True))
        else:
            return Response({'message': 'Invalid value sortorder parameter should be ASC or DESC'},
                            status=status.HTTP_400_BAD_REQUEST)
        slice_index = fetch_param if fetch_param < len(bank_lead) else len(bank_lead)
        data = dict(islice(data.items(), slice_index))
        return Response({"results": data, "available_data_count": available_record})


class StatisticsView(views.APIView):

    def get(self, request, *args, **kwargs):
        try:
            stat_data = json.loads(r.get('stats'))
            stats_param_sort = self.request.query_params.get('sortorder')
            stats_fetch_count_param = self.request.query_params.get('fetchcount')
            if stats_fetch_count_param and (int(stats_fetch_count_param) > 10000 or int(stats_fetch_count_param) < 1):
                return Response({'message': 'Fetch Count Value should be between 1 - 10000'})
            fetch_param = int(stats_fetch_count_param) if stats_fetch_count_param else len(stat_data)
            available_record = len(stat_data)
            sort_param = stats_param_sort if stats_param_sort else "ASC"
            if sort_param.upper() == 'ASC':
                data = sorted(stat_data, key=lambda x: x[1])
            elif sort_param.upper() == 'DESC':
                data = sorted(stat_data, key=lambda x: x[1], reverse=True)
            else:
                return Response({'message': 'Invalid value sortorder parameter should be ASC or DESC'},
                                status=status.HTTP_400_BAD_REQUEST)
            data = data[: fetch_param]
            return Response({"results": data, "available_data_count": available_record}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

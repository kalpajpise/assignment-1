import json
import redis

from datetime import datetime
from itertools import islice
from django.shortcuts import render

# Rest Frame Work Imports
from rest_framework import views , generics, status
from rest_framework.validators import ValidationError
from rest_framework.response import Response
from django.conf import settings

dict_data =  getattr(settings, "BANK_DATA_DIR", None)
bank_lead =  getattr(settings, "LEAD_COUNT", None)

# Configure redis 
r = redis.Redis(host='localhost', port=6379, db=0)

class IFSCSerachView(views.APIView):

    def get(self, request, *args , **kwargs):
        ifsc = self.request.query_params.get('ifsc_code')
        if ifsc  and dict_data.get(ifsc)  :
            data = dict_data.get(ifsc)
            #  TODO :  
            # Add Statics to the absolute search
            stats = r.get('stats')
            now = datetime.now()
            if stats :
                stats = json.loads(stats)
                print("Redis stats", stats)
                stats.append([ifsc , now.strftime("%m/%d/%Y, %H:%M:%S")])
                r.set('stats', json.dumps(stats))
            else :
                d = [[ifsc , now.strftime("%m/%d/%Y, %H:%M:%S")]]
                r.set('stats',json.dumps(d))
            return Response({'message' : 'Successful', "data" : json.dumps( data) }, status=status.HTTP_200_OK)
        else :
            return Response({'message' : 'Unscessfull - IFSC Not Found'}, status=status.HTTP_404_NOT_FOUND)


class BankLeadBoardView(views.APIView):

    def get(self,request,*args,**kwargs):
        lead_param = self.request.query_params.get('state')
        if lead_param:
            if lead_param.lower() == 'sortorder':
                sub_search = self.request.query_params.get('sub')
                if sub_search:
                    if sub_search.upper() == "ASC":
                        data = dict(sorted(bank_lead.items() , key= lambda x : x[1]))
                else :
                    data = dict(sorted(bank_lead.items() , key= lambda x : x[1], reverse= True))
                return Response({'message' : 'Successful', "data" : json.dumps( data) }, status=status.HTTP_200_OK)
            elif lead_param.lower() == 'fetchcount':
                sub_search = self.request.query_params.get('sub')
                if sub_search :
                    print(sub_search)
                    data = dict(islice(bank_lead.items(), int(sub_search)))
                else :
                    data = dict(islice(bank_lead.items(), 10))
                return Response({'message' : 'Successful', "data" : json.dumps(data) }, status=status.HTTP_200_OK)
            
        else :
            data = dict(sorted(bank_lead.items() , key= lambda x : x[1], reverse= True))
            data = dict(islice(data.items(), 10))
            return Response({'message' : 'Successful', "data" : json.dumps(data)}, status=status.HTTP_200_OK)

class StatisticsView(views.APIView):

    def get(self,request,*args,**kwargs):

        stats_param = self.request.query_params.get('state')
        if stats_param:
            data = json.loads(r.get('stats'))
            if stats_param.lower() == 'sortorder':
                sub_search = self.request.query_params.get('sub')
                if sub_search:
                    if sub_search.upper() == "ASC":
                        data = sorted(data,key=lambda x: x[1])
                else :
                        data = sorted(data,key=lambda x: x[1], reverse=True)
                return Response({'message' : 'Successful', "data" : data }, status=status.HTTP_200_OK)
            elif stats_param.lower() == 'fetchcount':
                    sub_search = self.request.query_params.get('sub')
                    if sub_search :
                        print(sub_search)
                        if len(data) < int(sub_search):
                            return Response({'message' : 'Fecth count number is more than list'},status=status.HTTP_400_BAD_REQUEST)
                        data = data[ : int(sub_search)]
                    return Response({'message' : 'Successful', "data" : data }, status=status.HTTP_200_OK)
        return Response({'message' : "Unsuccessfull Serach Paramater missing"}, status=status.HTTP_400_BAD_REQUEST)
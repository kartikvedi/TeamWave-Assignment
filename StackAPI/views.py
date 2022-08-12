import re
from urllib import response
from django.shortcuts import redirect, render
from .models import Link,Data,Tag
#Extraction of data
import json
import requests
import ast
from .models import Link, Data 
#Pagination
from django.core.paginator import Paginator
#ratelimit
from ratelimit import limits

#unixtimestamp
from datetime import datetime 
Pages=''
query_result=''
Tagged=''
# Create your views here.
@limits(calls=100,period=3600)
@limits(calls=5,period=60) 
def index(request):

    FromDate=''
    From_Timestamp=''
    ToDate=''
    To_Timestamp=''
    Pages=''
    Pagesize=''
    Not_Tagged=''
    MinDate=''
    Min_Timestamp=''
    MaxDate=''
    Max_Timestamp=' '
    Order=''
    Sort=''
    query_result=[]
    if (request.method=="POST"):
        #print("hi")
        Tagged=request.POST["Tagged"]
        FromDate=request.POST["FromDate"]
        ToDate=request.POST["ToDate"]
        Pages=request.POST["Pages"]
        Pagesize=request.POST['Pagesize']
        Not_Tagged=request.POST['Not_Tagged']
        MinDate=request.POST['MinDate']
        MaxDate=request.POST['MaxDate']
        Order=request.POST['Order']
        Sort=request.POST['Sort']
        print(request.POST)
        if(FromDate!=''):
            From_Timestamp=handle_date(FromDate)
        if(ToDate!=''):
            To_Timestamp=handle_date(ToDate)
        if(MinDate!=''):
            Min_Timestamp=handle_date(MinDate)
        if(MaxDate!=''):
            Max_Timestamp=handle_date(MaxDate)

        params={"tagged":Tagged,"fromdate":From_Timestamp,"todate":To_Timestamp,"page":Pages,
            "pagesize":Pagesize,"nottagged":Not_Tagged,"min":Min_Timestamp,
            "max":Max_Timestamp,"order":Order,"sort":Sort}

        keys=params.keys()

        final_keys=[]

        for key in keys:

            res=params.get(key)
            #print(res)
            
            if (res==""):
                pass
                
            else:
                final_keys.append(key)

            res=" "
        
        url="https://api.stackexchange.com/2.3/search?"
            
        for i in final_keys:
            print('------------------')
            print(i)
            print(params.get(i))
            print('------------------')

            url=url+i+"="+str(params.get(i))+"&"

        url=url+"site=stackoverflow"
        if(Link.objects.filter(url=url).exists()):
            print("Query Already Made")
            return redirect(index)
        else:
            resp=get_request(url)
            URL=Link()
            URL.url=url
            URL.save();

        json_data=json.loads(resp.text)
        #print(json_data)
        query_result=json_data["items"]
        #if(json_data["has_more"]==False):
            #query_result=False
            #return redirect(Show)
        load_data(query_result)                
        #data.dt=query_result
        tg=Tag()
        tg.tags=Tagged
        tg.save()
        #print(query_result)
        return redirect ('Show')    
    else:
        print("request not made")
        print(query_result)
        print(request.POST)
        return render (request,'Index.html')    

def Show(request):
    context={}
    url=Link.objects.latest('id')
    data=Data.objects.all()
    tag=Tag.objects.all()
    print(url)
    result=handle_data(data,tag)
    """""
    for dat in data:
        dat.delete()
    """""
    """""
    if(request.method=='POST'):
        end=request.POST['Finish']
        if(end==True):
    """""  
    if(request.method=="POST"):
        nxt=request.POST['Next']
        if(nxt==True):
         print(nxt)
        URL=updatelink(url)
        link=Link()
        link.url=URL
        link.save()
        resp=get_request(URL)
        json_data=json.loads(resp.text)
        query_result=json_data["items"]
        load_data(query_result)
        result=handle_data(data,tag)
        print(result)
        context = {"Result":result}
        return render(request,'Show.html',context)
    # sending the page object to index.html
    else:
        context={"Result":result}
        return render(request,'Show.html',context  )

def handle_date(date):
    date=date.split("-")
    year=int(date[0])
    month=int(date[1])
    day=int(date[-1])
    dt=datetime(year,month,day)
    ts=int(dt.timestamp())
    return(ts)

def load_data(query_result):

    for i in range(len(query_result)):
        data=Data()
        data.dt=json.dumps(query_result[i])
        data.save()
        

def handle_data(Data,tag):
    res=[]
    data=Data
    #print(data)
    for dat in data:
        #logic to extract tags from the data
        checker=json.loads(dat.dt)
        #print(checker)
        #print(checker)
        if(checker is not None):
            tg=checker['tags']

        else:
            print("None")

        for t in tag:
            store=Tag.objects.latest('id')
            store=str(store)
            store=store.lower()
            store=store.replace(" ","")
            print(store)
            for i in range(len(tg)):
                if(tg[i]==store):    
                    res.append(checker)
                    #print(store)
               #else:
                    #print(tg[i]+" != "+store ) 
    
    print(res)             
    return(res)


def get_request(url):
    resp=requests.get(url)
    return(resp)

def updatelink(url):     
    url=str(url)
    url=url.split("&")
    page=url[1]
    rep=int (page[-1])+1
    page=page.replace(page[-1],str(rep))
    url[1]=page
    URL=""
    for i in range(len(url)):
        if(i==len(url)-1):
            URL=URL+url[i]
        else:
            URL=URL+url[i]+"&"
    return(URL)
    

# send "one to one" notification to certain subscriber
'''response = ses.send_email(
    Source="",
    Destination={
        'ToAddresses': [""]
    },
    Message={
        'Subject': {
            'Data': "test1",
            'Charset': 'UTF-8'
        },
        'Body': {
            'Text': {
                'Data': "test1111",
                'Charset': 'UTF-8'
            }
        }
    }
)'''

# send notification to all subscribers


import boto3
import json

comprehend = boto3.client('comprehend', aws_access_key_id='',
                          aws_secret_access_key='',
                          region_name='')

sns = boto3.client(
    'sns',
    aws_access_key_id='',
    aws_secret_access_key='',
    region_name='',
    # aws_session_token=SESSION_TOKEN,
)
ses = boto3.client(
    '',
    aws_access_key_id='',
    aws_secret_access_key='',
    region_name='',
    # aws_session_token=SESSION_TOKEN,
)

import pymongo
import datetime
client = pymongo.MongoClient('', 27017)
#client = pymongo.MongoClient('localhost', 27017)
'''db3 = client.user2
db4 = client.event2
User= db3.user2
Event= db4.event2'''

db1 = client.user5
db2 = client.event5
User= db1.user5
Event= db2.event5

ID= 0
EID= 0
ID2=0
EID2=0

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
import certifi
endpoint = ''
es = Elasticsearch(hosts=[endpoint], port=443, use_ssl=True, verify_certs=True, ca_certs=certifi.where())

def send_reminder(text,user_id):
    response = json.dumps(comprehend.detect_sentiment(Text=text, LanguageCode='en'), sort_keys=True, indent=4)
    response = json.loads(response)
    result1 = response['Sentiment']
    '''result2 = response['SentimentScore']
    result_mixed = response['SentimentScore']['Mixed']
    result_negative = response['SentimentScore']['Negative']
    result_neutral = response['SentimentScore']['Neutral']
    result_positive = response['SentimentScore']['Positive']'''
    result = result1
    if result == "NEGATIVE":
        info=find_student(int(user_id))
        response = ses.send_email(
            Source="",
            Destination={
                'ToAddresses': [info['email']]
            },
            Message={
                'Subject': {
                    'Data': "Reminder from LionGroup",
                    'Charset': 'UTF-8'
                },
                'Body': {
                    'Text': {
                        'Data': "Dear Customer, we find that you might under negative mood recently. Please try to cheer yourself up. You might want to try our EatTogether service for some fun. We do hope that you could enjoy your life here.",
                        'Charset': 'UTF-8'
                    }
                }
            }
        )

def search_by_key(keyword):

    response = es.search(index='ccproject3', q=keyword)
    m = response['hits']['hits']
    result = []
    for i in m:
        result.append(i['_source'])
    return result

def create_student(info):
    #global ID
    global ID2
    #ID = ID + 1
    ID2=User.count()+1
    dic = {
        'user_id': ID2,
        'nick_name': info['nick_name'],
        'avatar': info['avatar'],
        'email': info['email'],
        'password': info['password'],
        'followings': None,
        'introduction': info['introduction'],
        'create_event': None,
        'join_event': None,
        'followers':None
    }
    User.insert(dic)

    #subscribe to our web application
    response1 = sns.subscribe(
        TopicArn='',
        Protocol='email',
        Endpoint=dic['email']
    )

    #verify ses service
    response2 = ses.verify_email_address(
        EmailAddress=dic['email']
    )

    return ID2

def update_student(info,student):
    User.update_one(
        {"user_id": info['user_id']},
        {
        "$set": {
            'nick_name': student['nick_name'],
            'avatar': student['avatar'],
            'email': student['email'],
            'password': student['password'],
            'followings': info['followings'],
            'introduction': student['introduction'],
            'create_event': info['create_event'],
            'join_event': info['join_event'],
            'followers': info['followers']
        }
        }
    )
    return info['user_id']

def create_event_db(info, user_id):
    #global EID
    global EID2
    #EID = EID + 1
    EID2 = Event.count()+1
    d= datetime.datetime.now()
    if (int(info['endyear']) * 100000000 + int(info['endmonth']) * 1000000 + int(info['endday']) * 10000 + int(
            info['endhour']) * 100 + int(
        info['endminute']) < int(info['startyear']) * 100000000 + int(info['startmonth']) * 1000000 + int(info['startday']) * 10000 + int(info['starthour']) * 100 + int(info['startminute'])):
        EID2=-1
        dic={}
        return dic, EID2
    dic = {
        'event_id': EID2,
        #'event_id':info['event_id'],
        'image': info['image'],
        'starter': user_id,
        'type':info['type'],
        'content':info['content'],
        'person_limit':30,
        'start_year': info['startyear'],
        'start_month': info['startmonth'],
        'start_day': info['startday'],
        'start_hour': info['starthour'],
        'start_minute': info['startminute'],
        'end_year': info['endyear'],
        'end_month': info['endmonth'],
        'end_day': info['endday'],
        'end_hour': info['endhour'],
        'end_minute': info['endminute'],
        'time_limit_flag':False,
        'person_limit_flag':False,
        'follower': None,
        'joined_flag':False
    }
    Event.insert(dic)

    m = {}
    m['start_month'] = dic['start_month']
    m['start_year'] = dic['start_year']
    m['event_id'] = dic['event_id']
    m['end_year'] = dic['end_year']
    m['image'] = dic['end_year']
    m['start_hour'] = dic['start_hour']
    m['end_hour'] = dic['end_hour']
    m['start_day'] = dic['start_day']
    m['content'] = dic['content']
    m['end_month'] = dic['end_month']
    m['end_day'] = dic['end_day']
    m['end_minute'] = dic['end_minute']
    m['start_minute'] = dic['start_minute']
    m['time_limit_flag'] = dic['time_limit_flag']
    m['type'] = dic['type']
    m['starter'] = dic['starter']
    #m1 = json.dumps(doc)
    #m2 = json.loads(m1)
    es.index(index='ccproject3', doc_type='test', id=m['event_id'], body=m)
    return dic, EID2


def find_student(user_id):
    info= User.find_one({"user_id": user_id})
    return info

def find_name_student(name):
    info = User.find_one({"nick_name": name})
    return info

def get_event_from_db():
    d = datetime.datetime.now()
    for c in Event.find():
        #if(c['end_year'] * 10000 + c['end_month'] * 100 + c['end_day'] < d.year * 10000 + d.month * 100 + d.day):
        if (int(c['end_year']) * 100000000 + int(c['end_month']) * 1000000 + int(c['end_day'])* 10000+  int(c['end_hour']) * 100 + int(c['end_minute'])< d.year * 100000000 + d.month * 1000000 + d.day*10000 + d.hour*100+ d.minute):
            Event.update_one(
                {"event_id": c['event_id']},
                {
                    "$set": {
                        'time_limit_flag': True
                    }
                }
            )
    content= Event.find({'person_limit_flag': False, 'time_limit_flag': False})
    return content

def get_event_from_db_search(event_id):
    d = datetime.datetime.now()
    return_content=[]
    for c in Event.find():
        #if(c['end_year'] * 10000 + c['end_month'] * 100 + c['end_day'] < d.year * 10000 + d.month * 100 + d.day):
        if (int(c['end_year']) * 100000000 + int(c['end_month']) * 1000000 + int(c['end_day'])* 10000+  int(c['end_hour']) * 100 + int(c['end_minute'])< d.year * 100000000 + d.month * 1000000 + d.day*10000 + d.hour*100+ d.minute):
            Event.update_one(
                {"event_id": c['event_id']},
                {
                    "$set": {
                        'time_limit_flag': True
                    }
                }
            )
    content= Event.find({'person_limit_flag': False, 'time_limit_flag': False})

    for c in content:
        for i in event_id:
            if c['event_id']==i:
                return_content.append(c)

    return return_content

def all_study_event():
    d = datetime.datetime.now()
    for c in Event.find():
        #if (c['end_year'] * 10000 + c['end_month'] * 100 + c['end_day'] < d.year * 10000 + d.month * 100 + d.day):
        if (int(c['end_year']) * 100000000 + int(c['end_month']) * 1000000 + int(c['end_day'])* 10000+  int(c['end_hour']) * 100 + int(c['end_minute'])< d.year * 100000000 + d.month * 1000000 + d.day*10000 + d.hour*100+ d.minute):
            Event.update_one(
                {"event_id": c['event_id']},
                {
                    "$set": {
                        'time_limit_flag': True
                    }
                }
            )
    context= Event.find({"type": 'study', "person_limit_flag": False, 'time_limit_flag': False})
    return context

def all_eat_event():
    d = datetime.datetime.now()
    for c in Event.find():
        #if (c['end_year'] * 10000 + c['end_month'] * 100 + c['end_day'] < d.year * 10000 + d.month * 100 + d.day):
        if (int(c['end_year']) * 100000000 + int(c['end_month']) * 1000000 + int(c['end_day'])* 10000+  int(c['end_hour']) * 100 + int(c['end_minute'])< d.year * 100000000 + d.month * 1000000 + d.day*10000 + d.hour*100+ d.minute):
            Event.update_one(
                {"event_id": c['event_id']},
                {
                    "$set": {
                        'time_limit_flag': True
                    }
                }
            )
    context = Event.find({"type": 'eat', "person_limit_flag": False, 'time_limit_flag': False})
    return context

def all_home_event():
    d = datetime.datetime.now()
    for c in Event.find():
        #if (c['end_year'] * 10000 + c['end_month'] * 100 + c['end_day'] < d.year * 10000 + d.month * 100 + d.day):
        if (int(c['end_year']) * 100000000 + int(c['end_month']) * 1000000 + int(c['end_day'])* 10000+  int(c['end_hour']) * 100 + int(c['end_minute'])< d.year * 100000000 + d.month * 1000000 + d.day*10000 + d.hour*100+ d.minute):
            Event.update_one(
                {"event_id": c['event_id']},
                {
                    "$set": {
                        'time_limit_flag': True
                    }
                }
            )
    context = Event.find({"type": 'home', "person_limit_flag": False, 'time_limit_flag': False})
    return context

def find_my_moment(info):
    follower= info['followers']
    return follower

def get_all_my_event(user_id):
    context= Event.find({'starter': user_id})
    return context

def add_join_event_db(user_id, event_id):
    user = User.find_one({"user_id": user_id})
    if user['join_event'] is None:
        list=[]
        list.append(event_id['event_id'])
    else:
        list=user['join_event']
        list.append(event_id['event_id'])
    User.update_one(
        {"user_id": user_id},
        {
            "$set": {
                'join_event': list
            }
        }
    )

def get_join_event_db(user_id):
    user = User.find_one({"user_id": user_id})
    list= user['join_event']
    context=[]
    if list is None:
        return context
    for j in list:
        e=Event.find_one({"event_id":int(j)})
        context.append(e)
    return context

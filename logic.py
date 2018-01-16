import datetime
from dynamodb import get_event_from_db_search, create_student, update_student, find_student, find_name_student, get_event_from_db, all_study_event, all_eat_event, all_home_event, create_event_db, find_my_moment, get_all_my_event, add_join_event_db, get_join_event_db

def login(user_id, password):
    user = find_student(int(user_id))
    if user is not None and user['password'] == password:
        return user
    else:
        return None

def create_student_l(student):
    student['since'] = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    user_id= create_student(student)
    return find_student(user_id)

def update_student_l(user_id,student):
    #student['since'] = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    m=find_student(user_id)
    user_id= update_student(m,student)
    return find_student(user_id)

def all_searched_event(user_id,event_id):
    context = get_event_from_db_search(event_id)
    content = []
    for c in context:
        if (c['starter'] != user_id):
            content.append(c)
    list = []
    for c in content:
        user = find_student(c['starter'])
        if (int(c['start_minute']) < 10):
            t = str(c['start_year']) + "-" + str(c['start_month']) + "-" + str(
                c['start_day'] + "-" + str(c['start_hour']) + ":" + '0' + str(c['start_minute']))
        else:
            t = str(c['start_year']) + "-" + str(c['start_month']) + "-" + str(
                c['start_day'] + "-" + str(c['start_hour']) + ":" + str(c['start_minute']))
        if (int(c['end_minute']) < 10):
            t2 = str(c['end_year']) + "-" + str(c['end_month']) + "-" + str(
                c['end_day'] + "-" + str(c['end_hour']) + ":" + '0' + str(c['end_minute']))
        else:
            t2 = str(c['end_year']) + "-" + str(c['end_month']) + "-" + str(
                c['end_day'] + "-" + str(c['end_hour']) + ":" + str(c['end_minute']))
        dic2 = {
            'event_id': c['event_id'],
            'nick_name': user['nick_name'],
            'starttime': t,
            'endtime': t2,
            'type': c['type'],
            'email': user['email'],
            'image': c['image'],
            'content': c['content']
        }
        list.append(dic2)
    return list

def all_alive_event(user_id):
    context= get_event_from_db()
    content=[]
    for c in context:
        if(c['starter']!= user_id):
            content.append(c)
    list = []
    for c in content:
        user = find_student(c['starter'])
        if (int(c['start_minute']) < 10):
            t = str(c['start_year']) + "-" + str(c['start_month']) + "-" + str(
                c['start_day'] + "-" + str(c['start_hour']) + ":" + '0' + str(c['start_minute']))
        else:
            t = str(c['start_year']) + "-" + str(c['start_month']) + "-" + str(
                c['start_day'] + "-" + str(c['start_hour']) + ":" + str(c['start_minute']))
        if (int(c['end_minute']) < 10):
            t2 = str(c['end_year']) + "-" + str(c['end_month']) + "-" + str(
                c['end_day'] + "-" + str(c['end_hour']) + ":" + '0' + str(c['end_minute']))
        else:
            t2 = str(c['end_year']) + "-" + str(c['end_month']) + "-" + str(
                c['end_day'] + "-" + str(c['end_hour']) + ":" + str(c['end_minute']))
        dic2 = {
            'event_id': c['event_id'],
            'nick_name': user['nick_name'],
            'starttime': t,
            'endtime':t2,
            'type': c['type'],
            'email': user['email'],
            'image': c['image'],
            'content': c['content']
        }
        list.append(dic2)
    return list

def study_event(user_id):
    context= all_study_event()
    content=[]
    for c in context:
        if(c['starter']!= user_id):
            content.append(c)
    list = []
    for c in content:
        user = find_student(c['starter'])
        if (int(c['start_minute']) < 10):
            t = str(c['start_year']) + "-" + str(c['start_month']) + "-" + str(
                c['start_day'] + "-" + str(c['start_hour']) + ":" + '0' + str(c['start_minute']))
        else:
            t = str(c['start_year']) + "-" + str(c['start_month']) + "-" + str(
                c['start_day'] + "-" + str(c['start_hour']) + ":" + str(c['start_minute']))
        if (int(c['end_minute']) < 10):
            t2 = str(c['end_year']) + "-" + str(c['end_month']) + "-" + str(
                c['end_day'] + "-" + str(c['end_hour']) + ":" + '0' + str(c['end_minute']))
        else:
            t2 = str(c['end_year']) + "-" + str(c['end_month']) + "-" + str(
                c['end_day'] + "-" + str(c['end_hour']) + ":" + str(c['end_minute']))
        dic2 = {
            'event_id': c['event_id'],
            'nick_name': user['nick_name'],
            'starttime': t,
            'endtime':t2,
            'type': c['type'],
            'email': user['email'],
            'image': c['image'],
            'content': c['content']
        }
        list.append(dic2)
    return list


def eat_event(user_id):
    context= all_eat_event()
    content=[]
    for c in context:
        if(c['starter']!= user_id):
            content.append(c)
    list = []
    for c in content:
        user = find_student(c['starter'])
        if (int(c['start_minute']) < 10):
            t = str(c['start_year']) + "-" + str(c['start_month']) + "-" + str(
                c['start_day'] + "-" + str(c['start_hour']) + ":" + '0' + str(c['start_minute']))
        else:
            t = str(c['start_year']) + "-" + str(c['start_month']) + "-" + str(
                c['start_day'] + "-" + str(c['start_hour']) + ":" + str(c['start_minute']))
        if (int(c['end_minute']) < 10):
            t2 = str(c['end_year']) + "-" + str(c['end_month']) + "-" + str(
                c['end_day'] + "-" + str(c['end_hour']) + ":" + '0' + str(c['end_minute']))
        else:
            t2 = str(c['end_year']) + "-" + str(c['end_month']) + "-" + str(
                c['end_day'] + "-" + str(c['end_hour']) + ":" + str(c['end_minute']))
        dic2 = {
            'event_id': c['event_id'],
            'nick_name': user['nick_name'],
            'starttime': t,
            'endtime':t2,
            'type': c['type'],
            'email': user['email'],
            'image': c['image'],
            'content': c['content']
        }
        list.append(dic2)
    return list

def home_event(user_id):
    context= all_home_event()
    content=[]
    for c in context:
        if(c['starter']!= user_id):
            content.append(c)
    list = []
    for c in content:
        user = find_student(c['starter'])
        if (int(c['start_minute']) < 10):
            t = str(c['start_year']) + "-" + str(c['start_month']) + "-" + str(
                c['start_day'] + "-" + str(c['start_hour']) + ":" + '0' + str(c['start_minute']))
        else:
            t = str(c['start_year']) + "-" + str(c['start_month']) + "-" + str(
                c['start_day'] + "-" + str(c['start_hour']) + ":" + str(c['start_minute']))
        if (int(c['end_minute']) < 10):
            t2 = str(c['end_year']) + "-" + str(c['end_month']) + "-" + str(
                c['end_day'] + "-" + str(c['end_hour']) + ":" + '0' + str(c['end_minute']))
        else:
            t2 = str(c['end_year']) + "-" + str(c['end_month']) + "-" + str(
                c['end_day'] + "-" + str(c['end_hour']) + ":" + str(c['end_minute']))
        dic2 = {
            'event_id': c['event_id'],
            'nick_name': user['nick_name'],
            'starttime': t,
            'endtime':t2,
            'type': c['type'],
            'email': user['email'],
            'image': c['image'],
            'content': c['content']
        }
        list.append(dic2)
    return list

def create_event(trend, user_id):
    return create_event_db(trend, user_id)

def get_my_moment(user_id):
    user= find_student(user_id)
    context= get_join_event_db(user_id)
    list = []
    for c in context:
        if (int(c['start_minute']) < 10):
            t = str(c['start_year']) + "-" + str(c['start_month']) + "-" + str(
                c['start_day'] + "-" + str(c['start_hour']) + ":" + '0' + str(c['start_minute']))
        else:
            t = str(c['start_year']) + "-" + str(c['start_month']) + "-" + str(
                c['start_day'] + "-" + str(c['start_hour']) + ":" + str(c['start_minute']))
        if (int(c['end_minute']) < 10):
            t2 = str(c['end_year']) + "-" + str(c['end_month']) + "-" + str(
                c['end_day'] + "-" + str(c['end_hour']) + ":" + '0' + str(c['end_minute']))
        else:
            t2 = str(c['end_year']) + "-" + str(c['end_month']) + "-" + str(
                c['end_day'] + "-" + str(c['end_hour']) + ":" + str(c['end_minute']))
        user2 = find_student(c['starter'])
        dic2 = {
            'nick_name': user2['nick_name'],
            'starttime': t,
            'endtime': t2,
            'type': c['type'],
            'email': user2['email'],
            'image': c['image'],
            'content': c['content']
        }
        list.append(dic2)
    return list

def get_my_own(user_id):
    #context = [{'nick_name': 'Jack', 'time': '2017-12-20', 'type': 'study', 'email': '1253263462@qq.com',
    #            'image': 'https://i.ytimg.com/vi/zNCz4mQzfEI/maxresdefault.jpg',
    #            'content': 'I would like to see coco.'}
    #           ]
    context= get_all_my_event(user_id)
    user= find_student(user_id)
    list=[]
    for c in context:
        if (int(c['start_minute']) < 10):
            t = str(c['start_year']) + "-" + str(c['start_month']) + "-" + str(
                c['start_day'] + "-" + str(c['start_hour']) + ":" + '0' + str(c['start_minute']))
        else:
            t = str(c['start_year']) + "-" + str(c['start_month']) + "-" + str(
                c['start_day'] + "-" + str(c['start_hour']) + ":" + str(c['start_minute']))
        if (int(c['end_minute']) < 10):
            t2 = str(c['end_year']) + "-" + str(c['end_month']) + "-" + str(
                c['end_day'] + "-" + str(c['end_hour']) + ":" + '0' + str(c['end_minute']))
        else:
            t2 = str(c['end_year']) + "-" + str(c['end_month']) + "-" + str(
                c['end_day'] + "-" + str(c['end_hour']) + ":" + str(c['end_minute']))
        '''dic = {
            'nick_name': user['nick_name'],
            'time': t,
            'type': c['type'],
            'email': user['email'],
            'image': c['image'],
            'content': c['content']
        }'''
        dic2 = {
            'nick_name': user['nick_name'],
            'starttime': t,
            'endtime': t2,
            'type': c['type'],
            'email': user['email'],
            'image': c['image'],
            'content': c['content']
        }
        list.append(dic2)
    return list

def add_join_event(user_id, event_id):
    add_join_event_db(user_id, event_id)







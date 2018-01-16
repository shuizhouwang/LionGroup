import datetime
import os
from flask import Flask, request, render_template, session, redirect
from flask_cors import CORS
from logic import create_student_l, update_student_l, login, all_alive_event, study_event, eat_event, home_event, create_event, \
    get_my_moment, get_my_own, add_join_event, all_searched_event
from dynamodb import search_by_key, send_reminder

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'template')
application = Flask(__name__, template_folder=tmpl_dir)
CORS(application)

application.secret_key = 'super secret key'
application.config['SESSION_TYPE'] = 'filesystem'


def args2dict(request_args, args):
    res = {}
    for arg in args:
        res[arg] = request_args.form[arg]
    return res


@application.route('/')
def home_page():
    return render_template('login.html')


@application.route('/register/')
def register_page():
    return render_template('register.html')


@application.route('/user/create/', methods=['POST'])
def register_user():
    args = ["nick_name", "avatar", "email", "password",
            "introduction"]
    user = args2dict(request, args)
    new_user = create_student_l(user)
    new_user['_id'] = str(new_user['_id'])
    session['user'] = new_user

    return redirect('/user/')


@application.route('/user/')
def user_home_page():
    if session['user'] is not None:
        return render_template('user.html')
    else:
        return render_template('error.html')


@application.route('/user/login/', methods=['POST'])
def login_user():
    user_id = request.form['user_id']
    password = request.form['password']
    user = login(user_id, password)
    if user is None:
        return render_template('error.html')
    user['_id'] = str(user['_id'])
    t = ""
    content = get_my_own(int(user_id))
    for c in content:
        t = t + " " + c['content']
    if t != "":
        send_reminder(t, user_id)
    if user is not None:
        session['user'] = user
        return redirect('/user/')


@application.route('/user/update/', methods=['POST'])
def update_st():
    args = ["nick_name", "avatar", "email", "password",
            "introduction"]
    user = args2dict(request, args)
    user_id=session['user']['user_id']
    update_user = update_student_l(user_id,user)
    update_user['_id'] = str(update_user['_id'])
    session['user'] = update_user

    return redirect('/user/')


@application.route('/discover/', methods=['GET'])
def get_all_event():
    user_id = session['user']['user_id']
    context = all_alive_event(user_id)
    return render_template('discover.html', events=context)


@application.route('/discover/search/', methods=['POST'])
def search_event():
    key_word = request.form['key_word']
    pre_context=search_by_key(key_word)
    user_id=session['user']['user_id']
    event_id=[]
    for i in pre_context:
        event_id.append(i['event_id'])
    context = all_searched_event(user_id,event_id)
    return render_template('discover.html', events=context)


@application.route('/discover/join/', methods=['POST'])
def join_event():
    event_id=request.form.to_dict('event_id')
    add_join_event(session['user']['user_id'], event_id)

    return redirect('/discover/')


@application.route('/discover/study/', methods=['GET'])
def get_study_event():
    user_id = session['user']['user_id']
    context = study_event(user_id)
    return render_template('discover.html', events=context)


@application.route('/discover/eat/', methods=['GET'])
def get_eat_event():
    user_id = session['user']['user_id']
    context = eat_event(user_id)
    return render_template('discover.html', events=context)


@application.route('/discover/home/', methods=['GET'])
def get_home_event():
    user_id = session['user']['user_id']
    context = home_event(user_id)
    return render_template('discover.html', events=context)


@application.route('/myevent/start/', methods=['GET'])
def get_my_own_event():
    user_id = session['user']['user_id']
    context = get_my_own(user_id)
    return render_template('myevent.html', events=context)


@application.route('/myevent/join/', methods=['GET'])
def get_my_join_event():
    user_id = session['user']['user_id']
    context = get_my_moment(user_id)
    return render_template('myevent.html', events=context)


@application.route('/event/create/', methods=['POST'])
def event_create():
    args = ["content", "image", "startmonth", "startday", "starthour", "startminute", "startyear", "endmonth", "endday",
            "endhour", "endminute", "endyear", "type", ]
    trend = args2dict(request, args)
    d = datetime.datetime.now()
    user_id = session['user']['user_id']
    dic, EID = create_event(trend, user_id)
    if (EID==-1):
        return render_template('error.html')


    if (int(trend['startminute']) < 10):
        t1 = str(trend['startyear']) + "-" + str(trend['startmonth']) + "-" + str(
            trend['startday'] + "-" + str(trend['starthour']) + ":" + '0' + str(trend['startminute']))
    else:
        t1 = str(trend['startyear']) + "-" + str(trend['startmonth']) + "-" + str(
            trend['startday'] + "-" + str(trend['starthour']) + ":" + str(trend['startminute']))
    if (int(trend['endminute']) < 10):
        t2 = str(trend['endyear']) + "-" + str(trend['endmonth']) + "-" + str(
            trend['endday'] + "-" + str(trend['endhour']) + ":" + '0' + str(trend['endminute']))
    else:
        t2 = str(trend['endyear']) + "-" + str(trend['endmonth']) + "-" + str(
            trend['endday'] + "-" + str(trend['endhour']) + ":" + str(trend['endminute']))

    #will be added later
    dic3 = {
        'nick_name': session['user']['nick_name'],
        'starttime': t1,
        'endtime':t2,
        'type': dic['type'],
        'email': session['user']['email'],
        'image': dic['image'],
        'content': dic['content']
    }

    context = []
    context.append(dic3)
    return render_template('myevent.html', events=context)


if __name__ == '__main__':
    import click


    @click.command()
    @click.option('--debug', is_flag=True)
    @click.option('--threaded', is_flag=True)
    @click.argument('HOST', default='0.0.0.0')
    @click.argument('PORT', default=8111, type=int)
    def run(debug, threaded, host, port):
        """
        This function handles command line parameters.
        Run the server using:
            python server.py
        Show the help text using:
            python server.py --help
        """

        HOST, PORT = host, port
        application.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


    run()

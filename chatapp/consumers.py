import json
import time
from datetime import datetime
from django.core.mail import send_mail
from django.contrib.auth.models import User, Group
from channels.channel import Group, Channel
from channels.auth import channel_session_user_from_http, channel_session_user
import sqlite3
from chatapp.models import Privat_Chat_User, Privat_Chat_Name, Chat, Privat_Chat, Reply_Channel


@channel_session_user_from_http
def ws_connect(message):

    # accept reply_channel
    message.reply_channel.send({'accept': True})

    # get path and add user in Group(path)
    path = message.content['path'].strip('/')
    Group(path).add(message.reply_channel)

    if (path == "chat"):
        # limit messages for show
        chatSize = Chat.objects.all().count()
        rows_limit = 100
        offset = (chatSize - rows_limit) if ((chatSize - rows_limit) > 0) else 0
        results = Chat.objects.all()[offset:].values('time', 'username', 'message')

    else:
        # get id of privat chat
        chat_id = int(path[4:])

        # set user_on = true and new_message = false in chat with correct chat_id
        user_id = message.user.id

        u = Privat_Chat_User.objects.filter(chat_id=chat_id).filter(user_id=user_id)
        for ob in u:
            ob.new_message = 0
            ob.user_on = 1
            ob.save()

        # search for messages in correct chat_id
        results = Privat_Chat.objects.filter(chat_id = chat_id).values('time', 'username', 'message').order_by('time')

    # send massages from DB
    for res in results:

        try:
            # time = datetime.strptime(res[2].rpartition('.')[0], "%Y-%m-%d %H:%M:%S")
            time = datetime.strftime(res['time'], "%d.%m.%y %H:%M:%S")
        except:
            time = res['time']

        message.reply_channel.send({'text': json.dumps({'message': res['message'],
                                                'username': res['username'],
                                                'time': time})})

    if not message.user.id:
        return

    # add reply_channel for user in DB
    user_id = message.user.id

    u = Reply_Channel(user_id=user_id, reply_channel=message.reply_channel.name)
    u.save()

    # check for new messages in other chats
    results = Privat_Chat_User.objects.filter(user_id = user_id).filter(new_message=1).count()
    if (results):

        Channel(message.reply_channel.name).send({'text': json.dumps({'message': "New message in another private chat",
                                                      'username': " - ",
                                                      'time': 0})})


@channel_session_user
def ws_message(message):

    path = message.content['path'].strip('/')

    # add message to DB
    if (path == "chat"):
        u = Chat(time=datetime.now(), username=message.user.username, message=message.content['text'])
        u.save()
    else:
        # get privat chat id
        chat_id = path[4:]
        chat_id = int(chat_id)

        u = Privat_Chat(chat_id=chat_id, time=datetime.now(), username=message.user.username, message=message.content['text'])
        u.save()

        # set new_message = true for users with user_on=false
        u = Privat_Chat_User.objects.filter(chat_id=chat_id).filter(user_on=0)

        for ob in u:
            ob.new_message = 1
            ob.save()

        # send "new message" for users with new_messages = true
        ids = Privat_Chat_User.objects.filter(chat_id=chat_id).filter(new_message=1).values('user_id')

        for id in ids:
            results = Reply_Channel.objects.filter(user_id=id['user_id']).values('reply_channel')
            if results:
                try:
                    Channel(results[0]['reply_channel']).send({'text': json.dumps({'message': "New message in another private chat",
                                                          'username': " - ",
                                                          'time': 0})})
                except:
                    print("ERROR Channel name must be a valid unicode string" )


    Group(path).send({'text': json.dumps({'message': message.content['text'],
                                            'username': message.user.username,
                                            'time': datetime.strftime(datetime.now(), "%d.%m.%y %H:%M:%S")})})


@channel_session_user
def ws_disconnect(message):
    path = message.content['path'].strip('/')

    if not message.user.id:
        Group(path).discard(message.reply_channel)
        return

    # delete reply_channel of user from DB
    user_id = int(message.user.id)
    Reply_Channel.objects.filter(user_id=user_id).delete()

    if (path != "chat"):

        # get privat chat id
        chat_id = path[4:]
        chat_id = int(chat_id)

        # set user_on = false in correct chat id
        u = Privat_Chat_User.objects.filter(chat_id=chat_id).filter(user_id=user_id)
        for ob in u:
            ob.user_on = 0
            ob.save()
    Group(path).discard(message.reply_channel)

from channels.routing import route
# from channels.staticfiles import StaticFilesConsumer
# from chatapp import consumers
print("in routing.py _______1________1__________1___________1________")
channel_routing ={
#     'http.request': StaticFilesConsumer(),

    'websocket.connect': 'chatapp.consumers.ws_connect',
    'websocket.receive': 'chatapp.consumers.ws_message',
    'websocket.disconnect': 'chatapp.consumers.ws_disconnect',

}

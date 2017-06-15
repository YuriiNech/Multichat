from channels.routing import route
# from channels.staticfiles import StaticFilesConsumer
from chatapp import consumers
print("in routing.py _______1________1__________1___________1________")
channel_routing ={
#     'http.request': StaticFilesConsumer(),

    'websocket.connect': consumers.ws_connect,
    'websocket.receive': consumers.ws_message,
    'websocket.disconnect': consumers.ws_disconnect,

}

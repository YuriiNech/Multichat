# from channels.routing import route
from channels.staticfiles import StaticFilesConsumer
from .chatapp import consumers

channel_routing ={
    'http.request': StaticFilesConsumer(),

    'websocket.connect': consumers.ws_connect,
    'websocket.receive': consumers.ws_message,
    'websocket.disconnect': consumers.ws_disconnect,

}

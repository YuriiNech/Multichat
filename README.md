# Multichat

Multichat is created in Python using the Django framework, Channels and WebSockets.

Chat messages are stored for some time (now it is 365 days) and can be viewed the next time you log in. In addition to the common chat, messages are visible to all visitors, registered users can create private chat rooms with other chat users.

If the private chat in which you are a member, has new messages, it will remind you with a special message. In addition, the private chat will be highlighted in red. Being in a private chat you can see who is the member of this chat and whether he is online or offline. You can sign out of this private chat or add new members.

This multichat was adapted for Heroku 
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/YuriiNech/Multichat)

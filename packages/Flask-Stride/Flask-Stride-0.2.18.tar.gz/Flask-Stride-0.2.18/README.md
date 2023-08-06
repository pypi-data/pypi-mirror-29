# Flask-Stride

## Introduction
Flask-Stride is a [Flask](http://flask.pocoo.org/) extension that lets you easily create [Atlassian Stride](https://www.stride.com/) apps (a.k.a bots)

## Installation
Using Pip: `pip install flask-stride`

## Example

```
from flask import Flask
from flask_stride import Stride

app = Flask(__name__)

s = Stride(key='My Bot')

# This is code will be triggered when someone @mentions your app.
@s.chat_bot('my_bot', '/mention', '/direct-message')
def chat_f():
    # Do Stuff
    # Make sure it returns within 10s.
    return ('',204)

# This is code will be triggered when there is a message that matches the specified regex.
@s.chat_bot_messages('my_msgs', 'a.regex.pattern.*', '/messages')
def chat_msg_f():
    # Do Other Stuff
    # Make sure it returns within 10s.
    return ('',204)

# This is code that will be used for a in-app dialog.
@s.chat_dialog(key='dlg-key-1', title='My Dialog', path='/dlg')
def chat_dlg_f():
    html = '<html><body>This is an awesome dialog box.</body></html>'
    return html

# This is code that will add a message action that triggers the 'dlg-key-1' dialog
s.chat_message_action('msg-act-key-1', 'Do Stuff', 'dlg-key-1')

# This is code that will add a input action that triggers the 'dlg-key-1' dialog
s.chat_input_action('inp-act-key-1', 'Do Other Stuff', 'dlg-key-1')

# This is code that will add an external page target
s.chat_external_page(key='ep-key-1', name='My External Page', url='https://example.com/some_page')

# This code will add Glance
s.chat_glance(key='gl-key', name='My Glance', icon_1x='/path/to/icon', icon_2x='/path/to/2x_icon')

# This defines queryUrl endpoint for a glance.
@s.chat_glance_query(key='gl-key', path='/gl-key-query')
def chat_glance_q():
    query_result = {}
    query_result['label'] = {}
    query_result['label']['value'] = 'My query result.'

    return str(query_result)

# This defines a chat:sidebar module.
@s.chat_sidebar(key='sb-key-1', name='My Sidebar', url='/sb-1')
def chat_sidebar():
  return 'Hello, my sidebar is awesome.'

# This needs to be called after defining all of your bot code
s.init_app(a)
```
The above code will create a simple bot called "My Bot" and setups all of the endpoints required.
Whenver your bot is mentioned in a conversation or directly, the `chat_f()` function will be executed.

As an added bonus, the App Descriptor endpoint is automatically configured for you. By default, it is located at [/app-descriptor.json]() of your web server.

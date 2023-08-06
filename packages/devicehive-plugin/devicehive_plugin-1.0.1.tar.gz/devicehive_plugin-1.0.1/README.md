[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE) 
[![Build Status](https://travis-ci.org/devicehive/devicehive-plugin-python.svg?branch=master)](https://travis-ci.org/devicehive/devicehive-plugin-python)

# Devicehive plugin
This library provides wrapper for DeviceHive plugin API

## Installation

To install this package run:
```bash
pip install devicehive-plugin
```

## Creating a client using Plugin class

First of all you need to create custom `Handler` class.

`Handler` class provides several `handle_*` methods:
* `handle_connect(self)` will be called after successful connection
* `handle_event(self, event)` will be called after event of any type is received. Takes [ApiEvent](#apievent-object) object.
* `handle_command_insert(self, command)` will be called after `command/insert` event is received. Takes [Command](#command-object) object.
* `handle_command_update(self, command)` will be called after `command/update` event is received. Takes [Command](#command-object) object.
* `handle_notification(self, notification)` will be called after `notification/insert` event is received. Takes [Notification](#notification-object) object.

`handle_event` will be called before type-special `handle` methods.

Example:

```python
from devicehive_plugin import Handler


class SimpleHandler(Handler):

    def handle_connect(self):
        print('Successfully connected')

    def handle_event(self, event):
        print(event.action)
        print(type(event.data))

    def handle_command_insert(self, command):
        print(command.command)

    def handle_command_update(self, command):
        print(command.command)

    def handle_notification(self, notification):
        print(notification.notification)
```

The second step is to use `Plugin` class for creating connection to the server.

Example:

```python
from devicehive_plugin import Handler
from devicehive_plugin import Plugin


class SimpleHandler(Handler):

    def handle_connect(self):
        print('Successfully connected')

    def handle_event(self, event):
        print(event.action)
        print(type(event.data))

    def handle_command_insert(self, command):
        print(command.command)

    def handle_command_update(self, command):
        print(command.command)

    def handle_notification(self, notification):
        print(notification.notification)


url = 'ws://playground-dev.devicehive.com/plugin/proxy/'
topic_name = 'PLUGIN_TOPIC_NAME'
plugin_access_token = 'PLUGIN_ACCESS_TOKEN'
plugin = Plugin(SimpleHandler)
plugin.connect(url, topic_name, plugin_access_token=plugin_access_token)
```

### Custom handler args

If you need to initialize your handler you can do it the next way:

```python
from devicehive_plugin import Handler
from devicehive_plugin import Plugin


class SimpleHandler(Handler):

    def __init__(self, api, some_arg, some_kwarg):
        super(SimpleHandler, self).__init__(api)
        self._some_arg = some_arg
        self._some_kwarg = some_kwarg


plugin = Plugin(SimpleHandler, 'some_arg', some_kwarg='some_kwarg')
```

### Authentication

There are several ways of initial authentication:

* Using plugin's access token
* Using plugin's refresh token
* Using user's access token
* Using user's refresh token
* Using user's login and password

If you want to use anything but plugin's access token you need to provide `auth_url` parameter.

Examples:

```python
url = 'ws://playground-dev.devicehive.com/plugin/proxy/'
topic_name = 'PLUGIN_TOPIC_NAME'
plugin.connect(url, topic_name,
               plugin_access_token='SOME_PLUGIN_ACCESS_TOKEN')
```

```python
url = 'ws://playground-dev.devicehive.com/plugin/proxy/'
topic_name = 'PLUGIN_TOPIC_NAME'
auth_url = 'http://playground-dev.devicehive.com/api/rest'
plugin.connect(url, topic_name, auth_url=auth_url,
               plugin_refresh_token='SOME_PLUGIN_REFRESH_TOKEN')
```

```python
url = 'ws://playground-dev.devicehive.com/plugin/proxy/'
topic_name = 'PLUGIN_TOPIC_NAME'
auth_url = 'http://playground-dev.devicehive.com/api/rest'
plugin.connect(url, topic_name, auth_url=auth_url,
               access_token='SOME_USER_ACCESS_TOKEN')
```

```python
url = 'ws://playground-dev.devicehive.com/plugin/proxy/'
topic_name = 'PLUGIN_TOPIC_NAME'
auth_url = 'http://playground-dev.devicehive.com/api/rest'
plugin.connect(url, topic_name, auth_url=auth_url,
               refresh_token='SOME_USER_REFRESH_TOKEN')
```

```python
url = 'ws://playground-dev.devicehive.com/plugin/proxy/'
topic_name = 'PLUGIN_TOPIC_NAME'
auth_url = 'http://playground-dev.devicehive.com/api/rest'
plugin.connect(url, topic_name, auth_url=auth_url,
               login='SOME_USER_LOGIN', password='SOME_USER_PASSWORD')
```

## Api reference

### ApiEvent object

Properties (read only):

* `is_command_insert_event`
* `is_command_update_event`
* `is_command_event`
* `is_notification_event`
* `action`
* `raw_data`
* `data`

### Command object

Properties (read only):

* `id`
* `user_id`
* `command`
* `parameters`
* `lifetime`
* `timestamp`
* `last_updated`
* `status`
* `result`

### Notification object

Properties (read only):

* `device_id`
* `id`
* `notification`
* `parameters`
* `timestamp`

## Docker tests

### Build image

```
docker build -f Dockerfile -t devicehive-plugin-tests .
```

### Run tests

You can run tests with refresh_token by setting `ADMIN_REFRESH_TOKEN` and/or `CLIENT_REFRESH_TOKEN` variable:

```
docker run -it -e ADMIN_REFRESH_TOKEN='SOME_ADMIN_REFRESH_TOKEN' devicehive-plugin-tests
```

Or with access_token by setting `ADMIN_ACCESS_TOKEN` and/or `CLIENT_ACCESS_TOKEN` variable:

```
docker run -it -e ADMIN_ACCESS_TOKEN='SOME_ADMIN_ACCESS_TOKEN' devicehive-plugin-tests
```

Or with user login and password by setting `ADMIN_LOGIN` and `ADMIN_PASSWORD` for admin account and/or `CLIENT_LOGIN` and `CLIENT_PASSWORD` for client account.

```
docker run -it -e ADMIN_LOGIN='SOME_ADMIN_LOGIN' -e ADMIN_PASSWORD='SOME_ADMIN_PASSWORD' devicehive-plugin-tests
```

To run tests with enabled requests logging you need to change `LOG_LEVEL` variable:

```
docker run -it -e ADMIN_REFRESH_TOKEN='SOME_ADMIN_REFRESH_TOKEN' -e LOG_LEVEL='DEBUG' devicehive-plugin-tests
```

To run the specific test you need to set `TEST` variable:

```
docker run -it -e TEST=test_api.py::test_get_info -e ADMIN_REFRESH_TOKEN='SOME_ADMIN_REFRESH_TOKEN' devicehive-plugin-tests
```

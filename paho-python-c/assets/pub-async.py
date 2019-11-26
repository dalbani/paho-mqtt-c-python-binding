import os, paho_mqtt3a as mqttv3, time


def delivery_complete(context, msgid):
    print("delivery_complete", msgid)


def connection_lost(context, cause):
    print("connection_lost", cause)


def message_arrived(context, topic_name, message):
    print("message_arrived", topic_name, message)
    return 1


def connected(context, cause):
    print("connected", cause)


def on_success(context, success_data):
    print("on_success", success_data)


def on_failure(context, failure_data):
    print("on_failure", failure_data)


rc, client = mqttv3.create('tcp://%s:%s' % (os.getenv("MQTT_SERVER_HOST"), os.getenv("MQTT_SERVER_PORT")),
                           os.getenv('MQTT_CLIENT_ID'), mqttv3.PERSISTENCE_DEFAULT,
                           {'sendWhileDisconnected': 1, 'maxBufferedMessages': 100000})
print('mqttv3.create(), rc = %d' % rc)

context = {'client': client}

rc = mqttv3.setcallbacks(client, client, connection_lost, message_arrived, delivery_complete)
print('mqttv3.setcallbacks(), rc = %d' % rc)

rc = mqttv3.connect(client, {
    'keepAliveInterval': int(os.getenv('MQTT_KEEP_ALIVE')),
    'cleansession': 0,
    'automaticReconnect': 1,
    'maxRetryInterval': 10,
    'context': context,
    'on_success': on_success,
    'on_failure': on_failure
})
print('mqttv3.connect(), rc = %d' % rc)

count = 0

while True:
    payload = str(count)
    print("OUT => " + payload)
    rc, _ = mqttv3.send(client, os.environ['MQTT_TOPIC'], payload, int(os.environ['MQTT_QOS']), 0, {})
    print('mqttv3.send(), rc = %d' % rc)
    time.sleep(1)
    count += 1

rc = mqttv3.disconnect(client, 1000)
print('mqttv3.disconnect(), rc = %d' % rc)

rc = mqttv3.destroy(client)
print('mqttv3.destroy, rc = %d' % rc)

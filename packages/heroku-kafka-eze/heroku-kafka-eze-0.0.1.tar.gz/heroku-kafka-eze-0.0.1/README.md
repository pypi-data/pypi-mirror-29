# Heroku Kafka Easy

**THIS IS AN UNOFFICIAL PACKAGE**

Heroku Kafka is a python package to help you get setup quickly and easily with Kafka on Heroku. There is an [offical package](https://github.com/heroku/kafka-helper) however it has not been does not seem to be maintained anymore. 


## Install

The easiest way to install the package is through pip.
```
pip install heroku-kafka-eze
```

## Usage

This package uses the [kafka-python package](https://github.com/dpkp/kafka-python) and the `HerokuKafkaProducer` and `HerokuKafkaConsumer` classes both inherit from the kafka-python base classes, and will contain all the same methods.

Note: You can use this package on locally too. 

Note: To test it is working on local I would install [heroku-kafka-util](https://github.com/osada9000/heroku-kafka-util) so you can see messages are being sent or simply use heroku CLI and 
install the heroku-kafka plugin.

### Producer

```python
from heroku_kafka_eze import HerokuSSL
from heroku_kafka_eze import HerokuKafkaProducer

app_name = 'your_heroku_app_name'
secret_key = 'your_heroku_api_key'
heroku_ssl = HerokuSSL(app_name, secret_key)
config = heroku_ssl.get_config()
"""
All the config variable needed well be received from heroku.
"""
producer = HerokuKafkaProducer(
        url=config['KAFKA_URL'], # Url string provided by heroku
        ssl_cert=config['KAFKA_CLIENT_CERT'], # Client cert string
        ssl_key=config['KAFKA_CLIENT_CERT_KEY'], # Client cert key string
        ssl_ca=config['KAFKA_TRUSTED_CERT'], # Client trusted cert string
        prefix=config['KAFKA_PREFIX'] # Prefix provided by heroku
    )

"""
The .send method will automatically prefix your topic with the KAFKA_PREFIX
NOTE: If the message doesn't seem to be sending try `producer.flush()` to force send.
"""
producer.send('topic_without_prefix', b"hola mundo")
```

For all other methods and properties refer to: [KafkaProducer Docs](https://kafka-python.readthedocs.io/en/master/apidoc/KafkaProducer.html).


### Consumer
```python
from heroku_kafka_eze import HerokuSSL
from heroku_kafka_eze import HerokuKafkaConsumer

"""
All the variable names here will be received from Heroku api
*topics are optional and you can pass as many as you want in for the consumer to track,
however if you want to subscribe after creation just use .subscribe as shown below.

Note: The KAFKA_PREFIX will be added on automatically so don't worry about passing it in.
"""
app_name = 'your_heroku_app_name'
secret_key = 'your_heroku_api_key'
heroku_ssl = HerokuSSL(app_name, secret_key)
config = heroku_ssl.get_config()

consumer = HerokuKafkaConsumer(
        'topic_without_prefix', # Optional: You don't need to pass any topic at all
        'topic_without_prefix_2', # You can list as many topics as you want to consume
        url=config['KAFKA_URL'], # Url string provided by heroku
        ssl_cert=config['KAFKA_CLIENT_CERT'], # Client cert string
        ssl_key=config['KAFKA_CLIENT_CERT_KEY'], # Client cert key string
        ssl_ca=config['KAFKA_TRUSTED_CERT'], # Client trusted cert string
        prefix=config['KAFKA_PREFIX'] # Prefix provided by heroku
    )
"""
To subscribe to topic(s) after creating a consumer pass in a list of topics without the
KAFKA_PREFIX.
"""
consumer.subscribe(topics=('topic_without_prefix'))
"""
.assign requires a full topic name with prefix
"""
consumer.assign([TopicPartition('topic_with_prefix', 2)])
"""
Listening to events it is exactly the same as in kafka_python.
Read the documention linked below for more info!
"""
for msg in consumer:
    print (msg)
```

For all other methods and properties refer to: [KafkaConsumer Docs](https://kafka-python.readthedocs.io/en/master/apidoc/KafkaConsumer.html).

## Known Issues 
- `.assign` does not add in the topic prefix.
- .NamedTemporaryFile may not work properly on a Windows system

## Contribution
If you come across any issues feel free to fork and create a PR!

## Setup
Fork the repo, setup virtualenv and pip install
```bash
>>> git clone git@github.com:<fork-repo>.git
>>> cd <fork-repo>
>>> virtualenv -p python3 venv
>>> source venv/bin/activate
>>> pip install -r requirements.txt
```

Create a config.py file with working heroku api key and the name of your app. 
```

APP_NAME=""
SECRET_KEY=""

TOPIC1=""
TOPIC2=""
```

## Tests
Please make sure that any extra code you write comes with a test, it doesn't need to be over the top but just check what you have written works.

All tests at the moment require a working kafka setup as its pretty hard to check it is connecting correctly without them. This means it will also require an internet connection.

To run the tests:
```bash
>>> python test.py
```
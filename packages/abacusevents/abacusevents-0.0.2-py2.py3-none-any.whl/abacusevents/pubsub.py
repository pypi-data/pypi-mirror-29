import json

from .abacusevents import Event
from .utils import singleton, curry, env
from google.api_core.exceptions import AlreadyExists
from google.cloud.pubsub import PublisherClient, SubscriberClient
from queue import Queue


def _assert_topic(topic_path: str, publisher: PublisherClient) -> ():
    try:
        publisher.create_topic(topic_path)
    except AlreadyExists:
        pass


def _assert_subscription(subscription_path: str,
                         topic_path: str,
                         publisher: PublisherClient,
                         subscriber: SubscriberClient) -> ():
    _assert_topic(topic_path, publisher)
    try:
        subscriber.create_subscription(subscription_path, topic_path)
    except AlreadyExists:
        pass


def _emit_event(publisher_client: PublisherClient, topic: str, event: Event) -> ():
    # Make topic path
    topic_path = publisher_client.topic_path(env('GOOGLE_CLOUD_PROJECT'),
                                             topic)

    # Get or create topic
    _assert_topic(topic_path, publisher_client)

    # Publish the serialized Event
    print(publisher_client, topic_path, event)
    publisher_client.publish(topic_path, data=event.serialize())


@singleton
class PubSub(object):
    def __init__(self):
        self.publisher = PublisherClient()
        self.subscriber = SubscriberClient()


@curry
def emit(topic, event: Event) -> ():
    _emit_event(PubSub().publisher, topic, event)


class Subscription(object):
    def __init__(self, subscription):
        self.q = Queue()
        self.subscription = subscription.open(self._callback)
        self.events = {}

    def __iter__(self):
        return self

    def __next__(self):
        yield self.get_next()

    def _callback(self, message):
        try:
            job = json.loads(message.data.decode('utf-8'))
            self.q.put(job)

        except json.JSONDecodeError as error:
            self.events.get('JSONDecodeError', False) \
                and self.events['JSONDecodeError'](error)

        except Exception as error:
            self.events.get('Exception', False) \
                and self.events['Exception'](error)

        finally:
            message.ack()

    def get_next(self):
        return self.q.get()

    def on(self, event, callback):
        self.events[event] = callback
        return self


def subscribe(subscription_name, topic):
    subscription_path = PubSub().subscriber.subscription_path(env('GOOGLE_CLOUD_PROJECT'),
                                                              subscription_name)
    topic_path = PubSub().publisher.topic_path(env('GOOGLE_CLOUD_PROJECT'),
                                               topic)
    _assert_subscription(subscription_path,
                         topic_path,
                         PubSub().publisher,
                         PubSub().subscriber)

    subscription = PubSub().subscriber.subscribe(subscription_path)

    return Subscription(subscription)


def get_next(subscription):
    return subscription.get_next()

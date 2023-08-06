import threading

import redis



class Listener(threading.Thread):

    def __init__(self, channel, manager):
        self.manager = manager
        threading.Thread.__init__(self)
        self.channel = channel
        self.listener = redis.Redis().pubsub()
        self.listener.subscribe(channel)

    def stage_event(self, ievent):
        with threading.Lock():
            self.manager.stage_ievent(self.channel, ievent)

    def run(self):
        for item in self.listener.listen():
            if item['data'] == "KILL":
                self.listener.unsubscribe()
                break
            if item['type'] == 'message':
                self.stage_event(item)

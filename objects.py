import redis
from messages import JobServer

class Listener(object):
    def __init__(self):
        self.redis = redis.Redis()
        self.job_server = JobServer()
        self.job_server.listen()

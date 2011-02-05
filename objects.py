import json
import redis
from messages import JobServer

redis = redis.Redis()

class Listener(object):
    def __init__(self, channel = "system"):
        self.job_server = JobServer()
        self.job_server.listen(channel=channel, executor=self.system)
        self.channel = channel

    def system(self, jobdata):
        # Do something with the job.
        if jobdata["data"]["job"] == "create":
            obj_id = redis.incr("system:object_id")
            payload = jobdata["data"]["payload"]
            redis.set("object:{0}".format(obj_id), json.dumps(payload))
        # Return a jid on success or deferred fail on failure.
        return jobdata["jid"]

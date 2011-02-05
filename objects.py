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
        data = json.loads(jobdata["data"])
        # Do something with the job.
        if data["job"] == "create":
            obj_id = redis.incr("system:object_id")
            payload = data["payload"]
            redis.set("object:{0}".format(obj_id), json.dumps(payload))
        # Return a jid on success or deferred fail on failure.
        return jobdata["jid"]

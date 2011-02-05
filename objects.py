import json
from pymongo import Connection
from messages import JobServer

mongo = Connection()
mdb = mongo.QOO
objects = mdb.objects

class Listener(object):
    def __init__(self, channel = "system"):
        self.job_server = JobServer()
        self.job_server.listen(channel=channel, executor=self.system)
        self.channel = channel

    def system(self, jobdata):
        data = json.loads(jobdata["data"])
        # Do something with the job.
        if data["job"] == "create":
            payload = data["payload"]
            objects.insert(payload)
        # Return a jid on success or deferred fail on failure.
        return jobdata["jid"]

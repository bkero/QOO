import beanstalk
from twisted.internet import reactor, protocol
from twisted.python import log
import json

LOG = 1

def jobCall(bs, channel, job_dict):
    bs.use(channel)
    d = bs.put(json.dumps(job_dict))
    if LOG > 0:
        d.addCallback(
            lambda x: log.msg("Queued job: %s\n" % `x`))

class JobServer(object):
    def __init__(self):
        cc = protocol.ClientCreator(reactor,
                                    beanstalk.twisted_client.Beanstalk)
        self.deferred = cc.connectTCP("localhost", 11300)

    def add(self, job, channel = "system", **kwargs):
        self.deferred.addCallback(jobCall, channel, {"job":job, "payload":kwargs})

    def createObject(self, class_name, name):
        self.add("create", type=class_name, name=name)

    def runVerb(self, obj_id, verb, **kwargs):
        self.add("do", channel = obj_id, verb = verb, kwargs = kwargs)

    def setProperty(self, obj_id, prop, value):
        self.add("set", channel = obj_id, prop = prop, value = value)

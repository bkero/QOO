import beanstalk
from twisted.internet import reactor, protocol
from twisted.python import log
import json

LOG = 1

def jobCall(bs, job_dict):
    bs.use("qoo")
    d = bs.put(json.dumps(job_dict))
    if LOG > 0:
        d.addCallback(
            lambda x: log.msg("Queued job: %s\n" % `x`))

class JobServer(object):
    def __init__(self):
        cc = protocol.ClientCreator(reactor,
                                    beanstalk.twisted_client.Beanstalk)
        self.deferred = cc.connectTCP("localhost", 11300)

    def add(self, job, **kwargs):
        self.deferred.addCallback(jobCall, {"job":job, "payload":kwargs})

import beanstalk
from twisted.internet import protocol
from twisted.python import log

LOG = 1

def jobCall(bs, job_dict):
    bs.use("qoo")
    d = bs.put(job_dict)
    if LOG > 0:
        d.addCallback(
            lambda x: log.msg("Queued job: %s\n" % `x`))

class JobServer(object):
    def __init__(self, reactor):
        cc = protocol.ClientCreator(reactor,
                                    beanstalk.twisted_client.Beanstalk)
        self.deferred = cc.connectTCP("localhost", 11300)

    def add(job, **kwargs):
        d.addCallback(jobCall, {"job":job, "payload":kwargs})

import beanstalk
from twisted.internet import protocol

def jobCall(bs, job_dict):
    bs.use("qoo")
    d = bs.put(job_dict)
    if LOG > 0:
        d.addCallback(
            lambda x: log.msg("Queued job: %s\n" % `x`))

def job(d, job, **kwargs):
    d.addCallback(jobCall, {"job":job, "payload":kwargs})

def connect(reactor):
    cc = protocol.ClientCreator(reactor,
                                beanstalk.twisted_client.Beanstalk)
    d = cc.connectTCP("localhost", 11300)
    return d

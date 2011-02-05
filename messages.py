import beanstalk
from twisted.internet import reactor, protocol, task
from twisted.python import log
import json

LOG = 1

def start(jobdata, bs):
    bs.touch(jobdata['jid'])
    if LOG:
        log.msg(jobdata)
    return jobdata

def stop(jid, bs):
    bs.delete(jid)

def executionGenerator(bs, executor):
    while True:
        if LOG:
            log.msg("Waiting for job...")
        job = bs.reserve()
        job.addCallback(start, bs)
        if executor:
            job.addCallback(executor)
        job.addCallback(stop, bs)
        yield job

def jobListen(bs, channel, executor):
    bs.watch(channel)
    bs.ignore("default")
    
    coop = task.Cooperator()
    coop.coiterate(executionGenerator(bs, executor))

def jobCall(bs, channel, job_dict):
    bs.use(channel)
    d = bs.put(json.dumps(job_dict))
    if LOG:
        d.addCallback(
            lambda x: log.msg("Queued job: %s\n" % `x`))

class JobServer(object):
    def __init__(self):
        cc = protocol.ClientCreator(reactor,
                                    beanstalk.twisted_client.Beanstalk)
        self.deferred = cc.connectTCP("localhost", 11300)

    def add(self, job, channel = "system", **kwargs):
        self.deferred.addCallback(jobCall, channel, {"job":job, "payload":kwargs})

    def listen(self, channel = "system", executor=None):
        self.deferred.addCallback(jobListen, channel, executor)

    def createObject(self, class_name, name):
        self.add("create", type=class_name, name=name)

    def programVerb(self, obj_id, verb, code):
        self.add("program", channel = obj_id, verb = verb, code = code)

    def runVerb(self, obj_id, verb, **kwargs):
        self.add("do", channel = obj_id, verb = verb, kwargs = kwargs)

    def setProperty(self, obj_id, prop, value):
        self.add("set", channel = obj_id, prop = prop, value = value)

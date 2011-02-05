import beanstalk
from twisted.internet import reactor, protocol, task
from twisted.python import log
import json

import objects

LOG = 1

def executor(v, bs):
    bs.touch(jobdata['jid'])
    if LOG:
        log.msg(v)
    bs.delete(jobdata['jid'])

def executionGenerator(bs):
    while True:
        if LOG:
            log.msg("Waiting for job...")
        job = bs.reserve()
        job.addCallback(executor, bs)
        yield job

def jobListen(bs, channel):
    bs.watch(channel)
    bs.ignore("default")
    
    coop = task.Cooperator()
    coop.coiterate(executionGenerator(bs))

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

    def listen(self, channel = "system"):
        self.deferred.addCallback(jobListen, channel)

    def createObject(self, class_name, name):
        self.add("create", type=class_name, name=name)

    def programVerb(self, obj_id, verb, code):
        self.add("program", channel = obj_id, verb = verb, code = code)

    def runVerb(self, obj_id, verb, **kwargs):
        self.add("do", channel = obj_id, verb = verb, kwargs = kwargs)

    def setProperty(self, obj_id, prop, value):
        self.add("set", channel = obj_id, prop = prop, value = value)

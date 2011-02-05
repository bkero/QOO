#!/usr/bin/env python
import sys
from twisted.internet import reactor
from twisted.python import log
from twisted.web.server import Site
from twisted.web.resource import Resource

from messages import JobServer
from objects import Listener

class VerbCallResource(Resource):
    isLeaf = True
    def __init__(self, obj, verb):
        Resource.__init__(self)
        self.obj = obj
        self.verb = verb

    def render_GET(self, request):
        job_server.runVerb(self.obj, self.verb, request.args)
        return "<html><body>Running {0}.{1}({2}).</body></html>".format(self.obj, self.verb, request.args)

class VerbResource(Resource):
    def __init__(self, obj):
        Resource.__init__(self)
        self.obj = obj

    def render_GET(self, request):
        # something like obj.listverbs()
        return "<html><body>#list of verbs#</body></html>"

    def getChild(self, name, request):
        return VerbCallResource(self.obj, name)

class ObjectResource(Resource):
    def __init__(self, name):
        Resource.__init__(self)
        self.name = name
        self.obj = None # load(name) or load(id) or something

    def render_GET(self, request):
        return "<html><body>#list of verbs#</body></html>"

    def getChild(self, name, request):
        return VerbResource(self.obj)

class ObjectParent(Resource):
    def getChild(self, name, request):
        return ObjectResource(name)

class AdminResource(Resource):
    def __init__(self, call):
        Resource.__init__(self)
        self.call = call

    def render_GET(self, request):
        if self.call == "install":
            job_server.createObject("object", "root")
        return "<html><body>{0}: running</body></html>".format(self.call)

class AdminParent(Resource):
    def getChild(self, name, request):
        return AdminResource(name)

class QooRoot(Resource):
    def render_GET(self, request):
        return "<html><body>Qoo server.</body></html>"

if __name__ == "__main__":
    log.startLogging(sys.stderr)
    job_server = JobServer()
    listener = Listener()
    root = QooRoot()
    root.putChild("obj", ObjectParent())
    root.putChild("admin", AdminParent())
    factory = Site(root)
    reactor.listenTCP(8880, factory)
    reactor.run()

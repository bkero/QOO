#!/usr/bin/env python
from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.resource import Resource

class VerbCallResource(Resource):
    isLeaf = True
    def __init__(self, obj, verb):
        Resource.__init__(self)
        self.obj = obj
        self.verb = verb

    def render_GET(self, request):
        return "<html><body>VERB OUTPUT!</body></html>"

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

class QooRoot(Resource):
    def render_GET(self, request):
        return "<html><body>Qoo server.</body></html>"

    def getChild(self, name, request):
        return ObjectResource(name)

root = QooRoot()
factory = Site(root)
reactor.listenTCP(8880, factory)
reactor.run()

import xmlrpclib
from worldstate import WorldState

class French75Client():

    def __init__(self, ip):
        print ip
        self.world = WorldState.Instance()
        self.server = xmlrpclib.ServerProxy('http://' + ip + ':8000')

    def perform_actions(self):
        pass

    def list_actions(self):
        print self.server.system.listMethods()

    def start_partner_client(self):
        self.server.start_client("dog")

    def test(self):
        print self.server.test()

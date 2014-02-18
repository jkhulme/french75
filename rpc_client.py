import xmlrpclib
from worldstate import WorldState

class French75Client():

    def __init__(self, ip, port):
        print "Starting client to connect on port", port
        self.world = WorldState.Instance()
        self.server = xmlrpclib.ServerProxy('http://' + ip + ':' + str(port))

    def perform_actions(self):
        pass

    def list_actions(self):
        print self.server.system.listMethods()

    def start_partner_client(self, ip):
        self.server.start_client(ip)

    def test(self):
        print self.server.test()

    def request_session(self):
        data = self.server.get_session_dict()
        self.world.unpickle_session(data)
        print self.world.session_dict

from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
from rpc_client import French75Client
from worldstate import WorldState
from threading import Thread

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

class French75Server():

    def __init__(self, port):
        print "starting server on port", port
        self.world = WorldState.Instance()
        self.server = SimpleXMLRPCServer(("0.0.0.0", port), requestHandler=RequestHandler, allow_none=True)
        self.server.register_introspection_functions()
        self.server.register_function(self.start_client, 'start_client')
        self.server.register_function(self.test, 'test')
        self.server.register_function(self.get_session_dict, 'get_session_dict')

        self.server.serve_forever()

    def start_client(self, ip):
        client_thread = Thread(target=self.run_client, args=(ip,))
        client_thread.start()
        return True

    def run_client(self, ip):
        self.world.client = French75Client(ip, 8001)
        self.world.client.test()

    def test(self):
        return "hello world"

    def get_session_dict(self):
        return self.world.pickle_session()

from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

class MyFuncs:
    def div(self, x, y):
        return x // y


class French75Server():

    def __init__(self):
        self.server = SimpleXMLRPCServer(("0.0.0.0", 8000), requestHandler=RequestHandler)
        self.server.register_introspection_functions()
        self.server.register_function(pow)
        self.server.register_function(self.adder_function, 'add')
        self.server.register_instance(MyFuncs())

        self.server.serve_forever()

    def adder_function(self, x,y):
        return x + y


if __name__ == "__main__":
    x = French75Server()

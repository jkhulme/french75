import xmlrpclib


class French75Client():

    def __init__(self, ip):
        self.server = xmlrpclib.ServerProxy('http://' + ip + ':8000')

    def perform_actions(self):
        print self.server.pow(2,3)
        print self.server.add(2,3)
        print self.server.div(5,2)

    def list_actions(self):
        print self.server.system.listMethods()


if __name__ == "__main__":
    x = French75Client()
    x.perform_actions()

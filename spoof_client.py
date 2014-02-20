import xmlrpclib
import pickle
from annotation import Annotation
import sys

class SpoofClient():

    def __init__(self, ip, port):
        print "Starting client to connect on port", port
        self.server = xmlrpclib.ServerProxy('http://' + ip + ':' + str(port))

    def add_annotation(self, annotation):
        self.server.add_annotation(pickle.dumps(annotation))

if __name__ == "__main__":
    client = SpoofClient(sys.argv[1], sys.argv[2])
    client.add_annotation(Annotation(1, (0.5, 0.5), (1.5, 1.5)))

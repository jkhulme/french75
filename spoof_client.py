import xmlrpclib
import pickle
from annotation import Annotation
import sys

class SpoofClient():

    """
    Was used to provide a testing client on systems where I couldn't run
    the program
    """

    def __init__(self, ip, port):
        print "ip", ip
        print "port", port
        self.server = xmlrpclib.ServerProxy('http://' + ip + ':' + str(port))

    def add_annotation(self, annotation):
        self.server.add_annotation(pickle.dumps(annotation))

if __name__ == "__main__":
    client = SpoofClient(sys.argv[1], sys.argv[2])
    client.add_annotation(Annotation(1, (2000, 2000), (9000, 9000)))
    print "done"

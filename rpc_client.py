import xmlrpclib
from worldstate import WorldState
from utils import refresh_plot
import pickle

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
        return True

    def add_annotation(self, annotation):
        self.server.add_annotation(pickle.dumps(annotation))

    def update_annotation(self, a_id, text):
        self.server.update_annotation(a_id, text)

    def launch_large_plot(self):
        self.server.launch_large_plot()

    def update_legend(self, line, file_key, species_key):
        self.server.update_legend(line, file_key, species_key)

    def reset_session(self):
        self.server.reset_session()

    def change_cursor(self, cursor):
        self.server.change_cursor(cursor)

    def undo(self):
        self.server.undo()

    def redo(self):
        self.server.redo()

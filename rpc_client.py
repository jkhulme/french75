import xmlrpclib
from worldstate import WorldState
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
        self.world.lamport_clock += 1
        self.server.test(self.world.lamport_clock)

    def request_session(self):
        """
        works
        """
        data = self.server.get_session_dict()
        self.world.unpickle_session(data)
        self.world.push_state()
        return True

    def add_annotation(self, annotation):
        """
        works
        """
        self.server.add_annotation(self.world.lamport_clock, pickle.dumps(annotation))

    def update_annotation(self, a_id, text):
        """
        works
        """
        self.server.update_annotation(self.world.lamport_clock, pickle.dumps(a_id), pickle.dumps(text))

    def launch_large_plot(self):
        """
        works
        """
        self.server.launch_large_plot()

    def close_large_plot(self):
        """
        works
        """
        self.server.close_large_plot()

    def update_legend(self, line, file_key, species_key):
        """
        works
        """
        self.server.update_legend(self.world.lamport_clock, pickle.dumps((line, file_key, species_key)))

    def reset_session(self):
        self.server.reset_session()

    def undo(self):
        self.server.undo()

    def redo(self):
        self.server.redo()

    def delete_anime_annotation(self, a_id):
        self.server.delete_anime_annotation(self.world.lamport_clock, a_id)

    def add_anime_annotation(self, (key, annotation)):
        self.server.add_anime_annotation(self.world.lamport_clock, pickle.dumps((key, annotation)))

    def delete_annotation(self, a_id):
        """
        works
        """
        self.server.delete_annotation(self.world.lamport_clock, pickle.dumps(a_id))

    def toggle_param(self, param, value):
        self.server.toggle_param(self.world.lamport_clock, param, value)

    def play_animation(self):
        self.server.play_animation(self.world.lamport_clock)

    def set_clock(self):
        self.server.set_clock(self.world.lamport_clock, pickle.dumps(self.world.session_dict['clock']))

    def switch_animation(self, n):
        self.server.switch_animation(self.world.lamport_clock, n)

    def change_animation_species(self, n):
        self.server.change_animation_species(self.world.lamport_clock, n)

    def change_animation_file(self, n):
        self.server.change_animation_file(self.world.lamport_clock, n)

import xmlrpclib
from worldstate import WorldState
import pickle
from threading import Thread


class French75Client():

    def __init__(self, ip, port):
        print "Starting client to connect on port", port
        #WorldState.Instance() = WorldState.Instance()
        self.server = xmlrpclib.ServerProxy('http://' + ip + ':' + str(port))

    def perform_actions(self):
        pass

    def list_actions(self):
        print self.server.system.listMethods()

    def start_partner_client(self, ip):
        self.server.start_client(ip)

    def test(self):
        WorldState.Instance().lamport_clock += 1
        self.server.test(WorldState.Instance().lamport_clock)

    def request_session(self):
        """
        works
        """
        data = self.server.get_session_dict()
        WorldState.Instance().unpickle_session(data)
        WorldState.Instance().push_state()
        return True

    def add_annotation(self, annotation):
        """
        works
        """
        new_clock = self.server.add_annotation(WorldState.Instance().lamport_clock, pickle.dumps(annotation))
        if new_clock is not None:
            WorldState.Instance().lamport_clock = new_clock

    def update_annotation(self, a_id, text):
        """
        works
        """
        self.server.update_annotation(WorldState.Instance().lamport_clock, pickle.dumps(a_id), pickle.dumps(text))

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
        self.server.update_legend(WorldState.Instance().lamport_clock, pickle.dumps((line, file_key, species_key)))

    def reset_session(self):
        self.server.reset_session()

    def undo(self):
        self.server.undo()

    def redo(self):
        self.server.redo()

    def delete_anime_annotation(self, a_id):
        self.server.delete_anime_annotation(WorldState.Instance().lamport_clock, a_id)

    def add_anime_annotation(self, (key, annotation)):
        thread = Thread(target=self.non_blocking, args=(WorldState.Instance().lamport_clock, pickle.dumps((key, annotation)),), kwargs={'name':self.server.add_anime_annotation})
        thread.start()
        #self.server.add_anime_annotation(WorldState.Instance().lamport_clock, pickle.dumps((key, annotation)))

    def non_blocking(self, *args, **kwargs):
        kwargs['name'](*args)

    def delete_annotation(self, a_id):
        """
        works
        """
        self.server.delete_annotation(WorldState.Instance().lamport_clock, pickle.dumps(a_id))

    def toggle_param(self, param, value):
        self.server.toggle_param(WorldState.Instance().lamport_clock, param, value)

    def play_animation(self):
        self.server.play_animation(WorldState.Instance().lamport_clock)

    def set_clock(self):
        self.server.set_clock(WorldState.Instance().lamport_clock, pickle.dumps(WorldState.Instance().session_dict['clock']))

    def switch_animation(self, n):
        self.server.switch_animation(WorldState.Instance().lamport_clock, n)

    def change_animation_species(self, n):
        self.server.change_animation_species(WorldState.Instance().lamport_clock, n)

    def change_animation_file(self, n):
        self.server.change_animation_file(WorldState.Instance().lamport_clock, n)

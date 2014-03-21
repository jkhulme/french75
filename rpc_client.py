import xmlrpclib
from worldstate import WorldState
import pickle
from threading import Thread


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
        thread = Thread(target=self.non_blocking, args=(self.world.lamport_clock, pickle.dumps(annotation),), kwargs={'name':self.server.add_annotation})
        thread.start()
        #if new_clock is not None:
        #    self.world.lamport_clock = new_clock

    def update_annotation(self, a_id, text):
        """
        works
        """
        thread = Thread(target=self.non_blocking, args=(self.world.lamport_clock, pickle.dumps(a_id), pickle.dumps(text),), kwargs={'name':self.server.update_annotation})
        thread.start()

    def launch_large_plot(self):
        """
        works
        """
        thread = Thread(target=self.non_blocking, args=(), kwargs={'name':self.server.launch_large_plot})
        thread.start()

    def close_large_plot(self):
        """
        works
        """
        thread = Thread(target=self.non_blocking, args=(), kwargs={'name':self.server.close_large_plot})
        thread.start()

    def update_legend(self, line, file_key, species_key):
        """
        works
        """
        thread = Thread(target=self.non_blocking, args=(self.world.lamport_clock, pickle.dumps((line, file_key, species_key)),), kwargs={'name':self.server.update_legend})
        thread.start()


    def reset_session(self):
        thread = Thread(target=self.non_blocking, args=(), kwargs={'name':self.server.reset_session})
        thread.start()

    def undo(self):
        thread = Thread(target=self.non_blocking, args=(), kwargs={'name':self.server.undo})
        thread.start()

    def redo(self):
        thread = Thread(target=self.non_blocking, args=(), kwargs={'name':self.server.redo})
        thread.start()

    def delete_anime_annotation(self, a_id):
        thread = Thread(target=self.non_blocking, args=(self.world.lamport_clock, a_id,), kwargs={'name':self.server.delete_anime_annotation})
        thread.start()

    def add_anime_annotation(self, (key, annotation)):
        thread = Thread(target=self.non_blocking, args=(self.world.lamport_clock, pickle.dumps((key, annotation)),), kwargs={'name':self.server.add_anime_annotation})
        thread.start()
        #self.server.add_anime_annotation(self.world.lamport_clock, pickle.dumps((key, annotation)))

    def non_blocking(self, *args, **kwargs):
        kwargs['name'](*args)

    def delete_annotation(self, a_id):
        """
        works
        """
        thread = Thread(target=self.non_blocking, args=(self.world.lamport_clock, pickle.dumps(a_id),), kwargs={'name':self.server.delete_annotation})
        thread.start()

    def toggle_param(self, param, value):
        thread = Thread(target=self.non_blocking, args=(self.world.lamport_clock, param, value,), kwargs={'name':self.server.toggle_param})
        thread.start()

    def play_animation(self):
        thread = Thread(target=self.non_blocking, args=(self.world.lamport_clock,), kwargs={'name':self.server.play_animation})
        thread.start()

    def set_clock(self):
        thread = Thread(target=self.non_blocking, args=(self.world.lamport_clock, pickle.dumps(self.world.session_dict['clock']),), kwargs={'name':self.server.set_clock})
        thread.start()

    def switch_animation(self, n):
        thread = Thread(target=self.non_blocking, args=(self.world.lamport_clock, n,), kwargs={'name':self.server.switch_animation})
        thread.start()

    def change_animation_species(self, n):
        thread = Thread(target=self.non_blocking, args=(self.world.lamport_clock, n,), kwargs={'name':self.server.change_animation_species})
        thread.start()

    def change_animation_file(self, n):
        thread = Thread(target=self.non_blocking, args=(self.world.lamport_clock, n,), kwargs={'name':self.server.change_animation_file})
        thread.start()

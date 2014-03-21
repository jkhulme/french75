from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
from rpc_client import French75Client
from worldstate import WorldState
from threading import Thread
from utils import refresh_plot
import pickle
from large_plot import LargePlotDialog

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

class French75Server():

    def __init__(self, port):
        print "starting server on port", port
        self.port = port
        self.world = WorldState.Instance()
        self.server = SimpleXMLRPCServer(("0.0.0.0", port), requestHandler=RequestHandler, allow_none=True)
        self.server.register_introspection_functions()
        self.server.register_function(self.start_client, 'start_client')
        self.server.register_function(self.test, 'test')
        self.server.register_function(self.get_session_dict, 'get_session_dict')
        self.server.register_function(self.add_annotation, 'add_annotation')
        self.server.register_function(self.update_annotation, 'update_annotation')
        self.server.register_function(self.launch_large_plot, 'launch_large_plot')
        self.server.register_function(self.update_legend, 'update_legend')
        self.server.register_function(self.reset_session, 'reset_session')
        self.server.register_function(self.undo, 'undo')
        self.server.register_function(self.redo, 'redo')
        self.server.register_function(self.delete_anime_annotation, 'delete_anime_annotation')
        self.server.register_function(self.delete_annotation, 'delete_annotation')
        self.server.register_function(self.toggle_param, 'toggle_param')
        self.server.register_function(self.close_large_plot, 'close_large_plot')
        self.server.register_function(self.add_anime_annotation, 'add_anime_annotation')
        self.server.register_function(self.play_animation, 'play_animation')
        self.server.register_function(self.set_clock, 'set_clock')
        self.server.register_function(self.switch_animation, 'switch_animation')
        self.server.register_function(self.change_animation_species, 'change_animation_species')
        self.server.register_function(self.change_animation_file, 'change_animation_file')

        self.server.serve_forever()

    def start_client(self, ip):
        client_thread = Thread(target=self.run_client, args=(ip,))
        client_thread.start()
        return True

    def run_client(self, ip):
        self.world.client = French75Client(ip, 8001)

    def test(self, clock):
        self.world.lamport_clock = max(clock, self.world.lamport_clock) + 1
        print clock

    def get_session_dict(self):
        return self.world.pickle_session()

    def add_annotation(self, clock, annotation):
        """
        Works
        """
        old_clock = clock
        if self.world.lamport_clock == clock:
            clock += 1
        self.world.push_state()
        self.world.lamport_clock = max(self.world.lamport_clock, clock) + 1
        self.world.session_dict['annotations'].append(pickle.loads(annotation))
        self.world.reorder(clock)
        refresh_plot()
        if old_clock != clock:
            return clock
        else:
            None

    def update_annotation(self, clock, a_id, text):
        """
        works
        """
        old_clock = clock
        if self.world.lamport_clock == clock:
            clock += 1
        self.world.push_state()
        self.world.lamport_clock = max(self.world.lamport_clock, clock) + 1
        text = pickle.loads(text)
        a_id = pickle.loads(a_id)
        self.world.update_annotation_text(a_id, text)
        self.world.reorder(clock)
        refresh_plot()
        if old_clock != clock:
            return clock
        else:
            None

    def launch_large_plot(self):
        """
        works
        """
        self.large_plot = LargePlotDialog(None, title='Big Plot')
        self.large_plot.ShowModal()
        self.large_plot.Destroy()

    def close_large_plot(self):
        """
        works
        """
        self.large_plot.Destroy()

    def update_legend(self, clock, update_tuple):
        """
        works
        """
        old_clock = clock
        if self.world.lamport_clock == clock:
            clock += 1
        self.world.push_state()
        self.world.lamport_clock = max(self.world.lamport_clock, clock) + 1
        line, file_key, species_key = pickle.loads(update_tuple)
        self.world.session_dict['lines'][file_key][species_key] = line
        self.world.legend.draw_legend()
        self.world.legend.legend_panel.Refresh()
        self.world.refresh_plot()
        self.world.reorder(clock)
        refresh_plot()
        if old_clock != clock:
            return clock
        else:
            None

    def reset_session(self):
        self.world.reset_session()

    def undo(self):
        self.world.undo()

    def redo(self):
        self.world.redo()

    def delete_anime_annotation(self, clock, a_id):
        old_clock = clock
        if self.world.lamport_clock == clock:
            clock += 1
        self.world.push_state()
        self.world.lamport_clock = max(self.world.lamport_clock, clock) + 1
        self.world.delete_anime_annotation(a_id)
        self.world.reorder(clock)
        refresh_plot()
        if old_clock != clock:
            return clock
        else:
            None

    def delete_annotation(self, clock, a_id):
        """
        works
        """
        old_clock = clock
        if self.world.lamport_clock == clock:
            clock += 1
        self.world.push_state()
        self.world.lamport_clock = max(self.world.lamport_clock, clock) + 1
        self.world.delete_annotation(pickle.loads(a_id))
        self.world.reorder(clock)
        refresh_plot()
        if old_clock != clock:
            return clock
        else:
            None

    def toggle_param(self, clock, param, value):
        old_clock = clock
        if self.world.lamport_clock == clock:
            clock += 1
        self.world.push_state()
        self.world.lamport_clock = max(self.world.lamport_clock, clock) + 1
        self.world.session_dict[param] = value
        self.world.reorder(clock)
        refresh_plot()
        if old_clock != clock:
            return clock
        else:
            None

    def add_anime_annotation(self, clock, annotation_tuple):
        old_clock = clock
        if self.world.lamport_clock == clock:
            clock += 1
        self.world.push_state()
        self.world.lamport_clock = max(self.world.lamport_clock, clock) + 1
        idx, annotation = pickle.loads(annotation_tuple)
        self.world.add_anime_annotation(idx, annotation)
        self.world.reorder(clock)
        refresh_plot()
        if old_clock != clock:
            return clock
        else:
            None

    def play_animation(self, clock):
        old_clock = clock
        if self.world.lamport_clock == clock:
            clock += 1
        self.world.push_state()
        self.world.lamport_clock = max(self.world.lamport_clock, clock) + 1
        self.world.play_animation()
        self.world.reorder(clock)
        refresh_plot()
        if old_clock != clock:
            return clock
        else:
            None

    def set_clock(self, clock, time):
        old_clock = clock
        if self.world.lamport_clock == clock:
            clock += 1
        self.world.push_state()
        self.world.lamport_clock = max(self.world.lamport_clock, clock) + 1
        self.world.set_time(pickle.loads(time))
        self.world.reorder(clock)
        refresh_plot()
        if old_clock != clock:
            return clock
        else:
            None

    def switch_animation(self, clock, n):
        old_clock = clock
        if self.world.lamport_clock == clock:
            clock += 1
        self.world.push_state()
        self.world.lamport_clock = max(self.world.lamport_clock, clock) + 1
        self.world.switch_animation(n)
        self.world.reorder(clock)
        refresh_plot()
        if old_clock != clock:
            return clock
        else:
            None

    def change_animation_species(self, clock, n):
        old_clock = clock
        if self.world.lamport_clock == clock:
            clock += 1
        self.world.push_state()
        self.world.lamport_clock = max(self.world.lamport_clock, clock) + 1
        self.world.create_cell_segments_by_file(n)
        self.world.reorder(clock)
        refresh_plot()
        if old_clock != clock:
            return clock
        else:
            None
    def change_animation_file(self, clock, n):
        old_clock = clock
        if self.world.lamport_clock == clock:
            clock += 1
        self.world.push_state()
        self.world.lamport_clock = max(self.world.lamport_clock, clock) + 1
        self.world.create_cell_segments_by_species(n)
        self.world.reorder(clock)
        refresh_plot()
        if old_clock != clock:
            return clock
        else:
            None

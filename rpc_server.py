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
        self.world.client.test()

    def test(self):
        return "hello world"

    def get_session_dict(self):
        return self.world.pickle_session()

    def add_annotation(self, annotation):
        """
        Works
        """
        self.world.session_dict['annotations'].append(pickle.loads(annotation))
        self.world.push_state()
        refresh_plot()
        return True

    def update_annotation(self, a_id, text):
        """
        works
        """
        text = pickle.loads(text)
        a_id = pickle.loads(a_id)
        self.world.update_annotation_text(a_id, text)

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

    def update_legend(self, update_tuple):
        """
        works
        """
        line, file_key, species_key = pickle.loads(update_tuple)
        self.world.session_dict['lines'][file_key][species_key] = line
        self.world.legend.draw_legend()
        self.world.legend.legend_panel.Refresh()
        self.world.refresh_plot()

    def reset_session(self):
        self.world.reset_session()

    def undo(self):
        self.world.undo()

    def redo(self):
        self.world.redo()

    def delete_anime_annotation(self, a_id):
        self.world.delete_anime_annotation(a_id)

    def delete_annotation(self, a_id):
        """
        works
        """
        self.world.delete_annotation(pickle.loads(a_id))

    def toggle_param(self, param, value):
        self.world.session_dict[param] = value
        refresh_plot()

    def add_anime_annotation(self, annotation_tuple):
        idx, annotation = pickle.loads(annotation_tuple)
        self.world.add_anime_annotation(idx, annotation)

    def play_animation(self):
        self.world.play_animation()

    def set_clock(self, time):
        self.world.set_time(pickle.loads(time))

    def switch_animation(self, by_species):
        self.world.switch_animation()

    def change_animation_species(self):
        self.world.create_cell_segments_by_file()

    def change_animation_file(self):
        self.world.create_cell_segments_by_species()

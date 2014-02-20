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
        self.server.register_function(self.change_cursor, 'change_cursor')
        self.server.register_function(self.undo, 'undo')
        self.server.register_function(self.redo, 'redo')
        self.server.register_function(self.delete_anime_annotation, 'delete_anime_annotation')
        self.server.register_function(self.delete_annotation, 'delete_annotation')
        self.server.register_function(self.toggle_param, 'toggle_param')
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
        print "before", self.world.session_dict['annotations']
        self.world.session_dict['annotations'].append(pickle.loads(annotation))
        print "after", self.world.session_dict['annotations']
        refresh_plot()
        return True

    def update_annotation(self, a_id, text):
        for annotation in self.world.session_dict['annotations']:
            if annotation.id == a_id:
                annotation.text = text
                break
        refresh_plot()

    def launch_large_plot(self):
        large_plot = LargePlotDialog(None, title='Big Plot')
        large_plot.ShowModal()
        large_plot.Destroy()

    def update_legend(self, line, file_key, species_key):
        self.world.session_dict['lines'][file_key][species_key]
        self.world.legend.draw_legend()
        self.world.legend.legend_panel.Refresh()

    def reset_session(self):
        self.world.reset_session()

    def change_cursor(self, cursor):
        self.world.change_cursor(cursor)

    def undo(self):
        self.world.undo()

    def redo(self):
        self.world.redo()

    def delete_anime_annotation(self, a_id):
        for key in self.world.session_dict['anime_annotations'].keys():
            new_annotation_list = [ann for ann in self.world.session_dict['anime_annotations'][key] if int(a_id) != int(ann.a_id)]
            self.world.session_dict['anime_annotations'][key] = new_annotation_list
        #self.anime_annotations_list.Delete(selected)
        #self.world.client.delete_anime_annotation(a_id)
        for panel in self.world.panels:
            panel.Refresh()

    def delete_annotation(self, a_id):
        new_annotation_list = [annotation for annotation in self.world.session_dict['annotations'] if annotation != self.selected_annotation]
        self.world.session_dict['annotations'] = new_annotation_list

    def toggle_param(self, param, value):
        self.world.session_dict[param] = value
        refresh_plot()

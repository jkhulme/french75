from copy import deepcopy
import inspect


class UndoStack:

    """
    Basic stack really, returns a deepcopy due to annoying dict copying
    """

    def __init__(self):
        self.stack = []
        self.redo_stack = []

    def undo_push(self, item):
        #print 'caller name:', inspect.stack()[1][3]
        self.stack.insert(0, deepcopy(item))
        self.history()

    def undo_pop(self):
        self.redo_push(deepcopy(self.stack.pop(0)))
        return deepcopy(self.stack[0][1])

    def redo_push(self, item):
        self.redo_stack.insert(0, deepcopy(item))

    def redo_pop(self):
        item = deepcopy(self.redo_stack.pop(0))
        self.undo_push(deepcopy(item))
        return deepcopy(item[1])

    def __len__(self):
        return len(self.stack)

    def reorder(self):
        self.stack.sort()
        self.stack.reverse()
        return deepcopy(self.stack.pop(0)[1])

    def timestamps(self):
        undo = [clock for clock, session in self.stack]
        redo = [clock for clock, session in self.redo_stack]
        #print "Undo:", undo
        #print "Redo:", redo

    def history(self):
        num_annotations = [len(session['annotations']) for clock, session in self.stack]
        #print num_annotations

from copy import deepcopy


class UndoStack:

    """
    Basic stack really, returns a deepcopy due to annoying dict copying
    will also probably have the redo stack inside of it <- TODO
    """

    def __init__(self):
        self.stack = []
        self.redo_stack = []

    def undo_push(self, item):
        print len(self.stack)
        self.stack.insert(0, item)
        print len(self.stack)

    def undo_pop(self):
        self.redo_push(deepcopy(self.stack.pop(0)))
        return deepcopy(self.stack[0][1])

    def redo_push(self, item):
        self.redo_stack.insert(0, item)

    def redo_pop(self):
        item = deepcopy(self.redo_stack.pop(0)[1])
        self.undo_push(item)
        return item

    def __len__(self):
        return len(self.stack)

    def reorder(self):
        print [clock for clock, stack in self.stack]
        self.stack.sort()
        self.stack.reverse()
        print [clock for clock, stack in self.stack]
        return deepcopy(self.stack.pop(0)[1])

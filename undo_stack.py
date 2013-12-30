from copy import deepcopy


class UndoStack:

    def __init__(self):
        self.stack = []

    def push(self, item):
        self.stack.insert(0, item)

    def undo_pop(self):
        self.stack.pop(0)
        return deepcopy(self.stack[0])

    def undo(self):
        return self.pop()

    def __len__(self):
        return len(self.stack)

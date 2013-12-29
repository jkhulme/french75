class UndoStack:

    def __init__(self):
        self.stack = []

    def push(self, item):
        self.stack.insert(0, item)

    def pop(self):
        return self.stack.pop(0)

    def undo(self):
        return self.pop()

    def __len__(self):
        return len(self.stack)

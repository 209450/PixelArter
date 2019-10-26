import abc


class UndoRedoManager:

    def __init__(self):
        self.undo_stack = []
        self.redo_stack = []
        self.stack_max_size = 5

    def registerSnapshot(self, snapshot):
        self._addSnapShotToMementoStack(self.undo_stack, snapshot)

    def undo(self, snapshot):
        if self.undo_stack:
            self._addSnapShotToMementoStack(self.redo_stack, snapshot)
            self.undo_stack.pop().restore()

    def redo(self, snapshot):
        if self.redo_stack:
            self._addSnapShotToMementoStack(self.undo_stack, snapshot)
            self.redo_stack.pop().restore()

    def _addSnapShotToMementoStack(self, stack, snapshot):
        if len(stack) > self.stack_max_size:
            stack.pop(0)
        stack.append(snapshot)


class Snapshot:

    @abc.abstractmethod
    def restore(self):
        pass

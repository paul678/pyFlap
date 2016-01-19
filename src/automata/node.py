from automata.nodestate import NodeState
from automata.transition import *


class Node:
    def __init__(self, name):
        self.name = name
        self._state = NodeState.NoState
        self._x = -1
        self._y = -1
        self.transitions = []

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        self._state = state

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self._y = y

    def add_transition(self, transition: Transition):
        self.transitions.append(transition)

    def remove_transition(self, transition: Transition):
        self.transitions.remove(transition)

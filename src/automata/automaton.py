import collections
import pickle

from automata.node import Node


class Automaton:
    def __init__(self):
        self.nodes = []
        self.transitionNames = []

    def is_nfa(self):

        self.transitionNames = []
        # init transition names
        for node in self.nodes:
            if node.transitions:
                for transition in node.transitions:
                    if self.transitionNames.count(transition.name) == 0:
                        self.transitionNames.append(transition.name)

        is_nfa = False

        # print all transitions
        for t in self.transitionNames:
            print(t)

        for node in self.nodes:
            if node.transitions:
                if not self.check_if_has(node.transitions):
                    is_nfa = True
        return is_nfa

    def add_node(self):
        node = Node(len(self.nodes))
        node.x = 100
        node.y = 100
        self.nodes.append(node)
        return node

    def set_node_state(self, index, new_state):
        self.nodes[int(index)].state = new_state

    def check_if_has(self, transitions):

        nodeTransitionName = [];

        for transition in transitions:
            if (self._is_name_in_transition(transition.name, transitions)):
                nodeTransitionName.append(transition.name)

        for t in nodeTransitionName:
            print(t);

        if collections.Counter(self.transitionNames) == collections.Counter(nodeTransitionName):
            return True
        return False

    def _is_name_in_transition(self, name, transitions):
        for t in transitions:
            if name == t:
                return False
        return True

    def _is_in_transition_names(self, name):
        for transition_name in self.transitionNames:
            if name == transition_name:
                return False
        return True

    def save(self, url):
        with open(url, 'wb') as output:
            pickle.dump(self.nodes, output, pickle.HIGHEST_PROTOCOL)

    def load(self, url):
        self.nodes = pickle.load(open(url, "rb"))

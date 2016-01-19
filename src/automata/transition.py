LAMBDA = "λ"


class Transition:
    def __init__(self, node, name):
        self.node = node
        self.name = name
        self.visited = False

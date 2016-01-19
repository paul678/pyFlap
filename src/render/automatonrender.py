import os
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog

from automata.automaton import Automaton
from automata.nodestate import NodeState
from automata.transition import *
from automata.transitionbind import TransitionBind
from render.quitdialog import QuitDialog
from render.inputdialog import InputDialog
from render.automatonaction import AutomatonAction

MOUSE_MOTION = "<B1-Motion>"

BUTTON_LEFT_RELEASE = "<ButtonRelease-1>"

BUTTON_LEFT_PRESS = "<ButtonPress-1>"

TAGT = "tagt"

TAGC = "tagc"

COLOR_INITIAL = "blue"
COLOR_FINAL = "red"
COLOR_NORMAL = "grey"


class AutomatonRender(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.automaton = Automaton()
        self.action = AutomatonAction.No_Action
        self.transitions = []
        self.quit_dialog = None
        # create a canvas
        self.canvas = Canvas(bg="white", width=640, height=480)
        self.canvas.pack(fill="both", expand=True)

        self._drag_data = {"x": 0, "y": 0, "item": None}

        self.init_menu()

    def init_menu(self):
        frame = Frame(self, bg='grey')
        frame.pack(side=TOP, fill=BOTH)

        menu = Menu(self, tearoff=False)
        file_menu = Menu(self, tearoff=False)
        about_menu = Menu(self, tearoff=False)
        menu.add_cascade(label="File", underline=0, menu=file_menu)
        menu.add_cascade(label="About", underline=0, menu=about_menu)
        file_menu.add_command(label="New File", underline=1, command=self.new_automaton)
        file_menu.add_command(label="Save", underline=1, command=self.save_automaton)
        file_menu.add_command(label="Load", underline=1, command=self.load_automaton)
        file_menu.add_command(label="Exit", underline=1, command=self.exit_window)
        about_menu.add_command(label="About", underline=1, command=self.about)

        self.config(menu=menu)

        cursor = Button(frame, text='Cursor', command=self.cursor_state_press, padx=20)
        cursor.pack(pady=20, padx=20, side=LEFT)

        add_state = Button(frame, text='Add state', command=self.add_state_press, padx=20)
        add_state.pack(pady=20, padx=20, side=LEFT)

        add_transition = Button(frame, text='Set transition', command=self.add_transition_press, padx=20)
        add_transition.pack(pady=20, padx=20, side=LEFT)

        set_initial = Button(frame, text='Set initial', command=self.set_initial_state_press, padx=20)
        set_initial.pack(pady=20, padx=20, side=LEFT)

        set_final = Button(frame, text='Set final', command=self.set_final_state_press, padx=20)
        set_final.pack(pady=20, padx=20, side=LEFT)

        # add_input = Button(frame, text='Add Input', command=self., padx=20)
        # add_input.pack(pady=20, padx=20, side=LEFT)

        check_dfa = Button(frame, text='Check automata', command=self.check_automaton, padx=20)
        check_dfa.pack(pady=20, padx=20, side=LEFT)

    @staticmethod
    def about():
        os.startfile("E:\\document.pdf", 'open')

    def exit_window(self):
        if self.automaton.nodes:
            self.quit_dialog = QuitDialog(self.canvas,
                                          text="Would you like to save before exiting?",
                                          buttons=["Yes", "No", "Cancel"],
                                          actions=[self.save_automaton, sys.exit, sys.exit],
                                          default=0,
                                          cancel=self.save_automaton,
                                          title="Quit dialog")
            self.quit_dialog.go()
        else:
            sys.exit(0)

    def new_automaton(self):
        self.automaton = Automaton()
        self.canvas.delete("all")

    def load_automaton(self):
        filename = filedialog.askopenfilename()
        self.canvas.delete("all")
        self.automaton.load(filename)
        self.draw_automaton()

    def check_automaton(self):
        if self.automaton.is_nfa():
            messagebox.showinfo("Automata", " The automate is NFA ")
        else:
            messagebox.showinfo("Automata", " The automate is DFA ")

    def save_automaton(self):
        save_file = filedialog.asksaveasfilename()
        self.automaton.save(save_file + ".pkl")

    def cursor_state_press(self):
        self.action = AutomatonAction.Add_State

    def add_state_press(self):
        self.action = AutomatonAction.Add_State
        node = self.automaton.add_node()
        self._draw_node(node, COLOR_NORMAL)

    def add_transition_press(self):
        self.action = AutomatonAction.Add_Transition

    def set_initial_state_press(self):
        self.action = AutomatonAction.Set_Initial

    def set_final_state_press(self):
        self.action = AutomatonAction.Set_Final

    # def add_input_press(self):

    def draw_automaton(self):
        for node in self.automaton.nodes:
            if node.state == NodeState.Initial:
                self._draw_node(node, COLOR_INITIAL)
            elif node.state == NodeState.Final:
                self._draw_node(node, COLOR_FINAL)
            else:
                self._draw_node(node, COLOR_NORMAL)
            for transition in node.transitions:
                if transition.node.name == node.name:
                    self._draw_arc(node, transition.name)
                else:
                    self._draw_line(node, transition.node, transition.name, "black")

    def _draw_node(self, node, color):
        """Create a node at the given coordinate in the given color"""
        x = node.x
        y = node.y
        self.canvas.create_oval(x - 25, y - 25, x + 25, y + 25,
                                outline="red", fill=color, tags=TAGC + str(node.name))
        self.canvas.create_text(x, y, text="q" + str(node.name), tags=TAGT + str(node.name))

        self.canvas.tag_bind(TAGC + str(node.name), BUTTON_LEFT_PRESS, self.on_node_press)
        self.canvas.tag_bind(TAGC + str(node.name), BUTTON_LEFT_RELEASE, self.on_node_release)
        self.canvas.tag_bind(TAGC + str(node.name), MOUSE_MOTION, self.on_node_move)

        self.canvas.tag_bind(TAGT + str(node.name), BUTTON_LEFT_PRESS, self.on_node_press)
        self.canvas.tag_bind(TAGT + str(node.name), BUTTON_LEFT_RELEASE, self.on_node_release)
        self.canvas.tag_bind(TAGT + str(node.name), MOUSE_MOTION, self.on_node_move)

    def _draw_line(self, first_node, second_node, transaction_name, color):
        """Create a token at the given coordinate in the given color"""
        x1 = first_node.x
        y1 = first_node.y

        x2 = second_node.x
        y2 = second_node.y

        coef = 0;
        for transaction in second_node.transitions:
            if transaction.node.name == first_node.name:
                coef = 20
                break

        middle_distance_point = (x1 + x2) / 2, (y1 + y2) / 2 + int(coef)
        points = [(x1, y1 + coef), (x2, y2 + coef)]
        self.canvas.create_line(points,
                                tag=str(first_node.name) + ":" + str(second_node.name), arrow="last")
        self.canvas.create_text(middle_distance_point,
                                text="" + str(transaction_name) + " (" + str(first_node.name) + "->" + str(
                                        second_node.name) + ")",
                                tag="t" + str(first_node.name) + ":" + str(second_node.name),
                                fill='black', font=("Purisa", 12))

    def _draw_arc(self, node, transaction_name):
        x1 = node.x
        y1 = node.y
        self.canvas.create_oval(x1 + 20, y1 - 25, x1 - 20, y1 - 50, tag=str(node.name) + ":" + str(node.name))
        self.canvas.create_text(x1, y1 - 60, text="" + str(transaction_name),
                                tag="t" + str(node.name) + ":" + str(node.name), fill='black', font=("Purisa", 12))

    def on_node_press(self, event):

        """Being drag of an object"""
        # record the item and its location
        if self.action == AutomatonAction.Add_State:
            self._drag_data["item"] = self.canvas.find_closest(event.x, event.y)[0]
            tag = self.canvas.gettags(self.canvas.find_closest(event.x, event.y)[0])[0]

            if tag[0:4] == TAGC:
                self._drag_data["item2"] = self.canvas.find_withtag(TAGT + str(tag[4:]))
            elif tag[0:4] == TAGT:
                self._drag_data["item2"] = self.canvas.find_withtag(TAGC + str(tag[4:]))

            self._drag_data["x"] = event.x
            self._drag_data["y"] = event.y
        elif self.action == AutomatonAction.Add_Transition:

            tag = self.canvas.gettags(self.canvas.find_closest(event.x, event.y)[0])[0]
            self.transitionBind = TransitionBind(self.automaton.nodes[int(tag[4:])])
            self.canvas.create_line(event.x, event.y, event.x, event.y, tag="templine")

            print("press")
        elif self.action == AutomatonAction.Set_Initial:
            # reset all nodes to normal state
            for node in self.automaton.nodes:
                if node.state == NodeState.Initial:
                    node.state = NodeState.NoState
                    self.canvas.itemconfig(self.canvas.find_withtag(TAGC + str(node.name)), fill=COLOR_NORMAL)
            tag = self.canvas.gettags(self.canvas.find_closest(event.x, event.y)[0])[0]
            if tag[0:4] == TAGC:
                self.automaton.set_node_state(tag[4:], NodeState.Initial)
                self.canvas.itemconfig(self.canvas.find_closest(event.x, event.y)[0], fill=COLOR_INITIAL)
        elif self.action == AutomatonAction.Set_Final:
            tag = self.canvas.gettags(self.canvas.find_closest(event.x, event.y)[0])[0]
            if tag[0:4] == TAGC:
                self.automaton.set_node_state(tag[4:], NodeState.Final)
                self.canvas.itemconfig(self.canvas.find_closest(event.x, event.y)[0], fill=COLOR_FINAL)

    def on_node_release(self, event):
        if self.action == AutomatonAction.Add_State:
            tag = self.canvas.gettags(self._drag_data["item"])[0]

            self.automaton.nodes[int(tag[4:])].x = event.x
            self.automaton.nodes[int(tag[4:])].y = event.y

            self._drag_data["item"] = None
            self._drag_data["x"] = 0
            self._drag_data["y"] = 0
        elif self.action == AutomatonAction.Add_Transition:
            self.canvas.delete("templine")
            tag = self.canvas.gettags(self.canvas.find_closest(event.x, event.y)[0])[0]
            if tag:
                self.transitionBind.set_secondNode(self.automaton.nodes[int(tag[4:])])
                first_node = self.transitionBind.firstnode
                second_node = self.transitionBind.secondNode

                dialog = InputDialog(self);
                self.wait_window(dialog.top)
                transaction_name = dialog.value
                if transaction_name == "":
                    transaction_name = LAMBDA
                first_node.add_transition(Transition(second_node, transaction_name))
                if second_node.name != first_node.name:
                    self._draw_line(first_node, second_node, transaction_name, "black")
                else:
                    self._draw_arc(first_node, transaction_name)

    def on_node_move(self, event):
        """Handle dragging of an object"""
        # compute how much this object has moved

        if self.action == AutomatonAction.Add_State:
            delta_x = event.x - self._drag_data["x"]
            delta_y = event.y - self._drag_data["y"]
            # move the object the appropriate amount
            self.canvas.move(self._drag_data["item"], delta_x, delta_y)
            self.canvas.move(self._drag_data["item2"], delta_x, delta_y)

            tag = self.canvas.gettags(self._drag_data["item"])[0]
            node = self.automaton.nodes[int(tag[4:])]

            if node.transitions:
                for i in node.transitions:
                    line = self.canvas.find_withtag(str(node.name) + ":" + str(i.node.name))
                    text = self.canvas.find_withtag("t" + str(node.name) + ":" + str(i.node.name))
                    if self.canvas.coords(line):
                        coordx = self.canvas.coords(line)[2]
                        coordy = self.canvas.coords(line)[3]
                        if node.name != i.node.name:
                            coef = 0
                            for transaction in i.node.transitions:
                                if transaction.node.name == node.name:
                                    coef = 20
                                    break
                            self.canvas.coords(line, (event.x, event.y + int(coef), coordx, i.node.y + int(coef)))
                            self.canvas.coords(text, (event.x + i.node.x) / 2,
                                               (i.node.y + event.y) / 2 + int(coef))
                        else:
                            self.canvas.move(line, delta_x, delta_y)
                            self.canvas.move(text, delta_x, delta_y)

            for nodeMove in self.automaton.nodes:
                for transition in nodeMove.transitions:
                    if transition.node.name == node.name:
                        line = self.canvas.find_withtag(str(nodeMove.name) + ":" + str(node.name))
                        text = self.canvas.find_withtag("t" + str(nodeMove.name) + ":" + str(node.name))
                        if self.canvas.coords(line):
                            if nodeMove.name != node.name:
                                self.canvas.coords(line, (nodeMove.x, nodeMove.y, event.x, event.y))
                                self.canvas.coords(text,
                                                   ((event.x + nodeMove.x) / 2, (event.y + nodeMove.y) / 2))

            # record the new position
            self._drag_data["x"] = event.x
            self._drag_data["y"] = event.y
        elif self.action == AutomatonAction.Add_Transition:
            node = self.transitionBind.firstnode
            line = self.canvas.find_withtag("templine")
            self.canvas.coords(line, (node.x, node.y, event.x, event.y))


if __name__ == "__main__":
    app = AutomatonRender()
    app.mainloop()

"""GUI class.

This class is responsible for the gui.
"""

import queue, time
from random import choice
import logging
from appJar import gui
import math

class GUI():
    """This class holds the gui.
    """

    def __init__(self, result_q, node_num):
        super(GUI, self).__init__()
        self.logger = logging.getLogger('app.netconflib.gui')
        self.logger.info("Initializing graphical user interface...")
        self.result_q = result_q

        self.colours = ["red", "blue", "green", "orange", "yellow", "PapayaWhip", "white", "brown"]
        self.node_num = node_num
        self.cols = 1
        self.rows = 1
        self.app = gui(title="Netconfig", geom="500x500", handleArgs=False, showIcon=False)
        self.init_gui()

    def run(self):
        """Starts the gui.
        """

        self.app.thread(self.handle_messages)
        self.app.go()

    def init_gui(self):
        """Initializes the gui.
        """

        self.app.setSticky("news")
        self.app.setExpand("both")
        self.app.setResizable(canResize=True)
        self.build_grid(self.node_num)

    def build_grid(self, size):
        """Builds the gui grid. Every node has its own cell.
        
        Arguments:
            size {integer} -- The number of nodes.
        """

        cols = math.ceil(math.sqrt(size))
        rows = math.ceil(size / cols)
        self.cols = cols
        self.rows = rows
        self.logger.debug("cols = %d, rows = %d, size = %d", cols, rows, size)

        for x in range(rows):
            for y in range(cols):
                n = x * cols + y + 1
                if n > size:
                    break
                lbl_name = "l{}".format(n)
                lbl_text = "Node {}".format(n)
                self.logger.debug("lbl_name = %s, lbl_text = %s", lbl_name, lbl_text)
                self.app.addLabel(lbl_name, lbl_text, x, y)

    def handle_messages(self):
        """Handles the incoming messages in the queue and notifies the gui.
        """

        while True:
            message = None
            try:
                message = self.result_q.get()
                message_str = ''.join(str(e) for e in message)
                self.logger.debug("Got a new message '%s', processing it...", message_str)
                if "--QUIT--" in str(message_str):
                    self.app.queueFunction(self.app.stop)
                    return
                n = int(float(message[0]))
                counter = int(float(message[1]))
                #row = math.ceil(n / self.cols) - 1
                #col = n - (row * self.cols) - 1
                lbl_name = "l{}".format(n)
                lbl_text = "Node {}\ncount = {}".format(n, counter)
                self.app.queueFunction(self.app.setLabel, lbl_name, lbl_text)
                self.app.queueFunction(self.app.setLabelBg, lbl_name, choice(self.colours))
            except queue.Empty:
                continue

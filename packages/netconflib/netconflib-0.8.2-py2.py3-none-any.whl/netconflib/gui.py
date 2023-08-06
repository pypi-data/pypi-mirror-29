"""GUI class.

This class is responsible for the gui.
"""

import queue, time
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
        self.counter = 0
        self.node_num = node_num
        self.cols = 1
        self.rows = 1
        self.app = gui(title="Netconfig", geom="1000x1000", handleArgs=False)
        self.init_gui()

    def run(self):
        self.app.thread(self.handle_messages)
        self.app.go()

    def init_gui(self):
        self.app.setSticky("news")
        self.app.setExpand("both")
        self.build_grid(self.node_num)

    def build_grid(self, size):
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
                lbl_text = "row={}\ncolumn={}".format(x, y)
                self.logger.debug("lbl_name = %s, lbl_text = %s", lbl_name, lbl_text)
                self.app.addLabel(lbl_name, lbl_text, x, y)

    def handle_messages(self):
        while True:
            message = None
            try:
                message = self.result_q.get()
                self.logger.debug("Got a new message %s, processing it...", message)
                self.counter += 1
                n = int(float(message))
                row = math.ceil(n / self.cols) - 1
                col = n - (row * self.cols) - 1
                lbl_name = "l{}".format(n)
                lbl_text = "row={}\ncolumn={} - count = {}".format(row, col, self.counter)
                self.app.queueFunction(self.app.setLabel, lbl_name, lbl_text)
            except queue.Empty:
                continue

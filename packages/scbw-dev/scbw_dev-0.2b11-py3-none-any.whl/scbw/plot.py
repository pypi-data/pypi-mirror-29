import matplotlib.pyplot as plt

import pandas as pd

from .logs import find_frames
import logging

logger = logging.getLogger(__name__)


class RealtimeFramePlotter:
    YLIM_MAX = 100

    def __init__(self, log_dir, game_name, players):
        self.log_dir = log_dir
        self.game_name = game_name

        plt.ion()
        self.figure = plt.figure(0)
        self.ax = []
        self.line_max = []
        self.line_avg = []
        self.ax.append(self.figure.add_subplot(211))
        self.ax.append(self.figure.add_subplot(212))

        for idx, player in enumerate(players):
            line_max, = self.ax[idx].plot([0], [0], 'r-', label="max")
            line_avg, = self.ax[idx].plot([0], [0], 'b-', label="avg")
            self.line_max.append(line_max)
            self.line_avg.append(line_avg)
            self.ax[idx].set_ylabel("Frame time [ms]")
            self.ax[idx].set_title(f"Bot {player.name}")
            self.ax[idx].set_xlim(0, 300)  # this will keep changing
            self.ax[idx].set_ylim(0, self.YLIM_MAX)
            self.ax[idx].legend(handles=[self.line_max[idx], self.line_avg[idx]])

        self.figure.tight_layout()

    def redraw(self):
        try:
            for idx, frame_file in enumerate(sorted(find_frames(self.log_dir, self.game_name))):
                df = pd.read_csv(frame_file)

                self.line_max[idx].set_xdata(df['frame_count'])
                self.line_max[idx].set_ydata(df['frame_time_max'])
                self.line_avg[idx].set_xdata(df['frame_count'])
                self.line_avg[idx].set_ydata(df['frame_time_avg'])
                self.ax[idx].set_xlim(0, df['frame_count'].max())

            self.figure.canvas.draw()
        except Exception as e:
            logger.warning(e)

    def save(self, file):
        self.figure.savefig(file)

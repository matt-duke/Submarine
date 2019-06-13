import logging
from logging.handlers import RotatingFileHandler
import common

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

#These are the sequences need to get colored ouput
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"


COLORS = {
    'WARNING': WHITE,
    'INFO': GREEN,
    'DEBUG': BLUE,
    'CRITICAL': RED,
    'ERROR': YELLOW
}

class ColoredFormatter(logging.Formatter):
    def __init__(self, format):
        self.noColour = common.platform == 'Windows'
        if self.noColour:
            format = format.replace("$RESET", "").replace("$BOLD", "")
        else:
            format = format.replace("$RESET", RESET_SEQ).replace("$BOLD", BOLD_SEQ)
        logging.Formatter.__init__(self, format)

    def format(self, record):
        levelname = record.levelname
        if levelname in COLORS and not self.noColour:
            levelname_color = COLOR_SEQ % (30 + COLORS[levelname]) + levelname + RESET_SEQ
            record.levelname = levelname_color
        return logging.Formatter.format(self, record)
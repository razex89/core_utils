"""
    name : logger.py
    
    purpose : logger.
    
    author : denjK
"""

# IMPORTS
from enum import Enum
import sys
from colorama import Fore, init, Style
from datetime import datetime
import os

init()


# ENUM
class Level(Enum):
    INFO = 0
    WARNING = 1
    CRITICAL = 2
    FATAL = 3


# CONSTS
LOG_TEMPLATE = "[{time}] {color}{type}{end_color}: {message}"
COLOR_DIC = {Level.INFO: Fore.CYAN, Level.WARNING: Fore.YELLOW, Level.FATAL: Fore.RED, Level.CRITICAL: Fore.GREEN}


def _format_log(message, level):
    """
    :param string message: the message to output.
    :param int level: (mostly comes as enum) the level of message (info , warning..)
    :return: 
    """
    try:
        level = Level(level)
        output = LOG_TEMPLATE.format(time=str(datetime.utcnow()), color=COLOR_DIC[level], type=level.name,
                                     end_color=Style.RESET_ALL, message=message)
        return output
    except ValueError:
        print "Level does not exist.. please take Level type from Level enum."
        sys.exit(1)


def log(message, level, **kwargs):
    """
        Purpose: prints a message to the log (usually the screen)
    :param string message: the message to output.
    :param int level: (mostly comes as enum) the level of message (info , warning..)
    
    optional:
    :param string file_destination: in addition to output to screen, also outputs to file.
    :return:
    """

    output = _format_log(message, level)
    print output
    if kwargs.has_key("file_destination"):
        with open(kwargs["file_destination"], "ab") as file_obj:
            file_obj.write(output + os.linesep)

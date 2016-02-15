import os
import ConfigParser


def get_absolute_path(relative_path):
    return os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        relative_path)

config = ConfigParser.ConfigParser()
config.read(get_absolute_path('serveistic.cfg'))

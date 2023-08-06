# -*- coding: utf-8-*-
import os

# main directory
APP_PATH = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), os.pardir))

DATA_PATH = os.path.join(APP_PATH, "static")
LIB_PATH = os.path.join(APP_PATH, "jeeves")
PLUGIN_PATH = os.path.join(LIB_PATH, "modules")

CONFIG_PATH = os.path.expanduser(os.getenv('JEEVES_CONFIG', '~/.jeeves'))


def config(*fname):
    return os.path.join(CONFIG_PATH, *fname)


def data(*fname):
    return os.path.join(DATA_PATH, *fname)

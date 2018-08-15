import os
import json
import pygame


class LoadError(Exception):
    pass

def calculate_real_path(path):
    path = os.path.expandvars(os.path.expanduser(path))
    path = os.path.realpath(path)
    path = os.path.abspath(path)
    return os.path.normcase(os.path.normpath(path))
def join_path(lpath, rpath):
    return os.path.normcase(os.path.normpath(os.path.join(lpath, rpath)))

def file_exists(path):
    return os.path.isfile(path)



def load_image(filename, params={}):
    if not os.path.isfile(filename):
        raise LoadError("Failed to load '{}'. Path missing or invalid.".format(filename))
    try:
        i = pygame.image.load(filename)
        return i.convert_alpha()
    except pygame.error as e:
        raise LoadError("Pygame/SDL Exception: {}".format(e))


def load_audio(filename, params={}):
    if not os.path.isfile(filename):
        raise LoadError("Failed to load '{}'. Path missing or invalid.".format(filename))
    try:
        if pygame.mixer.get_init() is not None:
            return pygame.mixer.Sound(filename)
    except pygame.error as e:
        raise LoadError("Pygame Exception: {}".format(e))
    raise LoadError("Audio subsystem not initialized before attempting to obtain resource.")

def load_font(filename, params={}):
    if not os.path.isfile(filename):
        raise LoadError("Failed to load '{}'. Path missing or invalid.".format(filename))
    try:
        if pygame.font.get_init():
            size = 26
            if "size" in params:
                if isinstance(params["size"], int) and params["size"] > 0:
                    size = params["size"]
            return pygame.font.Font(filename, size)
    except pygame.error as e:
        raise LoadError("Pygame Exception: {}".format(e))
    raise LoadError("Font subsystem not initialized before attempting to obtain resource.")


class DataContainer:
    def __init__(self, data):
        self._data = data
    @property
    def data(self):
        return self._data

def load_JSON(filename, params={}):
    if not os.path.isfile(filename):
        raise LoaderError("File '{}' is missing or not a file.".format(filename))
    data = None
    try:
        with open(filename) as f:
            data = json.load(f)
        return DataContainer(data)
    except Exception as e:
        raise e

def save_JSON(filename, data):
    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        raise e



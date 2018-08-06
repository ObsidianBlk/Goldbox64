import os
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





def load_image(filename):
    if not os.path.isfile(filename):
        raise LoadError("Failed to load '{}'. Path missing or invalid.".format(filename))
    with open(filename) as f:
        try:
            i = pygame.image.load(f, filename)
            return i.convert_alpha()
        except pygame.error as e:
            raise LoadError("Pygame/SDL Exception: {}".format(e.message))


def load_audio(filename):
    if not os.path.isfile(filename):
        raise LoadError("Failed to load '{}'. Path missing or invalid.".format(filename))
    try:
        return pygame.mixer.Sound(filename)
    except pygame.error as e:
        raise LoadError("Pygame Exception: {}".format(e.message))



def load_JSON(filename):
    if not os.path.isfile(filename):
        raise LoaderError("File '{}' is missing or not a file.".format(filename))
    data = None
    try:
        with open(filename) as f:
            data = json.load(f)
        return data
    except Exception as e:
        raise e



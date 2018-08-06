

import os, sys
import json
import weakref
import pygame
from .resourceLoaders import *


class ResourceError(Exception):
    pass

_GAME_PATH=calculate_real_path(os.path.dirname(sys.argv[0]))

_RESOURCES={}

def define_resource_type(rtype, sub_path, loader_fn):
    global _RESOURCES, _GAME_PATH, join_path
    if rtype in _RESOURCES:
        raise ResourceError("Resource '{}' already defined.".format(rtype))
    fullpath = join_path(_GAME_PATH, sub_path)
    if not os.path.isdir(fullpath):
        print("'{}' | '{}'".format(_GAME_PATH, fullpath))
        raise ResourceError("'{}' is not a valid directory.".format(sub_path))
    if not callable(loader_fn):
        raise ResourceError("Expected a callable as the resource loader.")
    _RESOURCES[rtype]={"r":[], "loader":loader_fn, "path":fullpath}


def configure(conf):
    global _RESOURCES, join_path
    if not isinstance(conf, dict):
        raise TypeError("Expected a dictionary.")
    for key in conf:
        if key in _RESOURCES:
            fullpath = join_path(_GAME_PATH, conf[key])
            if not os.path.isdir(fullpath):
                raise ResourceError("'{}' is not a valid directory.".format(conf[key]))
            _RESOURCES[key]["path"] = fullpath
            _RESOURCES[key]["r"] = [] # Completely drop old list.

class Manager:
    def __init__(self):
        pass

    @property
    def game_path(self):
        global _GAME_PATH
        return _GAME_PATH 

    @property
    def resource_types(self):
        global _RESOURCES
        rtypes = []
        for key in _RESOURCES:
            rtypes.append(key)
        return rtypes

    def _getResourceDict(self, rtype, src):
        global _RESOURCES
        if rtype in _RESOURCES:
            for r in _RESOURCES[rtype]["r"]:
                if r["src"] == src:
                    return r
        return None

    def has(self, rtype, src):
        return (self._getResourceDict(rtype, src) is not None)

    def store(self, rtype, src):
        global _RESOURCES
        if type not in _RESOURCES:
            raise ResourceError("Unknown resource type '{}'.".format(rtype))
        if self._getResourceDict(rtype, src) == None:
            _RESOURCES[rtype]["r"].append({"src":src, "instance":None, "locked":False})
        return self

    def remove(self, rtype, src):
        global _RESOURCES
        d = self._getResourceDict(rtype, src)
        if d is None:
            raise ResourceError("No '{}' resource '{}' stored.".format(rtype, src))
        _RESOURCES[rtype]["r"].remove(d)
        return self

    def clear(self, rtype, src, ignore_lock):
        d = self._getResourceDict(rtype, src)
        if d is None:
            raise ResourceError("No '{}' resource '{}' stored.".format(rtype, src))
        if d["locked"] == False or ignore_lock == True:
            d["instance"] = None
        return self

    def get(self, rtype, src):
        global _RESOURCES
        if rtype not in _RESOURCES:
            raise ResourceError("Unknown resource type '{}'.".format(rtype))
        d = self._getResourceDict(rtype, src)
        if d is None:
            raise ResourceError("No '{}' resource '{}' stored.".format(rtype, src))
        if d["instance"] is None:
            loader = _RESOURCES[rtype]["loader"]
            filename = join_path(self.data_path, src)
            try:
                d["instance"] = loader(filename)
            except Exception as e:
                raise e
        return weakref.ref(d["instance"])

    def lock(self, rtype, src, lock=True):
        d = self._getResourceDict(rtype, src)
        if d is None:
            raise ResourceError("No '{}' resource '{}' stored.".format(rtype, src))
        d["locked"]=lock
        return self

    def is_locked(self, rtype, src):
        d = self._getResourceDict(rtype, src)
        if d is not None and d["src"] == src:
            return d["locked"]
        return False

    def clear_resource_type(self, rtype, ignore_lock=False):
        global _RESOURCES
        if rtype in _RESOURCES:
            for r in _RESOURCES[rtype]["r"]:
                if r["locked"] == False or ignore_lock == True:
                    r["instance"] = None
        return self

    def clear_resources(self, ignore_lock=False):
        global _RESOURCES
        for key in _RESOURCES:
            self.clear_resource_type(key, ignore_lock)
        return self

    def remove_resource_type(self, rtype):
        global _RESOURCES
        if rtype not in _RESOURCES:
            raise ResourceError("Unknown resource type '{}'.".format(rtype))
        _RESOURCES[rtype]["r"] = []
        return self

    def remove_resources(self):
        global _RESOURCES
        for key in _RESOURCES:
            _RESOURCES[key]["r"] = []
        return self


# ---------------------------------------------------------------
# Defining the built-in loaders located in resourceLoaders.py
# ---------------------------------------------------------------
define_resource_type("graphic", "graphics/", load_image)
define_resource_type("audio", "audio/", load_audio)
define_resource_type("json", "data/json/", load_JSON)



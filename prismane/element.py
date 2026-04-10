from __future__ import annotations  # needed to make Object and ObjectGroup callses be able to reference each other
from .panels import MasterControlPanel
import pygame as pg


class Element():
    def __init__(self, singleton: bool = False, name: str | None = None):
        self.name = name if name else self.__class__.__name__
        self._singleton = singleton
        self.element_tree = element_tree
        self.element_tree.register_element(self)

    def update(self, master_panel: MasterControlPanel):
        pass

class ElementTree():
    def __init__(self):
        self.objects = {
            "singletons": {},
            "groups": {}
        }

    def register_element(self, elem: Element):
        if elem._singleton:
            self.objects["singletons"][elem.name] = elem
        elif elem.name not in self.objects["groups"]:
            self.objects["groups"][elem.name] = [elem]
        else:
            self.objects["groups"][elem.name].append(elem)

    def delete_element(self, elem: Element):
        if elem._singleton and elem.name in self.objects["singletons"]:
            self.objects["singletons"].pop(elem.name)
        elif elem.name in self.objects["groups"]:
            self.objects["groups"][elem.name].remove(elem)

    # only for singletons
    def __getitem__(self, key):
        return self.objects["singletons"][key]

    def get_group(self, group: str):
        if group in self.objects["groups"]:
            return self.objects["groups"][group]
        return []


element_tree: ElementTree = ElementTree()



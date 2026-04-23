from __future__ import annotations  # needed to make Object and ObjectGroup callses be able to reference each other


class Element():
    def __init__(self, singleton: bool = False, name: str | None = None):
        self.name = name if name else self.__class__.__name__
        self._singleton = singleton
        self.element_tree = element_tree
        self.element_tree.register_element(self)

    def destroy(self):
        self.element_tree.delete_element(self)

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
            del self.objects["singletons"][elem.name]
        elif elem.name in self.objects["groups"]:
            self.objects["groups"][elem.name].remove(elem)
            if len(self.objects["groups"][elem.name]) == 0:
                del self.objects["groups"][elem.name]

    # only for singletons
    def __getitem__(self, key):
        return self.objects["singletons"][key]

    def get_group(self, group: str):
        if group in self.objects["groups"]:
            return self.objects["groups"][group]
        return []

element_tree: ElementTree = ElementTree()

# Hey what's this doing here?

# What are you talkign abt

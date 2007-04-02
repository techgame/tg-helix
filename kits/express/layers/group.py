##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~ Copyright (C) 2002-2007  TechGame Networks, LLC.              ##
##~                                                               ##
##~ This library is free software; you can redistribute it        ##
##~ and/or modify it under the terms of the BSD style License as  ##
##~ found in the LICENSE file included with this distribution.    ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from TG.kvObserving import KVProperty
from ..stage import ExpressActor

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Group(ExpressActor):
    """A group of layers to be displayed

    Composite Sets:
        Group fade
        Add/Remove/Reorder
            Timeline "Animate" ops
        Does not own child Layers		
    """
    node_layers = KVProperty(list)

    def isLayer(self): return False
    def isComposite(self): return True

    def sceneNodeFor(self, nodeKey, node):
        node = ExpressActor.sceneNodeFor(self, nodeKey, node)
        if nodeKey == 'render':
            self._setupNodeLayers(node.addNew())
        return node

    def _setupNodeLayers(self, node_layers):
        # get existing node_layers *list* 
        layers = self.node_layers

        # put the layers list into the node children list
        node_layers.extend(layers)

        # and replace the node_layers with the node instance
        self.node_layers = node_layers

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __len__(self):
        return len(self.node_layers)
    def __iter__(self, idx):
        return iter(self.node_layers)
    def __getitem__(self, idx):
        return self.node_layers[idx]
    def __setitem__(self, idx, value):
        self.node_layers[idx] = value
    def __delitem__(self, idx):
        del self.node_layers[idx]

    def add(self, layer):
        self.node_layers.append(layer)
        return layer
    def remove(self, layer):
        self.node_layers.remove(layer)
        return layer
    def extend(self, layers):
        self.node_layers.extend(layers)

    def clear(self):
        del self.node_layers[:]

    def __iadd__(self, layer):
        if isinstance(layer, list):
            self.extend(layer)
        else: self.add(layer)
        return self
    def __isub__(self, layer):
        self.remove(layer)
        return self


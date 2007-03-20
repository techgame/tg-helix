##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~ Copyright (C) 2002-2006  TechGame Networks, LLC.              ##
##~                                                               ##
##~ This library is free software; you can redistribute it        ##
##~ and/or modify it under the terms of the BSD style License as  ##
##~ found in the LICENSE file included with this distribution.    ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Scene managers
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ScenePassMeter(object):
    def start(self): pass
    def end(self): pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SceneGraphPassManager(object):
    meter = ScenePassMeter()

    def __init__(self, scene, root):
        self.root = root
        sceneMeter = getattr(scene, 'meter', None)
        if sceneMeter is not None:
            self.meter = sceneMeter

    graphPassCache = []
    def graphPass(self):
        if self.root.isChanged():
            # there are changes... recompile the graph
            self.graphPassCache = self.compileGraphPass(self.root)
        return self.graphPassCache

    def compileGraphPass(self, root):
        graphPassItemsFrom = self.graphPassItemsFrom

        emptyUnwind = [] # a "constant" empty list
        passUnwindStack = [] # a stack of unwind op lists
        passResult = [] # a linearized graph pass -- will eventually contain
                        # the wind ops and all of the unwind op stack in 
                        # correct traversal order

        itree = root.iterTreeStack()
        for op, node in itree:
            if op < 0: 
                # a pop operation -- add the unwind stack top to our pass
                # result and continue the iteration
                passResult.extend(passUnwindStack.pop())
                continue
            pushUnwind = (op > 0)

            # get sgNodeItems fromm our node using template method
            sgNodeItems, cullStack = graphPassItemsFrom(node, pushUnwind)

            if pushUnwind and cullStack:
                itree.send(True)
                pushUnwind = False

            if sgNodeItems is None:
                if pushUnwind:
                    # push an empty unwind on the stack
                    passUnwindStack.append(emptyUnwind)
                continue

            # unpack sgNodeItems
            wind, unwind = sgNodeItems

            if wind:
                # wind ops go directly on the result
                passResult.extend(wind)

            # if we are pushing and not culling...
            if pushUnwind:
                # push the unwind ops on the stack
                passUnwindStack.append(unwind or emptyUnwind)
            elif unwind:
                # push(unwind); extend(pop) --> extend(unwind)
                passResult.extend(unwind)

        # make sure that all the pop operations came through to empty our unwind stack
        assert not passUnwindStack, passUnwindStack
        return passResult

    def graphPassItemsFrom(self, node, hasChildren):
        """Should return ((wind, unwind), cullStack) 
        
        where 'wind' and 'unwind' are list of pass items for node.  
        
        'cullStack' is a directive to the algorithm on whether to continue down
        the DFS traversal of the scene graph, and the 'hasChildren' parameters
        signifies that traversal will continue in DFS order unless cullStack is
        false."""
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))


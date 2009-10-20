##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~ Copyright (C) 2002-2009  TechGame Networks, LLC.              ##
##~                                                               ##
##~ This library is free software; you can redistribute it        ##
##~ and/or modify it under the terms of the BSD style License as  ##
##~ found in the LICENSE file included with this distribution.    ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

qt_host_impl = None
if qt_host_impl is None:
    # try for PySide implementation
    try: import PySide
    except ImportError: pass
    else: qt_host_impl = PySide

if qt_host_impl is None:
    # try for PyQt4 implementation
    try: import PyQt4
    except ImportError: pass
    else: qt_host_impl = PyQt4

if qt_host is None:
    raise ImportError("Unable to import PySide or PyQt4 for Qt GUI support")

# add qt_host's package path to ours, allowing our package to standin for theirs
__path__.extend(qt_host.__path__)


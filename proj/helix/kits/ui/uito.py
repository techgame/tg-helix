
class UIItemTypeObserver(ObservableTypeParticipant):
    def __init__(self, propMap):
        self.propMap = propMap

    def copy(self, propMapUpdate=()):
        self = self.__class__(self.propMap.copy())
        if propMapUpdate:
            self.propMap.update(propMapUpdate)
        return self

    def onObservableClassInit(self, selfAttrName, uiItemKlass, tcinfo):
        kvars = tcinfo['kvars']
        propMap = self.propMap
        for n, v in kvars.items():
            pm = propMap.get(n, None)
            if pm is not None:
                setattr(uiItemKlass, n, pm(v))

    def onObservableInit(self, selfAttrName, uiItem):
        propMap = self.propMap
        for n, v in propMap.iteritems():
            iv = getattr(uiItem, n, None)

            if iv is None: iv = v()
            else: iv = iv.copy()

            setattr(uiItem, n, iv)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


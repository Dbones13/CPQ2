#GS_Get_Set_AtvQty
def setAtvQty(Product,AttrName,sv,qty):
    pvs=Product.Attr(AttrName).Values
    for av in pvs:
        if av.Display == sv:
            av.IsSelected=False
            av.Quantity = 0
            if int(qty) > 0:
                av.IsSelected=True
                av.Quantity=qty
                Trace.Write('Selected ' + sv + ' in attribute ' + AttrName + ' at Qty ' + str(qty))
                break

def getAtvQty(Product,AttrName,sv):
    pvs=Product.Attr(AttrName).SelectedValues
    for av in pvs:
        if av.Display == sv:
            return av.Quantity
    return 0

def getAtvsQty(Product, AttrName, svs):
    pvs=Product.Attr(AttrName).Values
    res = dict()
    for av in pvs:
        if av.Display in svs:
            res[av.Display] = av.Quantity
    return res

def getAllAtvQty(Product, AttrName):
    pvs=Product.Attr(AttrName).Values
    res = dict()
    for av in pvs:
        res[av.Display] = av.Quantity
    return res

def resetAllAtvQty(Product, AttrName):
    pvs=Product.Attr(AttrName).Values
    for av in pvs:
        av.IsSelected=False
        av.Quantity = 0

def resetParamQty(Product, AttrName, ParamList):
    ct = 0
    total = len(ParamList)
    if total > 0:
        pvs=Product.Attr(AttrName).Values
        for av in pvs:
            if av.Display in ParamList:
                av.IsSelected=False
                av.Quantity = 0
                ct += 1
            if ct == total:
                break
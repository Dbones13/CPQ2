def setAtvQty(Product,AttrName,sv,qty):
    pvs=Product.Attr(AttrName).Values
    for av in pvs:
        if av.Display == sv:
            av.IsSelected=False
            av.Quantity = 0
            if qty > 0:
                av.IsSelected=True
                av.Quantity=qty
                Trace.Write('Selected ' + sv + ' in attribute ' + AttrName + ' at Qty ' + str(qty))
                break

def addAtvQty(Product, AttrName, sv, qty):
    pvs=Product.Attr(AttrName).Values
    for av in pvs:
        if av.Display == sv:
            if int(qty) > 0:
                av.IsSelected = True
                av.Quantity = av.Quantity + qty
                Trace.Write('Added Qty to value ' + sv + ' in attribute ' + AttrName + ' at Qty ' + str(qty) + '. Total Qty : ' + str(av.Quantity))
                break
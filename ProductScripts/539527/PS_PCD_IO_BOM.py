import math
def Roundup(a):
    if float(a)>int(a):
        return int(a)+1
    else:
        return int(a)
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
def BOMQty(AttributeName,DataPoints,sparepercent):
    Raw_IO = float(Product.Attr(AttributeName).GetValue())
    Spare_IO = Roundup(Raw_IO*sparepercent)
    Total_IO = float(Raw_IO+Spare_IO)
    Qty = Roundup(Total_IO/int(DataPoints))
    return Qty
total_qty_of_module = 0
sparepercent = float(Product.Attr("PCD_I/O_Spare_percentage").GetValue())/100
query = SqlHelper.GetList("Select AttributeName,DataPoints,ModelNo from PCD_IO_BOM")
if query is not None:
    for row in query:
        qty = BOMQty(row.AttributeName,row.DataPoints,sparepercent)
        setAtvQty(Product,"PCD_Part_Summary",row.ModelNo,qty)
        total_qty_of_module += qty
Product.Attr("PCD_Total_Qty_of_Modules").AssignValue(str(total_qty_of_module))
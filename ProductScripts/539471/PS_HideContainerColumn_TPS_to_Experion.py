def getAttributeValue(Name):
    return Product.Attr(Name).GetValue()

def getContainer(Name):
    return Product.GetContainerByName(Name)

def hideColumn(container,Column):
    Product.ParseString('<*CTX( Container({}).Column({}).SetPermission(Hidden) )*>'.format(container,Column))
    Product.ParseString('<*CTX( Container({}).Row(1).Column({}).Set() )*>'.format(container,Column))

def setDefaultColumnForDropdown(container,Column, value):
    Product.ParseString('<*CTX( Container({}).Row(1).Column({}).Set({}) )*>'.format(container,Column, value))

def visibleColumn(container,Column):
    Product.ParseString('<*CTX( Container({}).Column({}).SetPermission(Editable) )*>'.format(container,Column))

def isHidden(container,Column):
    return Product.ParseString('<*CTX( Container({}).Column({}).GetPermission )*>'.format(container,Column)) == 'Hidden'

def getContainer(Name):
    return Product.GetContainerByName(Name)
Msid_Scope=Product.Attr("Scope").GetValue()
if Product.Name =='TPS to Experion' and Msid_Scope in ["LABOR"]:
    tps3rdparty = getContainer('TPS_to_EX_3rd_Party_Items')
    count = tps3rdparty.Rows.Count
    if count > 0:
        while count > 0:
            tps3rdparty.DeleteRow(count-1)
            count-=1
    if not isHidden("TPS_to_EX_3rd_Party_Items","Thin_Client_cables_and_adapters"):
        hideColumn("TPS_to_EX_3rd_Party_Items","Thin_Client_cables_and_adapters")

if  Product.Name =='TPS to Experion' and Msid_Scope not in ["LABOR"]:
    if isHidden("TPS_to_EX_3rd_Party_Items","Thin_Client_cables_and_adapters"):
        visibleColumn("TPS_to_EX_3rd_Party_Items","Thin_Client_cables_and_adapters")
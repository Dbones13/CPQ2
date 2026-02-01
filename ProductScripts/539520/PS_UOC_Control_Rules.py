def getContainer(containerName):
    return Product.GetContainerByName(containerName)

def getAttributeValue(attribute_name):
    return Product.Attributes.GetByName(attribute_name)

def setHidden(cont,column):
    Product.ParseString('<*CTX( Container({}).Column({}).SetPermission(Hidden) )*>'.format(cont, column))
def setEditable(cont,column):
    Product.ParseString('<*CTX( Container({}).Column({}).SetPermission(Editable) )*>'.format(cont, column))

def disallowattrs(attname):
    return Product.DisallowAttr(attname)
def allowattrs(attname):
    return Product.AllowAttr(attname)

#DCS_UOC_System_Cabinet
Product.Messages.Clear()

UOC_sys_cabinet=getAttributeValue('UOC_Num_of_Sys_Cabinets').GetValue()
UOC_sys_cabinet = UOC_sys_cabinet if UOC_sys_cabinet else 0
UOC_sys_cabinet_RG=getAttributeValue('UOC_Num_of_Sys_Cabinets_RG').GetValue()
UOC_sys_cabinet_RG = UOC_sys_cabinet_RG if UOC_sys_cabinet_RG else 0
sum_UOC_cabinet= 0+float(UOC_sys_cabinet)+0+float(UOC_sys_cabinet_RG)
if getAttributeValue('DCS_UOC_System_Cabinet'):
    getAttributeValue('DCS_UOC_System_Cabinet').AssignValue(str(sum_UOC_cabinet))
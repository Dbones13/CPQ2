def getAttributeDict():
    dataDict = dict()
    for attr in Product.Attributes:
        if attr.GetHint() == "Bulk Update Attributes" and attr.DisplayType != "Button":
            dataDict[attr.Name] = attr.GetValue()
    return dataDict

def setAttrValue(attr , value):
    if attr.DisplayType == "DropDown":
        attr.SelectDisplayValue(value)
    if attr.DisplayType == "FreeInputNoMatching":
        attr.AssignValue(value)

def updateAttributes(product , attributeDict):
    for attr in product.Attributes:
        if attributeDict.get(attr.Name):
            setAttrValue(attr , attributeDict.get(attr.Name))

def bulkUpdate(container , attributeDict):
    for row in container.Rows:
        if row.IsSelected:
            prod = row.Product
            updateAttributes(prod , attributeDict)

container = Product.GetContainerByName("RTU Groups")

attributeDict = dict()

if container.HasSelectedRow:
    attributeDict = getAttributeDict()

if attributeDict:
    bulkUpdate(container , attributeDict)
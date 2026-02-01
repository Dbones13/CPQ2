from GS_R2Q_NewExpansion_Attribute_ContColms import R2QNewExpansionControlEdgePLC as PRDT
def hideAttr(attrList):
    for attr in attrList:
        Product.Attr(attr).Access = AttributeAccess.Hidden

def showAttr(attrList):
    for attr in attrList:
        Product.Attr(attr).Access = AttributeAccess.Editable

def readAttr(attrList):
    for attr in attrList:
        Product.Attr(attr).Access = AttributeAccess.ReadOnly

def setDisplayValue(attrDict):
    for attr, value in attrDict.items():
        #values = ''.join(attrDict[attr])
        Product.Attr(attr).SelectDisplayValue(value)

def hideContainerColumns(contColumnList):
    for contColumn in contColumnList:
        for col in contColumnList[contColumn]:
            Product.ParseString('<*CTX( Container({0}).Column({1}).SetPermission(Hidden) )*>'.format(contColumn,col))

def showContainerColumns(contColumnList):
    for contColumn in contColumnList:
        for col in contColumnList[contColumn]:
            Product.ParseString('<*CTX( Container({0}).Column({1}).SetPermission(Editable) )*>'.format(contColumn,col))

def setDefaultText(attrDict):
    for attr, value in attrDict.items():
        if (productName in ('FDM Upgrade 1', 'FDM Upgrade 2', 'FDM Upgrade 3') and Product.Attr(attr).GetValue() == '') or productName in ('Terminal Manager','HC900 Group', 'Fire Detection & Alarm Engineering','Industrial Security (Access Control)', 'Digital Video Manager', 'Digital Video Manager Group'):
            #values = ''.join(attrDict[attr])
            Product.Attr(attr).AssignValue(value)

productName = Product.Name
Log.Info('productName ' + str(productName))
checkproduct = Product.ParseString('<*CTX(Product.RootProduct.PartNumber)*>')
if Quote.GetCustomField('isR2QRequest').Content == 'Yes':
    Product.Attr('R2QRequest').AssignValue('Yes')
    Product.Attr('R2Q_QuoteNumber').AssignValue(str(Quote.CompositeNumber))
    if checkproduct =='PRJT R2Q':
        if productName in PRDT.products:
            hideAttr(PRDT.products[productName].get('hideAttrList', []))
            hideContainerColumns(PRDT.products[productName].get('hideContainerColumnDict', {}))
            showContainerColumns(PRDT.products[productName].get('showContainerColumnDict', {}))
            showAttr(PRDT.products[productName].get('showAttrList', []))
            readAttr(PRDT.products[productName].get('readAttrList', []))
            setDisplayValue(PRDT.products[productName].get('displayValueDict', {}))
            setDefaultText(PRDT.products[productName].get('defaultText', {}))

else:
    Product.Attr('R2QRequest').AssignValue('')
    hideAttr(PRDT.products[productName].get('nonR2QHideAttrList', []))
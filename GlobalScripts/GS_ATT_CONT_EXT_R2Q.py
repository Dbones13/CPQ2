def extractProductContainer(attrName, product):
    containerList = []
    containerRows = product.GetContainerByName(attrName).Rows
    if containerRows.Count > 0:
        for contanierRow in containerRows:
            contanierRowDict = {}
            for col in contanierRow.Columns:
                contanierRowDict[col.Name] = contanierRow[col.Name]
            containerList.append(contanierRowDict)
    return [containerList]


def extractProductAttributes(attributedict, product):
    for attr in product.Attributes:
        if attr.DisplayType == 'Container' and attr.Name not in attributedict:
            attributedict[attr.Name] = extractProductContainer(attr.Name, product)
        else:
            #Trace.Write("attr.Name ----- " + str(attr.Name))
            if product.Attr(attr.Name).GetValue() != '' and attr.Name not in ('R2Q_CONFIGURATION','WriteInProduct') and attr.Name not in attributedict:
                attributedict[attr.Name] = product.Attr(attr.Name).GetValue()
isR2Qquote = True 
if isR2Qquote:
    selectAttributedict = {}
    extractProductAttributes(selectAttributedict,Product)
    #Trace.Write("SelectedAttsData====> " +str(selectAttributedict))
    QuoteId = Quote.CompositeNumber
    row_data = {
        'Product': str(Product.Name),
        'ATTRIBUTE_DICT': str(selectAttributedict)
    }
    #Trace.Write(">>"+str(row_data))
    Product.Attr("R2Q_CONFIGURATION").AssignValue(str(selectAttributedict))
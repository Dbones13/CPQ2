def addQuoteMsg(Quote,message):
    if not Quote.Messages.Contains(message):
        Quote.Messages.Add(message)

def setCFValue(Quote, CF_Name, CF_Value):
    Quote.GetCustomField(CF_Name).Content = CF_Value

def getQuoteItemsQty(Quote):
    PartsList = []
    allParts = dict()
    for item in Quote.Items:
        PartsList.append(item.PartNumber)
        allParts[item.PartNumber] = item.Quantity
    return PartsList,allParts

def getMasterData(PartsList):
    tableParts = dict()
    query = ("select MinOrderQuantity,PartNumber,MindeliveryQuantity from HPS_PRODUCTS_MASTER where (MinOrderQuantity <> '0.000' and MinOrderQuantity <> '') and PartNumber in ('{}')").format("','".join(PartsList))
    PartsData = SqlHelper.GetList(query)
    if PartsData is not None:
        for part in PartsData:
            tableParts[part.PartNumber] = {"MinOrderQuantity":float(part.MinOrderQuantity),"MindeliveryQuantity":float(part.MindeliveryQuantity)}
        return tableParts

def CheckForInvalidQty(Quote):
    setCFValue(Quote,"InvalidQty",'')
    setCFValue(Quote,"InvalidMinDeliveryQty",'')
    PartsList,allParts = getQuoteItemsQty(Quote)
    tableParts = getMasterData(PartsList)
    QtyCheck = False
    MinDeliveryCheck = False
    for part in allParts:
        if tableParts:
            if part in tableParts:
                if allParts[part] < tableParts[part]["MinOrderQuantity"]:
                    message = Translation.Get('message.invalidQtypart').format(part,tableParts[part]["MinOrderQuantity"])
                    addQuoteMsg(Quote,message)
                    QtyCheck = True
                if tableParts[part]["MindeliveryQuantity"] != 0.000:
                    if allParts[part] % tableParts[part]["MindeliveryQuantity"] != 0:
                        message = Translation.Get('message.invalidMinDeliveryQty').format(part,tableParts[part]["MindeliveryQuantity"])
                        addQuoteMsg(Quote,message)
                        MinDeliveryCheck = True
    if QtyCheck:
        setCFValue(Quote,"InvalidQty",'1')
    if MinDeliveryCheck:
        setCFValue(Quote,"InvalidMinDeliveryQty",'1')
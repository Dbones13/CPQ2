def getQuantityDict(msidProduct , quantityDict,MSIDdict, MSID ,SystemNumber):
    container = msidProduct.GetContainerByName("MSID_Product_Container")
    for row in container.Rows:
        childProduct = row.Product
        childPartContainer = childProduct.GetContainerByName("MSID_Added_Parts_Common_Container")
        if childPartContainer is not None:
            for childRow in childPartContainer.Rows:
                quantityDict[childRow.UniqueIdentifier] = childRow["Quantity"]
                MSIDdict[childRow.UniqueIdentifier] = MSID + " - " + SystemNumber

def getQuantityDictfsc(msidProduct , quantityDict,MSIDdict, MSID ,SystemNumber):
    container = msidProduct.GetContainerByName("MSID_Product_Container_FSC_hidden")
    for row in container.Rows:
        childProduct = row.Product
        childPartContainer = childProduct.GetContainerByName("MSID_Added_Parts_Common_Container")
        for childRow in childPartContainer.Rows:
            quantityDict[childRow.UniqueIdentifier] = childRow["Quantity"]
            MSIDdict[childRow.UniqueIdentifier] = MSID + " - " + SystemNumber

def getQuantityDictvirt(msidProduct , quantityDict,MSIDdict, MSID, SystemNumber):
    container = msidProduct.GetContainerByName("MSID_Product_Container_Virtualization_hidden")
    for row in container.Rows:
        childProduct = row.Product
        childPartContainer = childProduct.GetContainerByName("MSID_Added_Parts_Common_Container")
        for childRow in childPartContainer.Rows:
            quantityDict[childRow.UniqueIdentifier] = childRow["Quantity"]
            MSIDdict[childRow.UniqueIdentifier] = MSID + " - " + SystemNumber
        childPartSummContainer = childProduct.GetContainerByName("Virtualization_partsummary_cont")
        for childRow in childPartSummContainer.Rows:
            MSIDdict[childRow.UniqueIdentifier] = MSID + " - " + SystemNumber

def getQuantityDictgen(msidProduct , quantityDict,MSIDdict, MSID, SystemNumber):
    container = msidProduct.GetContainerByName("MSID_Product_Container_Generic_hidden")
    for row in container.Rows:
        childProduct = row.Product
        childPartContainer = childProduct.GetContainerByName("MSID_Added_Parts_Common_Container")
        for childRow in childPartContainer.Rows:
            quantityDict[childRow.UniqueIdentifier] = childRow["Quantity"]
            MSIDdict[childRow.UniqueIdentifier] = MSID + " - " + SystemNumber

quantityDict = dict()
MSIDdict = dict()
msidContainer = Product.GetContainerByName("Migration_MSID_Selection_Container")
for row in msidContainer.Rows:
    msidProduct = row.Product
    getQuantityDict(msidProduct , quantityDict,MSIDdict,row['MSID'], row['System_Number'])
    getQuantityDictfsc(msidProduct , quantityDict,MSIDdict,row['MSID'],row['System_Number'])
    getQuantityDictvirt(msidProduct , quantityDict,MSIDdict,row['MSID'], row['System_Number'])
    getQuantityDictgen(msidProduct , quantityDict,MSIDdict,row['MSID'], row['System_Number'])
items = arg.QuoteItemCollection
for item in items:
    if quantityDict.get(item.QuoteItemGuid):
        item.Quantity = float(quantityDict.get(item.QuoteItemGuid))
        item["QI_Area"].Value = (MSIDdict.get(item.QuoteItemGuid))
    elif MSIDdict.get(item.QuoteItemGuid):
        item["QI_Area"].Value = (MSIDdict.get(item.QuoteItemGuid))
#Quote.Calculate(1)
Quote.Save(False)
#Log.Write(str(item.Quantity))
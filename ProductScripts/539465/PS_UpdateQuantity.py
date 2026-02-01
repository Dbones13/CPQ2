items = arg.QuoteItemCollection
product = sender

def getPartDict(partsContainer):
    partDict = dict()
    for row in partsContainer.Rows:
        partDict[row["Part Number"]] = row["ItemQuantity"]
    return partDict

partsContainer = product.GetContainerByName("RTU Parts")
partsDict = dict()
partsDict["ControlEdge RTU System"] = getPartDict(partsContainer)

groupContainer = product.GetContainerByName("RTU Groups")
for row in groupContainer.Rows:
    partsContainer = row.Product.GetContainerByName("RTU Parts")
    partsDict[row["Group Number"]] = getPartDict(partsContainer)

Trace.Write(str(partsDict))
keyDict = dict()
for item in items:
    keyDict[item.RolledUpQuoteItem] = [item.PartNumber , item.Quantity]
    if item.ParentRolledUpQuoteItem:
        parts = partsDict.get(keyDict[item.ParentRolledUpQuoteItem][0])
        parentQty = keyDict[item.ParentRolledUpQuoteItem][1]
        if parts:
            quantity = parts.get(item.PartNumber)
            if quantity:
                Log.Write(quantity)
                item.Quantity = float(quantity) * parentQty
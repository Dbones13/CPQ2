import GS_CommonModule as cm
itemsToBeDeleted = cm.getCFValue(Quote, "NoPriceParts")

for item in Quote.MainItems:
    if item.PartNumber in itemsToBeDeleted:
        item.Delete()
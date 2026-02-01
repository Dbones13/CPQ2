#PS_PAGA_Labor_Pricing_in_Quote
def getFloat(Var):
    if Var:
        return float(Var)
    return 0.00

partsNumbers = {}
labor_cont = Product.GetContainerByName('Labor_PriceCost_Cont')
for material in labor_cont.Rows:
    ##Trace.Write("Qty:{} PArt:{} cost:{} price:{} wtw:{} tot mpa:{} ".format(material["Qty"], material["Part Number"],material["Total Cost"], material["Total List Price"], material["Total WTW Cost"], material["Total MPA Price"] ))
    if material["Qty"] not in ('',0.0):
        system = partsNumbers[material["Part Number"]] = {}
        if material["Total Cost"] not in ('',0.0):
            system["QI_GESRegionalCost"] = getFloat(material["Total Cost"]) / getFloat(material["Qty"])
        if material["Total List Price"] not in ('',0.0):
            system["QI_LaorPartsListPrice"] = getFloat(material["Total List Price"]) / getFloat(material["Qty"])
        if material["Total WTW Cost"] not in ('',0.0):
            system["QI_UnitWTWCost"] = getFloat(material["Total WTW Cost"]) / getFloat(material["Qty"])
        if material["Total MPA Price"] not in ('',0.0):
            system["QI_MPA_Price"] = getFloat(material["Total MPA Price"]) / getFloat(material["Qty"])
Trace.Write(str(partsNumbers))
#This adds values from the dictionary to the fields in the quote line item
parentItemGuid = ''
for item in arg.QuoteItemCollection:
    Trace.Write("Part:{} Parent:{} GUID:{}".format(item.PartNumber, item.ParentItemGuid, item.QuoteItemGuid))
    if item.PartNumber == 'PRJT':
        parentItemGuid = item.QuoteItemGuid
    elif parentItemGuid == item.ParentItemGuid and item.PartNumber in partsNumbers:
        Trace.Write("Updating regional cost")
        partData = partsNumbers.get(item.PartNumber,None)
        if partData:
            for each in partData:
                if each == 'QI_GESRegionalCost':
                    item.QI_GESRegionalCost.Value = getFloat(partData[each])
                elif each == 'QI_LaorPartsListPrice':
                    item.QI_LaorPartsListPrice.Value = getFloat(partData[each])
                elif each == 'QI_UnitWTWCost':
                    item.QI_FoWTWCost.Value = getFloat(partData[each])
                elif each == 'QI_MPA_Price':
                    item.QI_MPA_Price.Value = getFloat(partData[each])
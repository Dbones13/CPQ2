def getFloat(Var):
    return float(Var) if Var else 0.00

#laborDict = {'QI_GESRegionalCost': 'Total Cost', 'QI_LaorPartsListPrice': 'Total List Price', 'QI_UnitWTWCost': 'Total WTW Cost', 'QI_MPA_Price': 'Total MPA Price'}

def updatelaborItemPrices(quote, labor_cont, ClearTable):
    laborDict = {'QI_GESRegionalCost': 'Total Cost', 'QI_LaorPartsListPrice': 'Total List Price', 'QI_UnitWTWCost': 'Total WTW Cost', 'QI_MPA_Price': 'Total MPA Price'}
    if labor_cont.Name == 'Winest_Labor_PriceCost_Cont':
        laborDict.pop('QI_MPA_Price')
    WTWQTDetails = quote.QuoteTables['WTW_Prices_Calculation']
    if ClearTable:
        WTWQTDetails.Rows.Clear()
    for material in labor_cont.Rows:
        qty = getFloat(material["Qty"])
        if qty in (0.0, 0.00, 0):
            continue
        dict_entry = {}
        for QIFC in laborDict:
            total_cost = getFloat(material[laborDict[QIFC]])
            if total_cost != 0.0:
                dict_entry[QIFC] = total_cost / qty
        if dict_entry:
            WTWPrices = WTWQTDetails.AddNewRow()
            for each in dict_entry:
                WTWPrices['GUID'] = material.UniqueIdentifier
                if each == 'QI_UnitWTWCost':
                    WTWPrices['QI_FoWTWCost'] = dict_entry[each]
                else:
                    WTWPrices[each] = dict_entry[each]
    if WTWQTDetails.Rows.Count > 0:
        WTWQTDetails.Save()
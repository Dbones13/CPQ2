from Scripting.QuoteTables import AccessLevel

#Declaring local variables/object
lineItemsProductList = []
quoteTableDict = {"Solution Enhancement Support Program" : "Renewal_Summary","BGP inc Matrikon" : "BGP_Renewal_Summary", "Third Party Services" : "SC_ThirdParty_Renewal_Summary", "Cyber" : "Cyber_Renewal_Summary","MES Performix":"MES_Renewal_Summary", "Honeywell Digital Prime":"Honeywell_Digital_Prime", "Hardware Refresh":"Hardware_Refresh_Renewal_Summary","Hardware Warranty":"Hardware_Warranty_Renewal_Summary","QCS 4.0":"QCS_4_0", "Experion Extended Support - RQUP ONLY":"RQUP_Renewal_Summary", "Condition Based Maintenance":"CBM_Renewal_Summary","Enabled Services":"SC_ES_Renewal_Summary","Labor":"SC_Labor_Module_Renewal_Summary","Parts Management":["SC_Parts_Management_Summary","SC_Parts_Replacement_Summary"],"Trace":"QT_SC_Trace_Renewal_Summary","Workforce Excellence Program" : "Workforce_Excellence_Program","Local Support Standby":"SC_LocalStandbySupport_Renewal_Summary", "Generic Module":"Genericl_Module_Renewal_Summary"}

quoteTableColDict = {"Hardware Warranty":["Asset"],"Hardware Refresh":["Asset"],"BGP inc Matrikon":["Model_Number"]}
prdTypeDict = {}
#Loop through main line items in quote and get the products which are added
for item in Quote.MainItems:
    if item.QI_SC_ItemFlag.Value == "Hidden" and item.IsComplete:
        lineItemsProductList.append(item.ProductName)
        SC_Product_Type = next((val.Values[0].Display for val in item.SelectedAttributes if val.Name == 'SC_Product_Type'), None)
        if SC_Product_Type:
            prdTypeDict[item.ProductName] = SC_Product_Type
#Check if SESP is with enabled services, as in quote line items enabled services will be shown separately
    if item.PartNumber == "Enabled Services":
        lineItemsProductList.append(item.PartNumber)

#Check if quote line items product available in quote table dictionary then do not hide otherwise hide the quote table
for productNameKey in quoteTableDict.keys():
    if productNameKey not in lineItemsProductList:
        if productNameKey == "Parts Management":
            for quoteTableList in quoteTableDict[productNameKey]:
                Quote.QuoteTables.Item[quoteTableList].AccessLevel = AccessLevel.Hidden
                Quote.QuoteTables.Item[quoteTableList].Rows.Clear()
        elif productNameKey != "Parts Management":
            Quote.QuoteTables.Item[quoteTableDict[productNameKey]].AccessLevel = AccessLevel.Hidden
            Quote.QuoteTables.Item[quoteTableDict[productNameKey]].Rows.Clear()
    else:
        if productNameKey in quoteTableColDict.keys():
            if prdTypeDict.get(productNameKey, None) not in (None, "Renewal"):
                for columnsToHide in quoteTableColToHide:
                    Quote.QuoteTables[quoteTableDict[productNameKey]].GetColumnByName(columnsToHide).AccessLevel = AccessLevel.Hidden
        if productNameKey == "Parts Management":
            for quoteTableList in quoteTableDict[productNameKey]:
                Quote.QuoteTables.Item[quoteTableList].AccessLevel = AccessLevel.Editable
        elif productNameKey != "Parts Management":
            Quote.QuoteTables.Item[quoteTableDict[productNameKey]].AccessLevel = AccessLevel.Editable
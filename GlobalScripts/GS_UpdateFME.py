#GS_UpdateFME updates FME column in Quote tables if there is a change in QI_FME value.
LV_QuoteItemGuid = Quote.GetGlobal('GV_QuoteItemGuid')
LV_FmeValue = Quote.GetGlobal('GV_FMEValue')
VCModelConfiguration = Quote.QuoteTables["VCModelConfiguration"]
ETO_Table = Quote.QuoteTables['PMC_ETO_Selection']
modelDecode_table = Quote.QuoteTables["PMC_FP_ModelDecode"]
#optable=Quote.QuoteTables["Optional_FP_Items"] #CXCPQ-46820:Commented
wstable = Quote.QuoteTables["WS_Table"]
for item in Quote.Items:
    for row in VCModelConfiguration.Rows:
        VCAttrValue = row["AttributeValue"].replace('(','').replace(')','')
        VCAttrDesc = row["AttributeDescription"].replace('(','').replace(')','')
        var = item.PartNumber+'-'
        if  var in VCAttrValue and row["CartItemGUID"] == LV_QuoteItemGuid:
            row["AttributeValue"] = LV_FmeValue
            Trace.Write(row["AttributeValue"])
        if  var in VCAttrDesc and row["CartItemGUID"] == LV_QuoteItemGuid:
            row["AttributeDescription"] = LV_FmeValue
            Trace.Write(row["AttributeDescription"])
if modelDecode_table.Rows.Count > 0:
    for row in modelDecode_table.Rows:
        if row["CartItemGUID"] == LV_QuoteItemGuid:
            row["Full_Model_Code"] = LV_FmeValue
#CXCPQ-46820:Commented :Start
''''if optable.Rows.Count > 0:
    for row in optable.Rows:
        if row["CartItemGUID"] == LV_QuoteItemGuid:
            row["ModelNumber_Op"] = LV_FmeValue'''
#CXCPQ-46820:Commented: end
if wstable.Rows.Count > 0:
    for row in wstable.Rows:
        if row["Item_Guid"] == LV_QuoteItemGuid:
            row["ModelCode"] = LV_FmeValue
if ETO_Table.Rows.Count > 0:
    for row in ETO_Table.Rows:
        if row["CartItemGUID"] == LV_QuoteItemGuid:
            row["FME"] = LV_FmeValue
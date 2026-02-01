isR2Qquote = True if Quote.GetCustomField("isR2QRequest").Content else False
if isR2Qquote:
    PLC_controlgrpRows = Product.GetContainerByName('Number_UOC_Remote_Groups').Rows
    if PLC_controlgrpRows.Count > 0:
    	PLC_controlgrp = PLC_controlgrpRows[0]
    	PLC_controlgrp.GetColumnByName('Number_UOC_Remote_Groups').HeaderLabel = "Number of Remote Group for ControlEdge UOC Remote Groups (0-10)"

isR2Qquote = True if Quote.GetCustomField("isR2QRequest").Content else False
Checkproduct = Product.ParseString('<*CTX(Product.RootProduct.PartNumber)*>')
if isR2Qquote and Checkproduct == "Migration":
    uocremote_cont = Product.GetContainerByName('UOC_RemoteGroup_Cont')
    for row in uocremote_cont.Rows:
        row.Product.Attr("UOC_RG_Name").AssignValue(row["Remote Group Name"])

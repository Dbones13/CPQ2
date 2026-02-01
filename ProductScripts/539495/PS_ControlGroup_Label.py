isR2Qquote = True if Quote.GetCustomField("isR2QRequest").Content else False
Trace.Write("plc-ce-isR2Qquote="+str(isR2Qquote))
if isR2Qquote:
    PLC_controlgrpRows = Product.GetContainerByName('Number_PLC_Control_Groups').Rows
    Trace.Write("plc-ce-PLC_controlgrpRows="+str(PLC_controlgrpRows.Count))
    if PLC_controlgrpRows.Count > 0:
    	PLC_controlgrp = PLC_controlgrpRows[0]
        Checkproduct = Product.ParseString('<*CTX(Product.RootProduct.PartNumber)*>')
        if Checkproduct == "Migration":
            PLC_controlgrp.GetColumnByName('Number_PLC_Control_Groups').HeaderLabel = "Number of CE PLC Control Groups (1-10)"
        else:
    		PLC_controlgrp.GetColumnByName('Number_PLC_Control_Groups').HeaderLabel = "Number of CE PLC Control Groups (1-32)"
        Trace.Write("plc-ce-Number_PLC_Control_Groups="+str(PLC_controlgrp.GetColumnByName('Number_PLC_Control_Groups').HeaderLabel))
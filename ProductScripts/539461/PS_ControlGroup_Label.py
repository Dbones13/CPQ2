isR2Qquote = True if Quote.GetCustomField("isR2QRequest").Content else False
if isR2Qquote:
    PLC_controlgrpRows = Product.GetContainerByName('Number_UOC_Control_Groups').Rows
    if PLC_controlgrpRows.Count > 0:
    	PLC_controlgrp = PLC_controlgrpRows[0]
    	PLC_controlgrp.GetColumnByName('Number_UOC_Control_Groups').HeaderLabel = "Number of CE UOC Control Groups (1-10)"

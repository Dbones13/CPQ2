TabName=''
for tab in Product.Tabs:
    if tab.IsSelected:
        TabName=tab.Name
        break;
if TabName != 'Part Summary':
    ScriptExecutor.ExecuteGlobal('HCI_ProductAttr_Validation')
    #ScriptExecutor.ExecuteGlobal('HCI_PHD_PartSummary')
    #part_summ_trace = Product.GetContainerByName("Trace_Software_Added_Parts_Common_Container")
    #part_summ_trace.Clear()
if Quote.GetCustomField('R2Q_Save').Content == 'Submit':
	ScriptExecutor.ExecuteGlobal('HCI_ProductAttr_Validation')
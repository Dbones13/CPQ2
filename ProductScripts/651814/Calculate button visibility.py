if Session["calculate"] == "yes" and Quote.GetCustomField('IsR2QRequest').Content != 'Yes':
	Product.AllowAttr('Calculation_Button')
	Product.Attr("Calculation_Button").Access = AttributeAccess.Editable
if Quote.GetCustomField('IsR2QRequest').Content == 'Yes':
	if Session["calculate"] == "yes":
		Product.Attributes.GetByName('Trigger_r2q_rules').AssignValue('True')
	ScriptExecutor.ExecuteGlobal('R2Q_HCI_Attributepermission', {'prd_name':Product.Name})
	ScriptExecutor.ExecuteGlobal('HCI_ProductAttr_Validation')
if Quote.GetCustomField('R2Q_Save').Content == 'Submit':
	ScriptExecutor.ExecuteGlobal('HCI_ProductAttr_Validation')
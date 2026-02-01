batch_unit_attrs = ['No_of_Batch_Unit_Copies(Replica of Master Units)','No_of_Product_on_Copy_Unit',
		'Number_of_Batch_Units (Master Units)  (0-100)','Number_of_Product(Master Recipes)  (0-100)','Number_of_Complex_Compexity_QA_Documents  (0-100)','Number_of_Medium_Compexity_QA_Documents  (0-100)','Number_of_Simple_Compexity_QA_Documents  (0-100)']
process_type = Product.Attr('C300_Process_Type').GetValue()
if process_type != 'Batch-Pharma' or process_type != 'Batch-Chemical':
	for attr in batch_unit_attrs:
		Product.DisallowAttr(attr)
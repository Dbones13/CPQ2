process_type = Product.Attr('C300_Process_Type').GetValue()
scope = Product.Attr('CE_Scope_Choices').GetValue()

batchpharma_attr = [
	'Number_of_Complex_Compexity_QA_Documents  (0-100)',
	'Number_of_Medium_Compexity_QA_Documents  (0-100)',
	'Number_of_Simple_Compexity_QA_Documents  (0-100)'
]

batchchemical_attr = [
	'No_of_Batch_Unit_Copies(Replica of Master Units)',
	'No_of_Product_on_Copy_Unit',
	'Number_of_Batch_Units (Master Units)  (0-100)',
	'Number_of_Product(Master Recipes)  (0-100)'
]

if process_type == 'None' or process_type == '':
	Product.Attr('C300_Process_Type').SelectDisplayValue('None')
	for attr in batchpharma_attr + batchchemical_attr:
		Product.DisallowAttr(attr)


if process_type not in ['Batch-Chemical', 'Batch-Pharma']:
	for attr in batchpharma_attr + batchchemical_attr:
		Product.DisallowAttr(attr)

if process_type == 'Batch-Chemical':
	Product.AllowAttr('Input_Quality (User Requirement Specification)')
	Product.Attr('Input_Quality (User Requirement Specification)').AssignValue('Function Plan available(One revision) 40 %')

	for attr in batchchemical_attr:
		Product.AllowAttr(attr)
		if Product.Attr(attr).GetValue() == '':
			Product.Attr(attr).AssignValue('0')

	for attr in batchpharma_attr:
		Product.DisallowAttr(attr)


if process_type == 'Batch-Pharma':
	Product.AllowAttr('Input_Quality (User Requirement Specification)')
	Product.Attr('Input_Quality (User Requirement Specification)').AssignValue('Function Plan available(One revision) 40 %')

	for attr in batchpharma_attr:
		Product.AllowAttr(attr)
		if Product.Attr(attr).GetValue() == '':
			Product.Attr(attr).AssignValue('0')

	for attr in batchchemical_attr:
		Product.AllowAttr(attr)
		if Product.Attr(attr).GetValue() == '':
			Product.Attr(attr).AssignValue('0')
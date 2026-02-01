process_type = Product.Attr('C300_Process_Type').GetValue()
if process_type in ('Batch-Chemical','Batch-Pharma'):
	Product.Attr('No_of_Batch_Unit_Copies(Replica of Master Units)').AssignValue('0')
	Product.Attr('No_of_Product_on_Copy_Unit').AssignValue('0')
	Product.Attr('Number_of_Batch_Units (Master Units)  (0-100)').AssignValue('0')
	Product.Attr('Number_of_Product(Master Recipes)  (0-100)').AssignValue('0')
Product.Attr('R2QRequest').AssignValue('Yes')
Product.Attr("R2Q_QuoteNumber").AssignValue(str(Quote.CompositeNumber))

def getContainer(Name):
	return Product.GetContainerByName(Name)

def hideContainerColumns(contColumnList):
	for contColumn in contColumnList:
		for col in contColumnList[contColumn]:
			TagParserProduct.ParseString('<*CTX( Container({0}).Column({1}).SetPermission(Hidden) )*>'.format(contColumn,col))


container = Product.GetContainerByName('UOC_Common_Questions_Cont')
if container.Rows.Count == 0:
	container.AddNewRow('R2Q_ControlEdge_UOC_System_cpq',False)
TagParserProduct.ParseString('<*CTX ( Container(UOC_Common_Questions_Cont).Row(1).Column(UOC_Exp_PKS_software_release).Set(R530) )*>')

container = Product.GetContainerByName('UOC_Labor_Details')
if container.Rows.Count == 0:
	container.AddNewRow(False)


control_container = Product.GetContainerByName('Number_UOC_Control_Groups')
if control_container.Rows.Count == 0:
	control_container.AddNewRow(False)

control_container.Rows[0].SetColumnValue('Number_UOC_Control_Groups', '1')

#to hide process details
process_cont = {"UOC_Labor_Details":["UOC_Num_Batch_Units_Master_Labour","UOC_Num_Batch_Units_Copies_Replica_Master_Labour","UOC_Num_Product_Master_Recipes_Labour","UOC_Num_Product_Copy_Unit_Product_Replicated_Unit","UOC_Num_Complex_SCMs_Per_Unit_Labour","UOC_Num_Complex_Operations_Per_Product_Labour"]}
process_type = Product.GetContainerByName('UOC_Labor_Details').Rows[0].GetColumnByName("UOC_Process_Type_Labour").Value
if process_type == 'None':
	hideContainerColumns(process_cont)
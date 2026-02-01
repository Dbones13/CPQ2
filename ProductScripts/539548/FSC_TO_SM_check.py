container = Product.GetContainerByName('CONT_MSID_SUBPRD')
ehpm_ehpmx_c300pm_check=''
C200_to_C300_check=''
C200_to_UOC_check= ''
FSC_TO_SM_check=''
FSC_TO_SM_IO_check=''
for row in container.Rows:
	if row['Selected_Products'] == 'EHPM/EHPMX/ C300PM':
		if row.Product.Attr('xPM_Select_the_migration_scenario').GetValue().Contains('xPM to EHPMX'):
			ehpm_ehpmx_c300pm_check = '1'
		else:
			ehpm_ehpmx_c300pm_check = '0'
		Product.Attr('xPM to EHPMX_check').AssignValue(ehpm_ehpmx_c300pm_check)
	if row['Selected_Products'] =='C200 Migration':
		if row.Product.Attr('C200_Select_Migration_Scenario').GetValue().Contains('C200 to C300'):
			C200_to_C300_check = '1'
			Product.Attr('C200_300_check').AssignValue(C200_to_C300_check)
		elif row.Product.Attr('C200_Select_Migration_Scenario').GetValue().Contains('C200 to ControlEdge UOC'):
			C200_to_UOC_check = '1'
			Product.Attr('C200_UOC_check').AssignValue(C200_to_UOC_check)
		else:
 			C200_to_UOC_check='0'
 			C200_to_C300_check = '0'
 			Product.Attr('C200_300_check').AssignValue(C200_to_C300_check)
 			Product.Attr('C200_UOC_check').AssignValue(C200_to_UOC_check)
	if row['Selected_Products'] =='FSC to SM':
		FSC_TO_SM_check='1'
		Product.Attr('FSC_TO_SM_check').AssignValue(FSC_TO_SM_check)
	if row['Selected_Products'] =='FSC to SM IO Migration':
		FSC_TO_SM_IO_check='1'
		Product.Attr('FSC_TO_SM_IO_check').AssignValue(FSC_TO_SM_IO_check)
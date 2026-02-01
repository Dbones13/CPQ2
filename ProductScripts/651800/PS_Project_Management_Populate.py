if Product.Attr('R2QRequest').GetValue() != 'Yes':
	from GS_CyberProductModule import CyberProduct

	cyber = CyberProduct(Quote, Product, TagParserQuote)

	# Populate Project Management Container
	projectManagementCon = Product.GetContainerByName('Cyber_Labor_Project_Management')
	generic_con = Product.GetContainerByName('Generic_System_Activities')
	if projectManagementCon is not None and projectManagementCon.Rows.Count == 0:
		cyber.populateprojectManagementCon(projectManagementCon)
	else:
		not_allowed = cyber.hide_year('Cyber_Labor_Project_Management')
		for row in projectManagementCon.Rows:
			row.Product.DisallowAttrValues('PM_Cyber_Execution_Year_Container', *not_allowed)
			row.Calculate()
		if generic_con and generic_con.Rows.Count>0:
			not_allowed = cyber.hide_year('Cyber Generic System')
			for row in generic_con.Rows:
				row.Product.DisallowAttrValues('Generic_Execution_Year_Container', *not_allowed)
				row.Calculate()

	cyber.populateprojectManagementSummary()
	cyber.populategenericsystemsummary()
	if Product.GetContainerByName('Generic_System_PartsSummary').Rows.Count>0:
		Product.AllowAttr('Generic_System_PartsSummary')
	else:
		Product.DisallowAttr('Generic_System_PartsSummary')

Session['Scope'] = Product.Attr('CYBER_Scope_Choices').GetValue()
#To show or hide FDS & DDS,FAT Document,SAT Document attributes based on selected products
CyberPrd=Product.Attr('AR_CyberPrdChoices').GetValue()
selectPrdsFlag=0
#PCNPrdsFlag=0
for row in Product.GetContainerByName('Cyber Configurations').Rows:
	prd=row['Part Desc']
	'''if prd=='PCN Hardening':
		PCNPrdsFlag=1'''
	if prd=='PCN Hardening' or prd=='Cyber App Control' or prd=='MSS':
		selectPrdsFlag=1
if CyberPrd in ['PCN Hardening','Cyber App Control','MSS'] or selectPrdsFlag:
	Product.Attr('FDS & DDS Documentation Required').Access = AttributeAccess.Editable
	Product.Attr('FAT Document Verification and Execution').Access = AttributeAccess.Editable
	Product.Attr('SAT Document Verification and Execution').Access = AttributeAccess.Editable
	'''if CyberPrd=='PCN Hardening' or PCNPrdsFlag==1:
		Product.Attr('SAT Document Verification and Execution').SelectValue('Yes')'''
else:
	Product.Attr('FDS & DDS Documentation Required').Access = AttributeAccess.Hidden
	Product.Attr('FAT Document Verification and Execution').Access = AttributeAccess.Hidden
	Product.Attr('SAT Document Verification and Execution').Access = AttributeAccess.Hidden
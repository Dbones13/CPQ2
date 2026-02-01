def getServiceProduct(Quote):
	sespTypeSP = ''
	accountName = Quote.GetCustomField("Account Name").Content if Quote and Quote.GetCustomField("Account Name").Content else " "
	getMSID = Product.Attr('Migration_MSID_Choices').GetValue()
	sespCurr = SqlHelper.GetFirst("Select * from MSID where SFDCIdentifier IS NOT NULL and Service_Product !=''  and MSID = '{}' and Account_Name='{}'" .format(getMSID,accountName))
	if sespCurr is not None:
		sespTypeSP= sespCurr.Service_Product
		if sespTypeSP == 'SESP Software Flex':
			return 'Yes'
		elif sespTypeSP == 'SESP Support Flex':
			return 'No'
	return 'Yes'

if Quote.GetCustomField("isR2QRequest").Content == 'Yes':
	Product.Attr('SESP_TYPE').AssignValue('')
if Product.Attr('SESP_TYPE').GetValue() == '':
	sespType = ''
	sesp = Quote.GetCustomField("Entitlement").Content if Quote and Quote.GetCustomField("Entitlement").Content else ""
	Trace.Write(sesp)
	if sesp in ['K&E Pricing Plus', 'Non-SESP MSID with new SESP Plus']:
		sespType = 'Yes'
	elif sesp in ['', 'Non-SESP MSID with new SESP Flex']:
		sespType = 'No'
	elif sesp in ['K&E Pricing Flex']:
		sespType = getServiceProduct(Quote)
	else:
		sespType = 'No'
	Product.Attr('SESP_TYPE').AssignValue(sespType)
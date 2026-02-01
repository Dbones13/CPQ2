from CPQ_SF_SC_Modules import CL_SC_Modules
ContractID      = Quote.GetCustomField("SC_CF_Parent_Contract_Number_Link").Content
class_contact_modules = CL_SC_Modules(Quote, TagParserQuote, None,Session)
resp = class_contact_modules.get_ContractRenewalLineItem_Data(ContractID)
reference_number=Quote.GetCustomField("SC_CF_Parent_Quote_Number_Link").Content
Trace.Write(reference_number)
entitlaments=[]
service_product=[]
Trace.Write(Product.Attr('SC_Product_Type').GetValue())
if Product.Attr('SC_Product_Type').GetValue() is not None and Product.Attr('SC_Product_Type').GetValue() == 'Renewal' and reference_number == '' :
	if resp and "records" in resp:
		recordList = resp["records"]
		for record in recordList:
			userData = record["Service_Product_Name__c"]
			enti=record["Name"]
			entitlaments.append(str(enti))
			service_product.append(str(userData))
			Trace.Write(str(entitlaments))
			if Product.Name =="Hardware Refresh" and Product.Name in service_product:
				Product.Attr('SC_ServiceProduct_HR_RWL').AssignValue('Hardware Refresh')
				Product.Attr('SC_ServiceProduct_HR_RWL').Access = AttributeAccess.ReadOnly
				setDefaultValues = SqlHelper.GetList("select ServiceProduct, Entitlement from CT_SC_ENTITLEMENTS_DATA where IsMandatory = 'FALSE' and ServiceProduct = '{}'".format('Hardware Refresh'))
				con = Product.GetContainerByName('SC_Entitlements_HR_RWL')
				if Product.GetContainerByName('SC_Entitlements_HR_RWL').Rows.Count <1:
					for i in setDefaultValues:
						n = con.AddNewRow(False)
						n['SC_Entitlement_HR_RWL'] = i.Entitlement
						if ['SC_Entitlement_HR_RWL'] in entitlaments:
							n.IsSelected = False
					else:
						con.Calculate()
				for i in con.Rows:
					if i['SC_Entitlement_HR_RWL'] in entitlaments:
						i.IsSelected = True
						break
			elif Product.Name  =="Hardware Warranty" and Product.Name in service_product:
				Product.Attr('SC_ServiceProduct_HR_RWL').AssignValue('Hardware Warranty')
				Product.Attr('SC_ServiceProduct_HR_RWL').Access = AttributeAccess.ReadOnly
				break
if Product.Attr('SC_Product_Type').GetValue() == 'Renewal':
    Product.Attr('SC_ServiceProduct_HR_RWL').Access = AttributeAccess.ReadOnly
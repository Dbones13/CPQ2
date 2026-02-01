from GS_R2Q_Product_Attribute_ContColms import MigrationProductsAttributesContainerColumns as PRD


def r2qsetDefaultdrop():
	attr_value = Product.Attr("C200_Select_Migration_Scenario").GetValue()
	containerMapping = {'C200_Migration_General_Qns_Cont': {'C200_Connection _to_Experion_Server': 'FTE','C200_Type_of_UOC':'UOC','C200_Type_of_downlink_communication_UOC':'CNET Redundant','C200_Is_Honeywell_Providing_FTE_cables':'Yes','C200_Average_Cable_Length':'2m'}}
	for contName, colDetails in containerMapping.items():
		system_cont = Product.GetContainerByName(contName).Rows
		for key, val in colDetails.items():
			emptyval=system_cont[0][key]
			#Trace.Write("bbb"+emptyval)
			if str(emptyval)=='':
				if key == 'C200_Type_of_downlink_communication_UOC':
					if attr_value == "C200 to ControlEdge UOC":
						system_cont[0].Product.Attr(key).SelectDisplayValue(str(val))
				else:
					system_cont[0].Product.Attr(key).SelectDisplayValue(str(val))

	contc200migrat = {'C200_Migration_Config_Cont': {'C200_Series_A_IO_in_Controller_Rack_Non-Redundant': 'No','C200_Number_of_CNI_segments':'1','C200_Cabinet_type_customer_plans':'Existing PM cabinet','C200_Existing_PM_or_Non_Standard_Cabinet_Used':'New Front & Rear Access Series C Cabinet'}}
	for contName, colDetails in contc200migrat.items():
		system_cont = Product.GetContainerByName(contName).Rows
		if system_cont.Count > 0:
			for row in system_cont:
				for key, val in colDetails.items():
					emptyval = row[key]
					#Trace.Write("bbb"+emptyval)
					if str(emptyval) in ['', '- none -']:
						if key in ('C200_Series_A_IO_in_Controller_Rack_Non-Redundant','C200_Number_of_CNI_segments'):
							if attr_value == "C200 to ControlEdge UOC":
								row[key] = str(val)
								row.Product.Attr(key).SelectDisplayValue(str(val))
								Product.ParseString('<*CTX( Container({}).Row().Column({}).Set({}) )*>'.format(contName, key, str(val)))
						else:
							row[key] = str(val)
							row.Product.Attr(key).AssignValue(str(val))
							row.Product.Attr(key).SelectDisplayValue(str(val))
							Product.ParseString('<*CTX( Container({}).Row().Column({}).Set({}) )*>'.format(contName, key, str(val)))
			row.Calculate()
def populate_dvm():
	attributes_dict={"DVM_Number_of_DVM_Workstations":"Numbers_of_CCTV_Work_Stations",
					"DVM_Number_of_Explosion_Proof_PTZ_Cameras":"Numbers_of_PTZ_Type_Camera_at_Hazardous_Area",
					"DVM_Number_of_Weather_Proof_PTZ_Cameras":"Numbers_of_PTZ_Type_Camera_at_Safe_Area",
					"DVM_Number_of_Explosion_Proof_Fixed_Cameras": "Numbers_of_FIXED_Type_Camera_at_Hazardous_Area",
					"DVM_Number_of_Interior_Fixed_Cameras": "Numbers_of_FIXED_Type_Camera_Indoor",
					"DVM_Number_of_Weather_Proof_Fixed_Cameras": "Numbers_of_FIXED_Type_Camera_at_Safe_Area",
					"DVM_Number_of_Interior_PTZ_Cameras":"Numbers_of_PTZ_Type_Camera_Indoor"
					}
	for attr_key, attr_value in attributes_dict.items():
		dvm_value = Product.Attr(attr_value).GetValue()
		Product.Attr(attr_key).AssignValue(str(dvm_value))
	total_value = 0
	for attr_value in ("Numbers_of_FIXED_Type_Camera_at_Hazardous_Area", "Numbers_of_PTZ_Type_Camera_at_Hazardous_Area", "Numbers_of_FIXED_Type_Camera_at_Safe_Area", "Numbers_of_PTZ_Type_Camera_at_Safe_Area", "Numbers_of_FIXED_Type_Camera_Indoor", "Numbers_of_PTZ_Type_Camera_Indoor"):
			value = Product.Attr(attr_value).GetValue()
			if value and value.isdigit():
				total_value += int(value)
	for row in Product.GetContainerByName('DVM_System_Group_Cont').Rows:
			row.Product.Attr('DVM_4_Camera_Interface').AssignValue(str(int(total_value/4)))

def hideAttr(attrList):
	for attr in attrList:
		Product.Attr(attr).Access = AttributeAccess.Hidden

def showAttr(attrList):
	for attr in attrList:
		Product.Attr(attr).Access = AttributeAccess.Editable

def readAttr(attrList):
	for attr in attrList:
		Product.Attr(attr).Access = AttributeAccess.ReadOnly

def setDisplayValue(attrDict):
	for attr,values in attrDict.items():
		#values = ''.join(attrDict[attr])
		Product.Attr(attr).SelectDisplayValue(values)

def setDefaultText(attrDict):
	for attr, value in attrDict.items():
		if (productName in ('FDM Upgrade 1', 'FDM Upgrade 2', 'FDM Upgrade 3') and Product.Attr(attr).GetValue() == '') or productName in ('Terminal Manager','HC900 Group', 'Fire Detection & Alarm Engineering','Industrial Security (Access Control)', 'Digital Video Manager', 'Digital Video Manager Group'):
			#values = ''.join(attrDict[attr])
			Product.Attr(attr).AssignValue(value)

def hideContainerColumns(contColumnList):
	for contColumn in contColumnList:
		for col in contColumnList[contColumn]:
			TagParserProduct.ParseString('<*CTX( Container({0}).Column({1}).SetPermission(Hidden) )*>'.format(contColumn,col))

def showContainerColumns(contColumnList):
	for contColumn in contColumnList:
		for col in contColumnList[contColumn]:
			TagParserProduct.ParseString('<*CTX( Container({0}).Column({1}).SetPermission(Editable) )*>'.format(contColumn,col))

def VSTriggerAttrHide():
	platform = Product.Attr('VS_Platform_Options').GetValue()
	if productName in PRD.VSproducts:
		if platform == 'Essentials - Lifecycle Bid':
			Product.AllowAttr('Virtualization_Additional On Site Activities hours')
			value = Product.Attr('Virtualization_Additional On Site Activities hours').GetValue()
			if not value:
				Product.Attr('Virtualization_Additional On Site Activities hours').AssignValue('0')
			hideAttr(PRD.VSproducts[productName].get('premium_show',[]))
			showAttr(PRD.VSproducts[productName].get('ownOS_attr',[]))
			showAttr(PRD.VSproducts[productName].get('essentials_show',[]))
		elif platform in ['Number of Performance A Servers (0-9 per cluster)','Number of Performance B Servers (0-9 per cluster)']:
			hideAttr(PRD.VSproducts[productName].get('essentials_show',[]))
			hideAttr(PRD.VSproducts[productName].get('ownOS_attr',[]))
			showAttr(PRD.VSproducts[productName].get('premium_show',[]))
			#Trace.Write("cluster_v91="+str(PRD.VSproducts[productName].get('premium_show',[])))
			#Trace.Write("cluster_v9="+str(Product.Attr("Virtualization_Number_of_Clusters_in_the_network").GetValue()))
			#Trace.Write("cluster_v92="+str(PRD.VSproducts[productName].get('premium_show',[])))
		else:
			hideAttr(PRD.VSproducts[productName].get('essentials_show',[]))
			hideAttr(PRD.VSproducts[productName].get('premium_show',[]))
			showAttr(PRD.VSproducts[productName].get('ownOS_attr',[]))

productName = Product.Name
Trace.Write('productName ' + str(productName))
checkproduct = Product.ParseString('<*CTX(Product.RootProduct.PartNumber)*>')
if Quote.GetCustomField('isR2QRequest').Content == 'Yes':
	Product.Attr('R2QRequest').AssignValue('Yes')
	Product.Attr('R2Q_QuoteNumber').AssignValue(str(Quote.CompositeNumber))
	if checkproduct =='Migration':
		if productName in PRD.products:
			hideAttr(PRD.products[productName].get('hideAttrList', []))
			hideContainerColumns(PRD.products[productName].get('hideContainerColumnDict', {}))
			showContainerColumns(PRD.products[productName].get('showContainerColumnDict', {}))
			showAttr(PRD.products[productName].get('showAttrList', []))
			readAttr(PRD.products[productName].get('readAttrList', []))
			setDisplayValue(PRD.products[productName].get('displayValueDict', {}))
			setDefaultText(PRD.products[productName].get('defaultText', {}))
			Trace.Write("dvm-data="+str(PRD.products[productName]))
			if productName == "Digital Video Manager":
				populate_dvm()
			elif productName == "C200 Migration":
				r2qsetDefaultdrop()
			if Quote.GetGlobal('VSFlag') == 'True' and productName in ('Virtualization System','Virtualization System Migration') :
				VSTriggerAttrHide()
				Quote.SetGlobal('VSFlag','False')

else:
	Product.Attr('R2QRequest').AssignValue('')
	hideAttr(PRD.products[productName].get('nonR2QHideAttrList', []))
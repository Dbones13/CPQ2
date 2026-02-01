import GS_SM_CompA1_Calcs,GS_SM_Comp_B_CNMPart_Calc
import System.Decimal as D
#parts_dict={}
def get_parts(Product, parts_dict):
	A = GS_SM_CompA1_Calcs.get_CompA1(Product)
	Experion_integration = Product.GetContainerByName('SM_CG_Common_Questions_Cont').Rows[0].GetColumnByName('SM_Experion_Integration').DisplayValue
	DNP3 = Product.GetContainerByName('SM_CG_Common_Questions_Cont').Rows[0].GetColumnByName('SM_DNP3_ProtocolLicense').Value
	IO_Link = Product.GetContainerByName('SM_CG_Common_Questions_Cont').Rows[0].GetColumnByName('SM_Switch_Safety_IO').Value
	Safenet_Options = Product.GetContainerByName('SM_CG_Common_Questions_Cont').Rows[0].GetColumnByName('SM_Safenet_Options').DisplayValue
	Safety_Builder_Options = Product.GetContainerByName('SM_CG_Common_Questions_Cont').Rows[0].GetColumnByName('SM_Safety_Builder_Options').DisplayValue
	Third_Party_Communication_Options = Product.GetContainerByName('SM_CG_Common_Questions_Cont').Rows[0].GetColumnByName('SM_ThirdParty_Communication_Options').DisplayValue
	switch_safety_io = Product.GetContainerByName('SM_CG_Common_Questions_Cont').Rows[0].GetColumnByName('SM_Switch_Safety_IO').DisplayValue

	count = 0
	qty = 0
	#CXCPQ-33264 & 33262 & 33260
	if Experion_integration in ["SCADA", "Advanced (CDA)"]:
		count += 2
		if Safenet_Options == "Via third party MOXA Separate Red Ethernet":
			count += 2
		if Safety_Builder_Options != "Via FTE" and Third_Party_Communication_Options == "Via Ethernet":
			count += 1
		elif Safety_Builder_Options != "Via FTE" or Third_Party_Communication_Options == "Via Ethernet":
			count += 1
		#CXCPQ-33263
		qty += 1 if Experion_integration == "SCADA" else 2
		if Safety_Builder_Options in ["Via Separate Ethernet", "Via FTE"]:
			qty += 1
			if Safenet_Options in ["Via CNM Separate Red Ethernet", "Via third party MOXA Separate Red Ethernet"]:
				qty += 1
			if Third_Party_Communication_Options == "Via Ethernet":
				qty += 1
	#CXCPQ-33236
	if parts_dict.get("FC-TCNT11") and float(parts_dict.get("FC-TCNT11")['Quantity']) > 0:
		parts_dict["50194005-001"] = {'Quantity': int(count), 'Description': 'HIGH SPEED ETHERNET SWITCH SDW-550-EC'}
		parts_dict["FS-CCI-HSE-02"] = {'Quantity': int(qty), 'Description': 'Internal communication cables '}
		parts_dict["FS-PDC-FTA24P"] = {'Quantity': 2, 'Description': 'Experion Integration FS-PDC-FTA24P'} if Experion_integration in ["SCADA", "Advanced (CDA)"] else parts_dict.get("FS-PDC-FTA24P", {'Quantity': 0, 'Description': ''})

	if DNP3 in ["Small", "Medium", "Large"]:
		parts_dict["FS-SC-DNP3-{}".format(DNP3[0])] = {'Quantity': 1, 'Description': 'SMSC DNP3 OUTSTATION {} LICENSE'.format(DNP3.upper())}
	#CXCPQ-33261
	if IO_Link=="Control Network Module (CNM)":
		pass
	if Safenet_Options == "Via CNM Separate Red Ethernet" and Product.Attr('SM_CG_Safety_IO_Link').GetValue() == "Control Network Module (CNM)" and A['M'] > 0:
		C1 = 2 * (D.Ceiling(A['M']))
		C2 = 2 * (int(A['M']))
		C3 = C1 - C2
		var = 2 + C3
		var1 = 2 + C1
		parts_dict["50165649-001"] = {'Quantity': var, 'Description': 'FILLER PLATE ASSEMBLY,CNM'}
		parts_dict["CC-INWM01"] = {'Quantity': var1, 'Description': 'CHASSIS FOR NON-REDUNDANT I/O MODULES CC'}
		parts_dict["CC-TNWD01"] = {'Quantity': var1, 'Description': 'A.R.T. CHASSIS FOR CONTROL PROCESSOR'}
	elif Safenet_Options == "Via CNM Separate Red Ethernet" and Product.Attr('SM_CG_Safety_IO_Link').GetValue() != "Control Network Module (CNM)":
		if parts_dict.get("FC-TCNT11") and float(parts_dict.get("FC-TCNT11")['Quantity']) > 0:
			parts_dict["50165649-001"] = {'Quantity': 2, 'Description': 'FILLER PLATE ASSEMBLY,CNM'}
			parts_dict["CC-INWM01"] = {'Quantity': 2, 'Description': 'CHASSIS FOR NON-REDUNDANT I/O MODULES CC'}
			parts_dict["CC-TNWD01"] = {'Quantity': 2, 'Description': 'A.R.T. CHASSIS FOR CONTROL PROCESSOR'}

	if switch_safety_io == "Third Party MOXA" and parts_dict.get("FC-TCNT11") and float(parts_dict.get("FC-TCNT11")['Quantity']) > 0:
		# CXCPQ-37625
		parts_dict["FS-CCI-HSE-30"] = {'Quantity': 1, 'Description': 'SM RIO ETHERNET CABLE SET L=3.0M'}

	return parts_dict
#Ans=get_parts(Product,parts_dict)
#Trace.Write("Ans "+str(Ans))
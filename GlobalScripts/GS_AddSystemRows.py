def AddRows(rowCount, container):
	get_sysid = SqlHelper.GetFirst("Select CHILD_SYSTEM_ID from R2Q_ATTRIBUTE_MAPPING where PRODUCT_NAME='"+str(Product.Name)+"'")
	sysid = get_sysid.CHILD_SYSTEM_ID if get_sysid else ""
	for i in range(rowCount):
		if container.Name == 'CE_SystemGroup_Cont':
			row = container.AddNewRow(False)
			row.Product.Attr("CE_System_Index").AssignValue(str(row.RowIndex + 1))
			row.Product.Attr('CE_Scope_Choices').SelectDisplayValue('HW/SW + LABOR')
			row.Product.ApplyRules()
			row.ApplyProductChanges()
			row.Calculate()
			Log.Info('if == product name== '+str(Product.Name))
		else:
			if Product.Name == "Experion Enterprise Group":
				#Log.Info("list cluster add")
				row = container.AddNewRow(False)
				Loc_Clus_Nw_Grp_cnt = Product.GetContainerByName('List of Locations/Clusters/Network Groups')
				if Loc_Clus_Nw_Grp_cnt.Rows.Count>0:
					#Log.Info("list cluster add if")
					i=1
					for row in Loc_Clus_Nw_Grp_cnt.Rows:
						Network_Group_Name = row.Product.Attr('List of Locations/Clusters/ Network_Groups').GetValue()
						if str(row["List of Locations/Clusters/ Network Groups"]) != Network_Group_Name and Quote.GetCustomField('IsR2QRequest').Content != 'Yes':
							row.Product.Attr('List of Locations/Clusters/ Network_Groups').AssignValue(TagParserProduct.ParseString('Location/Cluster/Network Group<* Eval(<*CTX( MyContainer.CurrentRow.Index )*>+1) *>'))
							row.Product.Attr('List_Of_Location_Clusters_Number').AssignValue(str(i))

							i=i+1
							row.ApplyProductChanges()
			elif Product.Name in ("Experion Enterprise System","R2Q Experion Enterprise System"):
				row1 = container.AddNewRow(sysid,False)
				exeperionEntContainer = Product.GetContainerByName('Experion_Enterprise_Cont')
				if exeperionEntContainer.Rows.Count > 0:
					i=1
					for row in exeperionEntContainer.Rows:
						Sys_Group_Name = row.Product.Attr('Experion Enterprise Group Name').GetValue()
						if str(row["Experion Enterprise Group Name"]) != Sys_Group_Name:
							row.Product.Attr('Experion Enterprise Group Name').AssignValue(str(row["Experion Enterprise Group Name"]))
						row.Product.Attr('Experion Enterprise Group Number').AssignValue(str(i))
						i = i + 1
						row.ApplyProductChanges()
				row1.Product.Attr('PERF_ExecuteScripts').AssignValue('SCRIPT_RUN')
				row1.Product.ApplyRules()
			elif Product.Name in ("Series-C Control Group","C300 System","R2Q C300 System","R2Q Series-C Control Group","R2Q ControlEdge UOC System","R2Q UOC Control Group","ControlEdge UOC System", "UOC Control Group","eServer System","R2Q eServer System","Field Device Manager","R2Q Field Device Manager","3rd Party Devices/Systems Interface (SCADA)", "R2Q 3rd Party Devices/Systems Interface (SCADA)","SM Control Group", "R2Q SM Control Group", "R2Q Safety Manager ESD","R2Q Safety Manager FGS", "Safety Manager ESD", "Safety Manager FGS"):
				row1 = container.AddNewRow(sysid,False)
				Log.Info('Outside == product name== '+str(Product.Name))
				if Product.Name in ("SM Control Group", "R2Q SM Control Group", "R2Q Safety Manager ESD","R2Q Safety Manager FGS", "Safety Manager ESD", "Safety Manager FGS", "3rd Party Devices/Systems Interface (SCADA)", "R2Q 3rd Party Devices/Systems Interface (SCADA)"):
					row1.Product.Attr('PERF_ExecuteScripts').AssignValue('SCRIPT_RUN')
					row1.Product.ApplyRules()
					Log.Info('Inside == product name== '+str(Product.Name))
			else:
				Log.Info('else == product name== '+str(Product.Name))
				container.AddNewRow(False)
if Product.Name == "New / Expansion Project":
	SG_cont = Product.GetContainerByName('Number_System_Groups').Rows[0]
	SG_rowCount = SG_cont.GetColumnByName('Number_System_Groups').Value
	SG_rowCount = int(SG_rowCount) if SG_rowCount else 0
	CE_SystemGroup_Cont = Product.GetContainerByName('CE_SystemGroup_Cont')
	try:
		AddRows(SG_rowCount, CE_SystemGroup_Cont)
	except:
		Product.Attr('ExceededLimit').AssignValue('True')
		pass
elif Product.Name in ["ControlEdge PLC System","ControlEdge PLC System Migration"]:
	if Quote.GetCustomField('IsR2QRequest').Content == 'Yes' and Product.Name in ("ControlEdge PLC System", "ControlEdge PLC System Migration"):
		Product.GetContainerByName('PLC_ControlGroup_Cont').Max = 10
	CG_cont = Product.GetContainerByName('Number_PLC_Control_Groups').Rows[0]
	PLC_CGCount = CG_cont.GetColumnByName('Number_PLC_Control_Groups').Value
	PLC_CGCount = int(PLC_CGCount) if PLC_CGCount else 0
	PLC_CG_Cont = Product.GetContainerByName('PLC_ControlGroup_Cont')
	try:
		AddRows(PLC_CGCount, PLC_CG_Cont)
	except:
		Product.Attr('ExceededLimit').AssignValue('True')
		pass
elif Product.Name == "CE PLC Control Group":
	if Quote.GetCustomField('IsR2QRequest').Content == 'Yes' and Product.Name == "CE PLC Control Group":
		Product.GetContainerByName('PLC_RemoteGroup_Cont').Max = 10
	RG_cont = Product.GetContainerByName('Number_PLC_Remote_Groups').Rows[0]
	PLC_RGrowCount = RG_cont.GetColumnByName('Number_PLC_Remote_Groups').Value
	PLC_RGrowCount = int(PLC_RGrowCount) if PLC_RGrowCount else 0
	PLC_RG_Cont = Product.GetContainerByName('PLC_RemoteGroup_Cont')
	try:
		AddRows(PLC_RGrowCount, PLC_RG_Cont)
	except:
		Product.Attr('ExceededLimit').AssignValue('True')
		pass
elif Product.Name in ["ControlEdge UOC System Migration","ControlEdge UOC System","R2Q ControlEdge UOC System"]:
	if Quote.GetCustomField('IsR2QRequest').Content == 'Yes' and Product.Name in ("R2Q ControlEdge UOC System", "ControlEdge UOC System Migration"):
		Product.GetContainerByName('UOC_ControlGroup_Cont').Max = 10
	UOC_CG_cont = Product.GetContainerByName('Number_UOC_Control_Groups').Rows[0]
	UOC_CGrowCount = UOC_CG_cont.GetColumnByName('Number_UOC_Control_Groups').Value
	UOC_CGrowCount = int(UOC_CGrowCount) if UOC_CGrowCount else 0
	UOC_CG_Cont = Product.GetContainerByName('UOC_ControlGroup_Cont')
	try:
		AddRows(UOC_CGrowCount,UOC_CG_Cont)
	except:
		Product.Attr('ExceededLimit').AssignValue('True')
		pass
elif Product.Name in ["ControlEdge CN900 System"]:
	CN900_CG_cont = Product.GetContainerByName('Number_CN900_Control_Groups').Rows[0]
	CN900_CGrowCount = CN900_CG_cont.GetColumnByName('Number_CN900_Control_Groups').Value
	CN900_CGrowCount = int(CN900_CGrowCount) if CN900_CGrowCount else 0
	CN900_CG_Cont = Product.GetContainerByName('CN900_ControlGroup_Cont')
	try:
		AddRows(CN900_CGrowCount,CN900_CG_Cont)
	except:
		Product.Attr('ExceededLimit').AssignValue('True')
		pass
elif Product.Name in ["UOC Control Group","R2Q UOC Control Group"]:
	if Quote.GetCustomField('IsR2QRequest').Content == 'Yes' and Product.Name == 'R2Q UOC Control Group':
		Product.GetContainerByName('UOC_RemoteGroup_Cont').Max = 10
	if Quote.GetCustomField('IsR2QRequest').Content == 'Yes' and Product.Name == 'UOC Control Group':
		Product.GetContainerByName('UOC_RemoteGroup_Cont').Max = 12
	UOC_RG_cont = Product.GetContainerByName('Number_UOC_Remote_Groups').Rows[0]
	UOC_RGrowCount = UOC_RG_cont.GetColumnByName('Number_UOC_Remote_Groups').Value
	UOC_RGrowCount = int(UOC_RGrowCount) if UOC_RGrowCount else 0
	UOC_RG_Cont = Product.GetContainerByName('UOC_RemoteGroup_Cont')
	try:
		AddRows(UOC_RGrowCount,UOC_RG_Cont)
	except:
		Product.Attr('ExceededLimit').AssignValue('True')
		pass
#Add by Raja/Himanshu for RTU Logic
elif Product.Name == "ControlEdge RTU System":
	RTU_CG_cont = Product.GetContainerByName('Number_RTU_Control_Groups').Rows[0]
	RTU_CGrowCount = RTU_CG_cont.GetColumnByName('Number_RTU_Control_Groups').Value
	RTU_CGrowCount = int(RTU_CGrowCount) if RTU_CGrowCount else 0
	RTU_CG_Cont = Product.GetContainerByName('RTU_ControlGroup_Cont')
	try:
		AddRows(RTU_CGrowCount,RTU_CG_Cont)
	except:
		Product.Attr('ExceededLimit').AssignValue('True')
		pass
#SAFETY MANAGER CXCPQ-94841,CXCPQ-95052,CXCPQ-94832 and CXCPQ-95015
elif Product.Name in ['Safety Manager ESD', 'Safety Manager FGS', 'Safety Manager BMS', 'Safety Manager HIPPS','R2Q Safety Manager ESD','R2Q Safety Manager FGS']:
	if Quote.GetCustomField('IsR2QRequest').Content == 'Yes':
		Product.GetContainerByName('SM_ControlGroup_Cont').Max = 10
	SM_CG_cont = Product.GetContainerByName('Number_SM_Control_Groups_Cont').Rows[0]
	SM_CGrowCount = SM_CG_cont.GetColumnByName('Number_SM_Control_Groups').Value
	SM_CGrowCount = int(SM_CGrowCount) if SM_CGrowCount else 0
	SM_CG_Cont = Product.GetContainerByName('SM_ControlGroup_Cont')
	try:
		AddRows(SM_CGrowCount,SM_CG_Cont)
	except:
		Product.Attr('ExceededLimit').AssignValue('True')
		pass
elif Product.Name in ["SM Control Group","R2Q SM Control Group"]:
	if Quote.GetCustomField('IsR2QRequest').Content == 'Yes':
		Product.GetContainerByName('SM_RemoteGroup_Cont').Max = 10
	SM_RG_cont = Product.GetContainerByName('Number_SM_Remote_Groups_Cont').Rows[0]
	SM_RGrowCount = SM_RG_cont.GetColumnByName('Number_SM_Remote_Groups').Value
	SM_RGrowCount = int(SM_RGrowCount) if SM_RGrowCount else 0
	SM_RG_Cont = Product.GetContainerByName('SM_RemoteGroup_Cont')
	try:
		AddRows(SM_RGrowCount,SM_RG_Cont)
	except:
		Product.Attr('ExceededLimit').AssignValue('True')
		pass     
elif Product.Name == "Experion HS System":
	Experion_Attr_count= Product.Attr('HS_Number_of_Experion').GetValue()
	Experion_Attr_count = int(Experion_Attr_count) if Experion_Attr_count else 0
	Experion_HS_Cont = Product.GetContainerByName('Experion_HS_Cont')
	try:
		AddRows(Experion_Attr_count,Experion_HS_Cont)
	except:
		Product.Attr('ExceededLimit').AssignValue('True')
		pass
elif Product.Name == "Experion Enterprise System":
	Experion_Attr_count= Product.Attr('Number of Experion Enterprise Groups').GetValue()
	Experion_Attr_count = int(Experion_Attr_count) if Experion_Attr_count else 0
	Experion_Enterprise_Cont = Product.GetContainerByName('Experion_Enterprise_Cont')
	try:
		AddRows(Experion_Attr_count,Experion_Enterprise_Cont)
	except:
		Product.Attr('ExceededLimit').AssignValue('True')
		pass
elif Product.Name == "R2Q Experion Enterprise System":
	Product.GetContainerByName('Experion_Enterprise_Cont').Max = 1
	Experion_Attr_count= Product.Attr('Number of Experion Enterprise Groups').GetValue()
	Experion_Attr_count = int(Experion_Attr_count) if Experion_Attr_count else 0
	Experion_Enterprise_Cont = Product.GetContainerByName('Experion_Enterprise_Cont')
	try:
		AddRows(Experion_Attr_count,Experion_Enterprise_Cont)
	except:
		Product.Attr('ExceededLimit').AssignValue('True')
		pass
elif Product.Name == "HC900 System":
	HC900_Attr_count= Product.Attr('Number_of_HC900').GetValue()
	HC900_Attr_count = int(HC900_Attr_count) if HC900_Attr_count else 0
	HC900_Cont = Product.GetContainerByName('HC900_Cont')
	try:
		AddRows(HC900_Attr_count,HC900_Cont)
	except:
		Product.Attr('ExceededLimit').AssignValue('True')
		pass
elif Product.Name == "PlantCruise System":
	PlantCruise_Attr_count= Product.Attr('Number_of_PlantCruise').GetValue()
	PlantCruise_Attr_count = int(PlantCruise_Attr_count) if PlantCruise_Attr_count else 0
	PlantCruise_Cont = Product.GetContainerByName('PlantCruise_Cont')
	try:
		AddRows(PlantCruise_Attr_count,PlantCruise_Cont)
	except:
		Product.Attr('ExceededLimit').AssignValue('True')
		pass
elif Product.Name == "ControlEdge PCD System":
	PCD_Attr_count= Product.Attr('Number_of_PCD').GetValue()
	PCD_Attr_count = int(PCD_Attr_count) if PCD_Attr_count else 0
	PCD_Cont = Product.GetContainerByName('PCD_Cont')
	try:
		AddRows(PCD_Attr_count,PCD_Cont)
	except:
		Product.Attr('ExceededLimit').AssignValue('True')
		pass
elif Product.Name in ["3rd Party Devices/Systems Interface (SCADA)", "R2Q 3rd Party Devices/Systems Interface (SCADA)"]:
	if Quote.GetCustomField('IsR2QRequest').Content == 'Yes':
		Product.GetContainerByName('Scada_CCR_Unit_Cont').Max = 10
	Scada_CCR_Unit_Count= Product.Attr('Scada_CCR_Unit_Count').GetValue()
	Scada_CCR_Unit_Count = int(Scada_CCR_Unit_Count) if Scada_CCR_Unit_Count else 0
	Scada_CCR_Unit_Cont = Product.GetContainerByName('Scada_CCR_Unit_Cont')
	try:
		AddRows(Scada_CCR_Unit_Count,Scada_CCR_Unit_Cont)
		#row1 = container.AddNewRow(sysid,False)
	except:
		Product.Attr('ExceededLimit').AssignValue('True')
		pass
elif Product.Name == "Experion Enterprise Group":

	Experion_Attr_count= Product.Attr('Number of Locations_Clusters_Network').GetValue()
	Experion_Attr_count = int(Experion_Attr_count) if Experion_Attr_count else 0
	Location_cluster = Product.GetContainerByName('List of Locations/Clusters/Network Groups')
	try:
		AddRows(Experion_Attr_count,Location_cluster)
		Product.Attr('PERF_ExecuteScripts').AssignValue('SCRIPT_RUN')
	except:
		Product.Attr('ExceededLimit').AssignValue('True')
		pass
elif Product.Name == "Experion MX System":
	MX_Scanner_Group_Count= Product.Attr('MX_Scanner_Group_Count').GetValue()
	MX_Scanner_Group_Count = int(MX_Scanner_Group_Count) if MX_Scanner_Group_Count else 0
	MX_Scanner_group = Product.GetContainerByName('MX_Scanner_group')
	try:
		AddRows(MX_Scanner_Group_Count,MX_Scanner_group)
	except:
		Product.Attr('ExceededLimit').AssignValue('True')
		pass
elif Product.Name == "Scanner Group":
	MX_sensor_count= Product.Attr('MX_sensor_count').GetValue()
	MX_sensor_count = int(MX_sensor_count) if MX_sensor_count else 0
	MX_Sensor_Group = Product.GetContainerByName('MX_Sensor_Group')
	scanner_type = Product.Attr('MX_SG_Type_of_Scanner').GetValue()
	try:
		AddRows(MX_sensor_count,MX_Sensor_Group)
	except:
		Product.Attr('ExceededLimit').AssignValue('True')
		pass
elif Product.Name == "MXProLine System":
	MXP_Scanner_Group_Count= Product.Attr('MXP_Scanner_Group_Count').GetValue()
	MXP_Scanner_Group_Count = int(MXP_Scanner_Group_Count) if MXP_Scanner_Group_Count else 0
	MXP_Scanner_group = Product.GetContainerByName('MXP_Scanner_group')
	try:
		AddRows(MXP_Scanner_Group_Count,MXP_Scanner_group)
	except:
		Product.Attr('ExceededLimit').AssignValue('True')
		pass
elif Product.Name == "QCS-SE System":
	MXP_Scanner_Group_Count= Product.Attr('MXP_Scanner_Group_Count').GetValue()
	MXP_Scanner_Group_Count = int(MXP_Scanner_Group_Count) if MXP_Scanner_Group_Count else 0
	QCS_Scanner_group = Product.GetContainerByName('QCS_Scanner_group')
	try:
		AddRows(MXP_Scanner_Group_Count,QCS_Scanner_group)
	except:
		Product.Attr('ExceededLimit').AssignValue('True')
		pass
elif Product.Name == "Simulation System":
	SS_Count= Product.Attr('SS_Count').GetValue()
	SS_Count = int(SS_Count) if SS_Count else 0
	SS_Group = Product.GetContainerByName('SS_Group')
	try:
		AddRows(SS_Count,SS_Group)
	except:
		Product.Attr('ExceededLimit').AssignValue('True')
		pass
elif Product.Name == "MXP Scanner Group":
	MXP_sensor_count= Product.Attr('MXP_sensor_count').GetValue()
	MXP_sensor_count = int(MXP_sensor_count) if MXP_sensor_count else 0
	MXP_Sensor_Group = Product.GetContainerByName('MXP_Sensor_Group')
	try:
		AddRows(MXP_sensor_count,MXP_Sensor_Group)
	except:
		Product.Attr('ExceededLimit').AssignValue('True')
		pass
elif Product.Name == "QCS Scanner Group":
	MXP_sensor_count= Product.Attr('MXP_sensor_count').GetValue()
	MXP_sensor_count = int(MXP_sensor_count) if MXP_sensor_count else 0
	QCS_Sensor_Group = Product.GetContainerByName('QCS_Sensor_Group')
	try:
		AddRows(MXP_sensor_count,QCS_Sensor_Group)
	except:
		Product.Attr('ExceededLimit').AssignValue('True')
		pass
elif Product.Name == "Electrical Substation Data Collector":
	ESDC_Count= Product.Attr('ESDC_Count').GetValue()
	ESDC_Count = int(ESDC_Count) if ESDC_Count else 0
	ESDC_Group = Product.GetContainerByName('ESDC_Group')
	try:
		AddRows(ESDC_Count,ESDC_Group)
	except:
		Product.Attr('ExceededLimit').AssignValue('True')
		pass
elif Product.Name in ["eServer System", "R2Q eServer System"]:
	if Quote.GetCustomField('IsR2QRequest').Content == 'Yes':
		Product.GetContainerByName('ES_Group').Max = 1
	ES_Count= Product.Attr('ES_Count').GetValue()
	ES_Count = int(ES_Count) if ES_Count else 0
	ES_Group = Product.GetContainerByName('ES_Group')
	try:
		AddRows(ES_Count,ES_Group)
	except:
		Product.Attr('ExceededLimit').AssignValue('True')
		pass
elif Product.Name == "C300 System":
	if Quote.GetCustomField('IsR2QRequest').Content == 'Yes':
		Product.GetContainerByName('Series_C_Control_Groups_Cont').Max = 10
	group_count= Product.Attr('Number_of_Series_C_Control_Groups').GetValue()
	group_count = int(group_count) if group_count else 0
	cont = Product.GetContainerByName('Series_C_Control_Groups_Cont')
	try:
		AddRows(group_count,cont)
	except:
		Product.Attr('ExceededLimit').AssignValue('True')
elif Product.Name == "Series-C Control Group":
	if Quote.GetCustomField('IsR2QRequest').Content == 'Yes':
		Product.GetContainerByName('Series_C_Remote_Groups_Cont').Max = 10
	group_count= Product.Attr('Number_of_Series_C_Remote_Groups').GetValue()
	group_count = int(group_count) if group_count else 0
	cont = Product.GetContainerByName('Series_C_Remote_Groups_Cont')
	try:
		AddRows(group_count,cont)
		Product.Attr('PERF_ExecuteScripts').AssignValue('SCRIPT_RUN')
	except:
		Product.Attr('ExceededLimit').AssignValue('True')
elif Product.Name == "R2Q C300 System":
	if Quote.GetCustomField('IsR2QRequest').Content == 'Yes':
		Product.GetContainerByName('Series_C_Control_Groups_Cont').Max = 10
	group_count= Product.Attr('Number_of_Series_C_Control_Groups').GetValue()
	group_count = int(group_count) if group_count else 0
	cont = Product.GetContainerByName('Series_C_Control_Groups_Cont')
	try:
		AddRows(group_count,cont)
	except:
		Product.Attr('ExceededLimit').AssignValue('True')
elif Product.Name == "R2Q Series-C Control Group":
	if Quote.GetCustomField('IsR2QRequest').Content == 'Yes':
		Product.GetContainerByName('Series_C_Remote_Groups_Cont').Max = 10
	group_count= Product.Attr('Number_of_Series_C_Remote_Groups').GetValue()
	group_count = int(group_count) if group_count else 0
	cont = Product.GetContainerByName('Series_C_Remote_Groups_Cont')
	try:
		AddRows(group_count,cont)
		#Product.Attr('PERF_ExecuteScripts').AssignValue('SCRIPT_RUN')
	except:
		Product.Attr('ExceededLimit').AssignValue('True')
elif Product.Name in ["Field Device Manager", "R2Q Field Device Manager"]:
	if Quote.GetCustomField('IsR2QRequest').Content == 'Yes':
		Product.GetContainerByName('FDM_System_Group_Cont').Max = 1
	group_count= Product.Attr('No. of FDM System groups').GetValue()
	group_count = int(group_count) if group_count else 0
	cont = Product.GetContainerByName('FDM_System_Group_Cont')
	try:
		AddRows(group_count,cont)
	except:
		Product.Attr('ExceededLimit').AssignValue('True')
elif Product.Name == "Digital Video Manager":
	group_count= Product.Attr('Number_of_Experion_DVM_Group').GetValue()
	group_count = int(group_count) if group_count else 0
	cont = Product.GetContainerByName('DVM_System_Group_Cont')
	try:
		AddRows(group_count,cont)
	except:
		Product.Attr('ExceededLimit').AssignValue('True')
elif Product.Name == "ARO, RESS & ERG System":
	group_count= Product.Attr('Number_of_Experion_ARO_Group').GetValue()
	group_count = int(group_count) if group_count else 0
	cont = Product.GetContainerByName('ARO_System_Group_Cont')
	try:
		AddRows(group_count,cont)
	except:
		Product.Attr('ExceededLimit').AssignValue('True')
def CG_Cal(part,cg_num):
	qty=int(part.get("CG_{0}".format(cg_num-1),0))
	return qty if cg_num==2 else qty+CG_Cal(part,cg_num-1)

salesOrg = Quote.GetCustomField('Sales Area').Content
query = SqlHelper.GetList("Select Part_Number from HPS_LABOR_COST_DATA where Sales_Org='{}' ".format(salesOrg))
labor_parts = [x.Part_Number for x in query]
plc_part_list = []
project = ""

for item in Quote.MainItems:
	if item.PartNumber == 'PRJT':
		project = item
		break

parts_dict = { #Sample values
 "900CP1-0200":
	{"Description":"Control Processor Module",
	 "PLC System":"3",
	 "CG_1":"1",
	 "CG_1_RG_1": "21",
	 "CG_1_RG_2": "4",
	 "CG_1_RG_3": "7",
	 "CG_2": "52",
	 "CG_2_RG_1": "5",
	 "Total": 153
	},
 "900R04-0200":
	{"Description":"4 I/O Slot Rack – Non-Redundant Power (Assembly)",
	 "PLC System":"8",
	 "CG_1":"8"
	}
}
parts_dict = {}
sg_num = 0
ioSum1=[]
scada=[]
uoccontrol=[]
esdcontrol = []
fgscontrol = []
cg_rg_map = {}
esd_cg_rg_map = {}
fgs_cg_rg_map ={}
names_dict = {}
for x in range(32):
	names_dict["CG_{0}".format(x+1)] = row = {}
	row["SG_1"] = row["SG_2"] = row["SG_3"] = row["SG_4"] = row["SG_5"] = row["SG_6"] = row["SG_7"] = row["SG_8"] = row["SG_9"] = row["SG_10"] = "Not Applicable"
	for y in range(16):
		names_dict["CG_{0}_RG_{1}".format(x+1,y+1)] = row = {}
		row["SG_1"] = row["SG_2"] = row["SG_3"] = row["SG_4"] = row["SG_5"] = row["SG_6"] = row["SG_7"] = row["SG_8"] = row["SG_9"] = row["SG_10"] = "Not Applicable"
if project != "":
	for sys_group in project.Children:
		sg_num += 1
		#system_group = parts_dict["{}".format(sg_num)] = {}
		system_group = parts_dict[sg_num] = {}
		system_group["SG_Name"] = sys_group.PartNumber
		for system in sys_group.Children:
			system_items = system_group["{0}".format(system.ProductName)] = {}
			Trace.Write('System Name:')
			Trace.Write(system.ProductName)
			if system.ProductName in ['ControlEdge PLC System']:
				cg_num = 0
				for plc_child in system.Children:
					if plc_child.ProductName in ['CE PLC Control Group']:
						cg_num += 1
						rg_num = 0
						names_dict["CG_{0}".format(cg_num)]["SG_{0}".format(sg_num)] = plc_child.PartNumber
						for control_group_child in plc_child.Children:
							if control_group_child.ProductName in ['CE PLC Remote Group']:
								rg_num += 1
								names_dict["CG_{0}_RG_{1}".format(cg_num, rg_num)]["SG_{0}".format(sg_num)] = plc_child.PartNumber
								for rg_part in control_group_child.Children:
									if rg_part.PartNumber not in system_items: #New part needs to be added
										part = system_items[rg_part.PartNumber] = {}
										part["Description"] = rg_part.ProductName
										part["Product_Line"] = str(rg_part.QI_PLSG.Value)
										part["Total"] = int(rg_part.Quantity)
										part["CG_{0}_RG_{1}".format(cg_num, rg_num)] = str(rg_part.Quantity)
									else: #Product already exists
										part = system_items[rg_part.PartNumber]
										part["Total"] += int(rg_part.Quantity)
										part["CG_{0}_RG_{1}".format(cg_num, rg_num)] = str(rg_part.Quantity)
							else: #normal control group parts
								if control_group_child.PartNumber not in system_items: #New part needs to be added
									part = system_items[control_group_child.PartNumber] = {}
									part["Description"] = control_group_child.ProductName
									part["Product_Line"] = str(control_group_child.QI_PLSG.Value)
									part["Total"] = int(control_group_child.Quantity)
									part["CG_{0}".format(cg_num)] = str(control_group_child.Quantity)
								else: #Product already exists
									part = system_items[control_group_child.PartNumber]
									part["Total"] += int(control_group_child.Quantity)
									part["CG_{0}".format(cg_num)] = str(control_group_child.Quantity)
					elif plc_child.PartNumber not in labor_parts: #plc system parts, excluded labor
						if plc_child.PartNumber not in system_items: #New part needs to be added
							part = system_items[plc_child.PartNumber] = {}
							part["Description"] = plc_child.ProductName
							part["Product_Line"] = str(plc_child.QI_PLSG.Value)
							part["Total"] = int(plc_child.Quantity)
							part["System_Items"] = str(plc_child.Quantity)
						else: #Product already exists
							part = system_items[plc_child.PartNumber]
							part["Total"] += int(plc_child.Quantity)
							part["System_Items"] = str(plc_child.Quantity)
			elif system.ProductName in ['ControlEdge UOC System']:
				contr = system.SelectedAttributes.GetContainerByName('UOC_ControlGroup_Cont')
				if contr:
					for row in contr.Rows:
						control_group_name = row['Control Group Name']
						uoccontrol.append(row['Control Group Name'])
						uoc_control_name = "|".join(uoccontrol)
						cg_rg_map[control_group_name] = []
				for item in filter(lambda item: item.ProductName.startswith("UOC Control Group"), system.Children):
					contr1 = item.SelectedAttributes.GetContainerByName('UOC_RemoteGroup_Cont')
					if contr1:
						control_group_name = item.PartNumber 
						if control_group_name in cg_rg_map:
							for row in contr1.Rows:
								remote_group_name = row['Remote Group Name']
								cg_rg_map[control_group_name].append(remote_group_name)
				for control_group_name in cg_rg_map:
					while len(cg_rg_map[control_group_name]) < 10:
						cg_rg_map[control_group_name].append("")
				cg_num = 0
				for uoc_child in system.Children:
					if uoc_child.ProductName in ['UOC Control Group']:
						cg_num += 1
						rg_num = 0
						names_dict["CG_{0}".format(cg_num)]["SG_{0}".format(sg_num)] = uoc_child.PartNumber
						for control_group_child in uoc_child.Children:
							if control_group_child.ProductName in ['UOC Remote Group']:
								rg_num += 1
								names_dict["CG_{0}_RG_{1}".format(cg_num, rg_num)]["SG_{0}".format(sg_num)] = uoc_child.PartNumber
								for rg_part in control_group_child.Children:
									if rg_part.PartNumber not in system_items: #New part needs to be added
										part = system_items[rg_part.PartNumber] = {}
										part["Description"] = rg_part.ProductName
										part["Product_Line"] = str(rg_part.QI_PLSG.Value)
										part["Total"] = int(rg_part.Quantity)
										part["CG_{0}_RG_{1}".format(cg_num, rg_num)] = str(rg_part.Quantity)
									else: #Product already exists
										part = system_items[rg_part.PartNumber]
										part["Total"] += int(rg_part.Quantity)
										part["CG_{0}_RG_{1}".format(cg_num, rg_num)] = str(rg_part.Quantity)
							else: #normal control group parts
								if control_group_child.PartNumber not in system_items: #New part needs to be added
									part = system_items[control_group_child.PartNumber] = {}
									part["Description"] = control_group_child.ProductName
									part["Product_Line"] = str(control_group_child.QI_PLSG.Value)
									part["Total"] = int(control_group_child.Quantity)
									part["CG_{0}".format(cg_num)] = str(control_group_child.Quantity)
								else: #Product already exists
									part = system_items[control_group_child.PartNumber]
									part["Total"] += int(control_group_child.Quantity)
									part["CG_{0}".format(cg_num)] = str(control_group_child.Quantity)
					elif uoc_child.PartNumber not in labor_parts: #rtu system parts, excluded labor
						if uoc_child.PartNumber not in system_items: #New part needs to be added
							part = system_items[uoc_child.PartNumber] = {}
							part["Description"] = uoc_child.ProductName
							part["Product_Line"] = str(uoc_child.QI_PLSG.Value)
							part["Total"] = int(uoc_child.Quantity)
							part["System_Items"] = str(uoc_child.Quantity)
						else: #Product already exists
							part = system_items[uoc_child.PartNumber]
							part["Total"] += int(uoc_child.Quantity)
							part["System_Items"] = str(uoc_child.Quantity)
			elif system.ProductName in ['ControlEdge RTU System']:
				cg_num = 0
				for rtu_child in system.Children:
					if rtu_child.ProductName in ['RTU Group']:
						cg_num += 1
						names_dict["CG_{0}".format(cg_num)]["SG_{0}".format(sg_num)] = rtu_child.PartNumber
						for control_group_child in rtu_child.Children:
							if control_group_child.PartNumber not in system_items: #New part needs to be added
								part = system_items[control_group_child.PartNumber] = {}
								part["Description"] = control_group_child.ProductName
								part["Product_Line"] = str(control_group_child.QI_PLSG.Value)
								part["Total"] = int(control_group_child.Quantity)
								part["CG_{0}".format(cg_num)] = str(control_group_child.Quantity)
							else: #Product already exists
								part = system_items[control_group_child.PartNumber]
								part["Total"] += int(control_group_child.Quantity)
								part["CG_{0}".format(cg_num)] = str(control_group_child.Quantity)
					elif rtu_child.PartNumber not in labor_parts: #rtu system parts, excluded labor
						if rtu_child.PartNumber not in system_items: #New part needs to be added
							part = system_items[rtu_child.PartNumber] = {}
							part["Description"] = rtu_child.ProductName
							part["Product_Line"] = str(rtu_child.QI_PLSG.Value)
							part["Total"] = int(rtu_child.Quantity)
							part["System_Items"] = str(rtu_child.Quantity)
						else: #Product already exists
							part = system_items[rtu_child.PartNumber]
							part["Total"] += int(rtu_child.Quantity)
							part["System_Items"] = str(rtu_child.Quantity)

			elif system.ProductName in ['Safety Manager ESD']:
				contr = system.SelectedAttributes.GetContainerByName('SM_ControlGroup_Cont')
				if contr:
					for row in contr.Rows:
						control_group_name = row['Control Group Name']
						esdcontrol.append(row['Control Group Name'])
						esd_control_name = "|".join(esdcontrol)
						esd_cg_rg_map[control_group_name] = []
				
				for item in filter(lambda item: item.ProductName.startswith("SM Control Group"), system.Children):
					contr1 = item.SelectedAttributes.GetContainerByName('SM_RemoteGroup_Cont')
					if contr1:
						control_group_name = item.PartNumber 
						if control_group_name in esd_cg_rg_map:
							for row in contr1.Rows:
								remote_group_name = row['Remote Group Name']
								esd_cg_rg_map[control_group_name].append(remote_group_name)

				for control_group_name in esd_cg_rg_map:
					while len(esd_cg_rg_map[control_group_name]) < 10:
						esd_cg_rg_map[control_group_name].append("")
				cg_num = 0
				for esd_child in system.Children:
					Trace.Write(esd_child.ProductName)
					if esd_child.ProductName in ['SM Control Group']:
						cg_num += 1
						rg_num = 0
						names_dict["CG_{0}".format(cg_num)]["SG_{0}".format(sg_num)] = esd_child.PartNumber
						for control_group_child in esd_child.Children:
							if control_group_child.ProductName in ['SM Remote Group']:
								rg_num += 1
								names_dict["CG_{0}_RG_{1}".format(cg_num, rg_num)]["SG_{0}".format(sg_num)] = esd_child.PartNumber
								for rg_part in control_group_child.Children:
									if rg_part.PartNumber not in system_items: #New part needs to be added
										part = system_items[rg_part.PartNumber] = {}
										part["Description"] = rg_part.ProductName
										part["Product_Line"] = str(rg_part.QI_PLSG.Value)
										part["Total"] = int(rg_part.Quantity)
										part["CG_{0}_RG_{1}".format(cg_num, rg_num)] = str(rg_part.Quantity)
									else: #Product already exists
										part = system_items[rg_part.PartNumber]
										part["Total"] += int(rg_part.Quantity)
										part["CG_{0}_RG_{1}".format(cg_num, rg_num)] = str(rg_part.Quantity)
							else: #normal control group parts
								if control_group_child.PartNumber not in system_items: #New part needs to be added
									part = system_items[control_group_child.PartNumber] = {}
									part["Description"] = control_group_child.ProductName
									part["Product_Line"] = str(control_group_child.QI_PLSG.Value)
									part["Total"] = int(control_group_child.Quantity)
									part["CG_{0}".format(cg_num)] = str(control_group_child.Quantity)
								else: #Product already exists
									part = system_items[control_group_child.PartNumber]
									part["Total"] += int(control_group_child.Quantity)
									part["CG_{0}".format(cg_num)] = str(control_group_child.Quantity)
					elif esd_child.PartNumber not in labor_parts: #rtu system parts, excluded labor
						if esd_child.PartNumber not in system_items: #New part needs to be added
							part = system_items[esd_child.PartNumber] = {}
							part["Description"] = esd_child.ProductName
							part["Product_Line"] = str(esd_child.QI_PLSG.Value)
							part["Total"] = int(esd_child.Quantity)
							part["System_Items"] = str(esd_child.Quantity)
						else: #Product already exists
							part = system_items[esd_child.PartNumber]
							part["Total"] += int(esd_child.Quantity)
							part["System_Items"] = str(esd_child.Quantity)
			elif system.ProductName in ['Safety Manager FGS']:
				contr = system.SelectedAttributes.GetContainerByName('SM_ControlGroup_Cont')
				if contr:
					for row in contr.Rows:
						control_group_name = row['Control Group Name']
						fgscontrol.append(row['Control Group Name'])
						fgs_control_name = "|".join(fgscontrol)
						fgs_cg_rg_map[control_group_name] = []

				for item in filter(lambda item: item.ProductName.startswith("SM Control Group"), system.Children):
					contr1 = item.SelectedAttributes.GetContainerByName('SM_RemoteGroup_Cont')
					if contr1:
						control_group_name = item.PartNumber 
						if control_group_name in fgs_cg_rg_map:
							for row in contr1.Rows:
								remote_group_name = row['Remote Group Name']
								fgs_cg_rg_map[control_group_name].append(remote_group_name)
				for control_group_name in fgs_cg_rg_map:
					while len(fgs_cg_rg_map[control_group_name]) < 10:
						fgs_cg_rg_map[control_group_name].append("")
				cg_num = 0
				for fgs_child in system.Children:
					Trace.Write(fgs_child.ProductName)
					if fgs_child.ProductName in ['SM Control Group']:
						cg_num += 1
						rg_num = 0
						names_dict["CG_{0}".format(cg_num)]["SG_{0}".format(sg_num)] = fgs_child.PartNumber
						for control_group_child in fgs_child.Children:
							if control_group_child.ProductName in ['SM Remote Group']:
								rg_num += 1
								names_dict["CG_{0}_RG_{1}".format(cg_num, rg_num)]["SG_{0}".format(sg_num)] = fgs_child.PartNumber
								for rg_part in control_group_child.Children:
									if rg_part.PartNumber not in system_items: #New part needs to be added
										part = system_items[rg_part.PartNumber] = {}
										part["Description"] = rg_part.ProductName
										part["Product_Line"] = str(rg_part.QI_PLSG.Value)
										part["Total"] = int(rg_part.Quantity)
										part["CG_{0}_RG_{1}".format(cg_num, rg_num)] = str(rg_part.Quantity)
									else: #Product already exists
										part = system_items[rg_part.PartNumber]
										part["Total"] += int(rg_part.Quantity)
										part["CG_{0}_RG_{1}".format(cg_num, rg_num)] = str(rg_part.Quantity)
							else: #normal control group parts
								if control_group_child.PartNumber not in system_items: #New part needs to be added
									part = system_items[control_group_child.PartNumber] = {}
									part["Description"] = control_group_child.ProductName
									part["Product_Line"] = str(control_group_child.QI_PLSG.Value)
									part["Total"] = int(control_group_child.Quantity)
									part["CG_{0}".format(cg_num)] = str(control_group_child.Quantity)
								else: #Product already exists
									part = system_items[control_group_child.PartNumber]
									part["Total"] += int(control_group_child.Quantity)
									part["CG_{0}".format(cg_num)] = str(control_group_child.Quantity)
					elif fgs_child.PartNumber not in labor_parts: #rtu system parts, excluded labor
						if fgs_child.PartNumber not in system_items: #New part needs to be added
							part = system_items[fgs_child.PartNumber] = {}
							part["Description"] = fgs_child.ProductName
							part["Product_Line"] = str(fgs_child.QI_PLSG.Value)
							part["Total"] = int(fgs_child.Quantity)
							part["System_Items"] = str(fgs_child.Quantity)
						else: #Product already exists
							part = system_items[fgs_child.PartNumber]
							part["Total"] += int(fgs_child.Quantity)
							part["System_Items"] = str(fgs_child.Quantity)

			elif system.ProductName in ['Safety Manager BMS']:
				cg_num = 0
				for bms_child in system.Children:
					Trace.Write(bms_child.ProductName)
					if bms_child.ProductName in ['SM Control Group']:
						cg_num += 1
						rg_num = 0
						names_dict["CG_{0}".format(cg_num)]["SG_{0}".format(sg_num)] = bms_child.PartNumber
						for control_group_child in bms_child.Children:
							if control_group_child.ProductName in ['SM Remote Group']:
								rg_num += 1
								names_dict["CG_{0}_RG_{1}".format(cg_num, rg_num)]["SG_{0}".format(sg_num)] = bms_child.PartNumber
								for rg_part in control_group_child.Children:
									if rg_part.PartNumber not in system_items: #New part needs to be added
										part = system_items[rg_part.PartNumber] = {}
										part["Description"] = rg_part.ProductName
										part["Product_Line"] = str(rg_part.QI_PLSG.Value)
										part["Total"] = int(rg_part.Quantity)
										part["CG_{0}_RG_{1}".format(cg_num, rg_num)] = str(rg_part.Quantity)
									else: #Product already exists
										part = system_items[rg_part.PartNumber]
										part["Total"] += int(rg_part.Quantity)
										part["CG_{0}_RG_{1}".format(cg_num, rg_num)] = str(rg_part.Quantity)
							else: #normal control group parts
								if control_group_child.PartNumber not in system_items: #New part needs to be added
									part = system_items[control_group_child.PartNumber] = {}
									part["Description"] = control_group_child.ProductName
									part["Product_Line"] = str(control_group_child.QI_PLSG.Value)
									part["Total"] = int(control_group_child.Quantity)
									part["CG_{0}".format(cg_num)] = str(control_group_child.Quantity)
								else: #Product already exists
									part = system_items[control_group_child.PartNumber]
									part["Total"] += int(control_group_child.Quantity)
									part["CG_{0}".format(cg_num)] = str(control_group_child.Quantity)
					elif bms_child.PartNumber not in labor_parts: #rtu system parts, excluded labor
						if bms_child.PartNumber not in system_items: #New part needs to be added
							part = system_items[bms_child.PartNumber] = {}
							part["Description"] = bms_child.ProductName
							part["Product_Line"] = str(bms_child.QI_PLSG.Value)
							part["Total"] = int(bms_child.Quantity)
							part["System_Items"] = str(bms_child.Quantity)
						else: #Product already exists
							part = system_items[bms_child.PartNumber]
							part["Total"] += int(bms_child.Quantity)
							part["System_Items"] = str(bms_child.Quantity)
			elif system.ProductName in ['Safety Manager HIPPS']:
				cg_num = 0
				for hipps_child in system.Children:
					Trace.Write(hipps_child.ProductName)
					if hipps_child.ProductName in ['SM Control Group']:
						cg_num += 1
						rg_num = 0
						names_dict["CG_{0}".format(cg_num)]["SG_{0}".format(sg_num)] = hipps_child.PartNumber
						for control_group_child in hipps_child.Children:
							if control_group_child.ProductName in ['SM Remote Group']:
								rg_num += 1
								names_dict["CG_{0}_RG_{1}".format(cg_num, rg_num)]["SG_{0}".format(sg_num)] = hipps_child.PartNumber
								for rg_part in control_group_child.Children:
									if rg_part.PartNumber not in system_items: #New part needs to be added
										part = system_items[rg_part.PartNumber] = {}
										part["Description"] = rg_part.ProductName
										part["Product_Line"] = str(rg_part.QI_PLSG.Value)
										part["Total"] = int(rg_part.Quantity)
										part["CG_{0}_RG_{1}".format(cg_num, rg_num)] = str(rg_part.Quantity)
									else: #Product already exists
										part = system_items[rg_part.PartNumber]
										part["Total"] += int(rg_part.Quantity)
										part["CG_{0}_RG_{1}".format(cg_num, rg_num)] = str(rg_part.Quantity)
							else: #normal control group parts
								if control_group_child.PartNumber not in system_items: #New part needs to be added
									part = system_items[control_group_child.PartNumber] = {}
									part["Description"] = control_group_child.ProductName
									part["Product_Line"] = str(control_group_child.QI_PLSG.Value)
									part["Total"] = int(control_group_child.Quantity)
									part["CG_{0}".format(cg_num)] = str(control_group_child.Quantity)
								else: #Product already exists
									part = system_items[control_group_child.PartNumber]
									part["Total"] += int(control_group_child.Quantity)
									part["CG_{0}".format(cg_num)] = str(control_group_child.Quantity)
					elif hipps_child.PartNumber not in labor_parts: #rtu system parts, excluded labor
						if hipps_child.PartNumber not in system_items: #New part needs to be added
							part = system_items[hipps_child.PartNumber] = {}
							part["Description"] = hipps_child.ProductName
							part["Product_Line"] = str(hipps_child.QI_PLSG.Value)
							part["Total"] = int(hipps_child.Quantity)
							part["System_Items"] = str(hipps_child.Quantity)
						else: #Product already exists
							part = system_items[hipps_child.PartNumber]
							part["Total"] += int(hipps_child.Quantity)
							part["System_Items"] = str(hipps_child.Quantity)
			elif system.ProductName == 'PMD System':
				for pmd_parts in system.Children:
					if pmd_parts.PartNumber not in labor_parts: #pmd system parts, excluded labor
						if pmd_parts.PartNumber not in system_items: #New part needs to be added
							part = system_items[pmd_parts.PartNumber] = {}
							part["Description"] = pmd_parts.ProductName
							part["Product_Line"] = str(pmd_parts.QI_PLSG.Value)
							part["Total"] = int(pmd_parts.Quantity)
							part["System_Items"] = str(pmd_parts.Quantity)
						else: #Product already exists
							part = system_items[pmd_parts.PartNumber]
							part["Total"] += int(pmd_parts.Quantity)
							part["System_Items"] = str(pmd_parts.Quantity)
			elif system.ProductName in ['Experion Enterprise System']:
				contr = system.SelectedAttributes.GetContainerByName('Experion_Enterprise_Cont')
				if contr:
					for row in contr.Rows:
						control_group_name = row['Experion Enterprise Group Name']
						ioSum1.append(row['Experion Enterprise Group Name'])
						control_name = "|".join(ioSum1)
				cg_num = 0
				for uoc_child in system.Children:
					Trace.Write(uoc_child.ProductName)
					if uoc_child.ProductName in ['Experion Enterprise Group']:
						cg_num += 1
						rg_num = 0
						names_dict["CG_{0}".format(cg_num)]["SG_{0}".format(sg_num)] = uoc_child.PartNumber
						for control_group_child in uoc_child.Children:
							if control_group_child.ProductName in ['List of Locations/Clusters/ Network Groups']:
								rg_num += 1
								names_dict["CG_{0}".format(cg_num)]["SG_{0}".format(sg_num)] = uoc_child.PartNumber
								for rg_part in control_group_child.Children:
									if rg_part.PartNumber not in system_items: #New part needs to be added
										part = system_items[rg_part.PartNumber] = {}
										part["Description"] = rg_part.ProductName
										part["Product_Line"] = str(rg_part.QI_PLSG.Value)
										part["Total"] = int(rg_part.Quantity)
										part["CG_{0}".format(cg_num)] = str(rg_part.Quantity)
									else: #Product already exists
										part = system_items[rg_part.PartNumber]
										part["Total"] += int(rg_part.Quantity)
										if cg_num > 1:
											part["CG_{0}".format(cg_num)] = str(int(part["Total"])-CG_Cal(part,cg_num))
										else:
											part["CG_{0}".format(cg_num)] = part["Total"]
							else: #normal control group parts
								if control_group_child.PartNumber not in system_items: #New part needs to be added
									part = system_items[control_group_child.PartNumber] = {}
									part["Description"] = control_group_child.ProductName
									part["Product_Line"] = str(control_group_child.QI_PLSG.Value)
									part["Total"] = int(control_group_child.Quantity)
									part["CG_{0}".format(cg_num)] = str(control_group_child.Quantity)
								else: #Product already exists
									part = system_items[control_group_child.PartNumber]
									part["Total"] += int(control_group_child.Quantity)
									part["CG_{0}".format(cg_num)] = str(control_group_child.Quantity)
					elif uoc_child.PartNumber not in labor_parts: #rtu system parts, excluded labor
						if uoc_child.PartNumber not in system_items: #New part needs to be added
							part = system_items[uoc_child.PartNumber] = {}
							part["Description"] = uoc_child.ProductName
							part["Product_Line"] = str(uoc_child.QI_PLSG.Value)
							part["Total"] = int(uoc_child.Quantity)
							part["System_Items"] = str(uoc_child.Quantity)
						else: #Product already exists
							part = system_items[uoc_child.PartNumber]
							part["Total"] += int(uoc_child.Quantity)
							part["System_Items"] = str(uoc_child.Quantity)
			elif system.ProductName in ['3rd Party Devices/Systems Interface (SCADA)']:
				contr = system.SelectedAttributes.GetContainerByName('Scada_CCR_Unit_Cont')
				if contr:
					for row in contr.Rows:
						control_group_name = row['Unit_Location']
						scada.append(row['Unit_Location'])
						scada_name = "|".join(scada)
				cg_num = 0
				for rtu_child in system.Children:
					if rtu_child.ProductName in ['CCR']:
						cg_num += 1
						names_dict["CG_{0}".format(cg_num)]["SG_{0}".format(sg_num)] = rtu_child.PartNumber
						for control_group_child in rtu_child.Children:
							if control_group_child.PartNumber not in system_items: #New part needs to be added
								part = system_items[control_group_child.PartNumber] = {}
								part["Description"] = control_group_child.ProductName
								part["Product_Line"] = str(control_group_child.QI_PLSG.Value)
								part["Total"] = int(control_group_child.Quantity)
								part["CG_{0}".format(cg_num)] = str(control_group_child.Quantity)
							else: #Product already exists
								part = system_items[control_group_child.PartNumber]
								part["Total"] += int(control_group_child.Quantity)
								part["CG_{0}".format(cg_num)] = str(control_group_child.Quantity)
					elif rtu_child.PartNumber not in labor_parts: #rtu system parts, excluded labor
						if rtu_child.PartNumber not in system_items: #New part needs to be added
							part = system_items[rtu_child.PartNumber] = {}
							part["Description"] = rtu_child.ProductName
							part["Product_Line"] = str(rtu_child.QI_PLSG.Value)
							part["Total"] = int(rtu_child.Quantity)
							part["System_Items"] = str(rtu_child.Quantity)
						else: #Product already exists
							part = system_items[rtu_child.PartNumber]
							part["Total"] += int(rtu_child.Quantity)
							part["System_Items"] = str(rtu_child.Quantity)


Trace.Write("PAS BOM parts: {}".format(parts_dict))
#=============================================================
#Section that loops through dictionary and adds it to the quote table
quoteTable = Quote.QuoteTables["BOM_Table_for_Proposals"]
#quoteTable.Rows.Clear()
Serial_number = 0
#s_number = 0
plc_number = 0
pmd_number = 0
rtu_number = 0
uoc_number = 0
Esd_number = 0
Fgs_number = 0
Bms_number = 0
Hipps_number = 0
unit_number = 0
ENT_number = 0
for sg_id,sys_group in sorted(parts_dict.items()):
	for system_name in sys_group:
		if system_name == 'SG_Name': #Skips the name, because it isn't a system.
			continue
		system = sys_group[system_name]

		for part_num in system:
			part = system[part_num]
			row = quoteTable.AddNewRow()
			if system_name == 'ControlEdge PLC System':
				plc_number += 1
				row['S_Number'] = plc_number
			elif system_name == 'PMD System':
				pmd_number += 1
				row['S_Number'] = pmd_number
			elif system_name == 'ControlEdge RTU System':
				rtu_number += 1
				row['S_Number'] = rtu_number
			elif system_name == 'ControlEdge UOC System':
				rtu_number += 1
				row['S_Number'] = rtu_number
				row['CG_Name'] = uoc_control_name
				for i, control_group_name in enumerate(uoccontrol, start=1):
					cg_name = control_group_name
					rg_name = "|".join(cg_rg_map[control_group_name])
					row["CG_" + str(i) + "_RG_NAME"] = rg_name
			elif system_name == 'Safety Manager ESD':
				Esd_number += 1
				row['S_Number'] = Esd_number
				row['CG_Name'] = esd_control_name
				for i, control_group_name in enumerate(esdcontrol, start=1):
					cg_name = control_group_name
					esd_name = "|".join(esd_cg_rg_map[control_group_name])
					row["CG_" + str(i) + "_RG_NAME"] = esd_name
			elif system_name == 'Safety Manager FGS':
				Fgs_number += 1
				row['S_Number'] = Fgs_number
				row['CG_Name'] = fgs_control_name
				for i, control_group_name in enumerate(fgscontrol, start=1):
					cg_name = control_group_name
					fgs_name = "|".join(fgs_cg_rg_map[control_group_name])
					row["CG_" + str(i) + "_RG_NAME"] = fgs_name
			elif system_name == 'Safety Manager BMS':
				Bms_number += 1
				row['S_Number'] = Bms_number
			elif system_name == 'Safety Manager HIPPS':
				Hipps_number += 1
				row['S_Number'] = Hipps_number
			elif system_name == 'Experion Enterprise System':
				ENT_number += 1
				row['S_Number'] = ENT_number
				row['CG_Name'] = control_name
			elif system_name == '3rd Party Devices/Systems Interface (SCADA)':
				#row['System_Items'] = 'SCADA Party Devices Systems Interface'
				unit_number += 1
				row['S_Number'] = unit_number
				row['CG_Name'] = scada_name
			row['Model_Number'] = part_num
			row['Sys_Name'] = 'SCADA Party Devices Systems Interface' if(system_name == '3rd Party Devices/Systems Interface (SCADA)') else system_name
			row['SG_Name'] = sys_group['SG_Name']
			row['SG_ID'] = sg_id

			for entry in part:
				row[entry] = part.get(entry)

if Quote.GetCustomField('R2QFlag').Content == 'Yes':
	area_col = {"ESD": {"Sys_Name": "Write-In Third Party for ESD","SG_Name": "Marshalling","Model_Number": "Write-Ins"},"FGS": {"Sys_Name": "Write-In Third Party for FGS","SG_Name": "Marshalling","Model_Number": "Write-Ins"},"Experion Write-in": {"Sys_Name": "Write-In Third Party for Experion","SG_Name": "Third Party","Model_Number": "Write-Ins"}}
	for item in Quote.MainItems:
		if item.PartNumber == "Write-In Third Party Hardware & Software" and str(item.QI_Area.Value) != "Experion Write-in":
			area_key = str(item.QI_Area.Value).split("_")[0]
			if area_key in area_col:
				area_dict = area_col[area_key]
				row = quoteTable.AddNewRow()
				row['Sys_Name'] = area_dict["Sys_Name"]
				row["Model_Number"] = area_dict["Model_Number"]
				row["Description"] = item.Description
				row["Total"] = item.Quantity
				if area_dict["SG_Name"] == "Marshalling":
					row["SG_Name"] = "Marshalling - " + str(item.QI_Area.Value)
				else:
					row["SG_Name"] = area_dict["SG_Name"]
				if area_key == "ESD":
					Esd_number += 1
					row['S_Number'] = Esd_number
				elif area_key == "FGS":
					Fgs_number += 1
					row['S_Number'] = Fgs_number
				#elif area_key == "Experion":
				#	Serial_number += 1
				#	row['S_Number'] = Serial_number
		if (item.PartNumber) in ["Write-In Third Party Hardware & Software","Write-In Third Party Hardware"] and str(item.QI_Area.Value) == "Experion Write-in":
			row = quoteTable.AddNewRow()
			Serial_number += 1
			row['Sys_Name'] = "Write-In Third Party for Experion"
			row['S_Number'] = Serial_number
			row["Description"] = item.Description
			row["SG_Name"] = "Third Party"
			row["Model_Number"] = "Write-Ins"
			row["Total"] = item.Quantity

quoteTable.Save()

#Section to update names table
names_table = Quote.QuoteTables["PAS_BOM_Group_Names"]
#names_table.Rows.Clear()
for col_name, column_dict in sorted(names_dict.items()):
	column_dict = names_dict[col_name]
	test3 = repr(column_dict)
	test4 = col_name
	row = names_table.AddNewRow()
	row['Column_ID'] = col_name

	for entry in column_dict:
		row[entry] = column_dict.get(entry)

names_table.Save()
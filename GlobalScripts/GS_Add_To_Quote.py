import datetime
from GS_Exp_Ent_Sys_Add_To_Quote import *
from Update_System_Labor_Cost_Price import updateLaborCostPrice
def addToQuote(Product, Quote, TagParserQuote):
	scope = Product.Attr('CE_Scope_Choices').GetValue()
	Log.Info("scope:{}".format(scope))

	if scope == 'HW/SW + LABOR':
		contList = ['SNE', 'SIE', 'HMI']
		contNameDict = {'SNE':'System_Network_Engineering_Labor_Container', 'SIE':'System_Interface_Engineering_Labor_Container', 'HMI':'HMI_Engineering_Labor_Container'}
		contDict = dict()
		contRowsDict = dict()
		for cont in contList:
			contDict[cont] = 'No'
			laborCont = Product.GetContainerByName(contNameDict[cont])
			contRowsDict[cont] = laborCont.Rows.Count

		updateContainer = 1
		updatePrice = 1
		attrList = ['Is Fieldbus Interface in Scope?', 'Is Modbus Interface in Scope?', 'Is Profibus Interface in Scope?', 'Is EtherNet IP Interface in Scope?', 'Is OPC Interface in Scope?', 'Is HART Interface in Scope?', 'Is Terminal Server Interface in Scope?', 'Is DeviceNet Interface in Scope?']
		for attr in attrList:
			val = Product.Attr(attr).GetValue()
			if val == 'Yes':
				contDict['SIE'] = 'Yes'
				break
		if Product.Attr('Is System Network Engineering in Scope?').GetValue() == 'Yes':
			contDict['SNE'] = 'Yes'
		if Product.Attr('Is HMI Engineering in Scope?').GetValue() == 'Yes':
			contDict['HMI'] = 'Yes'

		salesArea = Quote.GetCustomField('Sales Area').Content.strip()
		marketCode = Quote.SelectedMarket.MarketCode
		salesOrg = Quote.GetCustomField('Sales Area').Content
		currency = Quote.GetCustomField('Currency').Content
		query = SqlHelper.GetFirst("select Execution_County from NEW_EXECUTION_COUNTRY_SALES_ORG_MAPPING where Sales_Area = '{}' and Currency = '{}'".format(salesOrg,currency))
		current_year = datetime.datetime.now().year
		if Quote:
			if Quote.GetCustomField('EGAP_Contract_Start_Date').Content != "": #If there is a Contract Start Date in the quote:
				c_start_date = Quote.GetCustomField('EGAP_Contract_Start_Date').Content
				contract_start = int("20"+c_start_date[-2:])
				if contract_start > current_year+3: #Maxes out at 3 years in the future. Can't go beyond that.
					contract_start = current_year+3
			else:
				contract_start = current_year
		else:
			contract_start = current_year

		gesLocation = Product.Attr("Experion_HS_Ges_Location_Labour").GetValue()
		gesMapping = {'GES India':'IN','GES China':'CN','GES Romania':'RO','GES Uzbekistan':'UZ','None':'None','GES Egypt':'EG'}
		gesLocationVC = gesMapping.get(gesLocation)

		if contDict['SIE'] == 'Yes':
			Product.ApplyRules()
			disallow_lst = []
			process_type = Product.Attr('Is Fieldbus Interface in Scope?').GetValue()
			if process_type != "Yes":
				disallow_lst.append("SII Function Design Specification -Fieldbus")
				disallow_lst.append("SII Detail Design Specification -Fieldbus")
				disallow_lst.append("SII Test Procedure -Fieldbus")
			process_type1 = Product.Attr('Is Modbus Interface in Scope?').GetValue()
			if process_type1 != "Yes":
				disallow_lst.append("SII Function Design Specification -Modbus")
				disallow_lst.append("SII Detail Design Specification -Modbus")
				disallow_lst.append("SII I/F Configuration Settings -Modbus")
				disallow_lst.append("SII Test Procedure -Modbus")
				disallow_lst.append("SII Pre-FAT - Modbus")
				disallow_lst.append("SII FAT and Sign Off-Modbus")
			process_type2 = Product.Attr('Is Profibus Interface in Scope?').GetValue()
			if process_type2 != "Yes":
				disallow_lst.append("SII Function Design Specification -Profibus")
				disallow_lst.append("SII Detail Design Specification -Profibus")
				disallow_lst.append("SII I/F Configuration Settings -Profibus")
				disallow_lst.append("SII Test Procedure -Profibus")
				disallow_lst.append("SII Pre-FAT - Profibus")
				disallow_lst.append("SII FAT and Sign Off-Profibus")
			process_type3 = Product.Attr('Is EtherNet IP Interface in Scope?').GetValue()
			if process_type3 != "Yes":
				disallow_lst.append("SII Function Design Specification -EtherNet IP")
				disallow_lst.append("SII Detail Design Specification -EtherNet IP")
				disallow_lst.append("SII I/F Configuration Settings -EtherNet IP")
				disallow_lst.append("SII Test Procedure -EtherNet IP")
				disallow_lst.append("SII Pre-FAT - EtherNet IP")
				disallow_lst.append("SII FAT and Sign Off-EtherNet IP")
			process_type4 = Product.Attr('Is OPC Interface in Scope?').GetValue()
			if process_type4 != "Yes":
				disallow_lst.append("SII OPC Self Test")
				disallow_lst.append("SII Function Design Specification -OPC")
				disallow_lst.append("SII Detail Design Specification -OPC")
				disallow_lst.append("SII I/F Configuration Settings -OPC")
				disallow_lst.append("SII Test Procedure -OPC")
				disallow_lst.append("SII Pre-FAT - OPC")
				disallow_lst.append("SII FAT and Sign Off-OPC")
			process_type5 = Product.Attr('Is HART Interface in Scope?').GetValue()
			if process_type5 != "Yes":
				disallow_lst.append("SII Function Design Specification -HART")
				disallow_lst.append("SII Detail Design Specification -HART")
				disallow_lst.append("SII I/F Configuration Settings-HART")
				disallow_lst.append("SII Test Procedure -HART")
				disallow_lst.append("SII Pre-FAT - HART")
				disallow_lst.append("SII FAT and Sign Off-HART")
			process_type6 = Product.Attr('Is Terminal Server Interface in Scope?').GetValue()
			if process_type6 != "Yes":
				disallow_lst.append("SII Function Design Specification -Terminal Svr")
				disallow_lst.append("SII Detail Design Specification -Terminal Svr")
				disallow_lst.append("SII I/F Configuration Settings-Terminal Svr")
				disallow_lst.append("SII Test Procedure -Terminal Svr")
				disallow_lst.append("SII Pre-FAT - Terminal Svr")
				disallow_lst.append("SII FAT and Sign Off -Terminal Svr")
			process_type7 = Product.Attr('Is DeviceNet Interface in Scope?').GetValue()
			if process_type7 != "Yes":
				disallow_lst.append("SII Function Design Specification -Devicenet")
			process_type8 = Product.Attr('Labor_Site_Activities').GetValue()
			if process_type8 != "Yes":
				disallow_lst.append("SII Site Installation")
				disallow_lst.append("SII Site Acceptance Test and Sign Off")
			process_type9 = Product.Attr('Labor_Operation_Manual_Scope').GetValue()
			if process_type9 != "Yes":
				disallow_lst.append("SII Operation Manual for System Interface")
			process_type10 = Product.Attr('Labor_Custom_Scope').GetValue()
			if process_type10 != "Yes":
				disallow_lst.append("SII Customer Training for System Interface")
			process_type11 = Product.Attr('Is Site Survey Required').GetValue()
			if process_type11 != "Yes":
				disallow_lst.append("SII Site Survey Report")

			laborCont = Product.GetContainerByName('System_Interface_Engineering_Labor_Container')
			tableLabor = SqlHelper.GetList('select Deliverable,Productivity,GES_Eng_1_No,GES_Eng,FO_Eng_1_NoGES,FO_Eng_1_GES_None,FO_Eng_1_GES,FO_Eng_2_NoGES,FO_Eng_2_GES_None,FO_Eng_2_GES,Rank,Calculated_Hrs,Execution_Country from System_Interface_Labor')

			defaultGESEng = 'SYS GES Eng-BO-'+gesLocationVC
			populateLaborContainer(laborCont, tableLabor, disallow_lst, contract_start, query, salesArea, gesLocation, gesLocationVC, defaultGESEng)

			tableLabor = SqlHelper.GetList('Select Deliverable,Calculated_Hrs from SYSTEM_INTERFACE_LABOR')
			calc_dict = dict()
			calcHours(Product, tableLabor, laborCont, calc_dict)
		else:
			laborCont = Product.GetContainerByName('System_Interface_Engineering_Labor_Container')
			if laborCont.Rows.Count > 0:
				laborCont.Rows.Clear()

		if contDict['HMI'] == 'Yes':
			Product.ApplyRules()
			disallow_lst = []
			process_type = Product.Attr('Labor_Site_Activities').GetValue()
			if process_type != "Yes":
				disallow_lst.append("HMI SAT & Sign Off")
			process_type1 = Product.Attr('Labor_Operation_Manual_Scope').GetValue()
			if process_type1 != "Yes":
				disallow_lst.append("HMI Operation Manual")
			process_type2 = Product.Attr('Labor_Custom_Scope').GetValue()
			if process_type2 != "Yes":
				disallow_lst.append("HMI Customer Training")
			if Product.Attr('New_Expansion').GetValue() == 'Expansion':
				if Product.Attr('CE_Cutover').GetValue() != 'Yes':
					disallow_lst.append("HMI Cut Over Procedure")
			else:
				disallow_lst.append("HMI Cut Over Procedure")
			laborCont = Product.GetContainerByName('HMI_Engineering_Labor_Container')
			tableLabor = SqlHelper.GetList('select Deliverable,Productivity,GES_Eng_1_No,GES_Eng,FO_Eng_1_NoGES,FO_Eng_1_GES_None,FO_Eng_1_GES,FO_Eng_2_NoGES,FO_Eng_2_GES_None,FO_Eng_2_GES,Rank,Calculated_Hrs,Execution_Country from HMI_ENGINEERING_LABOR_CONTAINER')

			defaultGESEng = 'SYS GES HMI Eng-BO-'+gesLocationVC
			populateLaborContainer(laborCont, tableLabor, disallow_lst, contract_start, query, salesArea, gesLocation, gesLocationVC, defaultGESEng)

			tableLabor = SqlHelper.GetList("select * from HMI_ENGINEERING_LABOR_CONTAINER where Calculated_Hrs != ''")
			calc_dict = dict()
			calcHours(Product, tableLabor, laborCont, calc_dict)
		else:
			laborCont = Product.GetContainerByName('HMI_Engineering_Labor_Container')
			if laborCont.Rows.Count > 0:
				laborCont.Rows.Clear()

		if contDict['SNE'] == 'Yes':
			disallow_lst = [] 
			process_type = Product.Attr('Is Site Survey Required').GetValue()
			if process_type != "Yes":
				disallow_lst.append("SNC Site Visit Report")
			process_type1 = Product.Attr('Labor_Operation_Manual_Scope').GetValue()
			if process_type1 != "Yes":
				disallow_lst.append("SNC Operation Manual")
			process_type2 = Product.Attr('Labor_Custom_Scope').GetValue()
			if process_type2 != "Yes":
				disallow_lst.append("SNC Customer Training")
			process_type3 = Product.Attr('Labor_Site_Activities').GetValue()
			if process_type3 != "Yes":
				disallow_lst.append("SNC Site Installation")
				disallow_lst.append("SNC Site Acceptance Test & Sign off")
			process_type4 = Product.Attr('Network Assessment in scope?').GetValue()
			if process_type4 != "Yes":
				disallow_lst.append("SNC Network Assessment Report")

			laborCont = Product.GetContainerByName('System_Network_Engineering_Labor_Container')
			tableLabor = SqlHelper.GetList('select	Deliverable,Productivity,GES_Eng_1_No,GES_Eng,FO_Eng_1_NoGES,FO_Eng_1_GES_None,FO_Eng_1_GES,FO_Eng_2_NoGES,FO_Eng_2_GES_None,FO_Eng_2_GES,Rank,Calculated_Hrs,Execution_Country from System_Network_ENGINEERING_LABOR')

			defaultGESEng = 'SYS GES Eng-BO-'+gesLocationVC
			populateLaborContainer(laborCont, tableLabor, disallow_lst, contract_start, query, salesArea, gesLocation, gesLocationVC, defaultGESEng)

			ProjectSize,ser,stn,swt = getprojectsize(Product)
			Product.Attributes.GetByName('Project size message').AssignValue("")
			Product.Attributes.GetByName('ErrorMessage5').AssignValue("")
			Product.Attributes.GetByName('ErrorMessageDDS').AssignValue("")

			ser=int(ser)
			stn=int(stn)
			swt=int(swt)

			ges=Product.Attributes.GetByName("Experion_HS_Ges_Location_Labour").SelectedValue.Display
			fser=Product.Attributes.GetByName('Number of Non Factory Installed Servers').GetValue()
			ts=Product.Attributes.GetByName('EXP Terminal Server').GetValue()
			im=Product.Attributes.GetByName('Implementation Methodology').GetValue()

			fser=int(getfloat(fser))
			ts=int(getfloat(ts))

			ebr="No"
			cont=Product.GetContainerByName("Experion_Enterprise_Cont")
			for row in cont.Rows:
				y=row.Product
				try:
					if y.Attributes.GetByName("Experion Backup & Restore (Experion Server)").SelectedValue.Display == "Yes":
						ebr="Yes"
				except:
					pass
				try:
					if y.Attributes.GetByName("Experion Backup & Restore (ACE)").SelectedValue.Display == "Yes":
						ebr="Yes"
				except:
					pass
				try:
					if y.Attributes.GetByName("Experion Backup & Restore (Simulation PC)").SelectedValue.Display == "Yes":
						ebr="Yes"
				except:
					pass
				try:
					if y.Attributes.GetByName("Experion Backup & Restore (Mobile Terminal Server)").SelectedValue.Display == "Yes":
						ebr="Yes"
				except:
					pass
				try:
					if y.Attributes.GetByName("Experion Backup & Restore (Flex Station ES-F)").SelectedValue.Display == "Yes":
						ebr="Yes"
				except:
					pass
				try:
					if y.Attributes.GetByName("Experion Backup & Restore (Console Station ES-C)").SelectedValue.Display == "Yes":
						ebr="Yes"
				except:
					pass
				try:
					if y.Attributes.GetByName("Experion Backup & Restore (Console Station Extension: ES-CE)").SelectedValue.Display == "Yes":
						ebr="Yes"
				except:
					pass
				try:
					if y.Attributes.GetByName("Experion Backup & Restore (ACE)1").SelectedValue.Display == "Yes":
						ebr="Yes"
				except:
					pass
				try:
					if y.Attributes.GetByName("Experion Backup & Restore (Simulation PC)1").SelectedValue.Display == "Yes":
						ebr="Yes"
				except:
					pass
				try:
					if y.Attributes.GetByName("Experion Backup & Restore (Flex Station ES-F)1").SelectedValue.Display == "Yes":
						ebr="Yes"
				except:
					pass

			#CXCPQ-38353
			if ProjectSize == "Small Project":
				NONF = 8

			elif ProjectSize == "Medium Project":
				if ges =="None":
					NONF= swt*0.5 + fser *16 + (ser + stn + ts)*1
				elif ges != "None":
					NONF= (swt*0.5 + fser *16 + (ser + stn + ts)*1) * 1.15

			elif ProjectSize == "Large Project":
				NONF= 0
				Product.Attributes.GetByName('ErrorMessage5').AssignValue("Hours needs to be entered manually when FTE Communities > 3")

			#CXCPQ-38378
			nd=ser+stn+swt+fser
			if ProjectSize == "Small Project":
				Hrs = 8

			elif ProjectSize == "Medium Project":
				if im == "Non-Standard Build Estimate":
					Hrs = nd * 3 * 0.2
				elif im == "Standard Build Estimate" and ges == "None":
					Hrs = nd * 3 * 0.2 * 0.85
				elif im == "Standard Build Estimate" and ges != "None":
					Hrs = nd * 3 * 0.2 * 0.85 * 1.15
			else:
				Hrs=0
				Product.Attributes.GetByName('ErrorMessage5').AssignValue("Hours needs to be entered manually when FTE Communities > 3")

			#CXCPQ-38341
			tser=Product.Attributes.GetByName('Number of Server Types').GetValue()
			tstn=Product.Attributes.GetByName('Number of Station Types').GetValue()
			fte=Product.Attributes.GetByName('Number of FTE Communities').GetValue()
			tser=int(getfloat(tser))
			tstn=int(getfloat(tstn))
			fte=int(getfloat(fte))
			Hrsdds=10
			R=0
			NC=0
			SWC=0
			if ProjectSize == "Small Project":
				R = 0
				NC = 8 
				SWC = (tser * 8 + tstn * 4 )

			elif ProjectSize == "Medium Project":
				R = 24
				if im == "Non-Standard Build Estimate":
					NC = 60 + (fte - 1)*40
				elif im == "Standard Build Estimate" and ges == "None":
					NC = ( 60 + (fte - 1)*40 ) * 0.85
				elif im == "Standard Build Estimate" and ges != "None":
					NC = ( 60 + (fte - 1)*40 ) * 0.85 * 1.15

				if im == "Non-Standard Build Estimate":
					SWC = tser * 24 + tstn * 16 
				elif im == "Standard Build Estimate" and ges == "None":
					SWC = (tser * 24 + tstn * 16 ) * 0.85
				elif im == "Standard Build Estimate" and ges != "None":
					SWC = (tser * 24 + tstn * 16 ) * 0.85 * 1.15
			else:
				Hrsdds=0
				Product.Attributes.GetByName('ErrorMessage5').AssignValue("Hours needs to be entered manually when FTE Communities > 3")

			if Hrsdds!=0:
				Hrsdds = (R + NC + SWC ) * 0.9

			#CXCPQ-38354
			tnd=Product.Attributes.GetByName('Number of Types of Network Devices').GetValue()
			tnd=int(getfloat(tnd))
			if im == "Non-Standard Build Estimate":
				Hrsstp = tnd * 1.5
			else:
				Hrsstp = 0

			#CXCPQ-38326
			if ProjectSize == "Small Project":
				Hrep=4
			elif ProjectSize == "Medium Project":
				if im == "Non-Standard Build Estimate" and ges == "None":
					Hrep= 16
				elif im == "Standard Build Estimate" and ges == "None":
					Hrep= 16*0.7
				elif ges != "None":
					Hrep= 16*1.15
			else:
				Hrep=0
				Product.Attributes.GetByName('ErrorMessage5').AssignValue("Hours needs to be entered manually when FTE Communities > 3")

			#CXCPQ-38327
			lfte=Product.Attributes.GetByName('Number of FTE Community Locations').GetValue()
			lfte= int(getfloat(lfte))
			if ProjectSize == "Small Project":
				Hrfds=24*0.9
			elif ProjectSize == "Medium Project":
				if im == "Non-Standard Build Estimate":
					Hrfds=(48 + lfte * 40 + ser * 16) * 0.9
				elif im == "Standard Build Estimate" and ges == "None":
					Hrfds=(32 + (16 + lfte * 40 + ser * 16) * 0.85) * 0.9
				elif im == "Standard Build Estimate" and ges != "None":
					Hrfds=(32 + (16 + lfte * 40 + ser * 16) * 0.85 * 1.15) * 0.9
			else:
				Hrfds=0
				Product.Attributes.GetByName('ErrorMessage5').AssignValue("Hours needs to be entered manually when FTE Communities > 3")

			#CXCPQ-38352
			if ProjectSize == "Small Project":
				Hdr=0
			elif ProjectSize == "Medium Project" and ebr=="Yes":
				if ges=="None":
					Hdr=0.85*16*0.9
				elif ges != "None":
					Hdr=0.85*16*1.15*0.9
			elif ProjectSize == "Medium Project" and ebr=="No":
				Hdr=0
				Product.Attributes.GetByName('ErrorMessageDDS').AssignValue("As disaster recovery is going to be done without using Experion Backup & Restore(EBR), Please add the required hours for Disaster Recovery DDS after consultation with expert.")
			elif ProjectSize == "Large Project":
				Hdr= 0
				Product.Attributes.GetByName('ErrorMessage5').AssignValue("Hours needs to be entered manually when FTE Communities > 3")

			#CXCPQ-38320
			wlan = ''
			if Product.Attributes.GetByName("Is WLAN in Scope?").SelectedValue is not None:
				wlan=Product.Attributes.GetByName("Is WLAN in Scope?").SelectedValue.Display
			lswt=Product.Attributes.GetByName("Number of Locations with FTE Switches").GetValue()
			lswt=int(getfloat(lswt))
			if wlan=="Yes":
				W=80
			else:
				W=0

			if ges == "None" and lswt<=5:
				Hsvr=W+40
			elif ges == "None" and lswt>5:
				Hsvr=W+lswt*8*1.3
			elif ges != "None" and lswt<=5:
				Hsvr=(W+40)*1.15
			else:
				Hsvr=(W+lswt*8*1.3)*1.15

			#CXCPQ-38377
			if ProjectSize == "Small Project":
				Hspf=8
			elif ProjectSize == "Medium Project":
				if im=="Non-Standard Build Estimate":
					Hspf=nd*3
				elif im=="Standard Build Estimate" and ges=="None":
					Hspf=nd*3*0.85
				elif im =="Standard Build Estimate" and ges!="None":
					Hspf=nd*3*0.85*1.15
			else:
				Hspf=0
				Product.Attributes.GetByName('ErrorMessage5').AssignValue("Hours needs to be entered manually when FTE Communities > 3")

			#CXCPQ-38325
			if im=="Non-Standard Build Estimate" and lswt<=10:
				Hnar=24+16+80
			elif im=="Standard Build Estimate" and lswt<=10 and ges=="None":
				Hnar=24+16+80*0.85
			elif ges=="None" and lswt>10:
				Hnar=24+16+(lswt*8)
			elif ges != "None" and lswt<=10:
				Hnar=(24+16+80*0.85)*1.15
			elif ges != "None" and lswt>10:
				Hnar=(24+16+(lswt*8))*1.15
			else:
				Hnar=0

			con=Product.GetContainerByName("System_Network_Engineering_Labor_Container")
			for row in con.Rows:
				if row.GetColumnByName("Deliverable").Value=="SNC Site Acceptance Test & Sign off":
					row.GetColumnByName("Calculated Hrs").Value="8"
				#38353
				if row.GetColumnByName("Deliverable").Value=="SNC Network & Server Configuration":
					row.GetColumnByName("Calculated Hrs").Value=str(NONF)
				#38378
				if row.GetColumnByName("Deliverable").Value=="SNC Factory Acceptance Test":
					row.GetColumnByName("Calculated Hrs").Value=str(Hrs)
				#38341
				if row.GetColumnByName("Deliverable").Value=="SNC Detail Design Specifications":
					row.GetColumnByName("Calculated Hrs").Value=str(Hrsdds)
				#38354
				if row.GetColumnByName("Deliverable").Value=="SNC Test Procedure (FAT & SAT)":
					row.GetColumnByName("Calculated Hrs").Value=str(Hrsstp)
				#38326
				if row.GetColumnByName("Deliverable").Value=="SNC Engineering Plan":
					row.GetColumnByName("Calculated Hrs").Value=str(Hrep)
				#38327
				if row.GetColumnByName("Deliverable").Value=="SNC Functional Design Specification":
					row.GetColumnByName("Calculated Hrs").Value=str(Hrfds)
				#38352
				if row.GetColumnByName("Deliverable").Value=="SNC Disaster Recovery DDS":
					row.GetColumnByName("Calculated Hrs").Value=str(Hdr)
				#38320
				if row.GetColumnByName("Deliverable").Value=="SNC Site Visit Report":
					row.GetColumnByName("Calculated Hrs").Value=str(Hsvr)
				#38377
				if row.GetColumnByName("Deliverable").Value=="SNC Pre-FAT":
					row.GetColumnByName("Calculated Hrs").Value=str(Hspf)
				#38325
				if row.GetColumnByName("Deliverable").Value=="SNC Network Assessment Report":
					row.GetColumnByName("Calculated Hrs").Value=str(Hnar)
				lv_calc_hrs = getfloat(row.GetColumnByName('Calculated Hrs').Value)
				lv_productivity = getfloat(row.GetColumnByName('Productivity').Value)
				if lv_calc_hrs > 0:
					lv_final_hrs = round(lv_calc_hrs * lv_productivity)
					row.GetColumnByName('Final Hrs').Value = str(lv_final_hrs)
			con.Calculate()
			Product.Attributes.GetByName('Project size message').AssignValue(ProjectSize)
		else:
			laborCont = Product.GetContainerByName('System_Network_Engineering_Labor_Container')
			if laborCont.Rows.Count > 0:
				laborCont.Rows.Clear()

		#HW ENG Deliverables
		disallow_lst = []
		process_type = Product.Attr('Labor_Site_Activities').GetValue()
		if process_type != "Yes":
			disallow_lst.append("SHE Site Installation")
			disallow_lst.append("SHE Site Acceptance Test & Sign off")

		laborCont = Product.GetContainerByName('Hardware Engineering Labour Container')
		tableLabor = SqlHelper.GetList('select Deliverable,Productivity,GES_Eng_1_No,GES_Eng,FO_Eng_1_NoGES,FO_Eng_1_GES_None,FO_Eng_1_GES,FO_Eng_2_NoGES,FO_Eng_2_GES_None,FO_Eng_2_GES,Rank,Calculated_Hrs,Execution_Country from HARDWARE_ENGINEERING_DELIVERABLE')
		defaultGESEng = 'SYS GES Eng-BO-'+gesLocationVC
		populateLaborContainer(laborCont, tableLabor, disallow_lst, contract_start, query, salesArea, gesLocation, gesLocationVC, defaultGESEng)

		#Update Calculated Hours
		tps = 0
		mdb = 0
		ld = 0
		stn = 0
		svr = 0
		cab_flex = 0
		cab_con = 0
		cab_con_ext = 0
		cab_tps = 0
		desk_flex = 0
		desk_con = 0
		desk_con_ext = 0
		desk_tps = 0
		orion_flex = 0
		orion_con = 0
		orion_con_ext = 0
		orion_tps = 0
		add_station = 0
		ace_ser_tower = 0
		ace_ser_rack = 0
		acet_ser_tower = 0
		acet_ser_rack = 0
		exp_ser_tower = 0
		exp_ser_rack = 0
		mob_server = 0
		add_servers = 0
		server_red = 0

		nscab = float(Product.Attr("Network and Server Cabinet Count").GetValue() or 0)
		auxcab = float(Product.Attr("Auxiliary Cabinet Count").GetValue() or 0)
		oc = float(Product.Attr("Number of Operator Console Sections").GetValue() or 0)
		hc = float(Product.Attr("Number of Console Sections with Hardwired IO").GetValue() or 0)

		if Product.Attr("Labor_Marshalling_Database").GetValue() == "Yes":
			mdb = 1
		if Product.Attr("Labor_Loop_Drawings").GetValue() == "Yes":
			ld = 1

		if Product.Attr("New_Expansion").GetValue() == "Expansion":
			exp_groups = Product.GetContainerByName('Experion_Enterprise_Cont').Rows
			for exp in exp_groups:
				exp_product = exp.Product
				x = exp_product.Attr('Interface with TPS Required?').GetValue()
				if x == "Yes":
					tps = 1
					break
		else:
			tps = 0

		exp_groups = Product.GetContainerByName('Experion_Enterprise_Cont').Rows
		for exp in exp_groups:
			exp_product = exp.Product
			try:
				cab_flex = cab_flex + getattrvalue(exp_product.Attr('CMS Flex Station Qty 0_60').GetValue())
			except:
				cab_flex = cab_flex
			try:
				cab_con	 = cab_con + getattrvalue(exp_product.Attr('CMS Console Station Qty 0_20').GetValue())
			except:
				cab_con = cab_con
			try:
				cab_con_ext	 = cab_con_ext + getattrvalue(exp_product.Attr('CMS Console Station Extension Qty 0_15').GetValue())
			except:
				cab_con_ext = cab_con_ext
			try:
				cab_tps = cab_tps + getattrvalue(exp_product.Attr('CMS TPS Station Qty 0_20').GetValue())
			except:
				cab_tps = cab_tps
			try:
				desk_flex = desk_flex + getattrvalue(exp_product.Attr('DMS Flex Station Qty 0_60').GetValue())
			except:
				desk_flex = desk_flex
			try:
				desk_con = desk_con + getattrvalue(exp_product.Attr('DMS Console Station Qty 0_20').GetValue())
			except:
				desk_con = desk_con
			try:
				desk_con_ext = desk_con_ext + getattrvalue(exp_product.Attr('DMS Console Station Extension Qty 0_15').GetValue())
			except:
				desk_con_ext = desk_con_ext
			try:
				desk_tps = desk_tps + getattrvalue(exp_product.Attr('DMS TPS Station Qty 0_20').GetValue())
			except:
				desk_tps = desk_tps
			try:
				orion_flex = orion_flex + getattrvalue(exp_product.Attr('Flex Station Qty (0-60)').GetValue())
			except:
				orion_flex = orion_flex
			try:
				orion_con = orion_con + getattrvalue(exp_product.Attr('Console Station Qty (0-20)').GetValue())
			except:
				orion_con = orion_con
			try:
				orion_con_ext = orion_con_ext + getattrvalue(exp_product.Attr('Console Station Extension Qty  (0-15)').GetValue())
			except:
				orion_con_ext = orion_con_ext
			try:
				orion_tps = orion_tps + getattrvalue(exp_product.Attr('TPS Station Qty (0-20)').GetValue())
			except:
				orion_tps = orion_tps
			try:
				add_station = add_station + getattrvalue(exp_product.Attr('Additional Stations').GetValue())
			except:
				add_station = add_station
			try:
				ace_ser_tower = ace_ser_tower + getattrvalue(exp_product.Attr('ACE Node Tower Mount Desk').GetValue())
			except:
				ace_ser_tower = ace_ser_tower
			try:
				ace_ser_rack = ace_ser_rack + getattrvalue(exp_product.Attr('ACE Node Rack Mount Cabinet').GetValue())
			except:
				ace_ser_rack = ace_ser_rack
			try:
				acet_ser_tower = acet_ser_tower + getattrvalue(exp_product.Attr('ACE_T_Node _Tower_Mount_Desk').GetValue())
			except:
				acet_ser_tower = acet_ser_tower
			try:
				acet_ser_rack = acet_ser_rack + getattrvalue(exp_product.Attr('ACE_T_Node _Rack_Mount_Cabinet').GetValue())
			except:
				acet_ser_rack = acet_ser_rack
			try:
				exp_ser_tower = exp_ser_tower + getattrvalue(exp_product.Attr('Experion APP Node - Tower Mount').GetValue())
			except:
				exp_ser_tower = exp_ser_tower
			try:
				exp_ser_rack = exp_ser_rack + getattrvalue(exp_product.Attr('Experion APP Node - Rack Mount').GetValue())
			except:
				exp_ser_rack = exp_ser_rack
			try:
				mob_server = mob_server + getattrvalue(exp_product.Attr('Mobile Server Nodes (0-1)').GetValue())
			except:
				mob_server = mob_server
			try:
				add_servers = add_servers + getattrvalue(exp_product.Attr('Additional Servers').GetValue())
			except:
				add_servers = add_servers
			try:
				red = exp_product.Attr('Server Redundancy Requirement?').GetValue()
				if red == "Non Redundant":
					server_red = server_red + 1
				else:
					server_red = server_red + 2
			except:
				server_red = server_red

		stn = float(cab_flex) + float(cab_con) + float(cab_con_ext) + float(cab_tps) + float(desk_flex) + float(desk_con) + float(desk_con_ext) + float(desk_tps) + float(orion_flex) + float(orion_con) + float(orion_con_ext) + float(orion_tps) + float(add_station)
		svr = float(ace_ser_tower) + float(ace_ser_rack) + float(acet_ser_tower) + float(acet_ser_rack) + float(mob_server) + float(add_servers) + float(server_red)

		Hrs1 = 6 * ( nscab + oc + auxcab) + 16 * tps
		Product.Attr("SHE Site Installation").AssignValue(str(Hrs1))

		Integration = 2 + 6 * ( nscab + oc+ auxcab) + 8 * tps
		IntTest = 0.1* ( 24*nscab + (10+ 8*oc)+ 40*hc + 50*auxcab)
		Hrs2 = Integration + IntTest
		Product.Attr("SHE System Integration & Internal Test").AssignValue(str(Hrs2))

		BOM_Hrs = 0.1 * (nscab+ oc + hc + auxcab) + 2 * ( nscab + oc + hc + auxcab) / ( nscab + oc + hc + auxcab + 1) + 0.25 * svr + 0.25 * stn
		IPR_Hrs = 0.5 * oc + 2 * oc / (oc + 1) + 0.25 * svr + 0.25 * stn
		OPR_Hrs = nscab + 3 * nscab/ (nscab+ 1) + hc * 4 + auxcab * 4 + 0.25 * svr + 0.25 * stn
		Hrs3 = BOM_Hrs + IPR_Hrs + OPR_Hrs
		Product.Attr("SHE Procure Materials & Services").AssignValue(str(Hrs3))

		CD_Hrs = ((0.25 * hc * 40) * mdb ) * 1.05
		LD_Hrs = 0.25 * ld* ((( 0.25 * hc * 40) * mdb ) * 1.05)
		if Product.Attr("Implementation Methodology").GetValue() == "Non-Standard Build Estimate":
			CS_Hrs = 1.05 * ( 0.5 * nscab + 1.5 * hc + auxcab  + 0.08 * (svr +	stn))
		else:
			CS_Hrs = (1.05 * ( 0.5 * nscab + 1.5 * hc + auxcab	+ 0.08 * (svr +	 stn))) * 0.99
		Hrs4 = CS_Hrs + CD_Hrs + LD_Hrs
		Product.Attr("SHE Hardware Implementation").AssignValue(str(Hrs4))

		#Update calc hr and final hrs
		tableLabor = SqlHelper.GetList('Select Deliverable,Calculated_Hrs from HARDWARE_ENGINEERING_DELIVERABLE')
		calc_dict = dict()
		calcHours(Product, tableLabor, laborCont, calc_dict)
		#EBR Deliverables
		disallow_lst = []
		if process_type != "Yes":
			disallow_lst.append("EBR Site Acceptance Test & Sign Off")

		laborCont = Product.GetContainerByName('EBR_Engineering_Labor_Container')
		tableLabor = SqlHelper.GetList('select Deliverable,Productivity,GES_Eng_1_No,GES_Eng,FO_Eng_1_NoGES,FO_Eng_1_GES_None,FO_Eng_1_GES,FO_Eng_2_NoGES,FO_Eng_2_GES_None,FO_Eng_2_GES,Rank,Calculated_Hrs,Execution_Country from EBR_ENGINEERING_LABOR_CONTAINER')
		populateLaborContainer(laborCont, tableLabor, disallow_lst, contract_start, query, salesArea, gesLocation, gesLocationVC, defaultGESEng)
		#Update calc hr and final hrs
		tableLabor = SqlHelper.GetList('Select Deliverable,Calculated_Hrs from EBR_ENGINEERING_LABOR_CONTAINER')
		calc_dict = dict()
		calcHours(Product, tableLabor, laborCont, calc_dict)

		#PS_Labor_Part_Summary
		cont = Product.GetContainerByName('Labor_PriceCost_Cont')
		if Quote:
			contList = ['System_Network_Engineering_Labor_Container', 'System_Interface_Engineering_Labor_Container', 'Hardware Engineering Labour Container', 'HMI_Engineering_Labor_Container', 'Additional_CustomDev_Labour_Container','EBR_Engineering_Labor_Container']
			foEngColumn = {'System_Network_Engineering_Labor_Container':'System_Network_Labor_FO_Eng', 'System_Interface_Engineering_Labor_Container':'System_Interface_Labor_FO_Eng', 'Hardware Engineering Labour Container':'Hardware_Eng_FO_Eng_one', 'HMI_Engineering_Labor_Container':'HMI_Labor_FO_Eng', 'Additional_CustomDev_Labour_Container':'Additional_CustomDev_FO_Eng','EBR_Engineering_Labor_Container':'EBR_Labor_FO_Eng'}
			updateLaborCostPrice(Product, Quote, TagParserQuote, contList, foEngColumn, gesLocationVC, True)
			cont.Calculate()
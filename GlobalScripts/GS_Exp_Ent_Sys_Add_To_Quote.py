def isFloat(val):
	if val is not None and val != '':
		try:
			float(val)
			return True
		except:
			return False
	return False

def getfloat(val):
	if val:
		try:
			return float(val)
		except:
			return 0
	return 0

def sortRow(cont,rank,new_row_index):
    try:
        sort_needed = True
        if new_row_index == 0:
            return
        while sort_needed == True:
            if int(cont.Rows[new_row_index-1].GetColumnByName('Rank').Value) > int(rank):
                cont.MoveRowUp(new_row_index, False)
                new_row_index -= 1
            else:
                sort_needed = False
    except Exception,e:
        Log.Info(str(e)+ ' '+ str(rank)+ ' '+ str(new_row_index))

def rowsToDelete(rows_to_delete, laborCont):
	rows_to_delete.sort(reverse=True)
	for x in rows_to_delete:
		laborCont.DeleteRow(x)

def calcHours(Product, tableLabor, laborCont, calc_dict):
	calc_dict = {}
	for x in tableLabor:
		calc_dict[x.Deliverable] = x.Calculated_Hrs
	for row in laborCont.Rows:
		deliverable = row.GetColumnByName("Deliverable").Value
		lv_calc_hrs = getfloat(row.GetColumnByName("Calculated Hrs").Value)
		if deliverable in calc_dict.keys() and not isFloat(calc_dict[deliverable]):
			calc_name = calc_dict[deliverable]
			lv_calc_hrs = getfloat(Product.Attr(calc_name).GetValue())
			row.GetColumnByName("Calculated Hrs").Value = Product.Attr(calc_name).GetValue()
		try:
			lv_productivity = float(row.GetColumnByName('Productivity').Value)
			if lv_calc_hrs > 0 and lv_productivity > 0:
				lv_final_hrs = round(lv_calc_hrs * lv_productivity)
				row.GetColumnByName('Final Hrs').Value = str(lv_final_hrs)
		except Exception,e:
			row.GetColumnByName('Final Hrs').Value = '0'
	laborCont.Calculate()

def populateLaborContainer(laborCont, tableLabor, disallow_lst, contract_start, query, salesArea, gesLocation, gesLocationVC, defaultGESEng):
	current_deliverables = []
	rows_to_delete = []
	emptyGESDel = ['HMI Operator Interface Workshop', 'HMI Engineering Plan', 'HMI Customer Training']
	emptyGESDel.extend(['SHE Engineering Plan', 'SHE Procure Materials & Services', 'EBR Procure Materials & Services'])
	for row in laborCont.Rows:
		current_deliverables.append(row.GetColumnByName('Deliverable').Value)

	for row in tableLabor:
		if row.Deliverable not in disallow_lst and row.Deliverable not in current_deliverables:
			new_row = laborCont.AddNewRow(False)
			new_row["Deliverable"] = row.Deliverable
			new_row["Execution Year"] = str(contract_start)
			new_row["Rank"] = str(row.Rank)
			#sortRow(laborCont,row.Rank,new_row.RowIndex)
			if salesArea == "":
				new_row.GetColumnByName('Execution Country').Value = ""
			else:
				new_row.GetColumnByName('Execution Country').Value = query.Execution_County

			if row.FO_Eng_1_NoGES:
				new_row.GetColumnByName('FO Eng 1').SetAttributeValue(row.FO_Eng_1_NoGES)
				new_row['FO Eng 1'] = row.FO_Eng_1_NoGES
			else:
				new_row.GetColumnByName('FO Eng 1').SetAttributeValue('None')
				new_row['FO Eng 1'] = 'None'
			if row.FO_Eng_2_NoGES:
				new_row.GetColumnByName('FO Eng 2').SetAttributeValue(row.FO_Eng_2_NoGES)
				new_row['FO Eng 2'] = row.FO_Eng_2_NoGES
			else:
				new_row.GetColumnByName('FO Eng 2').SetAttributeValue('None')
				new_row['FO Eng 2'] = 'None'
			new_row["Productivity"]= row.Productivity
			new_row["Calculated Hrs"]= row.Calculated_Hrs
			new_row.SetColumnValue('GES Location', gesLocationVC)
			new_row.GetColumnByName('GES Location').ReferencingAttribute.AssignValue(gesLocationVC)
			if gesLocation == "None" or gesLocation == '':
				new_row["GES Eng % Split"]= row.GES_Eng_1_No
				new_row["FO Eng 1 % Split"]= row.FO_Eng_1_GES_None
				new_row["FO Eng 2 % Split"]= row.FO_Eng_2_GES_None
				new_row['GES Eng'] = ''
			else:
				new_row["GES Eng % Split"]= row.GES_Eng
				new_row["FO Eng 1 % Split"]= row.FO_Eng_1_GES
				new_row["FO Eng 2 % Split"]= row.FO_Eng_2_GES
				if row.Deliverable in emptyGESDel:
					new_row['GES Eng'] = ''
					new_row.SetColumnValue('GES Location', 'None')
					new_row.GetColumnByName('GES Location').ReferencingAttribute.AssignValue('None')
				else:
					new_row.GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue(defaultGESEng)
			new_row.ApplyProductChanges()
			new_row.Calculate()
			sortRow(laborCont,row.Rank,new_row.RowIndex)
		elif row.Deliverable in disallow_lst and row.Deliverable in current_deliverables:
			for cont_row in laborCont.Rows:
				if row.Deliverable == cont_row.GetColumnByName('Deliverable').Value:
					rows_to_delete.append(cont_row.RowIndex)
		elif row.Deliverable in current_deliverables:
			for cont_row in laborCont.Rows:
				if row.Deliverable == cont_row.GetColumnByName('Deliverable').Value:
					applyChanges = 0
					if cont_row['GES Location'] != gesLocationVC:
						cont_row.SetColumnValue('GES Location', gesLocationVC)
						cont_row.GetColumnByName('GES Location').ReferencingAttribute.AssignValue(gesLocationVC)
						if gesLocation == "None" or gesLocation == '' or row.Deliverable in emptyGESDel:
							cont_row['GES Eng'] = ''
							per = isFloat(cont_row["FO Eng 1 % Split"]) + isFloat(cont_row["FO Eng 2 % Split"])
							if per < 100:
								cont_row["FO Eng 1 % Split"] = row.FO_Eng_1_GES_None
								cont_row["FO Eng 2 % Split"] = row.FO_Eng_2_GES_None
							cont_row.SetColumnValue('GES Location', 'None')
							cont_row.GetColumnByName('GES Location').ReferencingAttribute.AssignValue('None')
						else:
							cont_row.GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue(defaultGESEng)
						applyChanges = 1
					if applyChanges:
						cont_row.ApplyProductChanges()
						cont_row.Calculate()
					break
	laborCont.Calculate()

	rowsToDelete(rows_to_delete, laborCont)

def getprojectsize(Product):
	ProjectSize=""
	SERRadd=0
	ANTMDadd=0
	ANRMCadd=0
	ATNTMDadd=0
	ATNRMCadd=0
	EAPPTadd=0
	EAPPRadd=0
	MNSadd=0
	ADDseradd=0
	FTE=0
	ser=0

	FSQOadd=0
	FSQDadd=0
	FSQCadd=0
	CSQOadd=0
	CSQCadd=0
	CSQDadd=0
	CSEQOadd=0
	CSEQCadd=0
	CSEQDadd=0
	TPSOadd=0
	TPSCadd=0
	TPSDadd=0
	Addsadd=0
	stn=0
	NLCadd=0
	BSRadd=0
	swt=0

	for row in Product.GetContainerByName("Experion_Enterprise_Cont").Rows:
		y=row.Product

		try:
			SERRav=y.Attributes.GetByName('Server Redundancy Requirement?').SelectedValue.Display
			if SERRav=="Non Redundant":
				SERR="1"
			elif SERRav=="Redundant":
				SERR="2"
		except:
			SERR="0"
		SERRadd=SERRadd+int(SERR)

		try:
			ANTMD=y.Attributes.GetByName('ACE Node Tower Mount Desk').GetValue()
		except:
			ANTMD="0"
		ANTMDadd=ANTMDadd+int(ANTMD)

		try:
			ANRMC=y.Attributes.GetByName('ACE Node Rack Mount Cabinet').GetValue()
		except:
			ANRMC="0"
		ANRMCadd=ANRMCadd+int(ANRMC)

		try:
			ATNTMD=y.Attributes.GetByName('ACE_T_Node _Tower_Mount_Desk').GetValue()
			if ATNTMD=="":
				ATNTMD=0
		except:
			ATNTMD="0"
		ATNTMDadd=ATNTMDadd+int(ATNTMD)

		try:
			ATNRMC=y.Attributes.GetByName('ACE_T_Node _Rack_Mount_Cabinet').GetValue()
			if ATNRMC=="":
				ATNRMC=0
		except:
			ATNRMC="0"
		ATNRMCadd=ATNRMCadd+int(ATNRMC)

		try:
			EAPPT=y.Attributes.GetByName('Experion APP Node - Tower Mount').GetValue()
			if EAPPT=="":
				EAPPT=0
		except:
			EAPPT="0"
		EAPPTadd=EAPPTadd+int(EAPPT)

		try:
			EAPPR=y.Attributes.GetByName('Experion APP Node - Rack Mount').GetValue()
			if EAPPR=="":
				EAPPR=0
		except:
			EAPPR="0"
		EAPPRadd=EAPPRadd+int(EAPPR)

		try:
			MNS=y.Attributes.GetByName('Mobile Server Nodes (0-1)').GetValue()
			if MNS=="":
				MNS=0
		except:
			MNS="0"
		MNSadd=MNSadd+int(MNS)

		try:
			ADDser=y.Attributes.GetByName('Additional Servers').GetValue()
			if ADDser=="":
				ADDser=0
		except:
			ADDser="0"
		ADDseradd=ADDseradd+int(ADDser)



		#Flex Station Qty (0-60)
		try:
			FSQO=y.Attributes.GetByName('Flex Station Qty (0-60)').GetValue()
			if FSQO=="":
				FSQO=0
		except:
			FSQO="0"
		FSQOadd=FSQOadd+int(FSQO)

		try:
			FSQD=y.Attributes.GetByName('DMS Flex Station Qty 0_60').GetValue()
			if FSQD=="":
				FSQD=0
		except:
			FSQD="0"
		FSQDadd=FSQDadd+int(FSQD)

		try:
			FSQC=y.Attributes.GetByName('CMS Flex Station Qty 0_60').GetValue()
			if FSQC=="":
				FSQC=0
		except:
			FSQC="0"
		FSQCadd=FSQCadd+int(FSQC)

		#Console Station Qty (0-20)
		try:
			CSQO=y.Attributes.GetByName('Console Station Qty (0-20)').GetValue()
			if CSQO=="":
				CSQO=0
		except:
			CSQO="0"
		CSQOadd=CSQOadd+int(CSQO)

		try:
			CSQC=y.Attributes.GetByName('CMS Console Station Qty 0_20').GetValue()
			if CSQC=="":
				CSQC=0
		except:
			CSQC="0"
		CSQCadd=CSQCadd+int(CSQC)

		try:
			CSQD=y.Attributes.GetByName('DMS Console Station Qty 0_20').GetValue()
			if CSQD=="":
				CSQD=0
		except:
			CSQD="0"
		CSQDadd=CSQDadd+int(CSQD)

		#Console Station Extension Qty	(0-15)
		try:
			CSEQO=y.Attributes.GetByName('Console Station Extension Qty	 (0-15)').GetValue()
			if CSEQO=="":
				CSEQO=0
		except:
			CSEQO="0"
		CSEQOadd=CSEQOadd+int(CSEQO)

		try:
			CSEQD=y.Attributes.GetByName('DMS Console Station Extension Qty 0_15').GetValue()
			if CSEQD=="":
				CSEQD=0
		except:
			CSEQD="0"
		CSEQDadd=CSEQDadd+int(CSEQD)

		try:
			CSEQC=y.Attributes.GetByName('CMS Console Station Extension Qty 0_15').GetValue()
			if CSEQC=="":
				CSEQC=0
		except:
			CSEQC="0"
		CSEQCadd=CSEQCadd+int(CSEQC)

		#TPS Station Qty (0-20)
		try:
			TPSO=y.Attributes.GetByName('TPS Station Qty (0-20)').GetValue()
			if TPSO=="":
				TPSO=0
		except:
			TPSO="0"
		TPSOadd=TPSOadd+int(TPSO)

		try:
			TPSC=y.Attributes.GetByName('CMS TPS Station Qty 0_20').GetValue()
			if TPSC=="":
				TPSC=0
		except:
			TPSC="0"
		TPSCadd=TPSCadd+int(TPSC)

		try:
			TPSD=y.Attributes.GetByName('DMS TPS Station Qty 0_20').GetValue()
			if TPSD=="":
				TPSD=0
		except:
			TPSD="0"
		TPSDadd=TPSDadd+int(TPSD)

		#Additional Stations
		try:
			Adds=y.Attributes.GetByName('Additional Stations').GetValue()
			if Adds=="":
				Adds=0
		except:
			Adds="0"
		Addsadd=Addsadd+int(Adds)

		#number of location cluster
		NLC=y.GetContainerByName("List of Locations/Clusters/Network Groups").Rows.Count
		NLC=int(NLC)*2
		NLCadd=(NLCadd+NLC)

		#Backbone Switch Required
		BSR=y.Attributes.GetByName("Backbone Switch Required").SelectedValue.Display
		if BSR=="Yes":
			BSRadd=BSRadd+2
		elif BSR=="No":
			BSRadd=BSRadd+0


	FTE=Product.Attributes.GetByName('Number of FTE Communities').GetValue()

	ser=SERRadd+ANTMDadd+ANRMCadd+ATNTMDadd+ATNRMCadd+EAPPTadd+EAPPRadd+MNSadd+ADDseradd

	stn=CSQOadd+CSQDadd+CSQCadd+CSEQOadd+CSEQDadd+CSEQCadd+FSQOadd+FSQDadd+FSQCadd+TPSOadd+TPSDadd+TPSCadd+Addsadd

	swt=BSRadd+NLCadd
	FTE=int(getfloat(FTE))
	ser=int(getfloat(ser))
	stn=int(getfloat(stn))
	swt=int(getfloat(swt))

	if (FTE == 1) and (ser <= 2) and (stn <= 10):
		ProjectSize = "Small Project"
	elif (FTE == 1) and (ser > 2 or stn > 10):
		ProjectSize = "Medium Project"
	elif (FTE <= 3):
		ProjectSize = "Medium Project"
	else:
		ProjectSize = "Large Project"

	return ProjectSize,ser,stn,swt

def getattrvalue(a):
	if a == "":
		a = 0
	return float(a)
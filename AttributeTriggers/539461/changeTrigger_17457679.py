Product.ParseString('<*CTX( Container(UOC_Labor_Details).Row(1).Column(UOC_Ges_Location_Labour).Set(<*VALUECODE(Default_Ges_Location)*>) )*>')
gesLocation=Product.Attr('Default_Ges_Location').GetValue()
Booking_LOB = TagParserQuote.ParseString('<* QuoteProperty (Booking LOB) *>')
gesMapping = {'GESIndia':'IN','GESChina':'CN','GESRomania':'RO','GESUzbekistan':'UZ','None':'None','GESEgypt':'EG'}
gesLocationVC = gesMapping.get(gesLocation)
laborCont = Product.GetContainerByName('CE UOC Engineering Labor Container')
tableLabor = SqlHelper.GetList("select Deliverable,Calculated_Hrs,GES_Eng_NoGES,GES_Eng_GES,FO_Eng_1,FO1_Eng_NoGES,FO1_Eng_GES,FO_Eng_2,FO2_Eng_NoGES,FO2_Eng_GES,Rank,Execution_Country from CE_UOC_Engineering_Deliverables where LOB = '"+str(Booking_LOB)+"'")
if laborCont.Rows.Count > 0:
	for new_row in laborCont.Rows:
		for row in tableLabor:
			if  new_row["Deliverable"]  ==  row.Deliverable:
				if gesLocation == "None" or gesLocation == '':
					new_row["GES Eng % Split"]= row.GES_Eng_NoGES
					new_row["FO Eng 1 % Split"]= row.FO1_Eng_NoGES
					new_row["FO Eng 2 % Split"]= row.FO2_Eng_NoGES
				elif gesLocation !="None":
					Trace.Write('-->>'+str(new_row["GES Eng"]))
					new_row["GES Eng % Split"]= row.GES_Eng_GES
					new_row["FO Eng 1 % Split"]= row.FO1_Eng_GES
					new_row["FO Eng 2 % Split"]= row.FO2_Eng_GES
				if gesLocationVC:
					gesPartnumber='LSS GES Eng-BO-'+gesLocationVC if Booking_LOB=="LSS" else 'SYS GES Eng-BO-'+gesLocationVC
					new_row.GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue(gesPartnumber)
					new_row['GES Eng'] = gesPartnumber
	laborCont.Calculate()

addilaborCont = Product.GetContainerByName('CE UOC Additional Custom Deliverables')
for new_row in addilaborCont.Rows:
	if gesLocationVC:
		gesPartnumber='LSS GES Eng-BO-'+gesLocationVC if Booking_LOB=="LSS" else 'SYS GES Eng-BO-'+gesLocationVC
		new_row.GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue(gesPartnumber)
		new_row['GES Eng'] = gesPartnumber
addilaborCont.Calculate()
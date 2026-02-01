prevGesLocation = Product.GetGlobal('prevGesLocationValue')
gesLocation = Product.Attr("C300_GES_Location").GetValue()
gesMapping = {'GES India':'IN','GES China':'CN','GES Romania':'RO','GES Uzbekistan':'UZ','None':'None','GES Egypt':'EG'}
gesLocationVC = gesMapping.get(gesLocation)
contList = []
allGesLocations = ('GES India', 'GES China', 'GES Romania', 'GES Uzbekistan','GES Egypt')
Booking_LOB = TagParserQuote.ParseString('<* QuoteProperty (Booking LOB) *>')
Trace.Write("Booking_LOB"+str(Booking_LOB))
laborCont = Product.GetContainerByName('C300_Engineering_Labor_Container')

tableLabor = SqlHelper.GetList("select Deliverable, GES_Eng_NoGES, GES_Eng_GES, FO_Eng_1_NoGES, FO_Eng_1_GES, FO1_Eng_NoGES, FO1_Eng_GES, FO_Eng_2_NoGES, FO_Eng_2_GES, FO2_Eng_NoGES, FO2_Eng_GES, Rank, Execution_Country from C300_ENGINEERING_DELIVERABLES WHERE LOB ='"+str(Booking_LOB)+"'")
if laborCont.Rows.Count > 0:
    for new_row in laborCont.Rows:
        for row in tableLabor:
            if new_row["Deliverable"]  ==  row.Deliverable:
                if gesLocation == "None" or gesLocation == '':
                    new_row["GES Eng % Split"]= row.GES_Eng_NoGES
                    new_row["FO Eng 1 % Split"]= row.FO1_Eng_NoGES
                    new_row["FO Eng 2 % Split"]= row.FO2_Eng_NoGES
                elif gesLocation != "None" and prevGesLocation in ["None",""]:
                    new_row["GES Eng % Split"]= row.GES_Eng_GES
                    new_row["FO Eng 1 % Split"]= row.FO1_Eng_GES
                    new_row["FO Eng 2 % Split"]= row.FO2_Eng_GES
    laborCont.Calculate()
    Product.SetGlobal('prevGesLocationValue', gesLocation)
    contList.append('C300_Engineering_Labor_Container')
laborCont4 = Product.GetContainerByName('C300_Additional_Custom_Deliverables_Container')
if laborCont4.Rows.Count > 0:
    for new_row in laborCont4.Rows:
        if gesLocation == "None" or gesLocation == '':
            new_row['GES Eng'] = ''
            new_row["GES Eng % Split"]= '0'
            new_row["FO Eng % Split"]= '100'
        else:
            new_row['GES Location'] = gesLocationVC
            new_row.GetColumnByName('GES Location').ReferencingAttribute.AssignValue(gesLocationVC)
            if Booking_LOB == 'LSS':
                new_row.GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue('LSS GES Eng-BO-'+gesLocationVC)
                Trace.Write("ges--loc--->"+str(new_row['GES Eng']))
            else:
                new_row.GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue('SYS GES Eng-BO-'+gesLocationVC)
            #new_row["GES Eng % Split"]= '0'
            #new_row["FO Eng % Split"]= '100'
    laborCont4.Calculate()
    contList.append('C300_Additional_Custom_Deliverables_Container')
if len(contList) > 0:
    ScriptExecutor.Execute('PS_Labor_Part_Summary')
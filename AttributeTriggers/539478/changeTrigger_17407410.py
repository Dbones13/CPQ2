gesLocation = Product.Attr("HC900_Ges_Location_Labour").GetValue()
laborCont = Product.GetContainerByName('HC900 Engineering Labor Container')
tableLabor = SqlHelper.GetList('select Deliverable,GES_Eng_NoGES,GES_Eng_GES,FO_Eng_1_NoGES,FO_Eng_1_GES,FO1_Eng_NoGES,FO1_Eng_GES,FO_Eng_2_NoGES,FO_Eng_2_GES,FO2_Eng_NoGES,FO2_Eng_GES,Rank,Execution_Country from HC900_ENGINEERING_DELIVERABLES')

gesMapping = {'GES India':'IN','GES China':'CN','GES Romania':'RO','GES Uzbekistan':'UZ','None':'None','GES Egypt':'EG'}
gesLocationVC = gesMapping.get(gesLocation)
contList = []

if laborCont.Rows.Count > 0:
    for new_row in laborCont.Rows:
        for row in tableLabor:
            if  new_row["Deliverable"]  ==  row.Deliverable:
                if gesLocation == "None" or gesLocation == '':
                    new_row.GetColumnByName('FO Eng 1').SetAttributeValue(row.FO_Eng_1_NoGES)
                    new_row.GetColumnByName('FO Eng 2').SetAttributeValue(row.FO_Eng_2_NoGES)
                    new_row['FO Eng 1']=row.FO_Eng_1_NoGES
                    new_row['FO Eng 2']=row.FO_Eng_2_NoGES
                    new_row["GES Eng % Split"]= row.GES_Eng_NoGES
                    new_row["FO Eng 1 % Split"]= row.FO1_Eng_NoGES
                    new_row["FO Eng 2 % Split"]= row.FO2_Eng_NoGES
                elif TagParserProduct.ParseString('<*CTX( Container(HC900 Engineering Labor Container).Column(GES Eng).GetPermission )*>') == "Hidden":
                    new_row.GetColumnByName('FO Eng 1').SetAttributeValue(row.FO_Eng_1_GES)
                    new_row.GetColumnByName('FO Eng 2').SetAttributeValue(row.FO_Eng_2_GES)
                    new_row['FO Eng 1']=row.FO_Eng_1_GES
                    new_row['FO Eng 2']=row.FO_Eng_2_GES
                    new_row["GES Eng % Split"]= row.GES_Eng_GES
                    new_row["FO Eng 1 % Split"]= row.FO1_Eng_GES
                    new_row["FO Eng 2 % Split"]= row.FO2_Eng_GES
                    new_row.GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue('SYS GES Eng-BO-'+gesLocationVC)
                else:
                    new_row.GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue('SYS GES Eng-BO-'+gesLocationVC)
    if gesLocation != "None" or gesLocation != "":
        TagParserProduct.ParseString('<*CTX( Container(HC900 Engineering Labor Container).Column(GES Eng).SetPermission(Editable) )*>')
        contList.append('HC900 Engineering Labor Container')
    laborCont.Calculate()

custom_deliverables = Product.GetContainerByName('HC900 Additional Custom Deliverables')
if custom_deliverables.Rows.Count > 0:
    for new_row in custom_deliverables.Rows:
        if gesLocation == "None" or gesLocation == '':
            new_row['GES Eng'] = ''
            new_row["GES Eng % Split"]= '0'
            new_row["FO Eng % Split"]= '100'
        else:
            new_row['GES Location'] = gesLocationVC
            new_row.GetColumnByName('GES Location').ReferencingAttribute.AssignValue(gesLocationVC)
            new_row.GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue('SYS GES Eng-BO-'+gesLocationVC)
            contList.append('HC900 Additional Custom Deliverables')
        custom_deliverables.Calculate()
if len(contList) >0:
    ScriptExecutor.Execute('PS_Labor_Part_Summary')
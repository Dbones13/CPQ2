gesLocation = Product.Attr('LMS_GES_Location').GetValue()
gesMapping = {'GES India':'IN','GES China':'CN','GES Romania':'RO','GES Uzbekistan':'UZ','None':'None','GES Egypt':'EG'}
gesLocationVC = gesMapping.get(gesLocation)
contList = []
sec=Product.Attr('Ges_Location_44925').GetValue()
laborCont = Product.GetContainerByName('LMS_Labor_Container')
tableLabor = SqlHelper.GetList('select Deliverable,Productivity,GES_Eng_1_No,GES_Eng,FO_Eng_1_NoGES,FO_Eng_1_GES_None,FO_Eng_1_GES,FO_Eng_2_NoGES,FO_Eng_2_GES_None,FO_Eng_2_GES,Rank,Execution_Country from LIQUID_METERINGSUITE_ENGINEERING_LABOR_CUSTOM_TABLE')
if laborCont.Rows.Count > 0:
    for new_row in laborCont.Rows:
        for row in tableLabor:
            if  new_row["Deliverable"]  ==  row.Deliverable:
                if gesLocation == "None" or gesLocation == '':
                    new_row.GetColumnByName('FO Eng 1').SetAttributeValue(row.FO_Eng_1_NoGES)
                    new_row.GetColumnByName('FO Eng 2').SetAttributeValue(row.FO_Eng_2_NoGES)
                    new_row["GES Eng % Split"]= row.GES_Eng_1_No
                    new_row["FO Eng 1 % Split"]= row.FO_Eng_1_GES_None
                    new_row["FO Eng 2 % Split"]= row.FO_Eng_2_GES_None
                else:
                    Trace.Write('Test2')
                    if gesLocation !="None" and sec in ("None","",None):
                        new_row.GetColumnByName('FO Eng 1').SetAttributeValue(row.FO_Eng_1_GES)
                        new_row.GetColumnByName('FO Eng 2').SetAttributeValue(row.FO_Eng_2_GES)
                        new_row["GES Eng % Split"]= row.GES_Eng
                        new_row["FO Eng 1 % Split"]= row.FO_Eng_1_GES
                        new_row["FO Eng 2 % Split"]= row.FO_Eng_2_GES
    laborCont.Calculate()
    contList.append('LMS_Labor_Container')
laborCont4 = Product.GetContainerByName('LMS_Additional_Labor_Container')
if laborCont4.Rows.Count > 0:
    for new_row in laborCont4.Rows:
        if gesLocation == "None" or gesLocation in ('',None,'None'):
            new_row['GES Eng'] = ''
            new_row["GES Eng % Split"]= '0'
            new_row["FO Eng % Split"]= '100'
        else:   
            new_row['GES Location'] = gesLocationVC
            new_row.GetColumnByName('GES Location').ReferencingAttribute.AssignValue(gesLocationVC)
            new_row.GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue('SYS GES Eng-BO-'+gesLocationVC)
            #new_row["GES Eng % Split"]= '0'
            #new_row["FO Eng % Split"]= '100'
    laborCont4.Calculate()
    contList.append('LMS_Additional_Labor_Container')
if len(contList) > 0:
    ScriptExecutor.Execute('PS_Labor_Part_Summary')
sec=Product.Attr('Ges_Location_44925').AssignValue(gesLocation)
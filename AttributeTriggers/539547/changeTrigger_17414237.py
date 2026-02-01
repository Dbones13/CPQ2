gesLocation = TagParserProduct.ParseString('<* Value(SCADA_Ges_Location_Labour) *>')
laborCont = Product.GetContainerByName('SCADA_Engineering_Labor_Container')
tableLabor = SqlHelper.GetList('select Deliverable,Productivity,GES_Eng_1_No,GES_Eng,FO_Eng_1_NoGES,FO_Eng_1_GES_None,FO_Eng_1_GES,FO_Eng_2_NoGES,FO_Eng_2_GES_None,FO_Eng_2_GES,Rank,Execution_Country from SCADA_LABOR_DELIVERABLES')
set_default = {'GES China':'SYS GES Eng-BO-CN', 'GES India':'SYS GES Eng-BO-IN', 'GES Romania':'SYS GES Eng-BO-RO', 'GES Uzbekistan':'SYS GES Eng-BO-UZ','GES Egypt':'SYS GES Eng-BO-EG'}
if laborCont.Rows.Count > 0:
    for new_row in laborCont.Rows:
        for row in tableLabor:
            if  new_row["Deliverable"]  ==  row.Deliverable:
                if gesLocation == "None" or gesLocation == '':
                    Product.Attr('scada_ges_GES_check').AssignValue('None')
                    new_row["GES Eng % Split"]= row.GES_Eng_1_No
                    new_row["FO Eng 1 % Split"]= row.FO_Eng_1_GES_None
                    new_row["FO Eng 2 % Split"]= row.FO_Eng_2_GES_None
                    new_row.GetColumnByName('FO Eng 1').ReferencingAttribute.SelectDisplayValue(row.FO_Eng_1_NoGES)
                    new_row.GetColumnByName('FO Eng 2').ReferencingAttribute.SelectDisplayValue(row.FO_Eng_2_NoGES)
                    new_row['FO Eng 1']=row.FO_Eng_1_NoGES
                    new_row['FO Eng 2']=row.FO_Eng_2_NoGES
                else:
                    if Product.Attr('scada_ges_GES_check').GetValue() != "Country":
                        new_row["GES Eng % Split"]= row.GES_Eng
                        new_row["FO Eng 1 % Split"]= row.FO_Eng_1_GES
                        new_row["FO Eng 2 % Split"]= row.FO_Eng_2_GES
                    new_row.GetColumnByName('FO Eng 1').ReferencingAttribute.SelectDisplayValue(row.FO_Eng_1_NoGES)
                    new_row.GetColumnByName('FO Eng 2').ReferencingAttribute.SelectDisplayValue(row.FO_Eng_2_NoGES)
                    new_row['FO Eng 1']=row.FO_Eng_1_NoGES
                    new_row['FO Eng 2']=row.FO_Eng_2_NoGES
                    Product.Attr('scada_ges_GES_check').AssignValue('Country')
                new_row.GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue(set_default.get(gesLocation))
                new_row['GES Eng'] = set_default.get(gesLocation)
                Trace.Write('=========++'+str(new_row['GES Eng']))
                new_row.Calculate()
                new_row.ApplyProductChanges()

    laborCont.Calculate()

    custom_deliverables = Product.GetContainerByName('SCADA_Additional_Custom_Deliverables_Container')
    for row in custom_deliverables.Rows:
        row.GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue(set_default.get(gesLocation))
        row['GES Eng'] = set_default.get(gesLocation)
        row.Calculate()
    custom_deliverables.Calculate()
    Trace.Write('------------Start-----')
    Product.Attr('SCADA_GES_Location_Flag').AssignValue('')
    Trace.Write('------------End-----')
    ScriptExecutor.Execute('PS_Populate_Prices')
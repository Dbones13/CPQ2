gesLocation = Product.Attr("TGE_GES Location").GetValue()
gesMapping = {'GES India':'IN','GES China':'CN','GES Romania':'RO','GES Uzbekistan':'UZ','None':'None'}
gesLocationVC = gesMapping.get(gesLocation)
contList = []
sec=Product.Attr('Ges_Location_44925').GetValue()
laborCont = Product.GetContainerByName('TGE_Engineering_Labor_Container')
tableLabor = SqlHelper.GetList('select Deliverable,Productivity,GES_Eng_1_No,GES_Eng,FO_Eng_1_NoGES,FO_Eng_1_GES_None,FO_Eng_1_GES,FO_Eng_2_NoGES,FO_Eng_2_GES_None,FO_Eng_2_GES,Rank,Execution_Country from Tank_Gauging_Engineering_LABOR_CUSTOM_TABLE')
eng_values = ['HPS_GES_P350B_CN','HPS_GES_P350F_CN','HPS_GES_P350B_IN','HPS_GES_P350F_IN']
allow_values = [val for val in eng_values if str(gesLocationVC) in val]
disallow_values = [val for val in eng_values if str(gesLocationVC) not in val]

if laborCont.Rows.Count > 0:
    for new_row in laborCont.Rows:
        for row in tableLabor:
            if  new_row["Deliverable"]  ==  row.Deliverable:
                if gesLocation == "None" or gesLocation == '':
                    new_row.GetColumnByName('FO Eng 1').SetAttributeValue(row.FO_Eng_1_NoGES)
                    new_row.GetColumnByName('FO Eng 2').SetAttributeValue(row.FO_Eng_2_NoGES)
                    new_row['FO Eng 1']=row.FO_Eng_1_NoGES
                    new_row['FO Eng 2']=row.FO_Eng_2_NoGES
                    new_row["GES Eng % Split"]= row.GES_Eng_1_No
                    new_row["FO Eng 1 % Split"]= row.FO_Eng_1_GES_None
                    new_row["FO Eng 2 % Split"]= row.FO_Eng_2_GES_None
                else:
                    Trace.Write('Test2')
                    if gesLocation !="None" and sec =="None":
                        new_row.GetColumnByName('FO Eng 1').SetAttributeValue(row.FO_Eng_1_GES)
                        new_row.GetColumnByName('FO Eng 2').SetAttributeValue(row.FO_Eng_2_GES)
                        new_row['FO Eng 1']=row.FO_Eng_1_GES
                        new_row['FO Eng 2']=row.FO_Eng_2_GES
                        new_row["GES Eng % Split"]= row.GES_Eng
                        new_row["FO Eng 1 % Split"]= row.FO_Eng_1_GES
                        new_row["FO Eng 2 % Split"]= row.FO_Eng_2_GES
                        new_row.GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue('SYS GES Eng-BO-'+gesLocationVC)
                        new_row['GES Eng']='SYS GES Eng-BO-'+gesLocationVC
                        new_row.Product.AllowAttrValues('TGE_Labor_GES_Eng',*allow_values)  
                        new_row.Product.DisallowAttrValues('TGE_Labor_GES_Eng',*disallow_values)
                        new_row.ApplyProductChanges()
                        new_row.Calculate()
                  
    laborCont.Calculate()
    contList.append('TGE_Engineering_Labor_Container')
laborCont4 = Product.GetContainerByName('TGE_Additional_Labour_Container')
if laborCont4.Rows.Count > 0:
    for new_row in laborCont4.Rows:
        if gesLocation == "None" or gesLocation == '':
            new_row['GES Eng'] = ''
            new_row["GES Eng % Split"]= '0'
            new_row["FO Eng % Split"]= '100'
        else:
            #new_row['GES Location'] = gesLocationVC
            #new_row.GetColumnByName('GES Location').ReferencingAttribute.AssignValue(gesLocationVC)
            new_row.GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue('SYS GES Eng-BO-'+gesLocationVC)
            new_row['GES Eng']='SYS GES Eng-BO-'+gesLocationVC
            #new_row["GES Eng % Split"]= '0'
            #new_row["FO Eng % Split"]= '100'
        attr_values  = new_row.Product.Attr('TGE_ADDI_Labor_GES_Eng').Values		
        add_eng_values = []
        for val in attr_values:
            add_eng_values.append(val.ValueCode)
        Trace.Write('-addneg values--'+str(add_eng_values))
        allow_add_values =  [val for val in add_eng_values if str(gesLocationVC) in val]
        disallow_add_values =  [val for val in add_eng_values if str(gesLocationVC) not in val]
        new_row.Product.AllowAttrValues('TGE_ADDI_Labor_GES_Eng',*allow_add_values)
        new_row.Product.DisallowAttrValues('TGE_ADDI_Labor_GES_Eng',*disallow_add_values)
        new_row.ApplyProductChanges()
        new_row.Product.ApplyRules()
        new_row.Calculate()
    laborCont4.Calculate()
    contList.append('TGE_Additional_Labour_Container')
if len(contList) > 0:
    ScriptExecutor.Execute('PS_Labor_Part_Summary')
sec=Product.Attr('Ges_Location_44925').AssignValue(gesLocation)
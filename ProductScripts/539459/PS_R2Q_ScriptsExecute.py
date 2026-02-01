def PS_Default(Product):
    labor_cont = Product.GetContainerByName('SM_Additional_Custom_Deliverables_Labor_Container')
    labor_cont.Rows[0].Product.Attr('SM_Labor_FO_Eng').SelectDisplayValue('SYS LE1-Lead Eng')
    labor_cont.Rows[0]['FO Eng']='SYS LE1-Lead Eng'
    labor_cont.Rows[0].Product.ApplyRules()
    labor_cont.Rows[0].ApplyProductChanges()
    labor_cont.Calculate()
    import GS_DropDown_Implementation
    GS_DropDown_Implementation.SetDropDownDefaultvalue(Product)
def OnProductRuleExecutionEnd(Product):
    CE_SystemGroup_Cont = Product.GetContainerByName('SM_ControlGroup_Cont')
    if CE_SystemGroup_Cont.Rows.Count == 0:
        newRow = CE_SystemGroup_Cont.AddNewRow('SM_Control_Group_cpq', False)
        newRow.ApplyProductChanges()
    SM_ControlGroup_Cont = Product.GetContainerByName('SM_ControlGroup_Cont')
    if SM_ControlGroup_Cont.Rows.Count > 0:
        contCal = False
        for row in SM_ControlGroup_Cont.Rows:
            SM_CG_Name = row.Product.Attr('SM_CG_Name').GetValue()
            if str(row["Control Group Name"]) != SM_CG_Name:
                row.Product.Attr('SM_CG_Name').AssignValue(str(row["Control Group Name"]))
                row.ApplyProductChanges()
                contCal = True
            if row.Product.Attr('SM_System_Scope').GetValue() != Product.Attr('SM_System_Scope').GetValue():
                row.Product.Attr('SM_System_Scope').AssignValue(Product.Attr('SM_System_Scope').GetValue())
                row.ApplyProductChanges()
                contCal = True
        if contCal:
            SM_ControlGroup_Cont.Calculate()
def PS_Hide_Attr_Values(Product):
    tabs = [tab.Name for tab in Product.Tabs if tab.IsSelected]
    allowed_count = 0
    expected_count = 4
    if 'Labor Deliverables' in tabs:
        years_list = Product.Attr('SM_Labor_Execution_Year').Values
        for year in years_list:
            allowed_count = allowed_count + 1 if year.Allowed else allowed_count
        if allowed_count > expected_count:
            import datetime
            current_year = datetime.datetime.now().year
            def hide_year(Product, current_year, attribute_name, expected_count, max_year ):
                years_list = Product.Attr(attribute_name).Values
                for year in years_list:
                    if int(year.ValueCode) in range(current_year + 4, max_year):
                        Product.DisallowAttrValues(attribute_name, year.ValueCode)
                    elif int(year.ValueCode) < current_year:
                        Product.DisallowAttrValues(attribute_name, year.ValueCode)
            max_year = 2037
            for attribute_name in ['SM_Labor_Execution_Year', 'SM_Labor_Execution_Year_adc']:
                hide_year(Product, current_year, attribute_name, expected_count, max_year)
    def disallow(location, dropdownlist):
        if location:
            for i in dropdownlist:
                if i.Display in location:
                    i.Allowed = False
                elif i.Display not in location:
                    i.Allowed = True
    def allow(location, dropdownlist):
        if location:
            for i in dropdownlist:
                if i.Display in location:
                    i.Allowed = True
                elif i.Display not in location:
                    i.Allowed = False

    switch_io = Product.GetContainerByName('SM_Common_Questions').Rows[0].GetColumnByName("Experion Software Release").Value if Product.GetContainerByName('SM_Common_Questions').Rows.Count > 0 else ''
    if Product.GetContainerByName('SM_Hardware_Simulation_Station_Cont').Rows.Count > 0 or Product.GetContainerByName('SM_Hardware_Builder_Station_Cont').Rows.Count > 0 or Product.GetContainerByName('SM_Hardware_Historian_Station_Cont').Rows.Count > 0:
        row = Product.GetContainerByName('SM_Hardware_Simulation_Station_Cont').Rows[0]
        row1 = Product.GetContainerByName('SM_Hardware_Builder_Station_Cont').Rows[0]
        row2 = Product.GetContainerByName('SM_Hardware_Historian_Station_Cont').Rows[0]
        list = row.GetColumnByName('Station_Type')
        list1 = row1.GetColumnByName('Station_Type')
        list2 = row2.GetColumnByName('Station_Type')
        value_list = list.ReferencingAttribute.Values
        value_list1 = list1.ReferencingAttribute.Values
        value_list2 = list2.ReferencingAttribute.Values
        location=['STN_PER_DELL_Tower_RAID1','STN_PER_DELL_Rack_RAID1','STN_STD_DELL_Tower_NonRAID','STN_PER_HP_Tower_RAID1']
        location1=['None']
        raid2_location = ['STN_PER_DELL_Tower_RAID2']
        if switch_io =="R530":
            allow(location, value_list)
            allow(location, value_list1)
            allow(location, value_list2)
            disallow(location1+raid2_location, value_list)
            disallow(location1+raid2_location, value_list1)
            disallow(location1+raid2_location, value_list2)
        elif switch_io =="R520":
            disallow(location+location1, value_list)
            disallow(location+location1, value_list1)
            disallow(location+location1, value_list2)
            allow(raid2_location, value_list)
            allow(raid2_location, value_list1)
            allow(raid2_location, value_list2)
        else:
            disallow(location+raid2_location, value_list)
            disallow(location+raid2_location, value_list1)
            disallow(location+raid2_location, value_list2)
            allow(location1, value_list)
            allow(location1, value_list1)
            allow(location1, value_list2)
def PS_populate_doc_param(Product):
    import operator
    cont = Product.GetContainerByName("SM_ControlGroup_Cont")
    countDict = {}
    for row in cont.Rows:
        countDict[row["SM_CG_Percent_Installed_Spare"]] = countDict.get(row["SM_CG_Percent_Installed_Spare"], 0) + 1
    maxSpare = "0"
    if len(countDict) > 0:
        maxSpare = str(max(countDict.iteritems(), key=operator.itemgetter(1))[0])
    if not maxSpare:
        maxSpare = "0"
    Product.Attr("doc_parameter_cg_spare_percent").AssignValue(maxSpare)
def PS_SM_Hide_Values(Product):
    tabs = [tab.Name for tab in Product.Tabs if tab.IsSelected]
    if Product.Attr('isProductLoaded').GetValue() == 'True' and 'Labor Deliverables' in tabs:
        specific_location = {'GESChina': ['HPS_GES_P350B_CN', 'HPS_GES_P350F_CN'], 'GESIndia': ['HPS_GES_P350B_IN', 'HPS_GES_P350F_IN'],'GESRomania':['HPS_GES_P350B_RO', 'HPS_GES_P350F_RO'],'GESUzbekistan':['HPS_GES_P350B_UZ', 'HPS_GES_P350F_UZ'],'GESEgypt':['HPS_GES_P350B_EG', 'HPS_GES_P350F_EG'],'GES China': ['HPS_GES_P350B_CN', 'HPS_GES_P350F_CN'], 'GES India': ['HPS_GES_P350B_IN', 'HPS_GES_P350F_IN'],'GES Romania':['HPS_GES_P350B_RO', 'HPS_GES_P350F_RO'],'GES Uzbekistan':['HPS_GES_P350B_UZ', 'HPS_GES_P350F_UZ'],'GES Egypt':['HPS_GES_P350B_EG', 'HPS_GES_P350F_EG']}
        def disallow(location, dropdownlist):
            if location:
                for i in dropdownlist:
                    if i.ValueCode in location:
                        i.Allowed = True
                    elif i.ValueCode not in location:
                        i.Allowed = False
        remove_deliverables = ['SSE User Requirement Specification']
        gesloc = ''
        if Product.GetContainerByName('SM_Labor_Cont').Rows.Count > 0:
            gesloc = Product.GetContainerByName('SM_Labor_Cont').Rows[0].GetColumnByName('GES_Location').Value
        if gesloc != "None" and gesloc != "":
            deliverables = Product.GetContainerByName('SM_SSE_Engineering_Labor_Container')
            for row in deliverables.Rows:
                if row['Deliverable'] not in remove_deliverables:
                    location = row.GetColumnByName('GES Eng')
                    value_list = location.ReferencingAttribute.Values
                    disallow(specific_location[gesloc], value_list)
                    row.ApplyProductChanges()
                    row.Calculate()
            deliverables.Calculate();
            deliverables1 = Product.GetContainerByName('SM Safety System - ESD/FGS/BMS/HIPPS Container')
            for row in deliverables1.Rows:
                if row['Deliverable'] not in remove_deliverables:
                    location = row.GetColumnByName('GES Eng')
                    value_list = location.ReferencingAttribute.Values
                    disallow(specific_location[gesloc], value_list)
                    row.ApplyProductChanges()
                    row.Calculate()
            deliverables1.Calculate();
            custom_deliverables = Product.GetContainerByName('SM_Additional_Custom_Deliverables_Labor_Container')
            for deliverable in custom_deliverables.Rows:
                deliverable_location = deliverable.GetColumnByName('GES Eng')
                dropdown_values = deliverable_location.ReferencingAttribute.Values
                disallow(specific_location[gesloc], dropdown_values)
                deliverable.ApplyProductChanges()
                deliverable.Calculate()
            custom_deliverables.Calculate()
def SM_System_PartSummary(Product):
    tabs = [tab.Name for tab in Product.Tabs if tab.IsSelected]
    if 'Part Summary' in tabs:
        import GS_SM_Part_Update
        import GS_SM_System_PartSumary_Calcs
        import GS_SM_Hardware_Safety_Parts
        parts_dict = {}
        try:
            parts_dict = GS_SM_System_PartSumary_Calcs.get_System_parts(Product,parts_dict)
        except Exception,e:
            Trace.Write(str(e))
        try:
            parts_dict = GS_SM_Hardware_Safety_Parts.getSMSystemParts(Product,parts_dict)
        except Exception,e:
            Trace.Write(str(e))
        GS_SM_Part_Update.execute(Product, 'SM_System_PartSummary_Cont', parts_dict)

def PS_SM_SSE_Engineering_Labor_Container_Populate(Product):
    import datetime
    def sortRow(cont,rank,new_row_index):
        sort_needed = True
        if new_row_index == 0:
            return
        while sort_needed == True:
            if int(cont.Rows[new_row_index-1].GetColumnByName('Rank').Value) > int(rank):
                cont.MoveRowUp(new_row_index, False)
                new_row_index -= 1
            else:
                sort_needed = False
    scope = Product.Attr('CE_Scope_Choices').GetValue()
    R2QFlag= Quote.GetCustomField('R2QFlag').Content
    if scope == 'HW/SW + LABOR':
        Product.ExecuteRulesOnce = True
        salesArea = Quote.GetCustomField('Sales Area').Content
        marketCode = Quote.SelectedMarket.MarketCode
        salesOrg = Quote.GetCustomField('Sales Area').Content
        currency = Quote.GetCustomField('Currency').Content
        query = SqlHelper.GetFirst("select Execution_County from NEW_EXECUTION_COUNTRY_SALES_ORG_MAPPING where Sales_Area = '{}' and Currency = '{}'".format(salesOrg,currency))
        disallow_lst = [] 
        process_type = Product.Attr('Labor_Site_Activities').GetValue()
        if process_type != "Yes":
            disallow_lst.append("SSE Site Installation-Base")
            disallow_lst.append("SSE Site Installation")
            disallow_lst.append("SSE SAT and Sign Off")
            disallow_lst.append("SSE Close Out Report")
        process_type1 = Product.Attr('Labor_Operation_Manual_Scope').GetValue()
        if process_type1 != "Yes":
            disallow_lst.append("SSE Operation Manual for Safety System")
        process_type2 = Product.Attr('Labor_Custom_Scope').GetValue()
        if process_type2 != "Yes":
            disallow_lst.append("SSE Customer Training for Safety System")
        if Product.Attr('New_Expansion').GetValue() == 'Expansion':
            if Product.Attr('CE_Cutover').GetValue() != 'Yes':
                disallow_lst.append("SSE Cut Over Procedure")
        else:
            disallow_lst.append("SSE Cut Over Procedure")
        current_year = datetime.datetime.now().year
        if Quote:
            if Quote.GetCustomField('EGAP_Contract_Start_Date').Content != "":
                c_start_date = Quote.GetCustomField('EGAP_Contract_Start_Date').Content
                contract_start = int("20"+c_start_date[-2:])
                if contract_start > current_year+3:
                    contract_start = current_year+3
            else:
                contract_start = current_year
        else:
            contract_start = current_year
        laborCont=''
        gesLocation = ''
        if Product.GetContainerByName('SM_Labor_Cont').Rows.Count > 0:
            gesLocation = Product.GetContainerByName('SM_Labor_Cont').Rows[0].GetColumnByName('GES_Location').Value
        gesMapping = {'GESIndia':'IN','GESChina':'CN','GESRomania':'RO','GESUzbekistan':'UZ','GESEgypt':'EG','None':'None','GES India':'IN','GES China':'CN','GES Romania':'RO','GES Uzbekistan':'UZ','GES Egypt':'EG'}
        if (not gesLocation or gesLocation == 'None') and R2QFlag and Quote.GetGlobal('ExGesLocation'):
            gesLocation = gesMapping.keys()[gesMapping.values().index(Quote.GetGlobal('ExGesLocation'))]
        gesLocationVC = gesMapping.get(gesLocation) if gesLocation !='' else 'None'
        gesEmptyDel = ['SSE User Requirement Specification', 'SSE Engineering Plan', 'SSE Customer Training for Safety System', 'SSE Close Out Report', 'SSE Procure Material & Services']
        if Product.Attr('SM_Product_Name').GetValue() == Product.Name:
            laborCont = Product.GetContainerByName('SM_SSE_Engineering_Labor_Container')
            tableLabor = SqlHelper.GetList('select Deliverable,Productivity,GES_Eng_1_No,GES_Eng,FO_Eng_1_NoGES,FO_Eng_1_GES_None,FO_Eng_1_GES,FO_Eng_2_NoGES,FO_Eng_2_GES_None,FO_Eng_2_GES,Rank,Calculated_Hrs,Execution_Country from SAFETY_MANAGER_LABOR_SSE_ENGINEERING_LABOR')
            current_deliverables = []
            rows_to_delete = []
            for row in laborCont.Rows:
                current_deliverables.append(row.GetColumnByName('Deliverable').Value)
            for row in tableLabor:
                if row.Deliverable not in disallow_lst and row.Deliverable not in current_deliverables:
                    new_row = laborCont.AddNewRow(False)
                    new_row["Deliverable"] = row.Deliverable
                    new_row["Execution Year"] = (Quote.GetCustomField('R2Q_PRJT_Execution_Year').Content  if R2QFlag == "Yes" else str(contract_start) )
                    new_row["Rank"] = str(row.Rank)
                    sortRow(laborCont,row.Rank,new_row.RowIndex)
                    new_row.GetColumnByName('Execution Country').Value = "" if salesArea == "" else query.Execution_County
                    if gesLocation == "None" or gesLocation == '':
                        new_row["GES Eng % Split"]= row.GES_Eng_1_No
                        new_row["FO Eng 1 % Split"]= row.FO_Eng_1_GES_None
                        new_row["FO Eng 2 % Split"]= row.FO_Eng_2_GES_None
                        new_row["Productivity"]= row.Productivity
                        new_row["Calculated Hrs"]= row.Calculated_Hrs if row.Calculated_Hrs.isnumeric() else '0'
                        new_row.GetColumnByName('FO Eng 1').SetAttributeValue(row.FO_Eng_1_NoGES)
                        new_row.GetColumnByName('FO Eng 2').SetAttributeValue(row.FO_Eng_2_NoGES)
                        new_row["FO Eng 1"]= row.FO_Eng_1_NoGES
                        new_row["FO Eng 2"]= row.FO_Eng_2_NoGES
                    else:
                        new_row["GES Eng % Split"]= row.GES_Eng
                        new_row["FO Eng 1 % Split"]= row.FO_Eng_1_GES
                        new_row["FO Eng 2 % Split"]= row.FO_Eng_2_GES
                        new_row["Productivity"]= row.Productivity
                        new_row["Calculated Hrs"]= row.Calculated_Hrs if row.Calculated_Hrs.isnumeric() else '0'
                        new_row.GetColumnByName('FO Eng 1').SetAttributeValue(row.FO_Eng_1_NoGES)
                        new_row.GetColumnByName('FO Eng 2').SetAttributeValue(row.FO_Eng_2_NoGES)
                        new_row["FO Eng 1"]= row.FO_Eng_1_NoGES
                        new_row["FO Eng 2"]= row.FO_Eng_2_NoGES
                        if row.Deliverable in gesEmptyDel:
                            new_row['GES Eng'] = ''
                        else:
                            new_row.GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue('SYS GES Eng-BO-'+gesLocationVC)
                            new_row['GES Eng']='SYS GES Eng-BO-'+gesLocationVC
                    new_row.Calculate()
                elif row.Deliverable in disallow_lst and row.Deliverable in current_deliverables:
                    for cont_row in laborCont.Rows:
                        if row.Deliverable == cont_row.GetColumnByName('Deliverable').Value:
                            rows_to_delete.append(cont_row.RowIndex)
                            break
            laborCont.Calculate()
            rows_to_delete.sort(reverse=True)
        laborCont1 = Product.GetContainerByName('SM Safety System - ESD/FGS/BMS/HIPPS Container')
        tableLabor1 = SqlHelper.GetList('select Deliverable,Productivity,GES_Eng_1_No,GES_Eng,FO_Eng_1_NoGES,FO_Eng_1_GES_None,FO_Eng_1_GES,FO_Eng_2_NoGES,FO_Eng_2_GES_None,FO_Eng_2_GES,Rank,Calculated_Hrs,Execution_Country from SAFETY_MANAGER_LABOR_SSE_ENGINEERING_LABOR_TWO')
        current_deliverables1 = []
        rows_to_delete1 = []
        for row in laborCont1.Rows:
            current_deliverables1.append(row.GetColumnByName('Deliverable').Value)
        for row in tableLabor1:
            if row.Deliverable not in disallow_lst and row.Deliverable not in current_deliverables1:
                new_row = laborCont1.AddNewRow(False)
                new_row["Deliverable"] = row.Deliverable
                if R2QFlag == "Yes":
                    new_row["Execution Year"] = Quote.GetCustomField('R2Q_PRJT_Execution_Year').Content
                else:
                    new_row["Execution Year"] = str(contract_start)
                new_row["Rank"] = str(row.Rank)
                sortRow(laborCont1,row.Rank,new_row.RowIndex)
                if salesArea == "":
                    new_row.GetColumnByName('Execution Country').Value = ""
                else:
                    new_row.GetColumnByName('Execution Country').Value = query.Execution_County
                if gesLocation == "None" or gesLocation == '':
                    new_row["GES Eng % Split"]= row.GES_Eng_1_No
                    new_row["FO Eng 1 % Split"]= row.FO_Eng_1_GES_None
                    new_row["FO Eng 2 % Split"]= row.FO_Eng_2_GES_None
                    new_row["Productivity"]= row.Productivity
                    new_row["Calculated Hrs"]= row.Calculated_Hrs if row.Calculated_Hrs.isnumeric() else '0'
                    new_row.GetColumnByName('FO Eng 1').SetAttributeValue(row.FO_Eng_1_NoGES)
                    new_row.GetColumnByName('FO Eng 2').SetAttributeValue(row.FO_Eng_2_NoGES)
                    new_row["FO Eng 1"]= row.FO_Eng_1_NoGES
                    new_row["FO Eng 2"]= row.FO_Eng_2_NoGES
                else:
                    new_row["GES Eng % Split"]= row.GES_Eng
                    new_row["FO Eng 1 % Split"]= row.FO_Eng_1_GES
                    new_row["FO Eng 2 % Split"]= row.FO_Eng_2_GES
                    new_row["Productivity"]= row.Productivity
                    new_row["Calculated Hrs"]= row.Calculated_Hrs if row.Calculated_Hrs.isnumeric() else '0'
                    new_row.GetColumnByName('FO Eng 1').SetAttributeValue(row.FO_Eng_1_NoGES)
                    new_row.GetColumnByName('FO Eng 2').SetAttributeValue(row.FO_Eng_2_NoGES)
                    new_row["FO Eng 1"]= row.FO_Eng_1_NoGES
                    new_row["FO Eng 2"]= row.FO_Eng_2_NoGES
                    if row.Deliverable in gesEmptyDel:
                        new_row['GES Eng'] = ''
                    else:
                        new_row.GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue('SYS GES Eng-BO-'+gesLocationVC)
                        new_row['GES Eng']=('SYS GES Eng-BO-'+gesLocationVC)
                new_row.Calculate()
            elif row.Deliverable in disallow_lst and row.Deliverable in current_deliverables1:
                for cont_row in laborCont1.Rows:
                    if row.Deliverable == cont_row.GetColumnByName('Deliverable').Value:
                        rows_to_delete1.append(cont_row.RowIndex)
                        break
        laborCont1.Calculate()
        rows_to_delete1.sort(reverse=True)
        laborAddi = Product.GetContainerByName('SM_Additional_Custom_Deliverables_Labor_Container').Rows
        for row1 in laborAddi:
            if row1.GetColumnByName('Execution Country').Value == "" and salesArea != "":
                row1['Execution Country'] = query.Execution_County
            if row1.GetColumnByName('Execution Year').Value == "":
                if R2QFlag == "Yes":
                    row1["Execution Year"] = Quote.GetCustomField('R2Q_PRJT_Execution_Year').Content
                else:
                    row1["Execution Year"] = str(contract_start)
            if gesLocation == "None" or gesLocation == '':
                row1["FO Eng % Split"] = '100'
                row1["GES Eng % Split"] = '0'
        Product.ExecuteRulesOnce = False
        Product.Attr('isProductLoaded').AssignValue('True')
        if Product.Attr('SM_Product_Name').GetValue() == Product.Name:
            for x in rows_to_delete:
                laborCont.DeleteRow(x)
        for x in rows_to_delete1:
            laborCont1.DeleteRow(x)
def PS_SM_Calculate_Labor_Hours(Product):
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
    scope = Product.Attr('CE_Scope_Choices').GetValue()
    if Product.Attr('isProductLoaded').GetValue() == 'True' and scope == 'HW/SW + LABOR':
        Product.ExecuteRulesOnce = True
        laborCont = Product.GetContainerByName('SM_SSE_Engineering_Labor_Container')
        laborCont1 = Product.GetContainerByName('SM Safety System - ESD/FGS/BMS/HIPPS Container')
        tableLabor = SqlHelper.GetList("select Deliverable,Productivity,GES_Eng_1_No,GES_Eng,FO_Eng_1_NoGES,FO_Eng_1_GES_None,FO_Eng_1_GES,FO_Eng_2_NoGES,FO_Eng_2_GES_None,FO_Eng_2_GES,Rank,Calculated_Hrs,Execution_Country from SAFETY_MANAGER_LABOR_SSE_ENGINEERING_LABOR where Calculated_Hrs != ''")
        tableLabor1 = SqlHelper.GetList('select Deliverable,Productivity,GES_Eng_1_No,GES_Eng,FO_Eng_1_NoGES,FO_Eng_1_GES_None,FO_Eng_1_GES,FO_Eng_2_NoGES,FO_Eng_2_GES_None,FO_Eng_2_GES,Rank,Calculated_Hrs,Execution_Country from SAFETY_MANAGER_LABOR_SSE_ENGINEERING_LABOR_TWO')
        calc_name_dict = {}
        calc_name_dict1 = {}
        for x in tableLabor:
            calc_name_dict[x.Deliverable] = x.Calculated_Hrs
        for x in tableLabor1:
            calc_name_dict1[x.Deliverable] = x.Calculated_Hrs
        try:
            bpd = 0
            if Quote:
                bpd = Quote.GetCustomField('EGAP_Project_Duration_Weeks').Content.strip()
                if bpd:
                    bpd = int(bpd)
                else:
                    bpd = 0
        except Exception,e:
            Product.ErrorMessages.Add("Error when Cacluating SM Labor Parameters: " + str(e))
        for row in laborCont.Rows:
            deliverable = row.GetColumnByName("Deliverable").Value
            if deliverable in calc_name_dict.keys() and not isFloat(calc_name_dict[deliverable]):
                calc_name = calc_name_dict[row.GetColumnByName("Deliverable").Value]
                try:
                    row.GetColumnByName("Calculated Hrs").Value = Product.Attr(calc_name).GetValue() #Get the calculated value of deliverable
                    final_hr = row.GetColumnByName('Final Hrs').Value
                    calc = getfloat(row.GetColumnByName('Calculated Hrs').Value)
                    if final_hr == '' and calc > 0:
                        calc = getfloat(row.GetColumnByName('Calculated Hrs').Value)
                        prod = getfloat(row.GetColumnByName('Productivity').Value)
                        final = round(calc * prod)
                        row.GetColumnByName('Final Hrs').Value = str(final)
                except Exception,e:
                    msg = "Error when Calculating Hours for: {0}, Error: {1}".format(calc_name, e)
                    Product.ErrorMessages.Add(msg)
        laborCont.Calculate()
        for row in laborCont1.Rows:
            deliverable = row.GetColumnByName("Deliverable").Value
            if deliverable in calc_name_dict1.keys() and not isFloat(calc_name_dict1[deliverable]):
                calc_name = calc_name_dict1[row.GetColumnByName("Deliverable").Value]
                try:
                    row.GetColumnByName("Calculated Hrs").Value = Product.Attr(calc_name).GetValue() #Get the calculated value of deliverable
                    final_hr = row.GetColumnByName('Final Hrs').Value
                    calc = getfloat(row.GetColumnByName('Calculated Hrs').Value)
                    if final_hr == '' and calc > 0:
                        calc = getfloat(row.GetColumnByName('Calculated Hrs').Value)
                        prod = getfloat(row.GetColumnByName('Productivity').Value)
                        final = round(calc * prod)
                        row.GetColumnByName('Final Hrs').Value = str(final)
                except Exception,e:
                    msg = "Error when Calculating Hours for: {0}, Error: {1}".format(calc_name, e)
                    Product.ErrorMessages.Add(msg)
        laborCont1.Calculate()
        Product.ExecuteRulesOnce = False
def Show_Safety_Manager_Error_Deliverables(Product):
    tabs = [tab.Name for tab in Product.Tabs if tab.IsSelected]
    scope = Product.Attr('CE_Scope_Choices').GetValue()
    Product.Attr('ErrorMessage1').AssignValue('')
    if (('Labor Deliverables' in tabs or 'General Inputs' in tabs) and scope == 'HW/SW + LABOR'):
        deliverables = Product.GetContainerByName('SM_SSE_Engineering_Labor_Container').Rows
        gesLocation = Product.GetContainerByName('SM_Labor_Cont').Rows[0].GetColumnByName('GES_Location').Value
        count = count1 = count2 = 0
        Labor_Message = Labor_Message2 = Labor_Message3 = ""
        for row in deliverables:
            deliverable = row.GetColumnByName('Deliverable')
            GES_Eng = FO1_Eng = FO2_Eng = FO1_Eng_Cost = FO2_Eng_Cost = GES_Eng_Cost = 0
            if row.GetColumnByName('GES Eng % Split').Value not in ('','0') and (gesLocation != "None" or gesLocation != ''):
                GES_Eng = float(row.GetColumnByName('GES Eng % Split').Value)
            if row.GetColumnByName('FO Eng 1 % Split').Value not in ('','0'):
                FO1_Eng = float(row.GetColumnByName('FO Eng 1 % Split').Value)
            if row.GetColumnByName('FO Eng 2 % Split').Value not in ('','0'):
                FO2_Eng = float(row.GetColumnByName('FO Eng 2 % Split').Value)
            if row.GetColumnByName('FO_Eng_1_Unit_Regional_Cost').Value not in ('','0'):
                FO1_Eng_Cost = float(row.GetColumnByName('FO_Eng_1_Unit_Regional_Cost').Value)
            if row.GetColumnByName('FO_Eng_2_Unit_Regional_Cost').Value not in ('','0'):
                FO2_Eng_Cost = float(row.GetColumnByName('FO_Eng_2_Unit_Regional_Cost').Value)
            if row.GetColumnByName('GES_Unit_Regional_Cost').Value not in ('','0'):
                GES_Eng_Cost = float(row.GetColumnByName('GES_Unit_Regional_Cost').Value)
            GES_Eng_Val = row.GetColumnByName('GES Eng').Value
            FO1_Eng_New = 0
            if(GES_Eng in range(101) and FO2_Eng in range(101)):
                FO1_Eng_New = float(100 - GES_Eng - FO2_Eng)
            if FO1_Eng_New < 0 and row.GetColumnByName('Final Hrs').Value not in ('','0','0.0'):
                count +=1
                Labor_Message = Labor_Message + " - " +str(deliverable.Value) + "<br>"
            FO_Eng_1_val = row.GetColumnByName('FO Eng 1').DisplayValue
            FO1_Eng = float(row.GetColumnByName('FO Eng 1 % Split').Value)
            FO_Eng_2_val = row.GetColumnByName('FO Eng 2').DisplayValue
            FO2_Eng = float(row.GetColumnByName('FO Eng 2 % Split').Value)
            finalHrs = row.GetColumnByName('Final Hrs').Value
            if (finalHrs not in ('','0','0.0') and (((FO_Eng_2_val == '' or FO_Eng_2_val == 'None') and FO2_Eng > 0 and FO2_Eng <= 100) or ((FO_Eng_1_val == '' or FO_Eng_1_val == 'None') and FO1_Eng_New > 0))):
                count1 = count1 + 1
                Labor_Message2 = Labor_Message2 + " - " +str(deliverable.Value) + "<br>"
            if (finalHrs not in ('','0','0.0') and ((FO_Eng_2_val != '' and FO_Eng_2_val != 'None' and FO2_Eng_Cost == 0 and FO2_Eng > 0) or (FO_Eng_1_val != '' and FO_Eng_1_val != 'None' and FO1_Eng_Cost == 0 and FO1_Eng > 0) or (GES_Eng_Val != '' and GES_Eng_Val != 'None' and GES_Eng_Cost == 0 and GES_Eng > 0))):
                count2 = count2 + 1
                Labor_Message3 = Labor_Message3 + " - " +str(deliverable.Value) + "<br>"
        if count > 0:
            Labor_Message = "<b>"+'Hours distribution among resources is not 100%. Please adjust the % Split column value to get the total 100% <br>'+"</b>" + Labor_Message
        if count1 > 0:
            Labor_Message2 = "<b>"+'Resource is not selected for deliverable. Please select respective Eng or change the Eng % Split to 0% <br>'+"</b>" + Labor_Message2
            if Labor_Message != "":
                Labor_Message += "<br>" + Labor_Message2
            else:
                Labor_Message = Labor_Message2
        if count2 > 0:
            Labor_Message3 = "<b>"+'Cost is not available for selected resource in Safety System Base. Please select different resource or different Execution Country.Deliverables to look into: <br>'+"</b>" + Labor_Message3
            if Labor_Message != "":
                Labor_Message += "<br>" + Labor_Message3
            else:
                Labor_Message = Labor_Message3
        Safety_Manager_Error_Message_val = Safety_Manager_Error_Message_val2 = ""
        deliverables = Product.GetContainerByName('SM_Additional_Custom_Deliverables_Labor_Container')
        count = count1 = count2 = 0
        Labor_Message3 = ''
        for row in deliverables.Rows:
            deliverable = row["Deliverable Name"] if row["Deliverable Name"] else row['Standard Deliverable']
            GES_Eng = FO1_Eng = FO1_Eng_Cost = GES_Eng_Cost = 0
            if row.GetColumnByName('GES Eng % Split').Value not in ('','0'):
                GES_Eng = float(row.GetColumnByName('GES Eng % Split').Value)
            if row.GetColumnByName('FO Eng % Split').Value not in ('','0'):
                FO1_Eng = float(row.GetColumnByName('FO Eng % Split').Value)
            if row.GetColumnByName('FO_Eng_1_Unit_Regional_Cost').Value not in ('','0'):
                FO1_Eng_Cost = float(row.GetColumnByName('FO_Eng_1_Unit_Regional_Cost').Value)
            if row.GetColumnByName('GES_Unit_Regional_Cost').Value not in ('','0'):
                GES_Eng_Cost = float(row.GetColumnByName('GES_Unit_Regional_Cost').Value)
            GES_Eng_Val = row.GetColumnByName('GES Eng').Value
            split = 100
            FO1_Eng_New = 0
            if(GES_Eng in range(101)):
                split = float(GES_Eng + FO1_Eng )
                FO1_Eng_New = float(100 - GES_Eng)
            if split != 100 and row.GetColumnByName('Final Hrs').Value not in ('','0','0.0') and deliverable != '':
                count +=1
                Safety_Manager_Error_Message_val = Safety_Manager_Error_Message_val + " - " +str(deliverable) + "<br>"
            FO_Eng_1_val = row.GetColumnByName('FO Eng').DisplayValue
            FO1_Eng = float(row.GetColumnByName('FO Eng % Split').Value)
            finalHrs = row.GetColumnByName('Final Hrs').Value
            if (finalHrs not in ('','0','0.0') and ((FO_Eng_1_val == '' or FO_Eng_1_val == 'None') and FO1_Eng_New > 0)):
                count1 = count1 + 1
                Safety_Manager_Error_Message_val2 = Safety_Manager_Error_Message_val2 + " - " +str(deliverable) + "<br>"
            if (finalHrs not in ('','0','0.0') and ((FO_Eng_1_val != '' and FO_Eng_1_val != 'None' and FO1_Eng_Cost == 0 and FO1_Eng > 0) or (GES_Eng_Val != '' and GES_Eng_Val != 'None' and GES_Eng_Cost == 0 and GES_Eng > 0))):
                count2 = count2 + 1
                Labor_Message3 = Labor_Message3 + " - " +str(deliverable) + "<br>"
        if count1 > 0:
            Safety_Manager_Error_Message_val2 = "<b>"+'Resource is not selected for deliverable. Please select respective Eng or change the Eng % Split to 0% <br>'+"</b>" + Safety_Manager_Error_Message_val2
            if Labor_Message != "":
                Labor_Message += "<br>" + Safety_Manager_Error_Message_val2
            else:
                Labor_Message = Safety_Manager_Error_Message_val2
        if count2 > 0:
            Labor_Message3 = "<b>"+'Cost is not available for selected resource in Additional Custom Deliverables. Please select different resource or different Execution Country.Deliverables to look into: <br>'+"</b>" + Labor_Message3
            if Labor_Message != "":
                Labor_Message += "<br>" + Labor_Message3
            else:
                Labor_Message = Labor_Message3
        if Labor_Message != '':
            Product.Attr('ErrorMessage1').AssignValue(Labor_Message)
def PS_Calc_Final_Hrs(Product):
    def getFloat(Var):
        if Var:
            return float(Var)
        return 0.00
    laborRows = Product.GetContainerByName('SM_SSE_Engineering_Labor_Container').Rows
    for row in laborRows:
        try:
            lv_calc_hrs = getFloat(row.GetColumnByName('Calculated Hrs').Value)
            lv_productivity = getFloat(row.GetColumnByName('Productivity').Value)
            lv_prev_calc_hrs = getFloat(row.GetColumnByName('Prev_Calc_Hrs').Value)
            if lv_calc_hrs != lv_prev_calc_hrs:
                lv_final_hrs = round(lv_calc_hrs * lv_productivity)
                row.GetColumnByName('Final Hrs').Value = str(lv_final_hrs)
                if lv_calc_hrs == 0:
                    row['Productivity']= '1'
                else:
                    row['Productivity']= str(lv_productivity)
                row.GetColumnByName('Prev_Calc_Hrs').Value = str(lv_calc_hrs)
        except Exception, e:
            Trace.Write(str(e))
def final_hr(Product):
    def getFloat(Var):
        if Var:
            return float(Var)
        return 0.00
    laborRows = Product.GetContainerByName('SM Safety System - ESD/FGS/BMS/HIPPS Container').Rows
    for row in laborRows:
        try:
            lv_calc_hrs = getFloat(row.GetColumnByName('Calculated Hrs').Value)
            lv_productivity = getFloat(row.GetColumnByName('Productivity').Value)
            lv_prev_calc_hrs = getFloat(row.GetColumnByName('Prev_Calc_Hrs').Value)
            if lv_calc_hrs != lv_prev_calc_hrs:
                lv_final_hrs = round(lv_calc_hrs * lv_productivity)
                row.GetColumnByName('Final Hrs').Value = str(lv_final_hrs)
                if lv_calc_hrs == 0:
                    row['Productivity']= '1'
                else:
                    row['Productivity']= str(lv_productivity)
                row.GetColumnByName('Prev_Calc_Hrs').Value = str(lv_calc_hrs)
        except Exception, e:
            Trace.Write(str(e))
def PS_Populate_Prices(Product):
    from Update_System_Labor_Cost_Price import updateLaborCostPrice
    tabs = [tab.Name for tab in Product.Tabs if tab.IsSelected]
    if Product.Attr('isProductLoaded').GetValue() == 'True' and 'Labor Deliverables' in tabs:
        gesLocation = 'None'
        if Product.GetContainerByName('SM_Labor_Cont').Rows.Count > 0:
            gesLocation = Product.GetContainerByName('SM_Labor_Cont').Rows[0].GetColumnByName('GES_Location').DisplayValue
        gesMapping = {'GES India':'IN','GES China':'CN','GES Romania':'RO','GES Uzbekistan':'UZ','GES Egypt':'EG','None':'None'}
        gesLocationVC = gesMapping.get(gesLocation)
        if Quote:
            contList = ['SM_SSE_Engineering_Labor_Container', 'SM Safety System - ESD/FGS/BMS/HIPPS Container', 'SM_Additional_Custom_Deliverables_Labor_Container']
            foEngColumn = {'SM_SSE_Engineering_Labor_Container':'SM_Labor_FO_Eng', 'SM Safety System - ESD/FGS/BMS/HIPPS Container':'SM_Labor_FO_Eng', 'SM_Additional_Custom_Deliverables_Labor_Container':'SM_Labor_FO_Eng'}
            updateLaborCostPrice(Product, Quote, TagParserQuote, contList, foEngColumn, gesLocationVC, True, Session)
def PS_System_LI_Part_Summary(Product):
    sm_cont_rows = Product.GetContainerByName('SM_System_PartSummary_Cont').Rows
    errorFlag = False
    for row in sm_cont_rows:
        finalQuantity = int(row['CE_Final_Quantity'])
        if finalQuantity < 0:
            errorFlag = True
            break
    if errorFlag:
        Product.Attr('PartSummaryErrorMsg').AssignValue('True')
    else:
        Product.Attr('PartSummaryErrorMsg').AssignValue('False')
        sm_cont_rows = Product.GetContainerByName('SM_System_PartSummary_Cont').Rows
        sm_li_cont = Product.GetContainerByName('SM_System_PartSummary_LI_Cont')
        sm_li_cont.Rows.Clear()
        for row in sm_cont_rows:
            part = row['CE_Part_Number']
            quantity = row['CE_Part_Qty']
            part_description = row['CE_Part_Description']
            adjQuantity = row['CE_Adj_Quantity'] if row['CE_Adj_Quantity'] else 0
            comments = row['CE_Comments']
            finalQuantity = int(row['CE_Final_Quantity'])
            if finalQuantity > 0:
                row = sm_li_cont.AddNewRow(part, False)
                row.GetColumnByName("CE_Part_Qty").Value = quantity
                row.GetColumnByName("CE_Part_Description").Value = part_description
                row.GetColumnByName("CE_Adj_Quantity").Value = str(adjQuantity)
                row.GetColumnByName("CE_Final_Quantity").ReferencingAttribute.AssignValue(str(finalQuantity))
                row.GetColumnByName("CE_Comments").Value = comments
                row.Calculate()
    Product.ApplyRules()
saveAction = Quote.GetCustomField("R2Q_Save").Content
isR2Qquote = Quote.GetCustomField("isR2QRequest").Content
if isR2Qquote and saveAction != 'Save':
    PS_Default(Product)
    OnProductRuleExecutionEnd(Product)
    PS_Hide_Attr_Values(Product)
    PS_populate_doc_param(Product)
    PS_SM_Hide_Values(Product)
    SM_System_PartSummary(Product)
    PS_SM_SSE_Engineering_Labor_Container_Populate(Product)
    PS_SM_Calculate_Labor_Hours(Product)
    Show_Safety_Manager_Error_Deliverables(Product)
    PS_Calc_Final_Hrs(Product)
    final_hr(Product)
    PS_Populate_Prices(Product)
    PS_System_LI_Part_Summary(Product)
    Product.ParseString('<* ExecuteScript(GS_SM_SSE_Engineering_Labor_Container_Populate)*>')
    Product.ParseString('<* ExecuteScript(GS_SM_Calculate_Labor_Hours)*>')
    Product.ParseString('<* ExecuteScript(GS_SM_UpdateFinalHours)*>')
    Product.ParseString('<* ExecuteScript(GS_SM_Populate_Price)*>')
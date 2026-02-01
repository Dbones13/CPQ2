if Product.Attr('MIgration_Scope_Choices').GetValue() == "":
    import datetime
    import GS_UOC_Labor_Parameters
    # PS_UOC_Engineering_Labor_Container_Populate
    scope = Product.Attr('CE_Scope_Choices').GetValue()
    migration_scope = migration_scope = Product.Attr('MIgration_Scope_Choices').GetValue()
    if scope == 'HW/SW + LABOR' or "LABOR" in migration_scope:
        def sortRow(cont,rank,new_row_index):
            sort_needed = True
            if new_row_index == 0:
                return
            while sort_needed == True:
                Trace.Write("rank of previous row: {0}, new_row_index: {1}".format(cont.Rows[new_row_index-1].GetColumnByName('Rank').Value, new_row_index))
                if int(cont.Rows[new_row_index-1].GetColumnByName('Rank').Value) > int(rank):
                    cont.MoveRowUp(new_row_index, False)
                    new_row_index -= 1
                else:
                    sort_needed = False

        Product.ExecuteRulesOnce = True #This is to improve performance. We keep triggering product rules execution with each change to each container cell. Sets back to False at end of script.
        #salesArea = Quote.GetCustomField('Sales Area').Content
        #marketCode = Quote.SelectedMarket.MarketCode
        #salesOrg = marketCode.partition('_')[0]
        #Updated logic for Defect 29879
        #currency = marketCode.partition('_')[2]
        salesOrg = Quote.GetCustomField('Sales Area').Content
        currency = Quote.GetCustomField('Currency').Content
        query = SqlHelper.GetFirst("select Execution_County from NEW_EXECUTION_COUNTRY_SALES_ORG_MAPPING where Sales_Area = '{}' and Currency = '{}'".format(salesOrg,currency))
        #query = SqlHelper.GetFirst("select Execution_County from EXECUTION_COUNTRY_SALES_ORG_MAPPING where Execution_Country_Sales_Org = '{}'".format(salesOrg))
        try:
            attrs = GS_UOC_Labor_Parameters.AttrStorage(Product,TagParserProduct)
        except Exception,e:
            attrs = None
            Trace.Write("Error when Cacluating UOC System Labor Parameters: " + str(e))

        disallow_lst = [] 
        process_type = Product.GetContainerByName('UOC_Labor_Details').Rows[0].GetColumnByName("UOC_Process_Type_Labour").Value
        if process_type != "BatchPharma" and process_type != "BatchChemical":
            disallow_lst.append("UOC Batch Design Workshop")
            disallow_lst.append("UOC Batch Protocols")
            disallow_lst.append("UOC Batch Application Configuration")

        if process_type != "BatchPharma":
            disallow_lst.append("UOC Pharma QA Documentation")
            disallow_lst.append("UOC Pre-Test (Batch-Pharma)")
            disallow_lst.append("UOC Pharma Project Quality Management")

        if Product.Attr('Labor_Site_Activities').GetValue() != 'Yes':
            disallow_lst.append("UOC Site Installation")
            disallow_lst.append("UOC Site Acceptance Test & Sign off")

        if Product.Attr('Labor_Operation_Manual_Scope').GetValue() != 'Yes':
            disallow_lst.append("UOC Operation Manual")

        if Product.Attr('Labor_Custom_Scope').GetValue() != 'Yes':
            disallow_lst.append("UOC Customer Training")

        if Product.Attr('CE_Cutover').GetValue() in ["No",'']:
            disallow_lst.append("UOC Cut Over Procedure")
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

        bookingLOB = TagParserQuote.ParseString('<* QuoteProperty (Booking LOB) *>')
        laborCont = Product.GetContainerByName('CE UOC Engineering Labor Container')
        tableLabor = SqlHelper.GetList("select Deliverable,Calculated_Hrs,GES_Eng_NoGES,GES_Eng_GES,FO_Eng_1,FO1_Eng_NoGES,FO1_Eng_GES,FO_Eng_2,FO2_Eng_NoGES,FO2_Eng_GES,Rank,Execution_Country from CE_UOC_Engineering_Deliverables where LOB = '"+str(bookingLOB)+"'")
        gesLocation = Product.GetContainerByName('UOC_Labor_Details').Rows[0].GetColumnByName('UOC_Ges_Location_Labour').Value
        gesMapping = {'GESIndia':'IN','GESChina':'CN','GESRomania':'RO','GESUzbekistan':'UZ','GESEgypt':'EG','None':'None'}
        gesLocationVC = gesMapping.get(gesLocation)
        gesEmptyDel = ['UOC User Requirement Specification', 'UOC Engineering Plan', 'UOC Procure Materials & Services', 'UOC Customer Training', 'UOC Project Close Out Report']
        if bookingLOB != 'LSS':
            disallowValues = ['SVC-ECON-ST','SVC-ECON-ST-NC', 'SVC-ESSS-ST', 'SVC-ESSS-ST-NC', 'SVC-EAPS-ST', 'SVC-EAPS-ST-NC', 'SVC-EST1-ST', 'SVC-EST1-ST-NC', 'SVC-PMGT-ST', 'SVC-PMGT-ST-NC']
            #disallowGesValues = ['SVC_GES_P350F_UZ', 'SVC_GES_P350B_UZ', 'SVC_GES_P350F_RO', 'SVC_GES_P350B_RO', 'SVC_GES_P350F_CN', 'SVC_GES_P350B_CN', 'SVC_GES_P350F_IN', 'SVC_GES_P350B_IN']

        current_deliverables = []
        rows_to_delete = []
        for row in laborCont.Rows:
            current_deliverables.append(row.GetColumnByName('Deliverable').Value)

        for row in tableLabor:
            if row.Deliverable not in disallow_lst and row.Deliverable not in current_deliverables:
                new_row = laborCont.AddNewRow(False)
                new_row["Deliverable"] = row.Deliverable
                Trace.Write('-if-')
                #new_row.GetColumnByName('FO Eng 2').SetAttributeValue(row.FO_Eng_2)
                #new_row.GetColumnByName('FO Eng 2').SetAttributeValue(row.FO_Eng_2 if row.FO_Eng_2 != '' else 'None')
                if bookingLOB != 'LSS':
                    new_row.Product.DisallowAttrValues('CE_UOC_FO_ENG_1', *disallowValues)
                    new_row.Product.DisallowAttrValues('CE_UOC_FO_ENG_2', *disallowValues)
                    #new_row.Product.DisallowAttrValues('CE UOC GES Eng', *disallowGesValues)
                new_row.GetColumnByName('FO Eng 1').ReferencingAttribute.SelectDisplayValue(str(row.FO_Eng_1))
                new_row.GetColumnByName('FO Eng 2').ReferencingAttribute.SelectDisplayValue(str(row.FO_Eng_2))
                new_row['FO Eng 1']=row.FO_Eng_1
                new_row['FO Eng 2']=row.FO_Eng_2
                new_row.GetColumnByName('Productivity').Value = '1.00'
                if Quote.GetCustomField('R2QFlag').Content == "Yes":
                    new_row["Execution Year"] = Quote.GetCustomField('R2Q_PRJT_Execution_Year').Content
                else:
                    new_row["Execution Year"] = str(contract_start)
                new_row["Rank"] = str(row.Rank)
                sortRow(laborCont,row.Rank,new_row.RowIndex)
                if not query:
                    new_row.GetColumnByName('Execution Country').Value = ""
                else:
                    new_row.GetColumnByName('Execution Country').Value = query.Execution_County

                Trace.Write('gesLocation: '+str(gesLocation))
                new_row['GES Eng'] = ''
                new_row.GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue('')
                if gesLocation == "None" or gesLocation == '':
                    Trace.Write("geslocation")
                    #new_row["GES Eng % Split"]= row.GES_Eng_NoGES
                    # new_row["FO Eng 1"]= row.FO_Eng_1
                    new_row["FO Eng 1 % Split"]= row.FO1_Eng_NoGES
                    # new_row["FO Eng 2"]= row.FO_Eng_2
                    new_row["FO Eng 2 % Split"]= row.FO2_Eng_NoGES
                else:
                    Trace.Write("geseng")
                    new_row["GES Eng % Split"]= row.GES_Eng_GES
                    # new_row["FO Eng 1"]= row.FO_Eng_1
                    new_row["FO Eng 1 % Split"]= row.FO1_Eng_GES
                    new_row["FO Eng 2 % Split"]= row.FO2_Eng_GES
                    if row.Deliverable not in gesEmptyDel:
                        if bookingLOB != 'LSS':
                            new_row.GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue('SYS GES Eng-BO-'+gesLocationVC)
                            new_row['GES Eng']='SYS GES Eng-BO-'+gesLocationVC
                        else:
                            new_row.Product.Attr('CE UOC GES Eng').SelectDisplayValue('LSS GES Eng-BO-'+gesLocationVC)
                            new_row.GetColumnByName('GES Eng').SetAttributeValue('LSS GES Eng-BO-'+gesLocationVC)
                            new_row['GES Eng']='LSS GES Eng-BO-'+gesLocationVC
                new_row.Calculate()
            elif row.Deliverable in disallow_lst and row.Deliverable in current_deliverables:
                Trace.Write('-elif1-')
                for cont_row in laborCont.Rows:
                    if row.Deliverable == cont_row.GetColumnByName('Deliverable').Value:
                        rows_to_delete.append(cont_row.RowIndex)
                        break
            elif row.Deliverable in current_deliverables:
                Trace.Write('-elif2-')
                for cont_row in laborCont.Rows:
                    if row.Deliverable == cont_row.GetColumnByName('Deliverable').Value:
                        if gesLocationVC != cont_row.GetColumnByName('GES Eng').DisplayValue.split('-')[-1]:
                            cont_row['GES Eng'] = ''
                            cont_row.GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue('')
                            if gesLocation != "None" and gesLocation != '':
                                if row.Deliverable not in gesEmptyDel:
                                    if bookingLOB != 'LSS':
                                        cont_row.GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue('SYS GES Eng-BO-'+gesLocationVC)
                                        cont_row['GES Eng']='SYS GES Eng-BO-'+gesLocationVC
                                    else:
                                        Trace.Write('-elif3-'+str(bookingLOB))
                                        cont_row.Product.Attr('CE UOC GES Eng').SelectDisplayValue('LSS GES Eng-BO-'+gesLocationVC)
                                        cont_row.GetColumnByName('GES Eng').SetAttributeValue('LSS GES Eng-BO-'+gesLocationVC)
                                        cont_row['GES Eng']='LSS GES Eng-BO-'+gesLocationVC
                            cont_row.Calculate()
                        break
        laborCont.Calculate()
        rows_to_delete.sort(reverse=True)



        #Added By Himanshu for Popuating Year and Country

        laborAddi = Product.GetContainerByName('CE UOC Additional Custom Deliverables').Rows

        for row1 in laborAddi:
            #Trace.Write(row1['UpdatedYear'])
            if bookingLOB != 'LSS':
                row1.Product.DisallowAttrValues('CE_UOC_FO_ENG_LD', *disallowValues)
                #row1.Product.DisallowAttrValues('CE UOC GES Eng', *disallowGesValues)
            if row1.GetColumnByName('Execution Country').Value == "" and query:
                row1['Execution Country'] = query.Execution_County
            if row1.GetColumnByName('Execution Year').Value == "":
                if Quote.GetCustomField('R2QFlag').Content == "Yes":
                    row1["Execution Year"] = Quote.GetCustomField('R2Q_PRJT_Execution_Year').Content
                else:
                    row1["Execution Year"] = str(contract_start)
            if gesLocation == "None" or gesLocation == '':
                row1["FO Eng % Split"] = '100'
                row1["GES Eng % Split"] = '0'

        Product.ExecuteRulesOnce = False

        Product.Attr('isProductLoaded').AssignValue('True')

        C = int(attrs.AI) + int(attrs.AO) + int(attrs.DI) + int(attrs.DO) + int(attrs.profitnet_IO or 0) + int(attrs.ethernet_IO or 0) + int(attrs.peer_pcdi or 0) + int(attrs.peer_cda or 0)
        tabs = [tab.Name for tab in Product.Tabs if tab.IsSelected]

        if 'Labor Deliverables' in tabs and C > 5000:
            Product.Messages.Add('Hours for Engineering Plan for project with more than 5000 IO need to be estimated based on customer requirements and should be done in consultation with the Lead Engineer. Please adjust the Final Hours as per requirement.')
            #Product.SetGlobal('displayinfo', 'True')

        for x in rows_to_delete:
                laborCont.DeleteRow(x)
elif Product.Attr('MIgration_Scope_Choices').GetValue() != "":
    Product.GetContainerByName('CE UOC Engineering Labor Container').Rows.Clear()
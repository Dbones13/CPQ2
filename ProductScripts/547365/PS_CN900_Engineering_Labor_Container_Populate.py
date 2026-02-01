if Product.Attr('MIgration_Scope_Choices').GetValue() == "":
    import datetime
    #import GS_UOC_Labor_Parameters
    # PS_CN900_Engineering_Labor_Container_Populate
    scope = Product.Attr('CE_Scope_Choices').GetValue()
    migration_scope = Product.Attr('MIgration_Scope_Choices').GetValue()
    if scope == 'HW/SW + LABOR' or "LABOR" in migration_scope:
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

        Product.ExecuteRulesOnce = True #This is to improve performance. We keep triggering product rules execution with each change to each container cell. Sets back to False at end of script.
        salesArea = Quote.GetCustomField('Sales Area').Content
        #marketCode = Quote.SelectedMarket.MarketCode
        #salesOrg = marketCode.partition('_')[0]
        #currency = marketCode.partition('_')[2]
        currency = Quote.GetCustomField('Currency').Content
        query = SqlHelper.GetFirst("select Execution_County from NEW_EXECUTION_COUNTRY_SALES_ORG_MAPPING where Sales_Area = '{}' and Currency = '{}'".format(salesArea,currency))
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
        #bookingLOB = TagParserQuote.ParseString('<* QuoteProperty (Booking LOB) *>')
        laborCont = Product.GetContainerByName('CE CN900 Engineering Labor Container')
        tableLabor = SqlHelper.GetList("select Deliverable,Calculated_Hrs,GES_Eng_NoGES,GES_Eng_GES,FO_Eng_1,FO1_Eng_NoGES,FO1_Eng_GES,FO_Eng_2,FO2_Eng_NoGES,FO2_Eng_GES,Rank,Execution_Country from CE_CN900_Engineering_Deliverables")
        gesLocation = Product.GetContainerByName('CN900_Labor_Details').Rows[0].GetColumnByName('CN900_Ges_Location_Labour').Value
        gesMapping = {'GESIndia':'IN','GESChina':'CN','GESRomania':'RO','GESUzbekistan':'UZ','GESEgypt':'EG','None':'None'}
        gesLocationVC = gesMapping.get(gesLocation)

        current_deliverables = []
        for row in laborCont.Rows:
            current_deliverables.append(row.GetColumnByName('Deliverable').Value)

        for row in tableLabor:
            if row.Deliverable not in current_deliverables:
                new_row = laborCont.AddNewRow(False)
                new_row["Deliverable"] = row.Deliverable
                new_row.GetColumnByName('FO Eng 1').ReferencingAttribute.SelectDisplayValue(row.FO_Eng_1)
                new_row.GetColumnByName('FO Eng 2').ReferencingAttribute.SelectDisplayValue(row.FO_Eng_2 if row.FO_Eng_2 != '' else 'None')
                new_row['FO Eng 1']=row.FO_Eng_1
                new_row['FO Eng 2']=row.FO_Eng_2
                new_row.GetColumnByName('Productivity').Value = '1.00'
                new_row["Execution Year"] = str(contract_start)
                new_row["Rank"] = str(row.Rank)
                sortRow(laborCont,row.Rank,new_row.RowIndex)
                if salesArea == "":
                    new_row.GetColumnByName('Execution Country').Value = ""
                else:
                    new_row.GetColumnByName('Execution Country').Value = query.Execution_County

                Trace.Write('gesLocation: '+str(gesLocation))
                if gesLocation == "None" or gesLocation == '':
                    new_row["FO Eng 1 % Split"]= row.FO1_Eng_NoGES
                    new_row["FO Eng 2 % Split"]= row.FO2_Eng_NoGES
                else:
                    new_row["GES Eng % Split"]= row.GES_Eng_GES
                    new_row["FO Eng 1 % Split"]= row.FO1_Eng_GES
                    new_row["FO Eng 2 % Split"]= row.FO2_Eng_GES
                    new_row['GES Eng']= 'SYS GES Eng-BO-'+gesLocationVC
                    new_row.GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue('SYS GES Eng-BO-'+gesLocationVC)
                new_row.Calculate()
            elif row.Deliverable in current_deliverables:
                for cont_row in laborCont.Rows:
                    if row.Deliverable == cont_row.GetColumnByName('Deliverable').Value:
                        if gesLocationVC != cont_row.GetColumnByName('GES Eng').DisplayValue.split('-')[-1]:
                            #cont_row['GES Eng'] = ''
                            #cont_row.GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue('')
                            if gesLocation != "None" and gesLocation != '':
                                cont_row['GES Eng']= 'SYS GES Eng-BO-'+gesLocationVC
                                cont_row.GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue('SYS GES Eng-BO-'+gesLocationVC)
                            cont_row.Calculate()
                        break


        laborAddi = Product.GetContainerByName('CE CN900 Additional Custom Deliverables').Rows
        for row1 in laborAddi:
            if row1.GetColumnByName('Execution Country').Value == "" and salesArea != "":
                row1['Execution Country'] = query.Execution_County
            if row1.GetColumnByName('Execution Year').Value == "":
                row1["Execution Year"] = str(contract_start)
            if gesLocation == "None" or gesLocation == '':
                row1["FO Eng % Split"] = '100'
                row1["GES Eng % Split"] = '0'

        Product.ExecuteRulesOnce = False
        Product.Attr('isProductLoaded').AssignValue('True')

        '''C = int(attrs.AI) + int(attrs.AO) + int(attrs.DI) + int(attrs.DO) + int(attrs.profitnet_IO) + int(attrs.ethernet_IO) + int(attrs.peer_pcdi) + int(attrs.peer_cda)
        tabs = [tab.Name for tab in Product.Tabs if tab.IsSelected]

        if 'Labor Deliverables' in tabs and C > 5000:
            Product.Messages.Add('Hours for Engineering Plan for project with more than 5000 IO need to be estimated based on customer requirements and should be done in consultation with the Lead Engineer. Please adjust the Final Hours as per requirement.')
            #Product.SetGlobal('displayinfo', 'True')'''

elif Product.Attr('MIgration_Scope_Choices').GetValue() != "":
    Product.GetContainerByName('CE CN900 Engineering Labor Container').Rows.Clear()
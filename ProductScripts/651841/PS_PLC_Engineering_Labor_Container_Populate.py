if Product.Attr('MIgration_Scope_Choices').GetValue() == "":
    # PLC Labor Container Populate - NEW
    import GS_Labor_Engineering_Calcs, GS_Labor_Functional_Calcs, GS_Labor_Procure_Calcs, GS_Labor_Detail_Calcs, GS_Labor_Procedure_Calcs, GS_Labor_Hardware_Calcs, GS_Labor_Software_Calcs, GS_Labor_Integration_Calcs, GS_Labor_Factory_Calcs, GS_Labor_Installation_Calcs, GS_Labor_Acceptance_Calcs, GS_Labor_Cutover_Calcs, GS_Labor_Operation_Calcs, GS_Labor_Training_Calcs, GS_Labor_Close_Calcs
    import GS_PLC_Labor_Parameters
    import datetime

    Product.ExecuteRulesOnce = True #This is to improve performance. We keep triggering product rules execution with each change to each container cell. Sets back to False at end of script.

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
    try:
        attrs = GS_PLC_Labor_Parameters.AttrStorage(Product)
    except Exception,e:
        attrs = None
        Product.ErrorMessages.Add("Error when Reading Labor Parameters: " + str(e))
        Trace.Write("Error when Reading Labor Parameters: " + str(e))
        Log.Error("Error when Reading Labor Parameters: " + str(e))
    disallow_lst = [] #Added by Ashok because of CXCPQ-22649
    if Product.Attr('Labor_Site_Activities').GetValue() == "No":
        disallow_lst.append("CE PLC Site Acceptance Test & Sign off")
        disallow_lst.append("CE PLC Site Installation")

    if Product.Attr('Labor_Operation_Manual_Scope').GetValue() == "No":
        disallow_lst.append("CE PLC Operation Manual")

    if Product.Attr('Labor_Custom_Scope').GetValue() == "No":
        disallow_lst.append("CE PLC Customer Training")

    if Product.Attr('CE_Cutover').GetValue() in ["No",'']:
        disallow_lst.append("CE PLC Cut Over Procedure")
	
    #Added by Abhijeet CXCPQ-22651
    # salesArea = TagParserQuote.ParseString('<* QuoteProperty (Sales Area) *>')
    # marketCode = TagParserQuote.ParseString('<* MCODE *>')
    # salesOrg = marketCode.partition('_')[0]
    salesOrg = Quote.GetCustomField('Sales Area').Content
    query = SqlHelper.GetFirst("select Execution_County from EXECUTION_COUNTRY_SALES_ORG_MAPPING where Execution_Country_Sales_Org = '{}'".format(salesOrg))
    laborCont = Product.GetContainerByName('CE PLC Engineering Labor Container')
    Booking_LOB = TagParserQuote.ParseString('<* QuoteProperty (Booking LOB) *>')
    Query=''
    if Booking_LOB=="LSS":
        Query='select Deliverable,Calculated_Hrs,LSS_GES_Eng_NoGES as GES_Eng_NoGES,LSS_GES_Eng_GES as GES_Eng_GES,LSS_FO_Eng_1 as FO_Eng_1,LSS_FO1_Eng_NoGES as FO1_Eng_NoGES,LSS_FO1_Eng_GES as FO1_Eng_GES,LSS_FO_Eng_2 as FO_Eng_2,LSS_FO2_Eng_NoGES as FO2_Eng_NoGES,LSS_FO2_Eng_GES as FO2_Eng_GES,Rank,Execution_Country from CE_PLC_Engineering_Deliverables'
    else:
        Query='select Deliverable,Calculated_Hrs,GES_Eng_NoGES,GES_Eng_GES,FO_Eng_1,FO1_Eng_NoGES,FO1_Eng_GES,FO_Eng_2,FO2_Eng_NoGES,FO2_Eng_GES,Rank,Execution_Country from CE_PLC_Engineering_Deliverables'
    tableLabor = SqlHelper.GetList(Query)
    gesLocation = TagParserProduct.ParseString('<*CTX( Container(PLC_Labour_Details).Row(1).Column(PLC_Ges_Location).GetDisplayValue )*>')
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

    calc_name_dict = {} #This is a mapping of deliverable name to script calculation name
    for x in tableLabor:
        calc_name_dict[x.Deliverable] = x.Calculated_Hrs
    attrs = GS_PLC_Labor_Parameters.AttrStorage(Product)

    #Populate the container's columns: 'Deliverable' and Calculated Hours
    current_deliverables = []
    rows_to_delete = []
    for row in laborCont.Rows:
        current_deliverables.append(row.GetColumnByName('Deliverable').Value)

    for row in tableLabor:
        if row.Deliverable not in disallow_lst and row.Deliverable not in current_deliverables: #Added by Ashok because of CXCPQ-22649
            calc_name = calc_name_dict[row.Deliverable]
            Trace.Write("calc name: {0}".format(calc_name))
            new_row = laborCont.AddNewRow()
            new_row["Deliverable"] = row.Deliverable
            new_row.GetColumnByName('FO Eng 1').ReferencingAttribute.SelectDisplayValue(row.FO_Eng_1) #CXCPQ-22537
            new_row.GetColumnByName('FO Eng 1').SetAttributeValue(row.FO_Eng_1) #CXCPQ-22537
            new_row['FO Eng 1']=row.FO_Eng_1 # CXCPQ-52541 Leo Joseph
            new_row.GetColumnByName('FO Eng 2').ReferencingAttribute.SelectDisplayValue(row.FO_Eng_2) #CXCPQ-22670
            new_row.GetColumnByName('FO Eng 2').SetAttributeValue(row.FO_Eng_2) #CXCPQ-22670
            new_row['FO Eng 2']=row.FO_Eng_2 # CXCPQ-52541 Leo Joseph
            new_row.GetColumnByName('Productivity').Value = '1.00'
            new_row["Execution Year"] = str(contract_start)
            new_row["Rank"] = str(row.Rank)
            sortRow(laborCont,row.Rank,new_row.RowIndex)
            #try:
            #    new_row["Calculated Hrs"] = str(getattr(globals()[calc_name], calc_name)(attrs)) #dynamically calls the function within the calculation module
            #    Trace.Write("Inside Try block"+str(new_row["Calculated Hrs"]))
            #except Exception,e:
            #    Product.ErrorMessages.Add("Error when Calculating Hrs for:" + str(calc_name) + str(e))
            #    Trace.Write("Error when Calculating Hrs for: " + str(calc_name) + str(e) )
            #    Log.Error("Error when Calculating Hrs for: " + str(calc_name) + str(e) )
            if not query:
                new_row.GetColumnByName('Execution Country').Value = "United States"
            else:
                new_row.GetColumnByName('Execution Country').Value = query.Execution_County if query else ""
            if gesLocation == "None" or gesLocation == '':
                new_row["GES Eng % Split"]= row.GES_Eng_NoGES
                new_row["FO Eng 1"]= row.FO_Eng_1
                new_row["FO Eng 1 % Split"]= row.FO1_Eng_NoGES
                new_row["FO Eng 2"]= row.FO_Eng_2
                new_row["FO Eng 2 % Split"]= row.FO2_Eng_NoGES
            else:
                new_row["GES Eng % Split"]= row.GES_Eng_GES
                new_row["FO Eng 1"]= row.FO_Eng_1
                new_row["FO Eng 1 % Split"]= row.FO1_Eng_GES
                new_row["FO Eng 2 % Split"]= row.FO2_Eng_GES
        elif row.Deliverable in disallow_lst and row.Deliverable in current_deliverables:
            for cont_row in laborCont.Rows:
                if row.Deliverable == cont_row.GetColumnByName('Deliverable').Value:
                    rows_to_delete.append(cont_row.RowIndex)
                    break
    laborCont.Calculate()
    rows_to_delete.sort(reverse=True)
    for x in rows_to_delete:
            laborCont.DeleteRow(x)

    #Added by Lazer CXCPQ-22681
    laboraddcont = Product.GetContainerByName('CE PLC Additional Custom Deliverables')
    for row in laboraddcont.Rows:
        if row.GetColumnByName('Execution Year').Value == "":
            row["Execution Year"] = str(contract_start)

    #Added By Abhijeet CXCPQ-22651
    laborAddi = Product.GetContainerByName('CE PLC Additional Custom Deliverables').Rows
    # salesArea = TagParserQuote.ParseString('<* QuoteProperty (Sales Area) *>')
    # marketCode = TagParserQuote.ParseString('<* MCODE *>')
    # salesOrg = marketCode.partition('_')[0]
    salesOrg = Quote.GetCustomField('Sales Area').Content
    query = SqlHelper.GetFirst("select Execution_County from EXECUTION_COUNTRY_SALES_ORG_MAPPING where Execution_Country_Sales_Org = '{}'".format(salesOrg))
    for row1 in laborAddi:
        Trace.Write(row1['UpdatedYear'])
        if row1['UpdatedYear']:
            row1['Execution Country'] = row1['UpdatedYear']
        else:
            row1['Execution Country'] = query.Execution_County if query else ""


    Product.ExecuteRulesOnce = False
    Product.Attr('isProductLoaded').AssignValue('True')

    #This is for Product Info Message If IO's more than 5000 qty
    C = attrs.AI + attrs.AO + attrs.DI + attrs.DO
    tabs = [tab.Name for tab in Product.Tabs if tab.IsSelected]

    if 'Labor Deliverables' in tabs and C > 5000:
        Product.Messages.Add('Hours for Engineering Plan for project with more than 5000 IO need to be estimated based on customer requirements and should be done in consultation with the Lead Engineer. Please adjust the Final Hours as per requirement.')
        Product.SetGlobal('displayinfo', 'True')
    #--------------------------------------------------------------
    #This is Used to calculate FO Eng 1 % split based on GES location
    def getFloat(v):
        if v:
            return float(v)
        return 0

    con = Product.GetContainerByName('PLC_Labour_Details')
    for row in con.Rows:
        loc = row.GetColumnByName("PLC_Ges_Location").Value
    con2 = Product.GetContainerByName('CE PLC Engineering Labor Container')
    con3 = Product.GetContainerByName('CE PLC Additional Custom Deliverables')
    for row in con2.Rows:
        if row.GetColumnByName("GES Eng % Split").Value:
            Log.Info(row.GetColumnByName("GES Eng % Split").Value)
            ges = float(row.GetColumnByName("GES Eng % Split").Value)
            FO_2 = float(row.GetColumnByName("FO Eng 2 % Split").Value)
            if str(loc) == "None" or str(loc) == '':
                fo1 = 100 - FO_2
                if fo1 >= 0 and fo1 <=100:
                    row.GetColumnByName("FO Eng 1 % Split").Value = str(100 -FO_2)
            else:
                fo1 = float(100 - ges -FO_2)
                if fo1 >= 0 and fo1 <=100:
                    row.GetColumnByName("FO Eng 1 % Split").Value = str(fo1)
                else:
                    row.GetColumnByName("FO Eng 1 % Split").Value = str(0.00)
    for row in con3.Rows:
        ges_eng =  getFloat(row.GetColumnByName("GES Eng % Split").Value)
        if loc == "None" or loc == '':
            row.GetColumnByName("FO Eng % Split").Value = str(100)
        else:
            fo_eng = float(100-ges_eng)
            if fo_eng >=0 and fo_eng <= 100:
                row.GetColumnByName("FO Eng % Split").Value = str(100 - ges_eng)
elif Product.Attr('MIgration_Scope_Choices').GetValue() != "":
    Product.GetContainerByName('CE PLC Engineering Labor Container').Rows.Clear()
    Product.GetContainerByName('CE PLC Additional Custom Deliverables').Rows.Clear()
# PMD Labor Container Populate - NEW
import GS_Labor_Engineering_Calcs, GS_Labor_Functional_Calcs, GS_Labor_Procure_Calcs, GS_Labor_Detail_Calcs, GS_Labor_Procedure_Calcs, GS_Labor_Hardware_Calcs, GS_Labor_Software_Calcs, GS_Labor_Integration_Calcs, GS_Labor_Factory_Calcs, GS_Labor_Installation_Calcs, GS_Labor_Acceptance_Calcs, GS_Labor_Cutover_Calcs, GS_Labor_Operation_Calcs, GS_Labor_Training_Calcs, GS_Labor_Close_Calcs
import GS_PMD_Labor_Parameters
import GS_PMD_ReadAttrs
import datetime

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
scope = Product.Attr('CE_Scope_Choices').GetValue()
if scope == 'HW/SW + LABOR':
    get_attrs = GS_PMD_ReadAttrs.AttrStorage(Product)
    Trace.Write("get_attrs"+str(get_attrs))
    try:
        attrs = GS_PMD_Labor_Parameters.AttrStorage(Product, get_attrs)
    except Exception,e:
        attrs = None
        Product.ErrorMessages.Add("Error when Reading Labor Parameters: " + str(e))
        Trace.Write("Error when Reading Labor Parameters: " + str(e))

    disallow_lst = []
    if Product.Attr('Labor_Site_Activities').GetValue() == "No":
        disallow_lst.append("PMD Site Acceptance Test & Sign off")
        disallow_lst.append("PMD Site Installation")

    if Product.Attr('Labor_Operation_Manual_Scope').GetValue() == "No":
        disallow_lst.append("PMD Operation Manual")

    if Product.Attr('Labor_Custom_Scope').GetValue() == "No":
        disallow_lst.append("PMD Customer Training")

    if Product.Attr('CE_Cutover').GetValue() in ["No",'']:
        disallow_lst.append("PMD Cut Over Procedure")
    #CXCPQ-22779
    salesArea = TagParserQuote.ParseString('<* QuoteProperty (Sales Area) *>')
    marketCode = TagParserQuote.ParseString('<* MCODE *>')
    #salesOrg = marketCode.partition('_')[0]
    salesOrg = Quote.GetCustomField('Sales Area').Content
    query = SqlHelper.GetFirst("select Execution_County from EXECUTION_COUNTRY_SALES_ORG_MAPPING where Execution_Country_Sales_Org = '{}'".format(salesOrg)) 
    laborCont = Product.GetContainerByName('PMD Engineering Labor Container')
    tableLabor = SqlHelper.GetList('select * from CE_PMD_Engineering_Deliverables')
    gesLocation = Product.GetContainerByName('PMD_Labour_Details').Rows[0].GetColumnByName('PMD_Ges_Location').Value

    #CXCPQ-23784
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

    #Populate the container's columns: 'Deliverable' and Calculated Hours
    current_deliverables = []
    rows_to_delete = []
    for row in laborCont.Rows:
        current_deliverables.append(row.GetColumnByName('Deliverable').Value)

    for row in tableLabor:
        if row.Deliverable not in disallow_lst and row.Deliverable not in current_deliverables:
            calc_name = calc_name_dict[row.Deliverable]
            Trace.Write("calc name: {0}".format(calc_name))
            new_row = laborCont.AddNewRow(True)
            new_row["Deliverable"]= row.Deliverable
            new_row.GetColumnByName('FO Eng 1').SetAttributeValue(row.FO_Eng_1)
            new_row["FO Eng 1"]=row.FO_Eng_1
            new_row.GetColumnByName('FO Eng 2').SetAttributeValue(row.FO_Eng_2)
            new_row["FO Eng 2"]=row.FO_Eng_2
            new_row.GetColumnByName('Productivity').Value = '1.00'
            #new_row["Final Hrs"]= row.Final_Hrs
            new_row["Execution Year"] = str(contract_start)
            new_row["Rank"] = str(row.Rank)
            sortRow(laborCont,row.Rank,new_row.RowIndex)
            #try:
            #    new_row["Calculated Hrs"] = str(getattr(globals()[calc_name], calc_name)(attrs)) #dynamically calls the function within the calculation module
            #    Trace.Write("Inside Try block"+str(new_row["Calculated Hrs"]))
            #except Exception,e:
            #    Product.ErrorMessages.Add("Error when Calculating Hrs for:" + str(calc_name) + str(e))
            #    Trace.Write("Error when Calculating Hrs for: " + str(calc_name) + str(e))

            if salesArea == "":
                new_row.GetColumnByName('Execution Country').Value = "United States"
            else:
                new_row.GetColumnByName('Execution Country').Value = query.Execution_County
            if gesLocation == "None" or gesLocation == '':
                new_row["GES Eng % Split"] = row.GES_Eng_NoGES
                new_row["FO Eng 1 % Split"] = row.FO1_Eng_NoGES
                new_row["FO Eng 2 % Split"] = row.FO2_Eng_NoGES
            else:
                new_row["GES Eng % Split"] = row.GES_Eng_Split
                new_row["FO Eng 1 % Split"] = row.FO_Eng_1_Split
                new_row["FO Eng 2 % Split"] = row.FO_Eng_2_Split
        elif row.Deliverable in disallow_lst and row.Deliverable in current_deliverables:
            for cont_row in laborCont.Rows:
                if row.Deliverable == cont_row.GetColumnByName('Deliverable').Value:
                    rows_to_delete.append(cont_row.RowIndex)
    laborCont.Calculate()
    rows_to_delete.sort(reverse=True)
    for x in rows_to_delete:
            laborCont.DeleteRow(x)

    laboraddcont = Product.GetContainerByName('PMD Labor Additional Custom Deliverable')
    for row in laboraddcont.Rows:
        if row.GetColumnByName('Execution Year').Value == "":
            row["Execution Year"] = str(contract_start)

    laborAddi = Product.GetContainerByName('PMD Labor Additional Custom Deliverable').Rows
    salesArea = TagParserQuote.ParseString('<* QuoteProperty (Sales Area) *>')
    marketCode = TagParserQuote.ParseString('<* MCODE *>')
    #salesOrg = marketCode.partition('_')[0]
    salesOrg = Quote.GetCustomField('Sales Area').Content
    query = SqlHelper.GetFirst("select Execution_County from EXECUTION_COUNTRY_SALES_ORG_MAPPING where Execution_Country_Sales_Org = '{}'".format(salesOrg))
    for row1 in laborAddi:
        Trace.Write(row1['UpdatedYear'])
        if row1['UpdatedYear']:
            row1['Execution Country'] = row1['UpdatedYear']
        else:
            row1['Execution Country'] = query.Execution_County

    Product.Attr('isProductLoaded').AssignValue('True')

    #This is for Product Info Message If IO's more than 5000 qty
    C = attrs.AI + attrs.AO + attrs.DI + attrs.DO
    tabs = [tab.Name for tab in Product.Tabs if tab.IsSelected]

    if 'Labor Deliverables' in tabs and C > 5000:
        Product.Messages.Add('Hours for Engineering Plan for project with more than 5000 IO need to be estimated based on customer requirements and should be done in consultation with the Lead Engineer. Please adjust the Final Hours as per requirement.')
        Product.SetGlobal('displayinfo', 'True')
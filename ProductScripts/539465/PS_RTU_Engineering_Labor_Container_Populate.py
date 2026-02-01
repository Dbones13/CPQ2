#PS_RTU_Engineering_Labor_Container_Populate
import datetime
#import GS_UOC_Labor_Parameters
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
    Product.ExecuteRulesOnce = True #This is to improve performance. We keep triggering product rules execution with each change to each container cell. Sets back to False at end of script.
    salesArea = Quote.GetCustomField('Sales Area').Content
    marketCode = Quote.SelectedMarket.MarketCode
    #salesOrg = marketCode.partition('_')[0]
    #Updated logic for Defect 29879
    #currency = marketCode.partition('_')[2]
    currency = Quote.GetCustomField('Currency').Content
    query = SqlHelper.GetFirst("select Execution_County from NEW_EXECUTION_COUNTRY_SALES_ORG_MAPPING where Sales_Area = '{}' and Currency = '{}'".format(salesArea,currency))
    #query = SqlHelper.GetFirst("select Execution_County from EXECUTION_COUNTRY_SALES_ORG_MAPPING where Execution_Country_Sales_Org = '{}'".format(salesArea))

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

    disallow_lst = [] 

    if Product.Attr('Labor_Site_Activities').GetValue() != 'Yes':
        disallow_lst.append("RTU Site Installation")
        disallow_lst.append("RTU Site Acceptance Test & Sign off")

    if Product.Attr('Labor_Operation_Manual_Scope').GetValue() != 'Yes':
        disallow_lst.append("RTU Operation Manual")

    if Product.Attr('Labor_Custom_Scope').GetValue() != 'Yes':
        disallow_lst.append("RTU Customer Training")

    if Product.Attr('New_Expansion').GetValue() == 'Expansion':   #in ["No",'']:
        if Product.Attr('CE_Cutover').GetValue() != 'Yes':
            disallow_lst.append("RTU Cut Over Procedure")
    else:
        disallow_lst.append("RTU Cut Over Procedure")

    '''if Product.Attr('CE_Cutover').GetValue() != 'Yes' and Product.Attr('New_Expansion').GetValue() != 'Expansion':   #in ["No",'']:
        disallow_lst.append("RTU Cut Over Procedure")'''


    laborCont = Product.GetContainerByName('CE RTU Engineering Labor Container')
    tableLabor = SqlHelper.GetList('select Deliverable,Calculated_Hrs,GES_Eng_NoGES,GES_Eng_GES,FO_Eng_1,FO1_Eng_NoGES,FO1_Eng_GES,FO_Eng_2,FO2_Eng_NoGES,FO2_Eng_GES,Rank,Execution_Country from CE_RTU_Engineering_Deliverables')
    gesLocation = Product.GetContainerByName('RTU_Software_Labor_Container2').Rows[0].GetColumnByName('RTU_GES_Location').Value
    gesMapping = {'GESIndia':'IN','GESChina':'CN','GESRomania':'RO','GESUzbekistan':'UZ','None':'None'}
    gesLocationVC = gesMapping.get(gesLocation)
    gesEmptyDel = ['RTU FEL Site Visit', 'RTU Procure Materials & Services', 'RTU Customer Training', 'RTU Project Close Out Report']
    current_deliverables = []
    rows_to_delete = []
    for row in laborCont.Rows:
        current_deliverables.append(row.GetColumnByName('Deliverable').Value)

    for row in tableLabor:
        if row.Deliverable not in disallow_lst and row.Deliverable not in current_deliverables:
            new_row = laborCont.AddNewRow(False)
            new_row["Deliverable"] = row.Deliverable
            new_row.GetColumnByName('FO Eng 1').SetAttributeValue(row.FO_Eng_1)
            new_row.GetColumnByName('FO Eng 2').SetAttributeValue(row.FO_Eng_2 if row.FO_Eng_2 != '' else 'None')
            new_row["FO Eng 1"]=row.FO_Eng_1
            new_row["FO Eng 2"]=row.FO_Eng_2
            #new_row.GetColumnByName('Productivity').Value = '1.00'
            new_row["Execution Year"] = str(contract_start)
            new_row["Rank"] = str(row.Rank)
            sortRow(laborCont,row.Rank,new_row.RowIndex)
            if salesArea == "":
                new_row.GetColumnByName('Execution Country').Value = ""
            else:
                new_row.GetColumnByName('Execution Country').Value = query.Execution_County

            Trace.Write('gesLocation: '+str(gesLocation))
            new_row['GES Eng'] = ''
            new_row.GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue('')
            if gesLocation == "None" or gesLocation == '':
                new_row["GES Eng % Split"]= row.GES_Eng_NoGES
                # new_row["FO Eng 1"]= row.FO_Eng_1
                new_row["FO Eng 1 % Split"]= row.FO1_Eng_NoGES
                # new_row["FO Eng 2"]= row.FO_Eng_2
                new_row["FO Eng 2 % Split"]= row.FO2_Eng_NoGES
            else:
                new_row["GES Eng % Split"]= row.GES_Eng_GES
                # new_row["FO Eng 1"]= row.FO_Eng_1
                new_row["FO Eng 1 % Split"]= row.FO1_Eng_GES
                new_row["FO Eng 2 % Split"]= row.FO2_Eng_GES
                if row.Deliverable in gesEmptyDel:
                    new_row['GES Eng'] = ''
                else:
                    new_row.GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue('SYS GES Eng-BO-'+gesLocationVC)
                    new_row['GES Eng']='SYS GES Eng-BO-'+gesLocationVC
                #if row.Deliverable not in gesEmptyDel:
                    #new_row.GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue('SYS GES Eng-BO-'+gesLocationVC)
        elif row.Deliverable in disallow_lst and row.Deliverable in current_deliverables:
            for cont_row in laborCont.Rows:
                if row.Deliverable == cont_row.GetColumnByName('Deliverable').Value:
                    rows_to_delete.append(cont_row.RowIndex)
                    break
        elif row.Deliverable in current_deliverables:
            for cont_row in laborCont.Rows:
                if row.Deliverable == cont_row.GetColumnByName('Deliverable').Value:
                    if gesLocationVC !='' and gesLocationVC != cont_row.GetColumnByName('GES Eng').DisplayValue.split('-')[-1]:
                        cont_row['GES Eng'] = ''
                        cont_row.GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue('')
                        if gesLocation != "None" and gesLocation != '':
                            if row.Deliverable not in gesEmptyDel:
                                cont_row.GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue('SYS GES Eng-BO-'+gesLocationVC)
                                cont_row['GES Eng']='SYS GES Eng-BO-'+gesLocationVC
                        cont_row.Calculate()
                    break
    laborCont.Calculate()
    rows_to_delete.sort(reverse=True)
    laborAddi = Product.GetContainerByName('CE RTU Additional Custom Deliverables').Rows

    for row1 in laborAddi:
        #Trace.Write(row1['UpdatedYear'])
        if row1.GetColumnByName('Execution Country').Value == "" and salesArea != "":
            row1['Execution Country'] = query.Execution_County
        if row1.GetColumnByName('Execution Year').Value == "":
            row1["Execution Year"] = str(contract_start)
        if gesLocation == "None" or gesLocation == '':
            row1["FO Eng % Split"] = '100'
            row1["GES Eng % Split"] = '0'

    Product.GetContainerByName('CE RTU Additional Custom Deliverables').Calculate()
    Product.ExecuteRulesOnce = False
    Product.Attr('isProductLoaded').AssignValue('True')

    for x in rows_to_delete:
            laborCont.DeleteRow(x)
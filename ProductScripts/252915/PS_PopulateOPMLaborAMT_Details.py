from GS_MigrationLaborHoursModule import getnumberOfjumpRealease
import math

def getContainer(Product,Name):
    return Product.GetContainerByName(Name)

def getRowData(Product,container,column):
    Container = getContainer(Product,container)
    for row in Container.Rows:
        return row[column]

def getRowDataIndex(Product,container,column,index):
    Container = getContainer(Product,container)
    for row in Container.Rows:
        if row.RowIndex == index:
            return row[column]

def getFloat(Var):
    if Var:
        return float(Var)
    return 0

def getSalesOrg(country):
    query = SqlHelper.GetFirst("select Execution_Country_Sales_Org from EXECUTION_COUNTRY_SALES_ORG_MAPPING where Execution_County = '{}'".format(country))
    if query is not None:
        #Trace.Write("SalesOrg = " + query.Execution_Country_Sales_Org)
        return query.Execution_Country_Sales_Org

def laborCostWithCOnversion(laborcostParts):
    quoteCurrency = Quote.SelectedMarket.CurrencyCode
    costWithConversion = dict()
    if laborcostParts:
        for key in laborcostParts:
            Trace.Write(laborcostParts[key]["stdcurrency"])
            if quoteCurrency == "USD" or laborcostParts[key]["stdcurrency"] == "USD":
                query = SqlHelper.GetFirst("select Exchange_Rate from Currency_ExchangeRate_Mapping where From_Currency = '{}' and To_Currency = '{}'".format(laborcostParts[key]["stdcurrency"],quoteCurrency))
                costWithConversion[key] = getFloat(laborcostParts[key]["cost"]) * getFloat(query.Exchange_Rate)
            else:
                factor = 1.00
                query1 = SqlHelper.GetFirst("select Exchange_Rate from Currency_ExchangeRate_Mapping where From_Currency = '{}' and To_Currency = '{}'".format(laborcostParts[key]["stdcurrency"],'USD'))
                if query1 is not None:
                    factor = factor * getFloat(query1.Exchange_Rate)
                    queryUSD = SqlHelper.GetFirst("select Exchange_Rate from Currency_ExchangeRate_Mapping where From_Currency = '{}' and To_Currency = '{}'".format('USD',quoteCurrency))
                    if queryUSD is not None:
                        factor = factor * getFloat(queryUSD.Exchange_Rate)
                    else:
                        factor = 1.00
                costWithConversion[key] = getFloat(laborcostParts[key]["cost"]) * factor
    #Trace.Write("cost conversion")
    #Trace.Write(str(costWithConversion))
    return costWithConversion

def getFopartsCost(salesOrg,partNumber,executionYear):
    query = "Select * from HPS_LABOR_COST_DATA where Sales_Org = '{0}' and Part_Number in ('{1}')".format(salesOrg,partNumber)
    res = SqlHelper.GetList(query)
    foCost = dict()
    for i in res:
        if executionYear == str(DateTime.Now.Year):
            foCost[i.Part_Number] = {"cost":i.Cost_CurrentMonth_Year1,"stdcurrency":i.Cost_Currency_Code}
        elif executionYear == str(DateTime.Now.Year + 1):
            foCost[i.Part_Number] = {"cost":i.Cost_CurrentMonth_Year2,"stdcurrency":i.Cost_Currency_Code}
        elif executionYear == str(DateTime.Now.Year + 2):
            foCost[i.Part_Number] = {"cost":i.Cost_CurrentMonth_Year3,"stdcurrency":i.Cost_Currency_Code}
        elif executionYear == str(DateTime.Now.Year + 3):
            foCost[i.Part_Number] = {"cost":i.Cost_CurrentMonth_Year4,"stdcurrency":i.Cost_Currency_Code}
    Trace.Write(str(foCost))
    foCostWithConversion = laborCostWithCOnversion(foCost)
    return foCostWithConversion

parameters = {"MSID_CommonQuestions":{"Var_22":"MSID_FEL_Data_Gathering_Required","Var_5":"MSID_Current_Experion_Release"},"OPM_Node_Configuration":{"Var_1":"OPM_No_of_Experion_Servers","Var_2_1":"OPM_No_of_ACET_Servers_LCN_Connected","Var_2_2":"OPM_No_of_EAPP_Servers_LCN_Connected","Var_3_1":"OPM_Qty_of_ESF_and_ES-CE_Rack_Mount","Var_3_2":"OPM_Qty_of_ESF_and_ESCE_Tower","Var_27_1":"OPM_Qty_of_ESC_Rack_Mount","Var_27_2":"OPM_Qty_of_ESC_Tower","Var_4_1":"OPM_No_of_EST_Rack_mount","Var_4_2":"OPM_No_of_EST_Tower","Var_8":"OPM_No_of_Other_Servers_to_be_migrated","Var_9":"OPM_Qty_of_RPS_and_Thin_Clients","Var_10":"OPM_Qty_of_Series_C_Controllers","Var_11":"OPM_Qty_of_Profibus_Modules","Var_12":"OPM_Qty_of_Control_Firewalls_CF9s","Var_13":"OPM_Qty_of_Series_C_IO_Modules_excluding_UIO","Var_14":"OPM_Qty_of_Fieldbus_Interface_Modules","Var_25":"OPM_Qty_of_Series_A_IO_Modules","Var_26":"OPM_Qty_of_UIO_UIO2_Modules"},"OPM_Services":{"Var_32":"OPM_is_system_required_Domain_controller_upgrade","Var_33":"OPM_Additional_hrs_for_Document_Customization","Var_23":"OPM_Acceptance_Test_Required"},"OPM_Basic_Information":{"Var_24":"OPM_RESS_Migration_in_scope","Var_21":"OPM_Is_the_Experion_System_LCN_Connected","Var_31":"OPM_Is_this_is_a_Remote_Migration_Service_RMS"},"OPM_FTE_Switches_migration_info":{"Var_28":"OPM_Quantity_of_L1_L2_Switches","Var_29":"OPM_Qty_of_Backbone_or_Agg_Fiber_Optic_Switch"}}
for key in parameters:
    if key == "MSID_CommonQuestions":
        Var_22 = getRowData(Product,key,parameters[key]["Var_22"])
        Var_5 = getRowData(Product,key,parameters[key]["Var_5"])
    elif key == "OPM_Node_Configuration":
        Var_1 = getFloat(getRowData(Product,key,parameters[key]["Var_1"]))
        Var_2 = getFloat(getRowData(Product,key,parameters[key]["Var_2_1"])) + getFloat(getRowData(Product,key,parameters[key]["Var_2_2"]))
        Var_3 = getFloat(getRowData(Product,key,parameters[key]["Var_3_1"])) + getFloat(getRowData(Product,key,parameters[key]["Var_3_2"]))
        Var_27 = getFloat(getRowData(Product,key,parameters[key]["Var_27_1"])) + getFloat(getRowData(Product,key,parameters[key]["Var_27_2"]))
        Var_4 = getFloat(getRowData(Product,key,parameters[key]["Var_4_1"])) + getFloat(getRowData(Product,key,parameters[key]["Var_4_2"]))
        Var_8 = getFloat(getRowData(Product,key,parameters[key]["Var_8"]))
        Var_9 = getFloat(getRowData(Product,key,parameters[key]["Var_9"]))
        Var_10 = getFloat(getRowData(Product,key,parameters[key]["Var_10"]))
        Var_11 = getFloat(getRowData(Product,key,parameters[key]["Var_11"]))
        Var_12 = getFloat(getRowData(Product,key,parameters[key]["Var_12"]))
        Var_13 = getFloat(getRowData(Product,key,parameters[key]["Var_13"]))
        Var_14 = getFloat(getRowData(Product,key,parameters[key]["Var_14"]))
        Var_25 = getFloat(getRowData(Product,key,parameters[key]["Var_25"]))
        Var_26 = getFloat(getRowData(Product,key,parameters[key]["Var_26"]))

    elif key == "OPM_Services":
        Var_32 = getRowData(Product,key,parameters[key]["Var_32"])
        Var_33 = getFloat(getRowData(Product,key,parameters[key]["Var_33"]))
        Var_23 = getRowData(Product,key,parameters[key]["Var_23"])
    elif key == "OPM_Basic_Information":
        ressScope = getRowData(Product,key,parameters[key]["Var_24"])
        Var_24 = 0
        Var_31 = getRowData(Product,key,parameters[key]["Var_31"])
        if ressScope == "Yes":
            Var_24 = 1
        elif ressScope == "No":
            Var_24 = 0
        Var_21 = getRowData(Product,key,parameters[key]["Var_21"])
    elif key == "OPM_FTE_Switches_migration_info":
        Var_28 = getFloat(getRowData(Product,key,parameters[key]["Var_28"]))
        Var_29 = getFloat(getRowData(Product,key,parameters[key]["Var_29"]))

additonOfParamenters = Var_1 + Var_2 + Var_3 + Var_4 + Var_8 + Var_27
Var_7 = getFloat(getnumberOfjumpRealease(Product))

def calculate_smallSystem(Var_1, Var_3, Var_4, Var_7, Var_8, Var_27, Var_24):
    # Calculate the inner part of the formula
    inner_result = Var_3 + Var_4 + Var_27 + Var_8 + Var_24
    inner_divisor = Var_1 if Var_1 < 2 else Var_1 / 2
    if inner_divisor == 0:
        return 0
    inner_result = inner_result / inner_divisor

    # Check the condition and assign the appropriate value
    if inner_result < 4:
        final_result = 19
    else:
        final_result = 0

    # Calculate the final result
    final_result = final_result * Var_7 * (Var_1 if Var_1 < 2 else math.ceil(Var_1 / 2))
    final_result = math.ceil(final_result)

    return final_result
    


def calculate_mediumSystem(Var_1, Var_3, Var_4, Var_7, Var_27):
    # Calculate the inner part of the formula
    inner_result = Var_3 + Var_4 + Var_27
    inner_divisor = Var_1 if Var_1 < 2 else Var_1 / 2
    if inner_divisor == 0:
        return 0
    inner_result = inner_result / inner_divisor
    inner_result = math.floor(inner_result)

    # Check the conditions and assign the appropriate value
    condition_1 = inner_result > 3
    condition_2 = inner_result < 8
    if condition_1 and condition_2:
        final_result = 22.2
    else:
        final_result = 0

    # Calculate the final result
    final_result = final_result * Var_7 * (Var_1 if Var_1 < 2 else math.ceil(Var_1 / 2))
    final_result = math.ceil(final_result)

    return final_result

def calculate_largeSystem(Var_1, Var_3, Var_4, Var_7, Var_27):
    # Calculate the inner part of the formula
    inner_divisor = Var_1 if Var_1 < 2 else Var_1 / 2
    if inner_divisor == 0:
        return 0
    inner_result = (Var_3 + Var_4 + Var_27) / inner_divisor
    inner_result = math.floor(inner_result)

    # Check the condition and assign the appropriate value
    if inner_result > 7:
        final_result = 27.44
    else:
        final_result = 0

    # Calculate the final result
    final_result = final_result * Var_7 * (Var_1 if Var_1 < 2 else math.ceil(Var_1 / 2))
    final_result = math.ceil(final_result)

    return final_result

sspc = calculate_smallSystem(Var_1, Var_3, Var_4, Var_7, Var_8, Var_27, Var_28)
mspc = calculate_mediumSystem(Var_1, Var_3, Var_4, Var_7, Var_27)
lspc = calculate_largeSystem(Var_1, Var_3, Var_4, Var_7, Var_27)
Trace.Write("SS {}  , MS  {}  , LS {} ".format(sspc,mspc,lspc))
mcoeHrsChange = str(sspc + mspc + lspc)
Trace.Write(mcoeHrsChange)
amt = getRowData(Product,'OPM_Basic_Information','OPM_Is_this_is_a_Remote_Migration_Service_RMS')
selectedProducts = Product.Attr('MSID_Selected_Products').GetValue().split('<br>')
scope = Product.Attr('MIgration_Scope_Choices').GetValue()
activeServiceContract = Product.Attr("MSID_Active_Service_Contract").GetValue()
Trace.Write(activeServiceContract)
exe_country = ''
exe_year = ''
depL2 = 0
migL2 = 0
mcoe_hrs = 0
salesOrg = ''
opmEng = getContainer(Product,'MSID_Labor_OPM_Engineering')

for row in opmEng.Rows:
    if row["Deliverable"] == "OPM MCOE - AMT":
        exe_country = row["Execution_Country"]
        exe_year = row["Execution_Year"]
        mcoe_hrs += getFloat(row["Calculated_Hrs"])
    if row["Deliverable"] == "OPM Deployment L2 - AMT":
        depL2 = getFloat(row["Calculated_Hrs"])

migL2 = mcoe_hrs + depL2
hrs_saved = getFloat(migL2) - (getFloat(depL2) + getFloat(mcoeHrsChange ))
eac_per = 0.00
if exe_country != '' and exe_year != '':
    salesOrg = getSalesOrg(exe_country)
if getFloat(migL2) > 0:
	eac_per = (getFloat(hrs_saved)/getFloat(migL2)) * 100

if eac_per > 0 and amt == 'Yes':
     Product.AllowAttr('OPM_LaborAMT_Details')
else:
    Product.DisallowAttr("OPM_LaborAMT_Details")

if 'OPM' in selectedProducts and scope != "HW/SW" and eac_per > 0:
    amt_cont = getContainer(Product,'OPM_LaborAMT_Details')
    query = SqlHelper.GetList('Select * from OPM_LABORAMT')
    amt_cont.Rows.Clear()
    for entry in query:
        Trace.Write(entry.Description)
        row = amt_cont.AddNewRow(False)
        row["Description"] = entry.Description
        row["Execution Country"] = exe_country
        row["Execution Year"] = exe_year
        if activeServiceContract == 'Yes':
            row["FO Engineer"] = 'SVC-EAPS-ST'
        if activeServiceContract == 'No':
            row["FO Engineer"] = 'SVC-EAPS-ST-NC'
        row["Actual MCOE hour charge for AMT (Hr)"] = mcoeHrsChange
        row["Deployment L2 - AMT (Hr)"] = str(depL2)
        row["Migration_L2_Non-AMT_Hr"] = str(migL2)
        row["L2 AMT Migration Hour saved (Hr)"] = str(hrs_saved)
        row["Productivity EAC in %"] = str(round(eac_per,2))
        if salesOrg != '':
            if activeServiceContract == 'Yes':
                cost = getFopartsCost(salesOrg,'SVC-EAPS-ST',exe_year)
                focost = cost['SVC-EAPS-ST']
                row["Cost Saving with AMT"] = str(round(getFloat(focost) * getFloat(hrs_saved),2))
            elif activeServiceContract == 'No':
                cost = getFopartsCost(salesOrg,'SVC-EAPS-ST-NC',exe_year)
                focost = cost['SVC-EAPS-ST-NC']
                row["Cost Saving with AMT"] = str(round(getFloat(focost) * getFloat(hrs_saved),2))
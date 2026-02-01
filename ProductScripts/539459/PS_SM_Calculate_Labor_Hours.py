#PS_SM_Calculate_Labor_Hours
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
#tabs = [tab.Name for tab in Product.Tabs if tab.IsSelected]
if Product.Attr('isProductLoaded').GetValue() == 'True' and scope == 'HW/SW + LABOR':

    Product.ExecuteRulesOnce = True
    laborCont = Product.GetContainerByName('SM_SSE_Engineering_Labor_Container')
    laborCont1 = Product.GetContainerByName('SM Safety System - ESD/FGS/BMS/HIPPS Container')

    tableLabor = SqlHelper.GetList("select Deliverable,Productivity,GES_Eng_1_No,GES_Eng,FO_Eng_1_NoGES,FO_Eng_1_GES_None,FO_Eng_1_GES,FO_Eng_2_NoGES,FO_Eng_2_GES_None,FO_Eng_2_GES,Rank,Calculated_Hrs,Execution_Country from SAFETY_MANAGER_LABOR_SSE_ENGINEERING_LABOR where Calculated_Hrs != ''")
    tableLabor1 = SqlHelper.GetList('select Deliverable,Productivity,GES_Eng_1_No,GES_Eng,FO_Eng_1_NoGES,FO_Eng_1_GES_None,FO_Eng_1_GES,FO_Eng_2_NoGES,FO_Eng_2_GES_None,FO_Eng_2_GES,Rank,Calculated_Hrs,Execution_Country from SAFETY_MANAGER_LABOR_SSE_ENGINEERING_LABOR_TWO')
    calc_name_dict = {} #This is a mapping of deliverable name to script calculation name
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
        Trace.Write("Error when Cacluating SM Labor Parameters: " + str(e))

    for row in laborCont.Rows:
        deliverable = row.GetColumnByName("Deliverable").Value
        if deliverable in calc_name_dict.keys() and not isFloat(calc_name_dict[deliverable]):
            calc_name = calc_name_dict[row.GetColumnByName("Deliverable").Value]
            Trace.Write("calc name: {0}".format(calc_name))
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
                Trace.Write(msg)
    laborCont.Calculate()

    for row in laborCont1.Rows:
        deliverable = row.GetColumnByName("Deliverable").Value
        if deliverable in calc_name_dict1.keys() and not isFloat(calc_name_dict1[deliverable]):
            calc_name = calc_name_dict1[row.GetColumnByName("Deliverable").Value]
            Trace.Write("calc name: {0}".format(calc_name))
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
                Trace.Write(msg)
    laborCont1.Calculate()
    Product.ExecuteRulesOnce = False
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

if Product.Name == "Virtualization System":
    scope = Product.Attr('CE_Scope_Choices').GetValue()
    if Product.Attr('isProductLoaded').GetValue() == 'True' and scope == 'HW/SW + LABOR':
        Product.ExecuteRulesOnce = True
        laborCont = Product.GetContainerByName('Virtualization_Labor_Deliverable')

        tableLabor = SqlHelper.GetList("select Deliverable,Productivity,GES_Eng_1_No,GES_Eng,FO_Eng_1_NoGES,FO_Eng_1_GES_None,FO_Eng_1_GES,FO_Eng_2_NoGES,FO_Eng_2_GES_None,FO_Eng_2_GES,Rank,Calculated_Hrs,Execution_Country from TABLE_VIRTUALIZATION_LABOR_DELIVERABLE where Calculated_Hrs != ''")
        calc_name_dict = {} #This is a mapping of deliverable name to script calculation name
        for x in tableLabor:
            calc_name_dict[x.Deliverable] = x.Calculated_Hrs

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
                    msg = "Error when Calculating Hours for: {0}, Error: {1}, Line Number: {2}".format(calc_name, e, sys.exc_traceback.tb_lineno)
                    Product.ErrorMessages.Add(msg)
                    Trace.Write(msg)
                    Log.Error(msg)
        laborCont.Calculate()
        Product.ExecuteRulesOnce = False
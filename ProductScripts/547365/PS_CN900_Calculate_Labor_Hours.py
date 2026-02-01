#PS_CN900_Calculate_Labor_Hours
if Product.Attr('isProductLoaded').GetValue() == 'True':
    import GS_CN900_Documentation_Calcs, GS_CN900_Configuration_Calcs
    import GS_CN900_Labor_Parameters

    Product.ExecuteRulesOnce = True
    laborCont = Product.GetContainerByName('CE CN900 Engineering Labor Container')
    tableLabor = SqlHelper.GetList("select Deliverable,Calculated_Hrs,GES_Eng_NoGES,GES_Eng_GES,FO_Eng_1,FO1_Eng_NoGES,FO1_Eng_GES,FO_Eng_2,FO2_Eng_NoGES,FO2_Eng_GES,Rank,Execution_Country from CE_CN900_Engineering_Deliverables where Calculated_Hrs != ''")
    calc_name_dict = {} #This is a mapping of deliverable name to script calculation name
    for x in tableLabor:
        calc_name_dict[x.Deliverable] = x.Calculated_Hrs
    try:
        attrs = GS_CN900_Labor_Parameters.AttrStorage(Product)
    except Exception,e:
        attrs = None
        Log.Error("Error when Calculating CN900 System Labor Parameters: " + str(e))

    for row in laborCont.Rows:
        deliverable = row.GetColumnByName("Deliverable").Value
        if deliverable in calc_name_dict.keys():
            calc_name = calc_name_dict[row.GetColumnByName("Deliverable").Value]
            #Trace.Write("calc name: {0}".format(calc_name))
            try:
                row.GetColumnByName("Calculated Hrs").Value = str(getattr(globals()[calc_name], calc_name)(attrs)) #dynamically calls the function within the calculation module
                final_hr = row.GetColumnByName('Final Hrs').Value
                calc_hr = float(row.GetColumnByName('Calculated Hrs').Value)
                if final_hr == '' and calc_hr > 0:
                    prod = float(row.GetColumnByName('Productivity').Value)
                    final = round(calc_hr * prod)
                    row.GetColumnByName('Final Hrs').Value = str(final)
            except Exception,e:
                msg = "Error when Calculating Hours for: {0}, Error: {1}".format(calc_name, e)
                #Product.ErrorMessages.Add(msg)
                Log.Error(msg)

    Product.ExecuteRulesOnce = False
    laborCont.Calculate()
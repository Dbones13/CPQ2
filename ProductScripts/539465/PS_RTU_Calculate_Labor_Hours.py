#PS_UOC_Calculate_Labor_Hours
if Product.Attr('isProductLoaded').GetValue() == 'True':
    import GS_RTU_Labor_Parameters, GS_RTU_System_Integration_Internal_Test_Pre_Fat, GS_RTU_Site_Installation, GS_RTU_Hardware_Engineering
    import GS_RTU_FEL_Site_Visit_Calcs
    import GS_RTU_FAT_and_SAT_Calcs
    import GS_RTU_Hardware_Detail_Design_Spec_Calcs
    import GS_RTU_Procure_Materials_Services_calcs
    import GS_RTU_Control_Detail_Design_Specifications_Calcs
    import GS_RTU_Functional_Design_Spec_Calcs
    import GS_RTU_Operation_Manual_calc
    import GS_RTU_Project_Close_Out_Report
    import GS_RTU_Software_Configuration_Calcs
    import GS_RTU_Site_Acceptance_Test_Sign_off_Calcs
    import GS_RTU_Factory_Acceptance_Test_Sign_off_Calcs
    Product.ExecuteRulesOnce = True
    laborCont = Product.GetContainerByName('CE RTU Engineering Labor Container')
    tableLabor = SqlHelper.GetList("select Deliverable,Calculated_Hrs,GES_Eng_NoGES,GES_Eng_GES,FO_Eng_1,FO1_Eng_NoGES,FO1_Eng_GES,FO_Eng_2,FO2_Eng_NoGES,FO2_Eng_GES,Rank,Execution_Country from CE_RTU_Engineering_Deliverables where Calculated_Hrs != ''")
    calc_name_dict = {} #This is a mapping of deliverable name to script calculation name
    for x in tableLabor:
        calc_name_dict[x.Deliverable] = x.Calculated_Hrs
    try:
        attrs = GS_RTU_Labor_Parameters.AttrStorage(Product)
    except Exception,e:
        attrs = None
        Product.ErrorMessages.Add("Error when Cacluating RTU System Labor Parameters")
        Trace.Write("Error when Cacluating RTU System Labor Parameters: " + str(e) )
        Log.Error("Error when Cacluating RTU System Labor Parameters: " + str(e) )

    for row in laborCont.Rows:
        deliverable = row.GetColumnByName("Deliverable").Value
        if deliverable in calc_name_dict.keys():
            calc_name = calc_name_dict[row.GetColumnByName("Deliverable").Value]
            Trace.Write("calc name: {0}".format(calc_name))
            try:
                row.GetColumnByName("Calculated Hrs").Value = str(getattr(globals()[calc_name], calc_name)(attrs)) #dynamically calls the function within the calculation module
                final_hr = row.GetColumnByName('Final Hrs').Value
                calc_hr = float(row.GetColumnByName('Calculated Hrs').Value)
                if final_hr == '' and calc_hr > 0:
                    prod = float(row.GetColumnByName('Productivity').Value)
                    final = round(calc_hr * prod)
                    row.GetColumnByName('Final Hrs').Value = str(final)
            except Exception,e:
                msg = "Error when Calculating Hours for: {0}, Error: {1}, Line Number: {2}".format(calc_name, e, 'sys.exc_traceback.tb_lineno')
                Product.ErrorMessages.Add(msg)
                Trace.Write(msg)
                Log.Error(msg)

    Product.ExecuteRulesOnce = False
    laborCont.Calculate()
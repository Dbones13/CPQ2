#PS_UOC_Calculate_Labor_Hours
if Product.Attr('isProductLoaded').GetValue() == 'True':
    import GS_UOC_Labor_Engineering_Plan_Calcs, GS_UOC_Test_Procedure_FAT_SAT_Calcs
    import GS_UOC_Labor_Parameters
    import GS_UOC_Labor_BatchDesignWorkshop_Calcs
    import GS_UOC_Labor_Detail_Design_Specification_Calcs
    import GS_UOC_Labor_SiteInstallation_Calcs
    import GS_UOC_BatchProtocols_Calcs
    import GS_UOC_Labor_SystemIntegration_Internal_Calcs
    import GS_UOC_Functional_Design_Specification_Calcs
    import GS_UOC_PharmaProjectQuality_Calcs
    import GS_UOC_ProcureMaterialService_Calcs
    import GS_UOC_Batch_Application_Configuration_Calcs
    import GS_UOC_Factory_Acceptance_Test_Calcs
    import GS_UOC_PharmaQADocumentation_Calcs
    import GS_UOC_Site_Acceptance_Test_Calcs
    import GS_UOC_CloseOutReport_Calcs
    import GS_UOC_OperationManual_Calcs
    import GS_UOC_Hardware_Engineering_Calcs
    import GS_UOC_Control_Application_Configuration_Calcs
    import GS_UOC_PharmaPreTest_Calcs
    import GS_UOC_Soft_IO_Configuration_Calcs
    import GS_UOC_Hardware_DetailDesign_Spec_Calcs

    Product.ExecuteRulesOnce = True
    ##checkMPA = GS_Labor_Utils.checkForMPACustomer(Quote, TagParserQuote)
    laborCont = Product.GetContainerByName('CE UOC Engineering Labor Container')

    tableLabor = SqlHelper.GetList("select Deliverable,Calculated_Hrs,GES_Eng_NoGES,GES_Eng_GES,FO_Eng_1,FO1_Eng_NoGES,FO1_Eng_GES,FO_Eng_2,FO2_Eng_NoGES,FO2_Eng_GES,Rank,Execution_Country from CE_UOC_Engineering_Deliverables where Calculated_Hrs != ''")
    calc_name_dict = {} #This is a mapping of deliverable name to script calculation name
    for x in tableLabor:
        calc_name_dict[x.Deliverable] = x.Calculated_Hrs
    try:
        attrs = GS_UOC_Labor_Parameters.AttrStorage(Product,TagParserProduct)
        #adding project duration value to the attrs object
        bpd = 0
        if Quote:
            #Updated logic for Defect 29866
            #bpd = Quote.GetCustomField('EGAP_Project_Duration_Months').Content.strip()
            bpd = Quote.GetCustomField('EGAP_Project_Duration_Weeks').Content.strip()
            if bpd:
                bpd = int(bpd)
            else:
                bpd = 0
        attrs.bpd = bpd
    except Exception,e:
        attrs = None
        #Product.ErrorMessages.Add("Error when Cacluating UOC System Labor Parameters: " + str(e) + " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))
        Trace.Write("Error when Cacluating UOC System Labor Parameters: " + str(e))
        Log.Error("Error when Cacluating UOC System Labor Parameters: " + str(e))

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
                Trace.Write(msg)
                Log.Error(msg)

    Product.ExecuteRulesOnce = False
    laborCont.Calculate()
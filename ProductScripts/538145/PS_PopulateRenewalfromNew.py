if Product.Attr('SC_Product_Type').GetValue() == "Renewal":
    Exchange_Rate = float(Quote.GetCustomField('SC_CF_PRVYR_EXCH_RATE').Content) if Quote.GetCustomField('SC_CF_PRVYR_EXCH_RATE').Content else 1
    Product.Attr('SC_Trace_PYListPrice').AssignValue('')
    Product.Attr('SC_License_type_PY').SelectValue(Product.Attr('SC_License_type').GetValue())
    Product.Attr('SC_Central_Managed_SQL_PY').SelectValue(Product.Attr('SC_Central_Managed_SQL').GetValue())
    Product.Attr('SC_Select_desired_Release_PY').SelectValue(Product.Attr('SC_Select_desired_Release').GetValue())
    Product.Attr('SC_Standard_User_CALs_PY').AssignValue(Product.Attr('SC_Standard_User_CALs').GetValue())
    Product.Attr('SC_Business_Level_Access_PY').SelectValue(Product.Attr('SC_Business_Level_Access').GetValue())
    Product.Attr('SC_L4_Trace_Server_Option_PY').SelectValue(Product.Attr('SC_L4_Trace_Server_Option').GetValue())
    Product.Attr('SC_Number_of_Concurrent_Users_PY').SelectValue(Product.Attr('SC_Number_of_Concurrent_Users').GetValue())
    Product.Attr('SC_Years_of_Support_PY').AssignValue(Product.Attr('SC_Years_of_Support').GetValue())
    Product.Attr('SC_ESVT_PY').AssignValue(Product.Attr('SC_ESVT').GetValue())
    Product.Attr('SC_Experion_PKS_PY').AssignValue(Product.Attr('SC_Experion_PKS').GetValue())
    Product.Attr('SC_Honeywell_TPS_PY').AssignValue(Product.Attr('SC_Honeywell_TPS').GetValue())
    Product.Attr('SC_Experion_LX_Plantcruise_PY').AssignValue(Product.Attr('SC_Experion_LX_Plantcruise').GetValue())
    Product.Attr('SC_Honeywell_Safety_Manager_S300_PY').AssignValue(Product.Attr('SC_Honeywell_Safety_Manager_S300').GetValue())
    Product.Attr('SC_Triconex_PY').AssignValue(Product.Attr('SC_Triconex').GetValue())
    Product.Attr('SC_FSC_PY').AssignValue(Product.Attr('SC_FSC').GetValue())
    Product.Attr('SC_Experion_SCADA_PY').AssignValue(Product.Attr('SC_Experion_SCADA').GetValue())
    Product.Attr('SC_APC_Aspen_DMC_or_ProfitSuite_PY').AssignValue(Product.Attr('SC_APC_Aspen_DMC_or_ProfitSuite').GetValue())
    Product.Attr('SC_Honeywell_ControlEdge_PLC_PY').AssignValue(Product.Attr('SC_Honeywell_ControlEdge_PLC').GetValue())
    Product.Attr('SC_Uniformance_PHD_PY').AssignValue(Product.Attr('SC_Uniformance_PHD').GetValue())
    Product.Attr('SC_OSI_PI_PY').AssignValue(Product.Attr('SC_OSI_PI').GetValue())
    Product.Attr('SC_SPI_Tools_PY').AssignValue(Product.Attr('SC_SPI_Tools').GetValue())
    Product.Attr('SC_RS_Logix_PY').AssignValue(Product.Attr('SC_RS_Logix').GetValue())
    Product.Attr('SC_Custom_User_Defined_System_PY').AssignValue(Product.Attr('SC_Custom_User_Defined_System').GetValue())
    if Product.Attr('SC_License_type_PY').GetValue() == "Term":
        Trace_Summary = Product.GetContainerByName("SC_Trace_Summary")
        Trace_Summary.Rows.Clear()
        Product.Attr('SC_ESVT').AssignValue('0')
        Product.Attr('SC_Experion_PKS').AssignValue('0')
        Product.Attr('SC_Honeywell_TPS').AssignValue('0')
        Product.Attr('SC_Experion_LX_Plantcruise').AssignValue('0')
        Product.Attr('SC_Honeywell_Safety_Manager_S300').AssignValue('0')
        Product.Attr('SC_Triconex').AssignValue('0')
        Product.Attr('SC_FSC').AssignValue('0')
        Product.Attr('SC_Experion_SCADA').AssignValue('0')
        Product.Attr('SC_APC_Aspen_DMC_or_ProfitSuite').AssignValue('0')
        Product.Attr('SC_Honeywell_ControlEdge_PLC').AssignValue('0')
        Product.Attr('SC_Uniformance_PHD').AssignValue('0')
        Product.Attr('SC_OSI_PI').AssignValue('0')
        Product.Attr('SC_SPI_Tools').AssignValue('0')
        Product.Attr('SC_RS_Logix').AssignValue('0')
        Product.Attr('SC_Custom_User_Defined_System').AssignValue('0')
        Product.Attr('SC_Business_Level_Access').SelectValue('No')
        Product.Attr('SC_L4_Trace_Server_Option').SelectValue('No')
        Product.Attr('SC_Number_of_Concurrent_Users').SelectValue('Up to 5 users')
        Product.Attr('SC_Central_Managed_SQL').SelectValue('No')
        Product.Attr('SC_Select_desired_Release').SelectValue('R160')
        license_period = 1
        if Quote:
            contract_duration = Quote.GetCustomField('SC_CF_CONTRACTDURYR').Content
            if contract_duration != "":
                contract_duration = contract_duration.split()
                if int(eval(contract_duration[0])) < float(contract_duration[0]):
                    contract_duration[0] = int(eval(contract_duration[0])) + 1
                else:
                    contract_duration[0] = int(eval(contract_duration[0]))
                license_period = contract_duration[0]
                if license_period > 5:
                    license_period = 5
        try:
            years_support = Product.Attr('SC_Years_of_Support').GetValue()
            if license_period <= 3:
                Product.Attr('SC_Years_of_Support').AssignValue(str(license_period))
                Trace.Write('checking.......'+str(years_support+Product.Attr('SC_Years_of_Support').GetValue()))
            else:
                Product.Attr('SC_Years_of_Support').AssignValue('3')
        except:
            pass
        Summary_Entitlement = Product.GetContainerByName("SC_Trace_ServiceProduct_Entitlement")
        Summary_Entitlement.Rows.Clear()
        entitlement_query = SqlHelper.GetList("select Entitlement,ServiceProduct,IsMandatory from CT_SC_ENTITLEMENTS_DATA where Product_Type='Trace'")
        if entitlement_query is not None:
            for row in entitlement_query:
                if row.ServiceProduct == "Trace Software Support" and row.IsMandatory == "TRUE":
                    new_row = Summary_Entitlement.AddNewRow(False)
                    new_row["Service_Product"] = row.ServiceProduct
                    new_row["Entitlement"] = row.Entitlement
                    new_row["Type"] = "Mandatory"
                    new_row["ServiceProductEntitlementPair"] = new_row["Service_Product"] + '|' + new_row["Entitlement"]
    pyListPrice = float(Product.Attr('SC_Trace_CY_ListPrice').GetValue()) if Product.Attr('SC_Trace_CY_ListPrice').GetValue() else 0
    pySellPrice = float(Product.Attr('SC_Trace_CY_CostPrice').GetValue()) if Product.Attr('SC_Trace_CY_CostPrice').GetValue() else 0
    Product.Attr('SC_Trace_PY_ListPrice').AssignValue(str(pyListPrice*Exchange_Rate))
    Product.Attr('SC_Trace_PY_CostPrice').AssignValue(str(pySellPrice*Exchange_Rate))
    Product.AttrValue('SC_License_type', 'Term').Allowed = False

Product.Attr('SC_Renewal_check').AssignValue('1')
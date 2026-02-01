if Product.Attr('isProductLoaded').GetValue() == 'True':
    import datetime
    #Added by Ashok - CXCPQ-22674

    #The following sets the proper value of 'Execution Year' in the Labor Container, based on the Contract Start Date in the Quote:
    current_year = datetime.datetime.now().year

    years_list = Product.Attr('CE PLC Engineering Execution Year').Values
    for year in years_list:
        if int(year.ValueCode) in range(current_year + 4, 2037):
            Product.DisallowAttrValues('CE PLC Engineering Execution Year', year.ValueCode)
        elif int(year.ValueCode) < current_year:
            Product.DisallowAttrValues('CE PLC Engineering Execution Year', year.ValueCode)

    #Added by Lazer - CXCPQ-22681

    years_list_cd = Product.Attr('PLC_CD_LD_Engineering_Execution_Year').Values
    for year in years_list_cd:
        if int(year.ValueCode) in range(current_year + 4, 2037):
            Product.DisallowAttrValues('PLC_CD_LD_Engineering_Execution_Year', year.ValueCode)
        elif int(year.ValueCode) < current_year:
            Product.DisallowAttrValues('PLC_CD_LD_Engineering_Execution_Year', year.ValueCode)
    Booking_LOB = TagParserQuote.ParseString('<* QuoteProperty (Booking LOB) *>')
    specific_location={}
    LSS_FO_Engg=['SVC-ECON-ST','SVC-ECON-ST-NC','SVC-ESSS-ST','SVC-ESSS-ST-NC','SVC-EAPS-ST','SVC-EAPS-ST-NC','SVC-EST1-ST','SVC-EST1-ST-NC','SVC-PMGT-ST','SVC-PMGT-ST-NC']
    '''if Booking_LOB=="LSS":
        specific_location = {'GESChina': ['HPS_GES_P350B_IN', 'HPS_GES_P350F_IN', 'HPS_GES_P350B_RO', 'HPS_GES_P350F_RO', 'HPS_GES_P350B_UZ', 'HPS_GES_P350F_UZ','SVC_GES_P350B_IN','SVC_GES_P350F_IN','SVC_GES_P350B_RO','SVC_GES_P350F_RO','SVC_GES_P350B_UZ','SVC_GES_P350F_UZ'], 'GESIndia': ['HPS_GES_P350B_CN', 'HPS_GES_P350F_CN', 'HPS_GES_P350B_RO', 'HPS_GES_P350F_RO', 'HPS_GES_P350B_UZ', 'HPS_GES_P350F_UZ','SVC_GES_P350B_CN','SVC_GES_P350F_CN','SVC_GES_P350B_RO','SVC_GES_P350F_RO','SVC_GES_P350B_UZ','SVC_GES_P350F_UZ'],'GESRomania':['HPS_GES_P350B_CN', 'HPS_GES_P350F_CN', 'HPS_GES_P350B_IN', 'HPS_GES_P350F_IN', 'HPS_GES_P350B_UZ', 'HPS_GES_P350F_UZ','SVC_GES_P350B_IN','SVC_GES_P350F_IN','SVC_GES_P350B_CN','SVC_GES_P350F_CN','SVC_GES_P350B_UZ','SVC_GES_P350F_UZ'],'GESUzbekistan':['HPS_GES_P350B_CN', 'HPS_GES_P350F_CN', 'HPS_GES_P350B_IN', 'HPS_GES_P350F_IN', 'HPS_GES_P350B_RO', 'HPS_GES_P350F_RO','SVC_GES_P350B_IN','SVC_GES_P350F_IN','SVC_GES_P350B_CN','SVC_GES_P350F_CN','SVC_GES_P350B_RO','SVC_GES_P350F_RO']}
    else:
        specific_location = {'GESChina': ['HPS_GES_P350B_IN', 'HPS_GES_P350F_IN', 'HPS_GES_P350B_RO', 'HPS_GES_P350F_RO', 'HPS_GES_P350B_UZ', 'HPS_GES_P350F_UZ','SVC_GES_P350B_IN','SVC_GES_P350F_IN','SVC_GES_P350B_CN','SVC_GES_P350F_CN','SVC_GES_P350B_RO','SVC_GES_P350F_RO','SVC_GES_P350B_UZ','SVC_GES_P350F_UZ'], 'GESIndia': ['HPS_GES_P350B_CN', 'HPS_GES_P350F_CN', 'HPS_GES_P350B_RO', 'HPS_GES_P350F_RO', 'HPS_GES_P350B_UZ', 'HPS_GES_P350F_UZ','SVC_GES_P350B_IN','SVC_GES_P350F_IN','SVC_GES_P350B_CN','SVC_GES_P350F_CN','SVC_GES_P350B_RO','SVC_GES_P350F_RO','SVC_GES_P350B_UZ','SVC_GES_P350F_UZ'],'GESRomania':['HPS_GES_P350B_CN', 'HPS_GES_P350F_CN', 'HPS_GES_P350B_IN', 'HPS_GES_P350F_IN', 'HPS_GES_P350B_UZ', 'HPS_GES_P350F_UZ','SVC_GES_P350B_IN','SVC_GES_P350F_IN','SVC_GES_P350B_CN','SVC_GES_P350F_CN','SVC_GES_P350B_RO','SVC_GES_P350F_RO','SVC_GES_P350B_UZ','SVC_GES_P350F_UZ'],'GESUzbekistan':['HPS_GES_P350B_CN', 'HPS_GES_P350F_CN', 'HPS_GES_P350B_IN', 'HPS_GES_P350F_IN', 'HPS_GES_P350B_RO', 'HPS_GES_P350F_RO','SVC_GES_P350B_IN','SVC_GES_P350F_IN','SVC_GES_P350B_CN','SVC_GES_P350F_CN','SVC_GES_P350B_RO','SVC_GES_P350F_RO','SVC_GES_P350B_UZ','SVC_GES_P350F_UZ']}'''
    
    if Booking_LOB=="LSS":
        specific_location = {'GESChina': ['SVC_GES_P350F_CN','SVC_GES_P350B_CN','HPS_GES_P350F_CN','HPS_GES_P350B_CN'], 'GESIndia': ['SVC_GES_P350F_IN','SVC_GES_P350B_IN','HPS_GES_P350F_IN','HPS_GES_P350B_IN'],'GESRomania':['SVC_GES_P350F_RO','SVC_GES_P350B_RO','HPS_GES_P350F_RO','HPS_GES_P350B_RO'],'GESUzbekistan':['SVC_GES_P350F_UZ','SVC_GES_P350B_UZ','HPS_GES_P350F_UZ','HPS_GES_P350B_UZ'],'GESEgypt':['HPS_GES_P350F_EG','HPS_GES_P350B_EG']}
    else:
        specific_location = {'GESChina': ['HPS_GES_P350F_CN','HPS_GES_P350B_CN'], 'GESIndia': ['HPS_GES_P350F_IN','HPS_GES_P350B_IN'],'GESRomania':['HPS_GES_P350F_RO','HPS_GES_P350B_RO'],'GESUzbekistan':['HPS_GES_P350F_UZ','HPS_GES_P350B_UZ'],'GESEgypt':['HPS_GES_P350F_EG','HPS_GES_P350B_EG']}
 
    def FOdisallow(LSS_FO_Engg, dropdownlist):
        if LSS_FO_Engg:
            for i in dropdownlist:
                if i.ValueCode in LSS_FO_Engg:
                    i.Allowed = False

    def disallow(location, dropdownlist):
        if location:
            for i in dropdownlist:
                if i.ValueCode in location:
                    i.Allowed = True
                elif i.ValueCode not in location:
                    i.Allowed = False

    remove_deliverables = ['CE PLC Engineering Plan', 'CE PLC Procure Materials & Services', 'CE PLC Customer Training', 'CE PLC Project Close Out Report']
    gesloc = Product.GetContainerByName('PLC_Labour_Details').Rows[0].GetColumnByName('PLC_Ges_Location')
    if gesloc.Value != "None" and gesloc.Value !='':
        deliverables = Product.GetContainerByName('CE PLC Engineering Labor Container')
        for row in deliverables.Rows:
            if row['Deliverable'] not in remove_deliverables:
                location = row.GetColumnByName('GES Eng')
                value_list = location.ReferencingAttribute.Values
                disallow(specific_location[gesloc.Value], value_list)
                if Booking_LOB!="LSS":
                    FO1_Eng = row.GetColumnByName('FO Eng 1')
                    value_list1 = FO1_Eng.ReferencingAttribute.Values
                    FOdisallow(LSS_FO_Engg, value_list1)
                    FO2_Eng = row.GetColumnByName('FO Eng 2')
                    value_list2 = FO2_Eng.ReferencingAttribute.Values
                    FOdisallow(LSS_FO_Engg, value_list2)
        deliverables.Calculate();
        custom_deliverables = Product.GetContainerByName('CE PLC Additional Custom Deliverables')
        for deliverable in custom_deliverables.Rows:
            deliverable_location = deliverable.GetColumnByName('GES Eng')
            dropdown_values = deliverable_location.ReferencingAttribute.Values
            disallow(specific_location[gesloc.Value], dropdown_values)
            if Booking_LOB!="LSS":
                FO_Eng = deliverable.GetColumnByName('FO Eng')
                value_list = FO_Eng.ReferencingAttribute.Values
                FOdisallow(LSS_FO_Engg, value_list)
        custom_deliverables.Calculate();
tabs = [tab.Name for tab in Product.Tabs if tab.IsSelected]
if Product.Attr('isProductLoaded').GetValue() == 'True' and 'Labor Deliverables' in tabs:
    Trace.Write('test')
    specific_location = {'GESChina': ['HPS_GES_P350B_CN', 'HPS_GES_P350F_CN'], 'GESIndia': ['HPS_GES_P350B_IN', 'HPS_GES_P350F_IN'],'GESRomania':['HPS_GES_P350B_RO', 'HPS_GES_P350F_RO'],'GESUzbekistan':['HPS_GES_P350B_UZ', 'HPS_GES_P350F_UZ'],'GESEgypt':['HPS_GES_P350B_EG', 'HPS_GES_P350F_EG'],'GES China': ['HPS_GES_P350B_CN', 'HPS_GES_P350F_CN'], 'GES India': ['HPS_GES_P350B_IN', 'HPS_GES_P350F_IN'],'GES Romania':['HPS_GES_P350B_RO', 'HPS_GES_P350F_RO'],'GES Uzbekistan':['HPS_GES_P350B_UZ', 'HPS_GES_P350F_UZ'],'GES Egypt':['HPS_GES_P350B_EG', 'HPS_GES_P350F_EG']}

    def disallow(location, dropdownlist):
        if location:
            for i in dropdownlist:
                if i.ValueCode in location:
                    i.Allowed = True
                elif i.ValueCode not in location:
                    i.Allowed = False

    remove_deliverables = ['SSE User Requirement Specification']
    gesloc = ''
    if Product.GetContainerByName('SM_Labor_Cont').Rows.Count > 0:
        gesloc = Product.GetContainerByName('SM_Labor_Cont').Rows[0].GetColumnByName('GES_Location').Value

    if gesloc != "None" and gesloc != "":
        deliverables = Product.GetContainerByName('SM_SSE_Engineering_Labor_Container')
        for row in deliverables.Rows:
            if row['Deliverable'] not in remove_deliverables:
                location = row.GetColumnByName('GES Eng')
                value_list = location.ReferencingAttribute.Values
                disallow(specific_location[gesloc], value_list)
                row.ApplyProductChanges()
                row.Calculate()
        deliverables.Calculate();
        deliverables1 = Product.GetContainerByName('SM Safety System - ESD/FGS/BMS/HIPPS Container')
        for row in deliverables1.Rows:
            if row['Deliverable'] not in remove_deliverables:
                location = row.GetColumnByName('GES Eng')
                value_list = location.ReferencingAttribute.Values
                disallow(specific_location[gesloc], value_list)
                row.ApplyProductChanges()
                row.Calculate()
        deliverables1.Calculate();
        custom_deliverables = Product.GetContainerByName('SM_Additional_Custom_Deliverables_Labor_Container')
        for deliverable in custom_deliverables.Rows:
            deliverable_location = deliverable.GetColumnByName('GES Eng')
            dropdown_values = deliverable_location.ReferencingAttribute.Values
            disallow(specific_location[gesloc], dropdown_values)
            deliverable.ApplyProductChanges()
            deliverable.Calculate()
        custom_deliverables.Calculate()
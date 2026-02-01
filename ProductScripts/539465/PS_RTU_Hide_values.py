tabs = [tab.Name for tab in Product.Tabs if tab.IsSelected]
if 'Labor Deliverables' in tabs:
    '''specific_location = {'GESChina': ['HPS_GES_P350B_IN', 'HPS_GES_P350F_IN', 'HPS_GES_P350B_RO', 'HPS_GES_P350F_RO', 'HPS_GES_P350B_UZ', 'HPS_GES_P350F_UZ'], 'GESIndia': ['HPS_GES_P350B_CN', 'HPS_GES_P350F_CN', 'HPS_GES_P350B_RO', 'HPS_GES_P350F_RO', 'HPS_GES_P350B_UZ', 'HPS_GES_P350F_UZ'],'GESRomania':['HPS_GES_P350B_CN', 'HPS_GES_P350F_CN', 'HPS_GES_P350B_IN', 'HPS_GES_P350F_IN', 'HPS_GES_P350B_UZ', 'HPS_GES_P350F_UZ'],'GESUzbekistan':['HPS_GES_P350B_CN', 'HPS_GES_P350F_CN', 'HPS_GES_P350B_IN', 'HPS_GES_P350F_IN', 'HPS_GES_P350B_RO', 'HPS_GES_P350F_RO']}'''
    
    specific_location ={'GESChina': ['HPS_GES_P350B_CN','HPS_GES_P350F_CN','SVC_GES_P350B_CN','SVC_GES_P350F_CN'], 'GESIndia': ['HPS_GES_P350B_IN','HPS_GES_P350F_IN','SVC_GES_P350B_IN','SVC_GES_P350F_IN'],'GESRomania':['HPS_GES_P350B_RO','HPS_GES_P350F_RO','SVC_GES_P350B_RO','SVC_GES_P350F_RO'],'GESUzbekistan':['HPS_GES_P350B_UZ','HPS_GES_P350F_UZ','SVC_GES_P350B_UZ','SVC_GES_P350F_UZ'],'GESEgypt':['HPS_GES_P350B_EG','HPS_GES_P350F_EG']}

    def disallow(location, dropdownlist):
        firstTrue = None
        shouldUpdate = True
        if location:
            for i in dropdownlist:
                if i.ValueCode not in location or i.ValueCode == 'None':
                    i.Allowed = False
                    i.IsSelected = False
                elif i.ValueCode  in location:
                    if not firstTrue:
                        firstTrue = i
                    if i.IsSelected:
                        shouldUpdate = False
                    i.Allowed = True
        if shouldUpdate:
            firstTrue.IsSelected = True

    remove_deliverables = ['RTU FEL Site Visit', 'RTU Procure Materials & Services', 'RTU Customer Training', 'RTU Project Close Out Report']
    gesloc = Product.GetContainerByName('RTU_Software_Labor_Container2').Rows[0].GetColumnByName('RTU_GES_Location')
    if gesloc.Value != "None" and gesloc.Value != "":
        Trace.Write(gesloc)
        deliverables = Product.GetContainerByName('CE RTU Engineering Labor Container')
        for row in deliverables.Rows:
            if row['Deliverable'] not in remove_deliverables :
                location = row.GetColumnByName('GES Eng')
                value_list = location.ReferencingAttribute.Values
                disallow(specific_location[gesloc.Value], value_list)
            else:
                row.GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue('None')
            row.ApplyProductChanges()
            row.Calculate()
        deliverables.Calculate();
        custom_deliverables = Product.GetContainerByName('CE RTU Additional Custom Deliverables')
        for deliverable in custom_deliverables.Rows:
            deliverable_location = deliverable.GetColumnByName('GES Eng')
            dropdown_values = deliverable_location.ReferencingAttribute.Values
            disallow(specific_location[gesloc.Value], dropdown_values)
            Trace.Write(dropdown_values)
            deliverable.Calculate()
        custom_deliverables.Calculate()
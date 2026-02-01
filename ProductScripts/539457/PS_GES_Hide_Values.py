if Product.Name == "Virtualization System":
    if 1:
        specific_location = {'GES China': ['HPS_GES_P350B_IN', 'HPS_GES_P350F_IN','HPS_GES_P350B_RO','HPS_GES_P350F_RO','HPS_GES_P350B_UZ','HPS_GES_P350F_UZ'], 'GES India': ['HPS_GES_P350B_CN', 'HPS_GES_P350F_CN','HPS_GES_P350B_RO','HPS_GES_P350F_RO','HPS_GES_P350B_UZ','HPS_GES_P350F_UZ'], 'GES Romania':['HPS_GES_P350B_CN', 'HPS_GES_P350F_CN','HPS_GES_P350B_IN','HPS_GES_P350F_IN','HPS_GES_P350B_UZ','HPS_GES_P350F_UZ'], 'GES Uzbekistan':['HPS_GES_P350B_CN', 'HPS_GES_P350F_CN','HPS_GES_P350B_IN','HPS_GES_P350F_IN','HPS_GES_P350B_RO','HPS_GES_P350F_RO'],'None':[]}
        def disallow(location, dropdownlist):
            if location:
                for i in dropdownlist:
                    if i.ValueCode in location:
                        i.Allowed = False
                    elif i.ValueCode not in location:
                        i.Allowed = True
        remove_deliverables = []
        gesloc = Product.Attr('Virtualization_Ges_Location').SelectedValue.ValueCode
        if gesloc != "None" or gesloc != "":
            deliverables = Product.GetContainerByName('Virtualization_Labor_Deliverable')
            for row in deliverables.Rows:
                if row['Deliverable'] not in remove_deliverables:
                    location = row.GetColumnByName('GES Eng')
                    value_list = location.ReferencingAttribute.Values
                    disallow(specific_location[gesloc], value_list)
                    row.Calculate()
            deliverables.Calculate()
            custom_deliverables = Product.GetContainerByName('Virtualization_Additional_Custom_Deliverables')
            for custom_deliverable in custom_deliverables.Rows:
                deliverable_location = custom_deliverable.GetColumnByName('GES Eng')
                dropdown_values = deliverable_location.ReferencingAttribute.Values
                disallow(specific_location[gesloc], dropdown_values)
                custom_deliverable.Calculate()
            custom_deliverables.Calculate()
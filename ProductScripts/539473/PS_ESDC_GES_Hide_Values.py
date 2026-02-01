tabs = [tab.Name for tab in Product.Tabs if tab.IsSelected]
#condition to run the below script only on Labor Deliverables tab
if 'Labor Deliverables' in tabs and Product.Attr('isProductLoaded').GetValue() == 'True':
    Trace.Write('test')
    specific_location = {'GES China': ['HPS_GES_P215B_CN','HPS_GES_P215F_CN','HPS_GES_P350B_CN','HPS_GES_P350F_CN','HPS_GES_P335B_CN','HPS_GES_P335F_CN'], 'GES India': ['HPS_GES_P215B_IN','HPS_GES_P215F_IN','HPS_GES_P350B_IN','HPS_GES_P350F_IN','HPS_GES_P335B_IN','HPS_GES_P335F_IN'], 'GES Romania':['HPS_GES_P215B_RO','HPS_GES_P215F_RO','HPS_GES_P350B_RO','HPS_GES_P350F_RO','HPS_GES_P335B_RO','HPS_GES_P335F_RO'], 'GES Uzbekistan':['HPS_GES_P215B_UZ','HPS_GES_P215F_UZ','HPS_GES_P350B_UZ','HPS_GES_P350F_UZ','HPS_GES_P335B_UZ','HPS_GES_P335F_UZ'], 'GES Egypt': ['HPS_GES_P350B_EG','HPS_GES_P350F_EG','HPS_GES_P215B_EG','HPS_GES_P215F_EG','HPS_GES_P335B_EG','HPS_GES_P335F_EG']}
    defaults = {'GES China': 'HPS_GES_P215B_CN', 'GES India': 'HPS_GES_P215B_IN', 'GES Romania': 'HPS_GES_P215B_RO', 'GES Uzbekistan': 'HPS_GES_P215B_UZ', 'GES Egypt': 'HPS_GES_P350B_EG'}
    def disallow(location, dropdownlist):
        defaultValue = None
        shouldUpdate = True
        if location:
            for i in dropdownlist:
                if i.ValueCode not in location:
                    i.Allowed = False
                    i.IsSelected = False
                elif i.ValueCode in location:
                    if i.ValueCode == defaults[gesloc.SelectedValue.ValueCode]:
                        defaultValue = i
                    if i.IsSelected:
                        shouldUpdate = False
                    i.Allowed = True
        if shouldUpdate:
            defaultValue.IsSelected = True

    remove_deliverables = []
    gesloc = Product.Attr('C300_GES_Location')
    if gesloc.GetValue() != "None" and gesloc.GetValue() != "":
        custom_deliverables = Product.GetContainerByName('ESDC_Labor_Additional_Cust_Deliverables_con')
        for deliverable in custom_deliverables.Rows:
            deliverable_location = deliverable.GetColumnByName('GES Eng')
            dropdown_values = deliverable_location.ReferencingAttribute.Values
            disallow(specific_location[gesloc.SelectedValue.ValueCode], dropdown_values)
            deliverable.Calculate()
        custom_deliverables.Calculate()
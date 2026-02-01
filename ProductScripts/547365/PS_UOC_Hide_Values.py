tabs = [tab.Name for tab in Product.Tabs if tab.IsSelected]
if 'Labor Deliverables' in tabs and Product.Attr('isProductLoaded').GetValue() == 'True':
    Trace.Write('test')
    specific_location = {'GESChina': ['HPS_GES_P350B_CN','HPS_GES_P350F_CN'], 'GESIndia': ['HPS_GES_P350B_IN','HPS_GES_P350F_IN'], 'GESRomania':['HPS_GES_P350B_RO','HPS_GES_P350F_RO'], 'GESUzbekistan':['HPS_GES_P350B_UZ','HPS_GES_P350F_UZ'], 'GESEgypt': ['HPS_GES_P350B_EG','HPS_GES_P350F_EG']}
    def disallow(location, dropdownlist):
        if location:
            for i in dropdownlist:
                if i.ValueCode not in location:
                    i.Allowed = False
                elif i.ValueCode in location:
                    i.Allowed = True

    remove_deliverables = []
    gesloc = Product.GetContainerByName('CN900_Labor_Details').Rows[0].GetColumnByName('CN900_Ges_Location_Labour').Value
    if gesloc != "None" and gesloc != "":
        containers = ['CE CN900 Engineering Labor Container','CE CN900 Additional Custom Deliverables']
        for cont in containers:
            deliverables = Product.GetContainerByName(cont)
            for deliverable in deliverables.Rows:
                deliverable_location = deliverable.GetColumnByName('GES Eng')
                dropdown_values = deliverable_location.ReferencingAttribute.Values
                disallow(specific_location[gesloc], dropdown_values)
                deliverable.Calculate()
            deliverables.Calculate()
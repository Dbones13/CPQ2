if Product.Attr('isProductLoaded').GetValue() == 'True':
    specific_location = {'GES China':['HPS_GES_P350B_CN','HPS_GES_P350F_CN','HPS_GES_P335B_CN','HPS_GES_P335F_CN'],'GES India': ['HPS_GES_P350B_IN','HPS_GES_P350F_IN','HPS_GES_P335B_IN','HPS_GES_P335F_IN'], 'GES Romania':['HPS_GES_P350B_RO','HPS_GES_P350F_RO','HPS_GES_P335B_RO','HPS_GES_P335F_RO'],'GES Uzbekistan':['HPS_GES_P350B_UZ','HPS_GES_P350F_UZ','HPS_GES_P335B_UZ','HPS_GES_P335F_UZ'],'GES Egypt':['HPS_GES_P350B_EG','HPS_GES_P350F_EG','HPS_GES_P335B_EG','HPS_GES_P335F_EG']}

    def disallow(location, dropdownlist):
        if location:
            for i in dropdownlist:
                if i.ValueCode in location:
                    i.Allowed = True
                elif i.ValueCode not in location:
                    i.Allowed = False

    remove_deliverables = []
    gesloc = Product.Attr('MSE GES Location')
    if gesloc.GetValue() != "None" and gesloc.GetValue() != "":
        deliverables = Product.GetContainerByName('MSE_Engineering_Labor_Container')
        for row in deliverables.Rows:
            if row['Deliverable'] not in remove_deliverables:
                location = row.GetColumnByName('GES Eng')
                value_list = location.ReferencingAttribute.Values
                disallow(specific_location[gesloc.SelectedValue.ValueCode], value_list)
                row.Calculate()
        deliverables.Calculate()
        custom_deliverables = Product.GetContainerByName('MSE_Additional_Labor_Container')
        for deliverable in custom_deliverables.Rows:
            deliverable_location = deliverable.GetColumnByName('GES Eng')
            dropdown_values = deliverable_location.ReferencingAttribute.Values
            disallow(specific_location[gesloc.SelectedValue.ValueCode], dropdown_values)
            deliverable.Calculate()
        custom_deliverables.Calculate()
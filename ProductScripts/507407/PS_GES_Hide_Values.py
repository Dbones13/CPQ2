if Product.Attr('isProductLoaded').GetValue() == 'True':
    specific_location = {'GES_India': ['HPS_GES_P350B_IN','HPS_GES_P350F_IN','HPS_GES_P335B_IN','HPS_GES_P335F_IN'],'GES_Egypt':['HPS_GES_P350B_EG','HPS_GES_P350F_EG','HPS_GES_P335B_EG','HPS_GES_P335F_EG']}

    def disallow(location, dropdownlist):
        if location:
            for i in dropdownlist:
                if i.ValueCode in location:
                    i.Allowed = True
                elif i.ValueCode not in location:
                    i.Allowed = False

    remove_deliverables = []
    gesloc = Product.Attr('FGC_GES_Location')
    if gesloc.GetValue() != "None" and gesloc.GetValue() != "":
        deliverables = Product.GetContainerByName('FGC_Engineering_Labor_Container')
        for row in deliverables.Rows:
            if row['Deliverable'] not in remove_deliverables:
                location = row.GetColumnByName('GES Eng')
                value_list = location.ReferencingAttribute.Values
                disallow(specific_location[gesloc.SelectedValue.ValueCode], value_list)
                row.Calculate()
        deliverables.Calculate()
        custom_deliverables = Product.GetContainerByName('FGC_Additional_Labour_Container')
        for deliverable in custom_deliverables.Rows:
            deliverable_location = deliverable.GetColumnByName('GES Eng')
            dropdown_values = deliverable_location.ReferencingAttribute.Values
            disallow(specific_location[gesloc.SelectedValue.ValueCode], dropdown_values)
            deliverable.Calculate()
        custom_deliverables.Calculate()
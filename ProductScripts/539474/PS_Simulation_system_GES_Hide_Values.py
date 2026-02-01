Trace.Write('-------' + Product.Attr('isProductLoaded').GetValue())
if Product.Attr('isProductLoaded').GetValue() == 'True':
    Trace.Write('-------test')
    specific_location = {'GES China': ['HPS_GES_P350B_CN','HPS_GES_P350F_CN'], 'GES India': ['HPS_GES_P350B_IN','HPS_GES_P350F_IN'], 'GES Romania':['HPS_GES_P350B_RO','HPS_GES_P350F_RO'], 'GES Uzbekistan':['HPS_GES_P350B_UZ','HPS_GES_P350F_UZ'], 'GES Egypt':['HPS_GES_P350B_EG','HPS_GES_P350F_EG']}
    def disallow(location, dropdownlist):
        if location:
            Trace.Write('-------' + str(location))
            for i in dropdownlist:
                if i.ValueCode not in location:
                    i.Allowed = False
                elif i.ValueCode in location:
                    i.Allowed = True

    remove_deliverables = []
    gesloc = Product.Attr('C300_GES_Location')
    Trace.Write('-------' + gesloc.GetValue())
    if gesloc.GetValue() != "None" and gesloc.GetValue() != "":
        custom_deliverables = Product.GetContainerByName('Simulation_Labor_Additional_Cust_Deliverables_con')
        Trace.Write('-------' + str(custom_deliverables.Rows.Count))
        for deliverable in custom_deliverables.Rows:
            deliverable_location = deliverable.GetColumnByName('GES Eng')
            dropdown_values = deliverable_location.ReferencingAttribute.Values
            disallow(specific_location[gesloc.SelectedValue.ValueCode], dropdown_values)
            deliverable.Calculate()
        custom_deliverables.Calculate()
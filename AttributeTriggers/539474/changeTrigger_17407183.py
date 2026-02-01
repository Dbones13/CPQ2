"""gesloc = Product.Attr('C300_GES_Location')
if Product.Attr('isProductLoaded').GetValue() == 'True':
    Trace.Write('test')
    specific_location = {'GES China': ['HPS_GES_P350F_IN','HPS_GES_P350B_IN','HPS_GES_P350B_RO','HPS_GES_P350F_RO','HPS_GES_P350B_UZ','HPS_GES_P350F_UZ'], 'GES India': ['HPS_GES_P350B_CN','HPS_GES_P350F_CN','HPS_GES_P350B_RO','HPS_GES_P350F_RO','HPS_GES_P350B_UZ','HPS_GES_P350F_UZ'], 'GES Romania':['HPS_GES_P350B_CN','HPS_GES_P350F_CN','HPS_GES_P350F_IN','HPS_GES_P350B_IN','HPS_GES_P350B_UZ','HPS_GES_P350F_UZ'], 'GES Uzbekistan':['HPS_GES_P350B_CN','HPS_GES_P350F_CN','HPS_GES_P350F_IN','HPS_GES_P350B_IN','HPS_GES_P350B_RO','HPS_GES_P350F_RO']}
    def disallow(location, dropdownlist):
        if location:
            for i in dropdownlist:
                if i.ValueCode in location:
                    i.Allowed = False
                elif i.ValueCode not in location:
                    i.Allowed = True

    remove_deliverables = []
    if gesloc.GetValue() != "None" and gesloc.GetValue() != "":
        custom_deliverables = Product.GetContainerByName('Simulation_Labor_Additional_Cust_Deliverables_con')
        for deliverable in custom_deliverables.Rows:
            deliverable_location = deliverable.GetColumnByName('GES Eng')
            dropdown_values = deliverable_location.ReferencingAttribute.Values
            disallow(specific_location[gesloc.SelectedValue.ValueCode], dropdown_values)
            deliverable.Calculate()
        custom_deliverables.Calculate()"""
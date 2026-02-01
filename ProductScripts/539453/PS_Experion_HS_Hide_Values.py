if Product.Attr('isProductLoaded').GetValue() == 'True':
    specific_location = {'GES China': ['HPS_GES_P350B_IN', 'HPS_GES_P350F_IN', 'HPS_GES_P350B_RO', 'HPS_GES_P350F_RO', 'HPS_GES_P350B_UZ', 'HPS_GES_P350F_UZ'], 'GES India': ['HPS_GES_P350B_CN', 'HPS_GES_P350F_CN', 'HPS_GES_P350B_RO', 'HPS_GES_P350F_RO', 'HPS_GES_P350B_UZ', 'HPS_GES_P350F_UZ'],'GES Romania':['HPS_GES_P350B_CN', 'HPS_GES_P350F_CN', 'HPS_GES_P350B_IN', 'HPS_GES_P350F_IN', 'HPS_GES_P350B_UZ', 'HPS_GES_P350F_UZ'],'GES Uzbekistan':['HPS_GES_P350B_CN', 'HPS_GES_P350F_CN', 'HPS_GES_P350B_IN', 'HPS_GES_P350F_IN', 'HPS_GES_P350B_RO', 'HPS_GES_P350F_RO']}

    def disallow(location, dropdownlist):
        if location:
            for i in dropdownlist:
                if i.ValueCode in location:
                    i.Allowed = False
                elif i.ValueCode not in location:
                    i.Allowed = True

    remove_deliverables = ['Experion HS Engineering Plan', 'Experion HS Procure Materials & Services', 'Experion HS Customer Training', 'Experion HS Project Close Out Report']
    gesloc = Product.Attr("Experion_HS_Ges_Location_Labour").GetValue()
    if gesloc != "None" and gesloc != "":
        deliverables = Product.GetContainerByName('Experion HS Engineering Labor Container')
        for row in deliverables.Rows:
            if row['Deliverable'] not in remove_deliverables:
                location = row.GetColumnByName('GES Eng')
                value_list = location.ReferencingAttribute.Values
                disallow(specific_location[gesloc], value_list)
        deliverables.Calculate();
        custom_deliverables = Product.GetContainerByName('Experion HS Additional Custom Deliverables')
        for deliverable in custom_deliverables.Rows:
            deliverable_location = deliverable.GetColumnByName('GES Eng')
            dropdown_values = deliverable_location.ReferencingAttribute.Values
            disallow(specific_location[gesloc], dropdown_values)
        custom_deliverables.Calculate()
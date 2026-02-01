if Product.Attr('isProductLoaded').GetValue() == 'True':
    specific_location = {'GES China': ['HPS_GES_P350F_IN', 'HPS_GES_P350B_IN', 'HPS_GES_P350B_RO', 'HPS_GES_P350F_RO', 'HPS_GES_P350B_UZ', 'HPS_GES_P350F_UZ','HPS_GES_P350F_EG', 'HPS_GES_P350B_EG'], 'GES India': ['HPS_GES_P350B_CN', 'HPS_GES_P350F_CN', 'HPS_GES_P350B_RO', 'HPS_GES_P350F_RO', 'HPS_GES_P350B_UZ', 'HPS_GES_P350F_UZ','HPS_GES_P350F_EG', 'HPS_GES_P350B_EG'],'GES Romania':['HPS_GES_P350B_CN', 'HPS_GES_P350F_CN', 'HPS_GES_P350F_UZ', 'HPS_GES_P350B_UZ','HPS_GES_P350F_IN', 'HPS_GES_P350B_IN','HPS_GES_P350F_EG', 'HPS_GES_P350B_EG'],'GES Uzbekistan':['HPS_GES_P350B_CN', 'HPS_GES_P350F_CN', 'HPS_GES_P350B_RO', 'HPS_GES_P350F_RO','HPS_GES_P350F_IN', 'HPS_GES_P350B_IN','HPS_GES_P350F_EG', 'HPS_GES_P350B_EG'],'GES Egypt':['HPS_GES_P350B_CN', 'HPS_GES_P350F_CN', 'HPS_GES_P350B_RO', 'HPS_GES_P350F_RO','HPS_GES_P350F_IN', 'HPS_GES_P350B_IN','HPS_GES_P350F_UZ', 'HPS_GES_P350B_UZ']}

    def disallow(location, dropdownlist):
        if location:
            for i in dropdownlist:
                if i.ValueCode in location:
                    i.Allowed = False
                elif i.ValueCode not in location:
                    i.Allowed = True

    remove_deliverables = []
    gesloc = Product.Attr("Experion_HS_Ges_Location_Labour").GetValue()
    if gesloc != "None" and gesloc != "":
        deliverables = Product.GetContainerByName('System_Interface_Engineering_Labor_Container')
        for row in deliverables.Rows:
            if row['Deliverable'] not in remove_deliverables:
                location = row.GetColumnByName('GES Eng')
                value_list = location.ReferencingAttribute.Values
                disallow(specific_location[gesloc], value_list)
        deliverables.Calculate();
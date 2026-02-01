if Product.Attr('isProductLoaded').GetValue() == 'True':
    Trace.Write('test')
    specific_location = {'China': ['HPS_GES_P350B_CN','HPS_GES_P350F_CN'],'India': ['HPS_GES_P350F_IN','HPS_GES_P350B_IN'],'Romania':['HPS_GES_P350B_RO','HPS_GES_P350F_RO'],'Uzbekistan':['HPS_GES_P350B_UZ','HPS_GES_P350F_UZ'],'Egypt':['HPS_GES_P350B_EG','HPS_GES_P350F_EG']}
    def disallow(location, dropdownlist):
        if location:
            for i in dropdownlist:
                if i.ValueCode in location:
                    i.Allowed = True
                elif i.ValueCode not in location:
                    i.Allowed = False

    remove_deliverables = []
    att_loc = Product.Attr('MX_HC_GES_Location').SelectedValue
    if att_loc:
        gesloc = Product.Attr('MX_HC_GES_Location').SelectedValue.ValueCode
        if gesloc != "None" or gesloc != "":
            deliverables = Product.GetContainerByName('Experion_mx_Labor_Container')
            for row in deliverables.Rows:
                if row['Deliverable'] not in remove_deliverables:
                    location = row.GetColumnByName('GES Eng')
                    value_list = location.ReferencingAttribute.Values
                    disallow(specific_location[gesloc], value_list)
                    row.Calculate()
            deliverables.Calculate()
            custom_deliverables = Product.GetContainerByName('Experion_mx_labor_Additional_Cust_Deliverables_con')
            for deliverable in custom_deliverables.Rows:
                deliverable_location = deliverable.GetColumnByName('GES Eng')
                dropdown_values = deliverable_location.ReferencingAttribute.Values
                disallow(specific_location[gesloc], dropdown_values)
                deliverable.Calculate()
            custom_deliverables.Calculate()
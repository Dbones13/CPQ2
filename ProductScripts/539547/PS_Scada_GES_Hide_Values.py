if Product.Attr('isProductLoaded').GetValue() == 'True':
    Trace.Write('test')
    specific_location = {'GESChina': ['HPS_GES_P335B_CN','HPS_GES_P335F_CN','HPS_GES_P350B_CN','HPS_GES_P350F_CN'], 'GESIndia': ['HPS_GES_P335B_IN','HPS_GES_P335F_IN','HPS_GES_P350B_IN','HPS_GES_P350F_IN'], 'GESRomania':['HPS_GES_P335B_RO','HPS_GES_P335F_RO','HPS_GES_P350B_RO','HPS_GES_P350F_RO'], 'GESUzbekistan':['HPS_GES_P335B_UZ','HPS_GES_P335F_UZ','HPS_GES_P350B_UZ','HPS_GES_P350F_UZ'], 'GESEgypt':['HPS_GES_P350B_EG','HPS_GES_P350F_EG','HPS_GES_P335B_EG','HPS_GES_P335F_EG']}
    def disallow(location, dropdownlist):
        if location:
            for i in dropdownlist:
                if i.ValueCode in location:
                    i.Allowed = True
                elif i.ValueCode not in location:
                    i.Allowed = False

    remove_deliverables = []
    gesloc = Product.Attr('SCADA_Ges_Location_Labour').SelectedValue.ValueCode
    if gesloc != "None" and gesloc != "":
        deliverables = Product.GetContainerByName('SCADA_Engineering_Labor_Container')
        for row in deliverables.Rows:
            if row['Deliverable'] not in remove_deliverables:
                location = row.GetColumnByName('GES Eng')
                value_list = location.ReferencingAttribute.Values
                disallow(specific_location[gesloc], value_list)
                row.Calculate()
        deliverables.Calculate()
        custom_deliverables = Product.GetContainerByName('SCADA_Additional_Custom_Deliverables_Container')
        for deliverable in custom_deliverables.Rows:
            deliverable_location = deliverable.GetColumnByName('GES Eng')
            dropdown_values = deliverable_location.ReferencingAttribute.Values
            disallow(specific_location[gesloc], dropdown_values)
            deliverable.Calculate()
        custom_deliverables.Calculate()
        if Product.Attr('SCADA_GES_Location_Flag').GetValue() == '':
            ScriptExecutor.Execute('PS_SetDefaultGES')
            Product.Attr('SCADA_GES_Location_Flag').AssignValue('1')
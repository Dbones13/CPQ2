tabs = [tab.Name for tab in Product.Tabs if tab.IsSelected]
if 'Labor Deliverables' in tabs:
    '''specific_location = {'GESChina': ['HPS_GES_P350B_IN', 'HPS_GES_P350F_IN', 'HPS_GES_P350B_RO', 'HPS_GES_P350F_RO', 'HPS_GES_P350B_UZ', 'HPS_GES_P350F_UZ'], 'GESIndia': ['HPS_GES_P350B_CN', 'HPS_GES_P350F_CN', 'HPS_GES_P350B_RO', 'HPS_GES_P350F_RO', 'HPS_GES_P350B_UZ', 'HPS_GES_P350F_UZ'],'GESRomania':['HPS_GES_P350B_CN', 'HPS_GES_P350F_CN', 'HPS_GES_P350B_IN', 'HPS_GES_P350F_IN', 'HPS_GES_P350B_UZ', 'HPS_GES_P350F_UZ'],'GESUzbekistan':['HPS_GES_P350B_CN', 'HPS_GES_P350F_CN', 'HPS_GES_P350B_IN', 'HPS_GES_P350F_IN', 'HPS_GES_P350B_RO', 'HPS_GES_P350F_RO'],'GESEgypt':['HPS_GES_P350B_CN', 'HPS_GES_P350F_CN', 'HPS_GES_P350B_IN', 'HPS_GES_P350F_IN', 'HPS_GES_P350B_RO', 'HPS_GES_P350F_RO','HPS_GES_P350B_UZ', 'HPS_GES_P350F_UZ']}'''

    specific_location_PAS ={'GESChina': ['HPS_GES_P350B_CN','HPS_GES_P350F_CN'], 'GESIndia': ['HPS_GES_P350B_IN','HPS_GES_P350F_IN'],'GESRomania':['HPS_GES_P350B_RO','HPS_GES_P350F_RO'],'GESUzbekistan':['HPS_GES_P350B_UZ','HPS_GES_P350F_UZ'],'GESEgypt':['HPS_GES_P350B_EG','HPS_GES_P350F_EG']}

    specific_location_LSS ={'GESChina': ['HPS_GES_P350B_CN','HPS_GES_P350F_CN','SVC_GES_P350B_CN','SVC_GES_P350F_CN'], 'GESIndia': ['HPS_GES_P350B_IN','HPS_GES_P350F_IN','SVC_GES_P350B_IN','SVC_GES_P350F_IN'],'GESRomania':['HPS_GES_P350B_RO','HPS_GES_P350F_RO','SVC_GES_P350B_RO','SVC_GES_P350F_RO'],'GESUzbekistan':['HPS_GES_P350B_UZ','HPS_GES_P350F_UZ','SVC_GES_P350B_UZ','SVC_GES_P350F_UZ'],'GESEgypt':['HPS_GES_P350B_EG','HPS_GES_P350F_EG']}

    '''extra_ges_options = ['SVC_GES_P350F_UZ', 'SVC_GES_P350B_UZ', 'SVC_GES_P335F_UZ', 'SVC_GES_P335B_UZ', 'SVC_GES_P215F_UZ', 'SVC_GES_P215B_UZ',
                         'SVC_GES_P350F_RO', 'SVC_GES_P350B_RO', 'SVC_GES_P335F_RO', 'SVC_GES_P335B_RO', 'SVC_GES_P215F_RO', 'SVC_GES_P215B_RO',
                         'SVC_GES_P350F_CN', 'SVC_GES_P350B_CN', 'SVC_GES_P335F_CN', 'SVC_GES_P335B_CN', 'SVC_GES_P215F_CN', 'SVC_GES_P215B_CN',
                         'SVC_GES_P350F_IN', 'SVC_GES_P350B_IN', 'SVC_GES_P335F_IN', 'SVC_GES_P335B_IN', 'SVC_GES_P215F_IN', 'SVC_GES_P215B_IN']'''

    def disallow(location, dropdownlist, gesloc):
        loc_code = {'GESChina' : '_CN', 'GESIndia' : '_IN', 'GESRomania' : '_RO', 'GESUzbekistan' : '_UZ','GESEgypt':'_EG'}
        firstTrue = None
        shouldUpdate = True
        if location:
            for i in dropdownlist:
                if i.ValueCode in location: #or (str(i.ValueCode).endswith(loc_code[gesloc])): #or i.ValueCode in extra_ges_options:
                    if not firstTrue:
                        firstTrue = i
                    if i.IsSelected:
                        shouldUpdate = False
                    i.Allowed = True
                elif i.ValueCode not in location:
                    i.Allowed = False
        '''if shouldUpdate:
            firstTrue.IsSelected = True'''

    bookingLOB = Quote.GetCustomField("Booking LOB").Content
    remove_deliverables = ['UOC User Requirement Specification', 'UOC Engineering Plan', 'UOC Procure Materials & Services', 'UOC Customer Training', 'UOC Project Close Out Report']
    gesloc = Product.GetContainerByName('UOC_Labor_Details').Rows[0].GetColumnByName('UOC_Ges_Location_Labour')
    if gesloc.Value != "None" and gesloc.Value != "":
        deliverables = Product.GetContainerByName('CE UOC Engineering Labor Container')
        for row in deliverables.Rows:
            if row['Deliverable'] not in remove_deliverables:
                location = row.GetColumnByName('GES Eng')
                value_list = location.ReferencingAttribute.Values
                if bookingLOB == 'PAS':
                    disallow(specific_location_PAS[gesloc.Value], value_list, gesloc.Value)
                elif bookingLOB == 'LSS':
                    disallow(specific_location_LSS[gesloc.Value], value_list, gesloc.Value)
            else:
                row.GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue('None')
            row.ApplyProductChanges()
            row.Calculate()
        deliverables.Calculate();
        custom_deliverables = Product.GetContainerByName('CE UOC Additional Custom Deliverables')
        for deliverable in custom_deliverables.Rows:
            deliverable_location = deliverable.GetColumnByName('GES Eng')
            dropdown_values = deliverable_location.ReferencingAttribute.Values
            if bookingLOB == 'PAS':
                disallow(specific_location_PAS[gesloc.Value], dropdown_values, gesloc.Value)
            elif bookingLOB == 'LSS':
                disallow(specific_location_LSS[gesloc.Value], dropdown_values, gesloc.Value)
            deliverable.ApplyProductChanges()
            deliverable.Calculate()
        custom_deliverables.Calculate()

for attr in Product.Attributes:
    if attr.DisplayType=="Container" and attr.Name not in ('CE UOC Engineering Labor Container', 'CE UOC Additional Custom Deliverables'):
        cont=Product.GetContainerByName(attr.Name).Rows
        for row in cont:
            for column in row.Columns:
                if column.DisplayType=="DropDown" and not row[column.Name] and column.ReferencingAttribute:
                    for val in column.ReferencingAttribute.Values:
                        if val.Display != '- none -':
                            row.SetColumnValue(column.Name,val.Display)
                            break
            row.Calculate()
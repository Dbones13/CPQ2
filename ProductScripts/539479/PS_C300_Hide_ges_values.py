specific_location_PAS = {'GES China': ['HPS_GES_P350B_CN', 'HPS_GES_P350F_CN'], 'GES India':['HPS_GES_P350B_IN', 'HPS_GES_P350F_IN'], 'GES Romania':['HPS_GES_P350B_RO', 'HPS_GES_P350F_RO'],'GES Uzbekistan':['HPS_GES_P350B_UZ', 'HPS_GES_P350F_UZ'],'GES Egypt':['HPS_GES_P350B_EG','HPS_GES_P350F_EG']}

specific_location_LSS = {'GES China': ['HPS_GES_P350B_CN', 'HPS_GES_P350F_CN','SVC_GES_P350B_CN','SVC_GES_P350F_CN'], 'GES India':['HPS_GES_P350B_IN', 'HPS_GES_P350F_IN','SVC_GES_P350B_IN','SVC_GES_P350F_IN'], 'GES Romania':['HPS_GES_P350B_RO', 'HPS_GES_P350F_RO','SVC_GES_P350B_RO','SVC_GES_P350F_RO'],'GES Uzbekistan':['HPS_GES_P350B_UZ', 'HPS_GES_P350F_UZ','SVC_GES_P350B_UZ','SVC_GES_P350F_UZ'],'GES Egypt':['HPS_GES_P350B_EG','HPS_GES_P350F_EG']}

def disallow(location, dropdownlist):
    if location:
        for i in dropdownlist:
            if i.ValueCode in location:
                i.Allowed = True
            elif i.ValueCode not in location:
                i.Allowed = False

bookingLOB = Quote.GetCustomField("Booking LOB").Content
gesloc = Product.Attr('C300_GES_Location')
if gesloc.GetValue() != "None" and gesloc.GetValue() != "":
    containers = ['C300_Engineering_Labor_Container','C300_Additional_Custom_Deliverables_Container']
    for cont in containers:
        deliverables = Product.GetContainerByName(cont)
        for row in deliverables.Rows:
            location = row.GetColumnByName('GES Eng')
            value_list = location.ReferencingAttribute.Values
            if bookingLOB == 'PAS':
                disallow(specific_location_PAS[gesloc.GetValue()], value_list)
            elif bookingLOB == 'LSS':
                disallow(specific_location_LSS[gesloc.GetValue()], value_list)
            row.Calculate()
        deliverables.Calculate()
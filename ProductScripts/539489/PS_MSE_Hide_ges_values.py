specific_location = {'GES China': ['HPS_GES_P350B_CN', 'HPS_GES_P350F_CN','SVC_GES_P350B_CN','SVC_GES_P350F_CN'], 'GES India':['HPS_GES_P350B_IN', 'HPS_GES_P350F_IN','SVC_GES_P350B_IN','SVC_GES_P350F_IN'], 'GES Romania':['HPS_GES_P350B_RO', 'HPS_GES_P350F_RO','|SVC_GES_P350B_RO','SVC_GES_P350F_RO'],'GES Uzbekistan':['HPS_GES_P350B_UZ', 'HPS_GES_P350F_UZ','SVC_GES_P350B_UZ','SVC_GES_P350F_UZ'],'GES Egypt':['HPS_GES_P350B_EG','HPS_GES_P350F_EG','HPS_GES_P335B_EG','HPS_GES_P335F_EG']}

def disallow(location, dropdownlist):
    if location:
        for i in dropdownlist:
            if i.ValueCode in location:
                i.Allowed = True
            elif i.ValueCode not in location:
                i.Allowed = False

gesloc = Product.Attr('MSC GES Location')
if gesloc.GetValue() != "None" and gesloc.GetValue() != "":
    deliverables = Product.GetContainerByName('MSC_Engineering_Labor_Container')
    for row in deliverables.Rows:
        location = row.GetColumnByName('GES Eng')
        value_list = location.ReferencingAttribute.Values
        disallow(specific_location[gesloc.GetValue()], value_list)
    deliverables.Calculate()
    custom_deliverables = Product.GetContainerByName('MSC_Additional_Labour_Container')
    for deliverable in custom_deliverables.Rows:
        deliverable_location = deliverable.GetColumnByName('GES Eng')
        dropdown_values = deliverable_location.ReferencingAttribute.Values
        disallow(specific_location[gesloc.GetValue()], dropdown_values)
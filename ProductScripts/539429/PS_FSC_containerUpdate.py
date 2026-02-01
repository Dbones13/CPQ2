producthiddenContainer = Product.GetContainerByName('MSID_Product_Container_FSC_hidden')
newRowfsc = producthiddenContainer.AddNewRow('FSC_to_SM_Audit_cpq')
newRowfsc['Product Name'] = "FSC to SM Audit"
newRowfsc.ApplyProductChanges()

#Assigning the default values to the attributes
attrList = ['ATT_FSC_to_SM_On_Site_Eng_hours', 'ATT_FSC_to_SM_In_Office_Eng_hours']
for attrName in attrList:
    if Product.Attr(attrName).GetValue() == '':
        Product.Attr(attrName).AssignValue('0')
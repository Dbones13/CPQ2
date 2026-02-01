SC_cont = Product.GetContainerByName("Service Contract Modules")
FLAG = False
Product.Attr('SC_Product_Status').AssignValue('')
incompleteModule = []

def check_FLAG(flag):
    if flag:
        return 'Complete'
    else:
        return 'Incomplete'

if SC_cont.Rows.Count:
    for row in SC_cont.Rows:
        prod = row.Product.Name
        FLAG = row.Product.IsComplete
        if str(row['Module']) == str(prod):
            row['Product_Status'] = check_FLAG(FLAG)
        if row['Module'] == 'Generic Module':
            row['Product_Name'] = row.Product.Attr('SC_GN_AT_Product_Family').GetValue()
        else:
            row['Product_Name'] = row['Module']
        if not FLAG:
            incompleteModule.append(row['Product_Name'])
    if len(incompleteModule):
        incompleteMsg = "{} - {}".format("Please review the configuration of following Module(s)", ", ".join(incompleteModule))
        Product.Attr('SC_Product_Status').AssignValue(incompleteMsg)
#nilesh -pavan - added code 28082025
Product.Attr('SC_Modules_List').AssignValue(Product.ParseString("<*CTX( Container(Service Contract Modules).UniqueValues(Product_Name).Separator(',') )*>"))
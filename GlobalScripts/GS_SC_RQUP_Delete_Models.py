Model_scope_cont = Product.GetContainerByName("SC_Experion_Models_Scope")
Msid_cont = Product.GetContainerByName("SC_MSID_Container")
m = []
msid_list = []
for row in Model_scope_cont.Rows:
    if row.IsSelected:
        m.append(row.RowIndex)
        if row['MSIDs'] != '':
            msid_list.append(row['MSIDs'])
m.reverse()
for msid_row in Msid_cont.Rows:
    if msid_row['MSIDs'] in msid_list:
        msid_row.IsSelected = False
Msid_cont.Calculate()
for i in m:
    Model_scope_cont.DeleteRow(i)
Model_scope_cont.Calculate()
ScriptExecutor.Execute('PS_Model_Error_msg')
#Change product status as incomplete
Product.Attr('SC_Product_Status').AssignValue("0")
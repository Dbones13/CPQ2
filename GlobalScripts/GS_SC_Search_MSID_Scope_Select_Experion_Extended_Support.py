#to filter MSID from MSID container:
MSID_Cont = Product.GetContainerByName('SC_MSID_Container')
Hid_Cont = Product.GetContainerByName('SC_MSID_Container_Hidden')
SearchText = Product.Attr('SC_MSID_Search_Field_Scope_Select').GetValue().lower().strip()
MSID_Cont.Clear()
for row in Hid_Cont.Rows:
    if SearchText == "" or SearchText == None or SearchText in row['MSIDs'].lower():
        msid = MSID_Cont.AddNewRow()
        msid['MSIDS'] = row['MSIDs']
        msid['System Name'] = row['System Name']
        msid['System Number'] = row['System Number']
        msid['Site'] = row['Site']
        msid.IsSelected = row.IsSelected
MSID_Cont.Calculate()
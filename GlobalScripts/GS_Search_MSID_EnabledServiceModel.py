MSID_CONT = Product.GetContainerByName('SC_Select_MSID_Cont')
MSID_HID_CONT = Product.GetContainerByName('SC_Select_MSID_Cont_Hidden')
SearchText = Product.Attr('EnabledsearchBox').GetValue()
MSID_CONT.Rows.Clear()
if SearchText == "" or SearchText == None:
    for row in MSID_HID_CONT.Rows:
        i = MSID_CONT.AddNewRow(False)
        i['MSIDs'] = row['MSIDs']
        i['System Name'] = row['System Name']
        i['System Number'] = row['System Number']
        i['siteName'] = row['siteName']
        i.IsSelected = row.IsSelected
else:
    for row in MSID_HID_CONT.Rows:
        if SearchText.lower() in row['MSIDs'].lower():
            i = MSID_CONT.AddNewRow(False)
            i['MSIDs'] = row['MSIDs']
            i['System Name'] = row['System Name']
            i['System Number'] = row['System Number']
            i['siteName'] = row['siteName']
            i.IsSelected = row.IsSelected
MSID_CONT.Calculate()
MSID_HID_CONT.Calculate()
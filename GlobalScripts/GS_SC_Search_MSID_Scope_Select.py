#to filter MSID from MSID container:
MSID_Cont = Product.GetContainerByName('SC_Select_MSID_Cont')
Hid_Cont = Product.GetContainerByName('SC_Select_MSID_Cont_Hidden')
SearchText = Product.Attr('SC_MSID_Search_Field_Scope_Select').GetValue()
MSID_Cont.Clear()
if SearchText == "" or SearchText == None:
    for row in Hid_Cont.Rows:
        i = MSID_Cont.AddNewRow(False)
        i['MSIDS'] = row['MSIDs']
        i['System Name'] = row['System Name']
        i['System Number'] = row['System Number']
        i['siteName'] = row['siteName']
        i['SiteID'] = row['SiteID']
        i['HiddenRowIndex'] = str(row.RowIndex)
        i.IsSelected = row.IsSelected
else:
    for row in Hid_Cont.Rows:
        if SearchText.lower() in row['MSIDs'].lower():
            i = MSID_Cont.AddNewRow(False)
            i['MSIDS'] = row['MSIDs']
            i['System Name'] = row['System Name']
            i['System Number'] = row['System Number']
            i['siteName'] = row['siteName']
            i['SiteID'] = row['SiteID']
            i['HiddenRowIndex'] = str(row.RowIndex)
            i.IsSelected = row.IsSelected
#MSID_Cont.Calculate()
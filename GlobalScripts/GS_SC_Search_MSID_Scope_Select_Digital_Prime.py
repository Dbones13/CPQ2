#to filter MSID from MSID container:
def getInt(n):
    try:
        return int(n)
    except:
        return 0
MSID_Cont = Product.GetContainerByName('SC_MSID_Container')
Hid_Cont = Product.GetContainerByName('SC_MSID_Container_Hidden')
SearchText = Product.Attr('SC_MSID_Search_Field_Scope_Select').GetValue()
MSID_Cont.Clear()
if SearchText == "" or SearchText == None:
    for row in Hid_Cont.Rows:
        i = MSID_Cont.AddNewRow()
        i['MSIDS'] = row['MSIDs']
        i['System Name'] = row['System Name']
        i['System Number'] = row['System Number']
        i['Site'] = row['Site']
        i.IsSelected = row.IsSelected
else:
    for row in Hid_Cont.Rows:
        if SearchText.lower() in row['MSIDs'].lower():
            i = MSID_Cont.AddNewRow()
            i['MSIDS'] = row['MSIDs']
            i['System Name'] = row['System Name']
            i['System Number'] = row['System Number']
            i['Site'] = row['Site']
            i.IsSelected = row.IsSelected
#MSIDRows = MSID_Cont.Rows.Count
#Product.Attr('SC_Num_of_MSID').AssignValue(str(MSIDRows))
count = 0
for row in MSID_Cont.Rows:
    if row.IsSelected == True:
        count += 1
msidCount = Product.Attr('SC_Digital_Prime_MSID_Count').GetValue()
if getInt(msidCount) != count:
    Product.Attr('SC_Digital_Prime_MSID_Count').AssignValue(str(count))
    Product.Attr('SC_Num_of_MSID').AssignValue(str(count))
MSID_Cont.Calculate()
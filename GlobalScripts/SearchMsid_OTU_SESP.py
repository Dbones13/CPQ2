MSID_CONT = Product.GetContainerByName('MSIDS_V1_OTU_SESP')
MSID_HID_CONT = Product.GetContainerByName('SC_Select_MSID_Cont_Hidden')
MSID_Models_cont = Product.GetContainerByName('SC_Models_Scope')
SearchText = Product.Attr('SearchBoxMsid_OTU_SESP').GetValue()
MSID_CONT.Rows.Clear()
if SearchText == "" or SearchText == None:
    for row in MSID_HID_CONT.Rows:
        i = MSID_CONT.AddNewRow()
        i.Product.Attr('MSIDS_OTU_SESP').AssignValue(mrow['MSIDs'])
        i['MSIDS_OTU_SESP'] = row['MSIDs']
        #i.Product.Attr('SystemNameChild_OTU_SESP').AssignValue(row['System Name'])
        #i['SystemNumber_OTU_SESP'] = row['System Number']
        #i['siteName'] = row['siteName']
        #i.IsSelected = row.IsSelected
    else :
        MSID_CONT.Calculate()
    for mrow in MSID_Models_cont.Rows:
		i = MSID_CONT.AddNewRow()
		i.Product.Attr('MSIDS_OTU_SESP').AssignValue(mrow['MSIDs'])
		i['MSIDS_OTU_SESP'] = mrow['MSIDs']
		#i.Product.Attr('SystemNameChild_OTU_SESP').AssignValue(mrow['System_Name'])
		#i['SystemNumber_OTU_SESP'] = mrow['System_Number']
    else : 
        MSID_CONT.Calculate()
else:
    models_msids = [row['MSIDs'] for row in MSID_Models_cont.Rows if SearchText.lower() in row['MSIDs'].lower()]
    for row in MSID_HID_CONT.Rows:
        if SearchText.lower() in row['MSIDs'].lower():
            i = MSID_CONT.AddNewRow()
            i.Product.Attr('MSIDS_OTU_SESP').AssignValue(mrow['MSIDs'])
            i['MSIDS_OTU_SESP'] = row['MSIDs']
            #i.Product.Attr('SystemNameChild_OTU_SESP').AssignValue(row['System Name'])
            #i['SystemNumber_OTU_SESP'] = row['System Number']
            #i['siteName'] = row['siteName']
            #i.IsSelected = row.IsSelected
    else :
        MSID_CONT.Calculate()
    for mrow in MSID_Models_cont.Rows:
        if SearchText.lower() in mrow['MSIDs'].lower() :
            i = MSID_CONT.AddNewRow()
            i.Product.Attr('MSIDS_OTU_SESP').AssignValue(mrow['MSIDs'])
            i['MSIDS_OTU_SESP'] = mrow['MSIDs']
            #i.Product.Attr('SystemNameChild_OTU_SESP').AssignValue(mrow['System_Name'])
            #i['SystemNumber_OTU_SESP'] = mrow['System_Number']
    else :
        MSID_CONT.Calculate()
#MSID_CONT.Calculate()
MSID_HID_CONT.Calculate()
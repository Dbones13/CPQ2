if Product.Attr('SC_Product_Type').GetValue() == "New":
    Msid_cont = Product.GetContainerByName("SC_MSID_Container")
    Model_cont = Product.GetContainerByName("SC_Experion_Models_Scope")
    # Constants
    DESC = 'Experion Extended Support - RQUP only'
    QTY = '1'
    msids_list = []
    if Model_cont.Rows.Count > 0:
        for row in Model_cont.Rows:
            if row["MSIDs"] not in ['',None]:
                msids_list.append(row["MSIDs"])

    for msid_row in Msid_cont.Rows:
        if msid_row.IsSelected:
            if len(msids_list) and msid_row["MSIDs"] in msids_list:
                continue
            else:
                msid_val = msid_row["MSIDs"]
                rowModel = Model_cont.AddNewRow(False)
                Trace.Write("New Row added:--- ")
                rowModel['MSIDs'] = msid_val
                rowModel['Description'] = DESC
                rowModel['Quantity'] = QTY
        else:
            delete_msids = []
            for model in Model_cont.Rows:
                if model['MSIDs'] == msid_row['MSIDs']:
                    msid_index = model.RowIndex
                    delete_msids.append(msid_index)
                    #Model_cont.DeleteRow(msid_index)
                    #Trace.Write("Row Delete :--- ")
            delete_msids.reverse()
            for remove_msid in delete_msids:
                Model_cont.DeleteRow(remove_msid)
                Model_cont.Calculate()
                #Trace.Write("Row Delete :--- "+str(remove_msid))
elif Product.Attr('SC_Product_Type').GetValue() == "Renewal":
    Msid_cont = Product.GetContainerByName("SC_MSID_Container")
    Model_cont = Product.GetContainerByName("SC_Experion_Models_Scope")
    # Constants
    DESC = 'Experion Extended Support - RQUP only'
    QTY = '1'
    msids_list = []
    if Model_cont.Rows.Count > 0:
        for row in Model_cont.Rows:
            if row["MSIDs"] not in ['',None]:
                msids_list.append(row["MSIDs"])

    for msid_row in Msid_cont.Rows:
        if msid_row.IsSelected:
            if len(msids_list) and msid_row["MSIDs"] in msids_list:
                continue
            else:
                msid_val = msid_row["MSIDs"]
                rowModel = Model_cont.AddNewRow(False)
                Trace.Write("New Row added:--- ")
                rowModel['MSIDs'] = msid_val
                rowModel['Description'] = DESC
                rowModel['Renewal_Quantity'] = QTY
                rowModel['PY_Quantity'] = '0'
                rowModel['PY_ListPrice'] = '0'
                rowModel['PY_CostPrice'] = '0'
                rowModel['HW_ListPrice'] = '0'
                rowModel['Cost_Price'] = '0'
                rowModel['SR_Price'] = '0'
                rowModel['SA_Price'] = '0'
                rowModel['Comment'] = 'No Scope Change'
        else:
            delete_msids = []
            for model in Model_cont.Rows:
                if model['MSIDs'] == msid_row['MSIDs']:
                    msid_index = model.RowIndex
                    delete_msids.append(msid_index)
                    #Model_cont.DeleteRow(msid_index)
                    #Trace.Write("Row Delete :--- ")
            delete_msids.reverse()
            for remove_msid in delete_msids:
                Model_cont.DeleteRow(remove_msid)
                Model_cont.Calculate()
                #Trace.Write("Row Delete :--- "+str(remove_msid))
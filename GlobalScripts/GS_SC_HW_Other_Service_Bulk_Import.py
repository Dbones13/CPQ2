#GS_SC_HW_Other_Service_Bulk_Import
def insertValidHRHWModels(Valid_Model_Cont, Asset, Model, Description, Quantity, Renewal_Quantity, Previous_Year_Unit_Price, Honeywell_List_Price, Cost_Price, Select,pre_qnt,PreviousYearListPrice,PreviousYearCostPrice,HoneywellListPrice,CurrentYearCostPrice,reference_number,Product_Type):
    #reference_number=reference_number(Quote)
    newModelRow = Valid_Model_Cont.AddNewRow(False)
    newModelRow["SC_Asset_HR_RWL"] = Asset
    newModelRow["SC_Model_HR_RWL"] = Model
    newModelRow["SC_Description_HR_RWL"] = Description
    newModelRow["SC_RenewalQuantity_HR_RWL"] = Renewal_Quantity
    newModelRow["BackupRenewalQuantity"] = Renewal_Quantity
    if Product_Type =="New":
        newModelRow['Sc_CurrentYearListPrice_HR_RWL'] = str(float(Honeywell_List_Price) * float(Renewal_Quantity))
        newModelRow["SC_HoneywellListPrice_HR_RWL"] = Honeywell_List_Price
        newModelRow["SC_CurrentYearUnitCostPrice_HR_RWL"] = Cost_Price
        newModelRow["SC_CurrentYearCostPrice_HR_RWL"] = str(float(Cost_Price) * float(Renewal_Quantity))
    elif Product_Type =="Renewal":
        newModelRow['SC_Quantity_HR_RWL'] = pre_qnt
        newModelRow["SC_PreviousYearListPrice_HR_RWL"] = PreviousYearListPrice
        newModelRow["SC_PreviousYearCostPrice_HR_RWL"] = PreviousYearCostPrice
        newModelRow["Sc_CurrentYearListPrice_HR_RWL"] = HoneywellListPrice
        newModelRow["SC_CurrentYearCostPrice_HR_RWL"] = CurrentYearCostPrice
        newModelRow["Backup_SC_HoneywellListPrice_HR_RWL"] = HoneywellListPrice
        newModelRow["Backup_SC_CurrentYearCostPrice_HR_RWL"] = CurrentYearCostPrice
        if pre_qnt >0:
            newModelRow['SC_PreviousYearUnitPrice_HR_RWL'] = str(float(PreviousYearListPrice) / float(pre_qnt))
            newModelRow["SC_PreviousYearUnitCostPrice_HR_RWL"] = str(float(PreviousYearCostPrice)/ float(pre_qnt))
        if Renewal_Quantity >0:
            newModelRow["SC_HoneywellListPrice_HR_RWL"] = str(float(HoneywellListPrice)/ float(Renewal_Quantity))
            newModelRow["SC_CurrentYearUnitCostPrice_HR_RWL"] = str(float(CurrentYearCostPrice)/ float(Renewal_Quantity))
    if float(Renewal_Quantity) > float(pre_qnt):
        newModelRow["SC_Comment_HR_RWL"] = 'Scope Addition'
    elif float(Renewal_Quantity) < float(pre_qnt):
        newModelRow["SC_Comment_HR_RWL"] = 'Scope Reduction'
    else:
        newModelRow["SC_Comment_HR_RWL"] = 'No Scope Change'
    newModelRow["Backup_SC_Comment_HR_RWL"] = newModelRow["SC_Comment_HR_RWL"]
    selectFlag = True if Select.upper() == "TRUE" else False
    newModelRow.IsSelected = selectFlag

def insertInvalidHRHWModels(InValid_Model_Cont, Asset, Model, Description, Quantity, Renewal_Quantity, Previous_Year_Unit_Price, Honeywell_List_Price, Select, Reason,pre_qnt,PreviousYearListPrice,PreviousYearCostPrice,HoneywellListPrice,CurrentYearCostPrice):
    newModelRow  = InValid_Model_Cont.AddNewRow(False)
    newModelRow["SC_Asset_HR_RWL"] = Asset
    newModelRow["SC_Model_HR_RWL"] = Model
    newModelRow["SC_Description_HR_RWL"] = Description
    newModelRow["SC_Quantity_HR_RWL"] = Renewal_Quantity
    newModelRow["SC_Reason_HR_RWL"] = Reason

def uploadHRHWModels(Product, Workbook, SFDC_Response):
    reference_number=Product.Attr('SC_Previouse_Quote_Number').GetValue()
    Product_Type=Product.Attr('SC_Product_Type').GetValue()
    HRRSheet = Workbook.GetSheet("Data").Cells
    LastCellPosition = HRRSheet.GetLastColumnPosition + str(HRRSheet.GetRowCount)
    ColumnCount = HRRSheet.GetColumnCount
    HRRModels = HRRSheet.GetRange("A1",LastCellPosition)
    HRRModelsCount = HRRSheet.GetRowCount
    Valid_Model_Cont = Product.GetContainerByName('SC_ValidModels_HR_RWL')
    Ex_Cont_Assets = [[validRow["SC_Asset_HR_RWL"],validRow['SC_Model_HR_RWL']] for validRow in Valid_Model_Cont.Rows]
    InValid_Model_Cont = Product.GetContainerByName('SC_InvalidModels_HR_RWL')
    for i in range(1,HRRModelsCount):
        #added for OPB data >>> Start--- Lahu
        pre_qnt=HRRModels[i,3]
        PreviousYearListPrice=HRRModels[i,5] if HRRModels[i,5] else '0'
        PreviousYearCostPrice=HRRModels[i,6] if HRRModels[i,6] else '0'
        HoneywellListPrice=HRRModels[i,7] if HRRModels[i,7] else '0'
        CurrentYearCostPrice=HRRModels[i,8] if HRRModels[i,8] else '0'
        #added for OPB data >>> end--- Lahu
        Asset = HRRModels[i,0]
        Model = HRRModels[i,1]
        Description = HRRModels[i,2]
        Quantity = '0'
        Renewal_Quantity = '0'
        flag=False
        if str(HRRModels[i,4]).strip() != '':
            Renewal_Quantity = str(HRRModels[i,4]).strip()
        else:
            Renewal_Quantity = HRRModels[i,4]
        try:
            if int(Renewal_Quantity):
                flag=True
                if int(Renewal_Quantity) <0:
                    flag=False
        except:
            flag=False
        Previous_Year_Unit_Price = 1
        Honeywell_List_Price =1 #HRRModels[i,4]
        Cost_Price =1 #HRRModels[i,5] if ColumnCount == 6 else '0'
        Select = 'False'
        isAssetModelAlreadyExists = False
        Ex_Cont_Assets = [[validRow["SC_Asset_HR_RWL"],validRow['SC_Model_HR_RWL']] for validRow in Valid_Model_Cont.Rows]
        for a in Ex_Cont_Assets:
            if a[0] == Asset: #and a[1] == Model:
                isAssetModelAlreadyExists = True
                break
        if Product_Type =="New":
            if  isAssetModelAlreadyExists == False and Asset != '' and Model != ''  and Description != '' and Previous_Year_Unit_Price != '' and float(Previous_Year_Unit_Price) > 0 and PreviousYearListPrice != '' and (float(PreviousYearListPrice) > 0 ) and Cost_Price != '' and float(Cost_Price) > 0:
                if SFDC_Response is not None:
                    count = 0
                    for asse in SFDC_Response.records:
                        if asse['Name'] == Asset:
                            insertValidHRHWModels(Valid_Model_Cont,Asset,Model,Description,Quantity,Renewal_Quantity,Previous_Year_Unit_Price,Honeywell_List_Price,Cost_Price,Select,pre_qnt,PreviousYearListPrice,PreviousYearCostPrice,HoneywellListPrice,CurrentYearCostPrice,reference_number,Product_Type)
                            break
                        else:
                            count += 1
                    if count == len(SFDC_Response.records):
                        Reason = 'Invalid Asset'
                        insertInvalidHRHWModels(InValid_Model_Cont,Asset,Model,Description,Quantity,Renewal_Quantity,Previous_Year_Unit_Price,Honeywell_List_Price,Select,Reason,pre_qnt,PreviousYearListPrice,PreviousYearCostPrice,HoneywellListPrice,CurrentYearCostPrice)
                else:
                    Reason = 'Invalid Asset'
                    insertInvalidHRHWModels(InValid_Model_Cont,Asset,Model,Description,Quantity,Renewal_Quantity,Previous_Year_Unit_Price,Honeywell_List_Price,Select,Reason,pre_qnt,PreviousYearListPrice,PreviousYearCostPrice,HoneywellListPrice,CurrentYearCostPrice)
            else:
                Reason = ""
                if isAssetModelAlreadyExists:
                    Reason += "Duplicate entry"+ "<br>"
                if Asset == '':
                    Reason += 'Blank Asset'+ "<br>"
                if Model == '':
                    Reason += 'Blank Models'+ "<br>"
                if Description == '':
                    Reason += 'Model Description is blank'+ "<br>"
                if ((Honeywell_List_Price == '' or float(Honeywell_List_Price) <= 0) or (Cost_Price == '' or float(Cost_Price) <= 0)):
                    Reason += 'Zero Unit Price'+ "<br>"
                insertInvalidHRHWModels(InValid_Model_Cont,Asset,Model,Description,Quantity,Renewal_Quantity,Previous_Year_Unit_Price,Honeywell_List_Price,Select,Reason,pre_qnt,PreviousYearListPrice,PreviousYearCostPrice,HoneywellListPrice,CurrentYearCostPrice)
        elif Product_Type =="Renewal":
            if  isAssetModelAlreadyExists == False and Asset != '' and Model != ''  and Description != '' and Previous_Year_Unit_Price != '' and Honeywell_List_Price != '' and pre_qnt != '' and CurrentYearCostPrice != '' and float(CurrentYearCostPrice) > 0 and HoneywellListPrice != '' and float(HoneywellListPrice) > 0 and flag==True:
                if SFDC_Response is not None:
                    count = 0
                    for asse in SFDC_Response.records:
                        if asse['Name'] == Asset:
                            insertValidHRHWModels(Valid_Model_Cont,Asset,Model,Description,Quantity,Renewal_Quantity,Previous_Year_Unit_Price,Honeywell_List_Price,Cost_Price,Select,pre_qnt,PreviousYearListPrice,PreviousYearCostPrice,HoneywellListPrice,CurrentYearCostPrice,reference_number,Product_Type)
                            break
                        else:
                            count += 1
                    if count == len(SFDC_Response.records):
                        Reason = 'Invalid Asset'
                        insertInvalidHRHWModels(InValid_Model_Cont,Asset,Model,Description,Quantity,Renewal_Quantity,Previous_Year_Unit_Price,Honeywell_List_Price,Select,Reason,pre_qnt,PreviousYearListPrice,PreviousYearCostPrice,HoneywellListPrice,CurrentYearCostPrice)
                else:
                    Reason = 'Invalid Asset'
                    insertInvalidHRHWModels(InValid_Model_Cont,Asset,Model,Description,Quantity,Renewal_Quantity,Previous_Year_Unit_Price,Honeywell_List_Price,Select,Reason,pre_qnt,PreviousYearListPrice,PreviousYearCostPrice,HoneywellListPrice,CurrentYearCostPrice)
            else:
                Reason = ""
                if isAssetModelAlreadyExists == True:
                    Reason += "Duplicate entry" + "<br>"
                if Asset == '':
                    Reason = 'Blank Asset'+ "<br>"
                if Model == '':
                    Reason += 'Blank Models'+ "<br>"
                if Description == '':
                    Reason += 'Model Description is blank'+ "<br>"
                if (pre_qnt) == '':
                    Reason += 'Previous Year Quantity is blank'+ "<br>"
                if (PreviousYearListPrice) == '':
                    Reason += 'Previous Year List Price is blank'+ "<br>"
                if flag==False:
                    Reason += 'Invalid Quantity'+ "<br>"
                if ((HoneywellListPrice == '' or float(HoneywellListPrice) <= 0) or (CurrentYearCostPrice == '' or float(CurrentYearCostPrice) <= 0)):
                    Reason += 'Zero Unit Price'+ "<br>"
                insertInvalidHRHWModels(InValid_Model_Cont,Asset,Model,Description,Quantity,Renewal_Quantity,Previous_Year_Unit_Price,Honeywell_List_Price,Select,Reason,pre_qnt,PreviousYearListPrice,PreviousYearCostPrice,HoneywellListPrice,CurrentYearCostPrice)
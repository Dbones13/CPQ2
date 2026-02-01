if Quote.GetCustomField('Booking LOB').Content == "PMC":
    def populateQuoteTableRow(table , dataDict , row = None):
        if not row:
            row = table.AddNewRow()
        for key , value in dataDict.items():
            row[key] = value


    vcmodelcf_table = Quote.QuoteTables["VCModelConfiguration"]
    modelDecode_table = Quote.QuoteTables["PMC_FP_ModelDecode"]
    modeldec_row={"ItemNumber_MD":"","Extended_Description_code":"","AttributeName_MD":"","AttributeDescription_MD":"","AttributeCode_System_Id":"", "Full_Model_Code":"", "CartItemGUID":""}

    modelDecode_table.Rows.Clear()
    modelDecode_table.Save()


    #read quote items when item is added to quote and check if item is present in quote table PMC_FP_Products
    for qitem in Quote.Items:
        fpquery = SqlHelper.GetFirst("SELECT 1 as flag FROM PMC_FP_Products WHERE PARTNUMBER = '{}'".format(qitem.PartNumber))
        #Trace.Write("fpquery: "+str(fpquery))
        #if quote item is a FP product then populate quote table - ModelDecode table from VCModelConfig table
        if fpquery is not None:
            #Trace.Write("fpexist: "+str(fpquery))
            vcrow_index = 1
            for vrow in vcmodelcf_table.Rows:
                if vrow["PartNumber"] == qitem.PartNumber and vcrow_index==1 and vrow["CartItemGUID"] == qitem.QuoteItemGuid:
                    modeldec_row["ItemNumber_MD"] = str(vrow["ItemNumber"])
                    modeldec_row["Extended_Description_code"] = qitem["QI_ExtendedDescription"].Value
                    modeldec_row["AttributeName_MD"] = ""
                    modeldec_row["AttributeDescription_MD"] = vrow["ProductDescription"]
                    modeldec_row["AttributeCode_System_Id"] = vrow["AttributeValueSystemId"]
                    modeldec_row["Full_Model_Code"] = qitem["QI_FME"].Value
                    #modeldec_row["FP_Worksheet_Col_Name"] = ''
                    modeldec_row["CartItemGUID"] = qitem.QuoteItemGuid
                    #CXCPQ-46820: Added ItemType field:08/17/2023
                    if qitem.ItemType == 0:
                        modeldec_row["ItemType"]="Base"
                    else:
                        modeldec_row["ItemType"]="Optional"
                    
                    #CXCPQ-46820: commented below logic as FP worksheet Tag upload is taken out from the requirements
                    ''''HW_Desc = SqlHelper.GetFirst("SELECT HW_Description FROM PMC_FP_HW_DESC WHERE Codes_Description = '{}'".format(qitem.QI_ExtendedDescription.Value))
                    if HW_Desc is not None and str(vrow["AttributeValueSystemId"])!='':
                        lv_attr_list = SqlHelper.GetList("SELECT FPColName,AttributeName FROM PMC_FP_COL_ATTR_MAPPING WHERE Partnumber = '{}' and ProductTypeCode='{}'".format(qitem.PartNumber,HW_Desc.HW_Description))
                        for i in lv_attr_list:
                            if i.AttributeName==vrow["AttributeValueSystemId"][0:len(i.AttributeName)]:
                                modeldec_row["FP_Worksheet_Col_Name"] = i.FPColName'''
                    populateQuoteTableRow(modelDecode_table,modeldec_row)
                    vcrow_index +=1
                elif vrow["PartNumber"] == qitem.PartNumber and vcrow_index > 1 and vrow["CartItemGUID"] == qitem.QuoteItemGuid:
                    modeldec_row["ItemNumber_MD"] = ""
                    modeldec_row["Extended_Description_code"] = ""
                    modeldec_row["AttributeName_MD"] = vrow["AttributeName"]
                    modeldec_row["AttributeDescription_MD"] = vrow["AttributeDescription"]
                    modeldec_row["AttributeCode_System_Id"] = vrow["AttributeValueSystemId"]
                    modeldec_row["Full_Model_Code"] = qitem["QI_FME"].Value
                    #modeldec_row["FP_Worksheet_Col_Name"] = ''
                    modeldec_row["CartItemGUID"] = qitem.QuoteItemGuid
                    #CXCPQ-46820: Added ItemType field:08/17/2023
                    modeldec_row["ItemType"]=""
                    #CXCPQ-46820: commented below logic as FP worksheet Tag upload is taken out from the requirements
                    ''''HW_Desc = SqlHelper.GetFirst("SELECT HW_Description FROM PMC_FP_HW_DESC WHERE Codes_Description = '{}'".format(qitem.QI_ExtendedDescription.Value))
                    if HW_Desc is not None and str(vrow["AttributeValueSystemId"])!='':
                        lv_attr_list = SqlHelper.GetList("SELECT FPColName,AttributeName FROM PMC_FP_COL_ATTR_MAPPING WHERE Partnumber = '{}' and ProductTypeCode='{}'".format(qitem.PartNumber,HW_Desc.HW_Description))
                        for i in lv_attr_list:
                            if i.AttributeName==vrow["AttributeValueSystemId"][0:len(i.AttributeName)]:
                                modeldec_row["FP_Worksheet_Col_Name"] = i.FPColName'''
                    populateQuoteTableRow(modelDecode_table,modeldec_row)
                    vcrow_index +=1
                #Trace.Write("VC_INFO: "+str(vrow["PartNumber"]))
                #modeldec_row={"ItemNumber_MD":"","AttributeName_MD":"","AttributeDescription_MD":""}
    modelDecode_table.Save()
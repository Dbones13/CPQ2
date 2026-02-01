a=Product.Attr('SC_Product_Type').GetValue()
if a=="Renewal":
    err_msg_1 = ""
    err_msg_2 = ""
    err_msg_3 = ""
    err_msg_4 = ""
    err_msg_5 = ""
    ErrorMsg=""
    validModelCont1 = Product.GetContainerByName("SC_Models_Scope_Renewal")
    Product.Attr("Error_Message").AssignValue('')
    Total_Quantity = 0
    if validModelCont1.Rows.Count > 0:
        for row in validModelCont1.Rows:
            if row['SESP_Models'] == str(''):
                err_msg_1+= "Service product with Blank Model Number: " + str(row.RowIndex+1) + "<br>"
            '''
            As per discussion with Rajesh on 28/08/2024 we don't need validation on system name and Description. Hence commneting the below lines
            if row['System_Name'] == str(''):
                err_msg_2+= "Service product with Blank SystemName: " + str(row.RowIndex+1) + "<br>"
            if row['Description'] == str(''):
                err_msg_3 += "Service product with Blank Description" + str(row.RowIndex+1) + "<br>"
            '''
            #Added this code for quantity validation as per discussion with Rajesh
            Total_Quantity = row['Quantity'] + row['Renewal Quantity']
            if Total_Quantity in ["","0","00"]:
                err_msg_2+= "Service product with Incorrect Quantity: " + str(row.RowIndex+1) + "<br>"
            if row['Platform']  == str(''):
                err_msg_4 += "Service product with Blank Platform:" + str(row.RowIndex+1) + "<br>"
            if err_msg_1!='' or err_msg_2!='' or err_msg_4!='':
                break
        ErrorMsg = err_msg_1 + err_msg_2 + err_msg_4
        Product.Attr("Error_Message").AssignValue(ErrorMsg)
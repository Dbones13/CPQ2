a=Product.Attr('SC_Product_Type').GetValue()
Trace.Write(a)
if a=="Renewal":
	err_msg_1 = ""
	err_msg_2 = ""
	err_msg_3 = ""
	err_msg_4 = ""
	err_msg_5 = ""
	ErrorMsg=""

	validModelCont1 = Product.GetContainerByName("SC_Models_Scope_Renewal")
	if validModelCont1.Rows.Count > 0:
		for row in validModelCont1.Rows:
			if row['SESP_Models'] == str(''):
				err_msg_1+= "Service product with Blank Model Number: " + str(row.RowIndex+1) + "<br>"
				
			if row['System_Name'] == str(''):
				err_msg_2+= "Service product with Blank SystemName: " + str(row.RowIndex+1) + "<br>"
			if row['Description'] == str(''):
				err_msg_3 += "Service product with Blank Description" + str(row.RowIndex+1) + "<br>"
			 
			if row['Platform']  == str(''):
				err_msg_4 += "Service product with Blank Platform:" + str(row.RowIndex+1) + "<br>"
			if err_msg_1!='' or err_msg_2!='' or err_msg_3!='' or err_msg_4!='':
				break
		ErrorMsg = err_msg_1 + err_msg_2 + err_msg_3 + err_msg_4 
		
		


		

	Trace.Write("ErrorMsg"+str(ErrorMsg))
	Product.Attr("SC_SESP_Error_Message").AssignValue(ErrorMsg)
	#Product.Attr("SC_Renewal_check").AssignValue("1")
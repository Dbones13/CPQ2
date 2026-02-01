if sender.PartNumber=="Trace Software":
	from GS_CommonConfig import CL_CommonSettings as CS
	from GS_Display_Warning_Message import Laborwarningmessage
	Labor_Execution_Year_List=''
	quoteTotalTable = Quote.QuoteTables["Quote_Details"]
	if quoteTotalTable.Rows.Count > 0:
		row = quoteTotalTable.Rows[0]
		Labor_Execution_Year_List=row['Labor_Execution_Year']
	productName=Product.PartNumber
	Guid=TagParserQuote.ParseString('<*CTX( Quote.CurrentItem.CartItemGuid )*>')
	Execution_Year_list=[]
	Quote_Guid=dict()
	if Labor_Execution_Year_List!='':
		Quote_Guid=eval(Labor_Execution_Year_List)

	if productName in CS.conNames:
		for conName in CS.conNames.get(productName):
			con=Product.GetContainerByName(conName)
			if con is None:
				Trace.Write("con"+str(conName))
				continue
			else:
				for row in con.Rows:
					if row["Execution_year"]!='' and row["Final_Hrs"]!='' and float(row["Final_Hrs"])>0:
						Execution_Year_list.append(row["Execution_year"])

	if quoteTotalTable.Rows.Count > 0 and len(Execution_Year_list)>0:
		row = quoteTotalTable.Rows[0]
		Quote_Guid[Guid]=(',').join(set(Execution_Year_list))
		row['Labor_Execution_Year']=str(Quote_Guid)
	elif quoteTotalTable.Rows.Count > 0:
		if Guid in Quote_Guid:
			Quote_Guid.pop(Guid)
		row = quoteTotalTable.Rows[0]
		row['Labor_Execution_Year']=str(Quote_Guid)
	quoteTotalTable.Save()

Laborwarningmessage(Quote)
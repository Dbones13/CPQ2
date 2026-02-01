if sender.PartNumber=="Migration":
	Trace.Write("Migration exe")
	from GS_CommonConfig import CL_CommonSettings as CS
	from GS_Display_Warning_Message import Laborwarningmessage
	Labor_Execution_Year_List=''
	quoteTotalTable = Quote.QuoteTables["Quote_Details"]
	if quoteTotalTable.Rows.Count > 0:
		row = quoteTotalTable.Rows[0]
		Labor_Execution_Year_List=row['Labor_Execution_Year']
	
	Execution_Year_list=[]
	MSID_PRODUCTS_CONT=Product.GetContainerByName('CONT_Migration_MSID_Selection')
	Guid=TagParserQuote.ParseString('<*CTX( Quote.CurrentItem.CartItemGuid )*>')
	Quote_Guid=dict()
	if Labor_Execution_Year_List!='':
		Quote_Guid=eval(Labor_Execution_Year_List)

	for row in MSID_PRODUCTS_CONT.Rows:
		if row["Scope"] in ["HWSWLABOR","LABOR"]:
			product_list=row.Product.GetContainerByName("CONT_MSID_SUBPRD")
			msid_row=row.Product
			for row1 in product_list.Rows:
				productName=row1["Selected_Products"]
				if productName in CS.conNames:
					for conName in CS.conNames.get(productName):
						con=msid_row.GetContainerByName(conName)
						Trace.Write("container name- "+str(conName))
						if con is None:
							Trace.Write("con "+str(conName))
							continue
						else:
							for row in con.Rows:
								if row["Execution_year"]!='' and row["Final_Hrs"]!='' and float(row["Final_Hrs"])>0:
									Trace.Write("Got_years")
									Execution_Year_list.append(row["Execution_year"])
		else:
			Execution_Year_list.append("No Labor")

	if quoteTotalTable.Rows.Count > 0 and len(Execution_Year_list)>0:
		row = quoteTotalTable.Rows[0]
		Quote_Guid[Guid]=(',').join(set(Execution_Year_list))
		row['Labor_Execution_Year']=str(Quote_Guid)
	elif quoteTotalTable.Rows.Count > 0 and len(Execution_Year_list)==0:
		Trace.Write("year list is empty")
		if Guid in Quote_Guid:
			Quote_Guid.pop(Guid)
		row = quoteTotalTable.Rows[0]
		row['Labor_Execution_Year']=str(Quote_Guid)
	quoteTotalTable.Save()

Laborwarningmessage(Quote)
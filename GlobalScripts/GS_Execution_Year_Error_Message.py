def DisplayMessage(ProductName, item, CS, Quote, Execution_year="Execution_Year", Final_Hrs="Final_Hrs"):
	from System import DateTime
	Today_Year=str(DateTime.Now.Year)
	flag=0
	Quote.Messages.Remove(Translation.Get('Execution_Year_Error_Message'))
	if ProductName in CS.conNames:
		for conName in CS.conNames.get(ProductName):
			con = item.SelectedAttributes.GetContainerByName(conName)
			if con is None:
				continue
			else:
				for row in con.Rows:
					if (row[Execution_year]!='' and row[Final_Hrs]!='') and (int(row[Execution_year])<int(Today_Year) and float(row[Final_Hrs])>0 and flag==0):
						flag=1
						break
			if flag==1:
				Trace.Write("H")
				Quote.Messages.Add(Translation.Get('Execution_Year_Error_Message'))
				break
	return flag
def Quote_Items(CS, Quote):
    Messageflag=0
    Removemessagefalag=0
    for item in Quote.MainItems:
        if item.ProductName in CS.product_name:
            Messageflag=DisplayMessage(item.ProductName, item, CS, Quote, "Execution Year", "Final Hrs")
            if Messageflag==1:
                break
        elif item.ProductName=="MSID_New":
            Product=item.SelectedAttributes.GetContainerByName("CONT_MSID_SUBPRD")
            for row in Product.Rows:
                 Messageflag=DisplayMessage(row["Selected_Products"], item, CS, Quote)
                 if Messageflag==1:
                    Removemessagefalag=1
                    break
        elif item.ProductName=="MSID":
            Product=item.SelectedAttributes.GetContainerByName("MSID_Product_Container")
            for row in Product.Rows:
                 Messageflag=DisplayMessage(row["Product Name"], item, CS, Quote)
                 if Messageflag==1:
                    Removemessagefalag=1
                    break
        elif item.ProductName=="Trace Software":
                 Messageflag=DisplayMessage(item.ProductName, item, CS, Quote)
                 if Messageflag==1:
                    break
        if Removemessagefalag==1:
            break
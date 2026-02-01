def Laborwarningmessage(Quote):
	from System import DateTime
	Today_Year=str(DateTime.Now.Year)
	isConfigurableProduct=Quote.ContainsAnyProductByPartNumber("Migration","PRJT","Trace Software")
	if Quote.GetCustomField('Booking LOB').Content in ["LSS","PAS"] and Quote.GetCustomField('Quote Type').Content=="Projects" and str(Quote.OrderStatus.Name) in ['Preparing','Ready for Approval','Rejected']:
		quoteTotalTable = Quote.QuoteTables["Quote_Details"]
		if quoteTotalTable.Rows.Count > 0:
			row = quoteTotalTable.Rows[0]
			previous_year=[]
			if row['Labor_Execution_Year']!="":
				for key,year in eval(row['Labor_Execution_Year']).items():
					year_list=year.split(",")
					previous_year=[val for val in year_list if val!="No Labor" and int(Today_Year)>int(val)]
					break
				if len(previous_year)>0 and not Quote.Messages.Contains(Translation.Get('Execution_Year_Error_Message')):
					Trace.Write("previous year"+str(previous_year))
					Quote.Messages.Add(Translation.Get('Execution_Year_Error_Message'))
				elif len(previous_year)==0:
					Trace.Write("year"+str(previous_year))
					Quote.Messages.Remove(Translation.Get('Execution_Year_Error_Message'))
				Quote.Messages.Remove(Translation.Get('Update_quote'))
			elif row['Labor_Execution_Year']=="" and isConfigurableProduct==True :
				if not Quote.Messages.Contains(Translation.Get('Update_quote')):
					Quote.Messages.Add(Translation.Get('Update_quote'))
		else:
			Quote.Messages.Remove(Translation.Get('Execution_Year_Error_Message'))

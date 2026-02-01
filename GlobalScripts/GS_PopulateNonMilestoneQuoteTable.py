def getFloat(Var):
	return float(Var) if Var else 0
def Populaterow(Quote, NMQT,EGAP_Non_Milestone_Name,EGAP_Non_Milestone_Description,cf_totalsellprice):
	row=NMQT.AddNewRow()
	row['EGAP_Non_Milestone_Name']=EGAP_Non_Milestone_Name
	row['EGAP_Non_Milestone_Description']=Quote.GetCustomField(EGAP_Non_Milestone_Description).Label
	row['EGAP_Amount']=getFloat(cf_totalsellprice.Content)
	row['Proposed_Non_Milestones']='Non-Milestone '+str(NMQT.Rows.IndexOf(row))
	NMQT.Save()
def PopulateNonMilestone(Quote):
	NMQT=Quote.QuoteTables['EGAP_Non_Milestone_Billing']
	NMQT.Rows.Clear()
	cf_totalLaborSellPrice = Quote.GetCustomField('EGAP_Total_Sell_Price_of_Project_Labor')
	cf_totalHSSellPrice = Quote.GetCustomField('EGAP_Total_Sell_Price_of_Honeywell_Software')
	cf_totalThirdPartyGoodsSellPrice = Quote.GetCustomField('EGAP_Total_Sell_Price_of_Third_Party_Goods')
	cf_totalOtherGoodsSellPrice = Quote.GetCustomField('EGAP_Total_Sell_Price_of_Other_Goods')
	cf_totalSubSWSellPrice = Quote.GetCustomField('EGAP_Total_Sell_Price_of_Subscription_SW')
	#cf_totalHCILaborSellPrice = Quote.GetCustomField('EGAP_Total_Sell_Price_of_HCI_Labor')
	#cf_totalHCISWSellPrice = Quote.GetCustomField('EGAP_Total_Sell_Price_of_HCI_SW')
	#cf_nonMilestoneBillingTotal = Quote.GetCustomField('EGAP_Non_Milestone_Billing_Total_Sell_Price')
	#cf_milestonePrice = Quote.GetCustomField('EGAP_Milestone_Price')
	if cf_totalLaborSellPrice.Content !="" and getFloat(cf_totalLaborSellPrice.Content)>0.0:
		#row=NMQT.AddNewRow()
		Populaterow(Quote,NMQT,'Project Labor','EGAP_Project_Labor_Milestone_Billing_Ques',cf_totalLaborSellPrice)
		#row['EGAP_Non_Milestone_Name']='Project Labor'
		#row['EGAP_Non_Milestone_Description']=Quote.GetCustomField('EGAP_Project_Labor_Milestone_Billing_Ques').Label
		#row['EGAP_Amount']=float(cf_totalLaborSellPrice.Content)
		#NMQT.Save()
	if cf_totalSubSWSellPrice.Content !="" and getFloat(cf_totalSubSWSellPrice.Content)>0.0:
		Populaterow(Quote,NMQT,'Honeywell Subscription Software','EGAP_Subscription_SW_Milestone_Billing_Ques',cf_totalSubSWSellPrice)
	if cf_totalThirdPartyGoodsSellPrice.Content !="" and getFloat(cf_totalThirdPartyGoodsSellPrice.Content)>0.0:
		Populaterow(Quote,NMQT,'Third Party Goods & Services','EGAP_Third_Party_Goods_Milestone_Billing_Ques',cf_totalThirdPartyGoodsSellPrice)
	if cf_totalOtherGoodsSellPrice.Content !="" and getFloat(cf_totalOtherGoodsSellPrice.Content)>0.0:
		Populaterow(Quote,NMQT,'Other Goods & Services','EGAP_Other_Goods_Milestone_Billing_Ques',cf_totalOtherGoodsSellPrice)
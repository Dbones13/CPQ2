import GS_APIGEE_Integration_Util
from GS_PMCMatrixNameUtil import PMC_MatrixName
def getColumnIndex(quoteType, LOB, proposalType, quoteDiscount,SFDCQuotetype):
	colIdx = 0
	if quoteType in ['Projects','Contract New','Contract Renewal']  and LOB == 'LSS':
		if proposalType == 'Budgetary':
			if quoteDiscount <= 0:
				colIdx = 1
			elif quoteDiscount > 0 and quoteDiscount <= 25:
				colIdx = 2
			elif quoteDiscount > 25 and quoteDiscount <= 45:
				colIdx = 3
			elif quoteDiscount > 45 and quoteDiscount < 55:
				colIdx = 4
			elif quoteDiscount >= 55:
				colIdx = 5
		elif proposalType in ['Firm', 'Booking']:
			if quoteDiscount <= 0:
				colIdx = 1
			elif quoteDiscount > 0 and quoteDiscount <= 25:
				colIdx = 2
			elif quoteDiscount > 25 and quoteDiscount <= 40:
				colIdx = 3
			elif quoteDiscount > 40 and quoteDiscount <= 45:
				colIdx = 4
			elif quoteDiscount >45 and quoteDiscount < 55:
				colIdx = 5
			elif quoteDiscount >= 55:
				colIdx = 6
	elif quoteType == 'Projects' and LOB == 'PAS':
		if proposalType == 'Budgetary':
			if quoteDiscount <= 0:
				colIdx = 1
			elif quoteDiscount > 0 and quoteDiscount <= 15:
				colIdx = 2
			elif quoteDiscount > 15 and quoteDiscount <= 25:
				colIdx = 3
			elif quoteDiscount > 25 and quoteDiscount < 35:
				colIdx = 4
			elif quoteDiscount >= 35:
				colIdx = 5
		elif proposalType in ['Firm', 'Booking']:
			if quoteDiscount <= 0:
				colIdx = 1
			elif quoteDiscount > 0 and quoteDiscount <= 7.5:
				colIdx = 2
			elif quoteDiscount > 7.5 and quoteDiscount <= 12.5:
				colIdx = 3
			elif quoteDiscount > 12.5 and quoteDiscount <= 20:
				colIdx = 4
			elif quoteDiscount >20 and quoteDiscount < 40:
				colIdx = 5
			elif quoteDiscount >= 40:
				colIdx = 6
	elif LOB == 'CCC':
		if quoteDiscount <= 10:
			colIdx = 1
		elif quoteDiscount > 10 and quoteDiscount <= 25:
			colIdx = 2
		elif quoteDiscount > 25 and quoteDiscount <= 45:
			colIdx = 3
		elif quoteDiscount > 45 and quoteDiscount <= 55:
			colIdx = 4
		elif quoteDiscount >55:
			colIdx = 5
	elif LOB == 'HCP' and SFDCQuotetype !='Software Only':
		if quoteDiscount <= 0:
			colIdx = 1
		elif quoteDiscount > 0 and quoteDiscount <= 20:
			colIdx = 2
		elif quoteDiscount > 20 and quoteDiscount <= 30:
			colIdx = 3
		elif quoteDiscount > 30 and quoteDiscount <= 35:
			colIdx = 4
		elif quoteDiscount > 35 and quoteDiscount < 40:
			colIdx = 5
		elif quoteDiscount >= 40:
			colIdx = 6
	elif LOB == 'HCP' and SFDCQuotetype =='Software Only':
		if quoteDiscount <= 0:
			colIdx = 1
		elif quoteDiscount > 0 and quoteDiscount <= 20:
			colIdx = 2
		elif quoteDiscount > 20 and quoteDiscount <= 50:
			colIdx = 3
		elif quoteDiscount > 50 and quoteDiscount <= 60:
			colIdx = 4
		elif quoteDiscount > 60 and quoteDiscount < 70:
			colIdx = 5
		elif quoteDiscount >= 70:
			colIdx = 6
	return colIdx



def getRowIndex(quoteType, LOB, proposalType, sellPrice):
	rowIdx = 0
	if (quoteType in ['Projects', 'Contract New','Contract Renewal']  and LOB == 'LSS') or (LOB == 'PAS' and quoteType =='Projects') or LOB == 'CCC':
		if sellPrice < 1000000:
			rowIdx = 1
		elif sellPrice >= 1000000 and sellPrice < 5000000:
			rowIdx = 2
		elif sellPrice >= 5000000 and sellPrice < 10000000:
			rowIdx = 3
		elif sellPrice >= 10000000 and sellPrice < 1000000000000000:
			rowIdx = 4
	elif LOB == 'HCP':
		if sellPrice >= 0 and sellPrice < 1000000:
			rowIdx = 1
		elif sellPrice >= 1000000 and sellPrice < 5000000:
			rowIdx = 2
		elif sellPrice >= 5000000 and sellPrice < 10000000:
			rowIdx = 3
		elif sellPrice >= 10000000 and sellPrice < 1000000000000000:
			rowIdx = 4
	else:
		if sellPrice < 50000:
			rowIdx = 1
		elif sellPrice >= 50000 and sellPrice < 500000:
			rowIdx = 2
		elif sellPrice >= 500000 and sellPrice < 2000000:
			rowIdx = 3
		elif sellPrice >= 2000000 and sellPrice < 7500000:
			rowIdx = 4
		elif sellPrice >= 7500000 and sellPrice < 25000000:
			rowIdx = 5
		elif sellPrice >= 25000000 and sellPrice <= 1000000000000000:
			rowIdx = 6
	return rowIdx



LOB = Quote.GetCustomField("CF_ApprovalTabBookingLOB").Content
oppCategory = Quote.GetCustomField("CF_ApprovalTabOpportunityCategory").Content
quoteType = Quote.GetCustomField("Quote Type").Content
# RejectedBy = Quote.GetCustomField("Rejected By").Content
# RejectionComment = Quote.GetCustomField("Rejection Comment").Content
# RejectionDate = Quote.GetCustomField("Rejection Date").Content
# RejectionLevel = Quote.GetCustomField("Rejection Level").Content
SFDCQuotetype = Quote.GetCustomField("SFDC_Quote_Type").Content
Margin_Approval_Level = Quote.GetCustomField('EGAP_Highest_Price_Margin_Approval_Level').Content
													
ProposalType = ''
PMCApprovalMatrixName = '' #---> Added for handling PMC Approval Matrix Table Name H541049
LimitType = ""
ColHeader = {}
ColHeader['LSS_Budgetary'] = ["Sell Price(USD)", "<=0%", ">0% - <=25%", ">25% - <=45%", ">45% - <55%", '>=55%']
ColHeader['LSS_Firm_Booking'] = ["Sell Price(USD)", "<=0%", ">0% - <=25%", ">25% - <=40%", ">40% - <=45%",'>45% - <55%', '>=55%']
ColHeader['PAS_Budgetary'] = ["Sell Price(USD)", "<=0%", ">0% - <=15%", ">15% - <=25%", ">25% - <35%", '>=35%']
ColHeader['PAS_Firm_Booking'] = ["Sell Price(USD)", "<=0%", ">0% - <=7.5%", ">7.5% - <=12.5%", ">12.5% - <=20%", '>20% - <40%', '>=40%']
ColHeader['CCC_Budgetary'] = ["Sell Price(USD)", "<=10%", ">10% - <=25%", ">25% - <=45%", ">45% - <=55%", '>55%']
ColHeader['CCC_Firm_Booking'] = ["Sell Price(USD)", "<=10%", ">10% - <=25%", ">25% - <=45%", ">45% - <=55%", '>55%']

if SFDCQuotetype != 'Software Only' and LOB == 'HCP':
	ColHeader['HCP_Firm_Booking'] = ["Sell Price(USD)", "<=0%", ">0% - <=20%", ">20% - <=30%", ">30% - <=35%", '>35% - <40%', '>=40%']
	ColHeader['HCP_Budgetary'] = ["Sell Price(USD)", "<=0%", ">0% - <=20%", ">20% - <=30%", ">30% - <=35%", '>35% - <40%', '>=40%']
elif SFDCQuotetype == 'Software Only' and LOB == 'HCP':
	ColHeader['HCP_Firm_Booking'] = ["Sell Price(USD)", "<=0%", ">0% - <=20%", ">20% - <=50%", ">50% - <=60%", '>60% - <70%', '>=70%']
	ColHeader['HCP_Budgetary'] = ["Sell Price(USD)", "<=0%", ">0% - <=20%", ">20% - <=50%", ">50% - <=60%", '>60% - <70%', '>=70%']

Columns = ["Sell Price(USD)", ">25%", ">10% - <=25", ">5% - <=10%", "<=5%"]
if SFDCQuotetype == 'Software Only' and LOB == 'HCP':
	Columns =  ["Sell Price(USD)", "<=0%", ">0% - <=20%", ">20% - <=50%", ">50% - <=60%", '>60% - <70%', '>=70%']

Values = []
DisplayRecords = False
exchangeRate    = Quote.GetCustomField('Exchange Rate').Content if Quote.GetCustomField('Exchange Rate').Content.strip() !='' else 1.0
quoteDetails = Quote.QuoteTables["Quote_Details"]
sellPrice = 0
quoteDiscount = 0
colIdx = rowIdx = 0
cf_proposalType = ''
if quoteDetails.Rows.Count:
	row = quoteDetails.Rows[0]
	sellPrice = row["Quote_Sell_Price"] / float(exchangeRate)
	quoteDiscount = row["Quote_Discount_Percent"]
	if (quoteType in ['Projects', 'Contract New','Contract Renewal']  and LOB in ['LSS', 'PAS']) or (quoteType in ['Projects', 'Parts and Spot']  and LOB in ['CCC','HCP']):
		sellPrice = row["Walk_away_Sales_Price"] / float(exchangeRate)
		quoteWTWCost = row['Quote_WTW_Cost'] / float(exchangeRate)
		wtwMargin = sellPrice - quoteWTWCost
		quoteDiscount = round((wtwMargin/sellPrice)*100,2) if sellPrice > 0 else 0
		cf_proposalType = Quote.GetCustomField("EGAP_Proposal_Type").Content if Quote.GetCustomField("EGAP_Proposal_Type").Content else ''
		'''Determine the col and row to be Hightlighted'''
		#Log.Info("Sellprice check => "+str(sellPrice)+" WTW => "+str(wtwMargin)+" Qtdiscount=> "+str(quoteDiscount))
		if Margin_Approval_Level != 'None':
			colIdx = getColumnIndex(quoteType, LOB, cf_proposalType, quoteDiscount,SFDCQuotetype) # Removed sellPrice argument from here since the function call has only 4 arguments
			# if LOB == 'CCC' and float(Quote.QuoteTables["Quote_Details"].Rows[0]["Quote_Discount_Percent"]) in(0,0.0):
				# colIdx = 6
			rowIdx = getRowIndex(quoteType, LOB, cf_proposalType, sellPrice) # Removed quoteDiscount argument from here since the function call has only 4 arguments


if ((quoteType in ['Projects', 'Contract New','Contract Renewal']  and LOB in ['LSS', 'PAS']) or (quoteType in ['Projects', 'Parts and Spot']  and LOB in ['CCC','HCP'])) and cf_proposalType != '':
	ProposalType = cf_proposalType
	LOBPProposalType = "{}_{}".format(LOB,ProposalType)
	if cf_proposalType in ['Firm', 'Booking']:
		LOBPProposalType = "{}_{}".format(LOB,'Firm_Booking')
		ProposalType = 'Firm & Booking'
	#Log.Info("LOBPProposalType: {}".format(LOBPProposalType))
	Columns = ColHeader[LOBPProposalType]
	LimitType = "Wall-to-Wall Margin"
	SqlStmtLst = ["SELECT TOP 1000 Cast(MinimumSellPrice as Float) MinimumSellPrice, Cast(MaximumSellPrice as Float) MaximumSellPrice, Cast(MinimumLimit as Float) MinimumDiscount, Cast(MaximumLimit as Float) MaximumDiscount, "]
	if LOBPProposalType == 'LSS_Budgetary':
		SqlStmtLst.append("IIF(ApprovalLevel !='', ApprovalLevel , 'No Approval') ApprovalLevel FROM SEA_APPROVAL_DISCOUNT_MATRIX ")
	elif LOB == 'LSS':
		SqlStmtLst.append("IIF(ApprovalLevel !='', ApprovalLevel , 'No P&M Approval') ApprovalLevel FROM SEA_APPROVAL_DISCOUNT_MATRIX ")
	elif LOBPProposalType == 'PAS_Budgetary':
		SqlStmtLst.append("IIF(ApprovalLevel !='', ApprovalLevel , 'No Approval') ApprovalLevel FROM SEA_APPROVAL_DISCOUNT_MATRIX ")
	elif LOBPProposalType == 'PAS_Firm_Booking':
		SqlStmtLst.append("IIF(ApprovalLevel !='', ApprovalLevel , 'Functional Approvals Only') ApprovalLevel FROM SEA_APPROVAL_DISCOUNT_MATRIX ")
	elif LOBPProposalType == 'CCC_Firm_Booking':
		SqlStmtLst.append("IIF(ApprovalLevel !='', ApprovalLevel , 'Functional Approvals Only') ApprovalLevel FROM SEA_APPROVAL_DISCOUNT_MATRIX ")
	elif LOBPProposalType == 'CCC_Budgetary':
		SqlStmtLst.append("IIF(ApprovalLevel !='', ApprovalLevel , 'No Approval') ApprovalLevel FROM SEA_APPROVAL_DISCOUNT_MATRIX ")
	elif LOBPProposalType in ('HCP_Budgetary','HCP_Firm_Booking'):
		if SFDCQuotetype != 'Software Only':
			SqlStmtLst.append("ApprovalLevel FROM SEA_APPROVAL_DISCOUNT_MATRIX ")
		else:
			SqlStmtLst.append("ApprovalLevel FROM SEA_APPROVAL_DISCOUNT_MATRIX_SWONLY ")
	SqlStmtLst.append("WHERE LOB = '{}' AND ProposalType = '{}' AND LimitType = '{}' order by MinimumSellPrice")
	SqlQuery = "".join(SqlStmtLst).format(LOB,ProposalType,LimitType)
	#Log.Info(SqlQuery)
	# Trace.Write('SqlQuery2-'+str(SqlQuery))
	ApprovalLevels = SqlHelper.GetList(SqlQuery)
	DisplayRecords = False
	idx = PreviousPriceRange = 0
	if ApprovalLevels is not None and len(ApprovalLevels) > 0:
		DisplayRecords = True
		for row in ApprovalLevels:
			Discount0 = Discount1_25 = Discount26_45 = Discount46_54 = Discount55 = Discount66 = None
			if quoteType in ['Projects','Contract New','Contract Renewal']  and LOB == 'LSS':
				if ProposalType == 'Budgetary':
					if row.MaximumDiscount == 0:
						Discount0 = row.ApprovalLevel
					elif row.MinimumDiscount >= 0 and row.MaximumDiscount <= 25:
						Discount1_25 = row.ApprovalLevel
					elif row.MinimumDiscount >= 25 and row.MaximumDiscount <= 45:
						Discount26_45 = row.ApprovalLevel
					elif row.MinimumDiscount >= 45 and row.MaximumDiscount <= 55:
						Discount46_54 = row.ApprovalLevel
					elif row.MinimumDiscount >=55:
						Discount55 = row.ApprovalLevel
				else:
					if row.MaximumDiscount == 0:
						Discount0 = row.ApprovalLevel
					elif row.MinimumDiscount >= 0 and row.MaximumDiscount <= 25:
						Discount1_25 = row.ApprovalLevel
					elif row.MinimumDiscount >= 25 and row.MaximumDiscount <= 40:
						Discount26_45 = row.ApprovalLevel
					elif row.MinimumDiscount >= 40 and row.MaximumDiscount <= 45:
						Discount46_54 = row.ApprovalLevel
					elif row.MinimumDiscount >= 45 and row.MaximumDiscount < 55:
						Discount55 = row.ApprovalLevel
					elif row.MinimumDiscount >=55:
						Discount66 = row.ApprovalLevel
			elif quoteType == 'Projects' and LOB == 'PAS':
				if ProposalType == 'Budgetary':
					if row.MaximumDiscount == 0:
						Discount0 = row.ApprovalLevel
					elif row.MinimumDiscount >= 0 and row.MaximumDiscount <= 15:
						Discount1_25 = row.ApprovalLevel
					elif row.MinimumDiscount >= 15 and row.MaximumDiscount <= 25:
						Discount26_45 = row.ApprovalLevel
					elif row.MinimumDiscount >= 25 and row.MaximumDiscount <= 35:
						Discount46_54 = row.ApprovalLevel
					elif row.MinimumDiscount >=35:
						Discount55 = row.ApprovalLevel
				else:
					if row.MaximumDiscount == 0:
						Discount0 = row.ApprovalLevel
					elif row.MinimumDiscount >= 0 and row.MaximumDiscount <= 7.5:
						Discount1_25 = row.ApprovalLevel
					elif row.MinimumDiscount >= 7.5 and row.MaximumDiscount <= 12.5:
						Discount26_45 = row.ApprovalLevel
					elif row.MinimumDiscount >= 12.5 and row.MaximumDiscount <= 20:
						Discount46_54 = row.ApprovalLevel
					elif row.MinimumDiscount >= 20 and row.MaximumDiscount <= 40:
						Discount55 = row.ApprovalLevel
					elif row.MinimumDiscount >=40:
						Discount66 = row.ApprovalLevel
			elif LOB == 'CCC':
				if row.MaximumDiscount <= 10:
					Discount0 = row.ApprovalLevel
				elif row.MinimumDiscount >= 10 and row.MaximumDiscount <= 25:
					Discount1_25 = row.ApprovalLevel
				elif row.MinimumDiscount > 25 and row.MaximumDiscount <= 45:
					Discount26_45 = row.ApprovalLevel
				elif row.MinimumDiscount > 45 and row.MaximumDiscount <= 55:
					Discount46_54 = row.ApprovalLevel
				elif row.MinimumDiscount > 55:
					Discount55 = row.ApprovalLevel
			elif LOB == 'HCP' and SFDCQuotetype != 'Software Only':
				if row.MinimumDiscount <= 0:
					Discount0 = row.ApprovalLevel
				elif row.MinimumDiscount > 0 and row.MaximumDiscount <= 20:
					Discount1_25 = row.ApprovalLevel
				elif row.MinimumDiscount > 20 and row.MaximumDiscount <= 30:
					Discount26_45 = row.ApprovalLevel
				elif row.MinimumDiscount > 30 and row.MaximumDiscount <= 35:
					Discount46_54 = row.ApprovalLevel
				elif row.MinimumDiscount > 35 and row.MaximumDiscount < 40:
					Discount55 = row.ApprovalLevel
				elif row.MaximumDiscount >= 40:
					Discount66 = row.ApprovalLevel
			elif LOB == 'HCP' and SFDCQuotetype == 'Software Only':
				if row.MinimumDiscount <= 0:
					Discount0 = row.ApprovalLevel
				elif row.MinimumDiscount > 0 and row.MaximumDiscount <= 20:
					Discount1_25 = row.ApprovalLevel
				elif row.MinimumDiscount > 20 and row.MaximumDiscount <= 50:
					Discount26_45 = row.ApprovalLevel
				elif row.MinimumDiscount > 50 and row.MaximumDiscount <= 60:
					Discount46_54 = row.ApprovalLevel
				elif row.MinimumDiscount > 60 and row.MaximumDiscount < 70:
					Discount55 = row.ApprovalLevel
				elif row.MaximumDiscount >= 70:
					Discount66 = row.ApprovalLevel
			SellPriceRange = None
			if (quoteType in ['Projects', 'Contract New','Contract Renewal']  and LOB == 'LSS' and ProposalType in ['Budgetary','Firm & Booking']) or (quoteType == 'Projects' and LOB == 'PAS') or LOB == 'CCC':
				if row.MinimumSellPrice >= 0 and row.MaximumSellPrice < 1000000:
					SellPriceRange = " <${}M ".format(1)
				elif row.MinimumSellPrice >= 1000000 and row.MaximumSellPrice < 5000000:
					SellPriceRange = " >=${}M - <${}M ".format(1,5)
				elif row.MinimumSellPrice >= 5000000 and row.MaximumSellPrice < 10000000:
					SellPriceRange = " >=${}M - <${}M ".format(5,10)
				elif row.MinimumSellPrice >= 10000000 and row.MaximumSellPrice <= 1000000000000000:
					SellPriceRange = " >=${}M - <${}M ".format(10,50)
			elif LOB == "HCP" and SFDCQuotetype !='Software Only':
				if row.MinimumSellPrice >= 0 and row.MaximumSellPrice < 1000000:
					SellPriceRange = " <${}M ".format(1)
				elif row.MinimumSellPrice >= 1000000 and row.MaximumSellPrice < 5000000:
					SellPriceRange = " >=${}M - <${}M ".format(1, 5)
				elif row.MinimumSellPrice >= 5000000 and row.MaximumSellPrice < 10000000:
					SellPriceRange = " >=${}M - <${}M ".format(5, 10)
				elif row.MinimumSellPrice >= 10000000 and row.MaximumSellPrice <= 1000000000000000:
					SellPriceRange = " >=${}M - <${}M ".format(10, 50)
			elif LOB == "HCP" and SFDCQuotetype =='Software Only':
				if row.MinimumSellPrice >= 0 and row.MaximumSellPrice < 1000000:
					SellPriceRange = " <${}M ".format(1)
				elif row.MinimumSellPrice >= 1000000 and row.MaximumSellPrice < 5000000:
					SellPriceRange = " >=${}M - <${}M ".format(1, 5)
				elif row.MinimumSellPrice >= 5000000 and row.MaximumSellPrice < 10000000:
					SellPriceRange = " >=${}M - <${}M ".format(5, 10)
				elif row.MinimumSellPrice >= 10000000 and row.MaximumSellPrice < 50000000:
					SellPriceRange = " >=${}M - <${}M ".format(10, 50)
			if SellPriceRange is not None:
				if PreviousPriceRange == SellPriceRange:
					pre_idx = idx -1
					if Discount0 is not None:
						Values[pre_idx]["Discount0"] = Discount0
					elif Discount1_25 is not None:
						Values[pre_idx]["Discount1_25"] = Discount1_25
					elif Discount26_45 is not None:
						Values[pre_idx]["Discount26_45"] = Discount26_45
					elif Discount46_54 is not None:
						Values[pre_idx]["Discount46_54"] = Discount46_54
					elif Discount55 is not None:
						Values[pre_idx]["Discount55"] = Discount55
					elif Discount66 is not None:
						Values[pre_idx]["Discount66"] = Discount66
					'''elif Discount1_20 is not None:
						Values[pre_idx]["Discount1_20"] = Discount1_20
					elif Discount21_30 is not None:
						Values[pre_idx]["Discount21_30"] = Discount21_30
					elif Discount31_35 is not None:
						Values[pre_idx]["Discount31_35"] = Discount31_35
					elif Discount36_39 is not None:
						Values[pre_idx]["Discount36_39"] = Discount36_39
					elif Discount40 is not None:
						Values[pre_idx]["Discount40"] = Discount40'''
				else:
					Values.append({"SellPriceRange": SellPriceRange,"Discount0":Discount0, "Discount1_25": Discount1_25, "Discount26_45": Discount26_45, "Discount46_54": Discount46_54, "Discount55": Discount55, "Discount66": Discount66});
					idx +=1
					PreviousPriceRange = SellPriceRange
elif LOB == 'LSS':
	Values = []
	LOB = "LSS"
	ProposalType = "Parts & Spots"
	LimitType = "Discount"
	Booking_Country = Quote.GetCustomField('Booking Country').Content
	SqlStmtLst = ["SELECT TOP 1000 Cast(MinimumSellPrice as Float) MinimumSellPrice, Cast(MaximumSellPrice as Float) MaximumSellPrice, Cast(MinimumLimit as Float) MinimumDiscount, Cast(MaximumLimit as Float) MaximumDiscount, ",
				"ApprovalLevel FROM SEA_APPROVAL_DISCOUNT_MATRIX ",
				"WHERE LOB = '{}' AND ProposalType = '{}' AND LimitType = '{}' AND coalesce(BookingCountry,'') in ('{}','') order by MinimumSellPrice"]
	SqlQuery = "".join(SqlStmtLst).format(LOB,ProposalType,LimitType,Booking_Country)
	# Trace.Write('SqlQuery-'+str(SqlQuery))
	ApprovalLevels = SqlHelper.GetList(SqlQuery)
	idx = PreviousPriceRange = 0
	if ApprovalLevels is not None and len(ApprovalLevels) > 0:
		DisplayRecords = True
		for row in ApprovalLevels:
			Discount25 = Discount10_25 = Discount5_10 = Discount5 = None
			if row.MinimumDiscount >= 25:
				Discount25 = row.ApprovalLevel
			elif row.MinimumDiscount >= 10 and row.MaximumDiscount <= 25:
				Discount10_25 = row.ApprovalLevel
			elif row.MinimumDiscount >= 5 and row.MaximumDiscount <= 10:
				Discount5_10 = row.ApprovalLevel
			elif row.MaximumDiscount <= 5:
				Discount5 = row.ApprovalLevel



			SellPriceRange = None
			if row.MinimumSellPrice >= 0 and row.MaximumSellPrice < 25000:
				SellPriceRange = " <${}K ".format(25)
			elif row.MinimumSellPrice >= 25000 and row.MaximumSellPrice < 100000:
				SellPriceRange = " >=${}K - <${}K ".format(25, 100)
			elif row.MinimumSellPrice >= 100000 and row.MaximumSellPrice < 250000:
				SellPriceRange = " >=${}K - <${}K ".format(100, 250)
			elif row.MinimumSellPrice >= 250000 and row.MaximumSellPrice < 500000:
				SellPriceRange = " >=${}K - <${}K ".format(250, 500)
			elif row.MinimumSellPrice >= 500000 and row.MaximumSellPrice > 500000:
				SellPriceRange = " >=${}K ".format(500)



			if SellPriceRange is not None:
				if PreviousPriceRange == SellPriceRange:
					pre_idx = idx -1
					if Discount25 is not None:
						Values[pre_idx]["Discount25"] = Discount25
					elif Discount10_25 is not None:
						Values[pre_idx]["Discount10_25"] = Discount10_25
					elif Discount5_10 is not None:
						Values[pre_idx]["Discount5_10"] = Discount5_10
					elif Discount5 is not None:
						Values[pre_idx]["Discount5"] = Discount5
				else:
					Values.append({"SellPriceRange": SellPriceRange, "Discount25": Discount25, "Discount10_25": Discount10_25, "Discount5_10": Discount5_10, "Discount5": Discount5});
					idx +=1
					PreviousPriceRange = SellPriceRange
# PMC Approval Matrix Table Update Logic ----> H541049 (start)
elif LOB == 'PMC':
	Values = []
	MatrixName = PMC_MatrixName(Quote)
	LOB = "PMC"
	LimitType = "Discount"
	if MatrixName:
		PMCApprovalMatrixName = MatrixName.PMCMatrixName
		if (Quote.GetCustomField("Booking Country").Content).lower() == "india":
			BookingCountry = 'india'
			SqlQuery2 = "SELECT TOP 1000 Cast(MinimumSellPrice as int) MinimumSellPrice, Cast(MaximumSellPrice as int) MaximumSellPrice, Cast(MinimumLimit as float) MinimumDiscount, Cast(MaximumLimit as float) MaximumDiscount, ApprovalLevel FROM SEA_APPROVAL_DISCOUNT_MATRIX WHERE LOB = '{0}' AND LimitType = '{1}' AND BookingCountry = '{2}' AND PMCMatrixName = '{3}' GROUP BY MinimumSellPrice, MaximumSellPrice, MinimumLimit, MaximumLimit, ApprovalLevel".format(LOB,LimitType,BookingCountry,PMCApprovalMatrixName)
		else:
			BookingCountry = ''
			SqlQuery2 = "SELECT TOP 1000 Cast(MinimumSellPrice as int) MinimumSellPrice, Cast(MaximumSellPrice as int) MaximumSellPrice, Cast(MinimumLimit as float) MinimumDiscount, Cast(MaximumLimit as float) MaximumDiscount, ApprovalLevel FROM SEA_APPROVAL_DISCOUNT_MATRIX WHERE LOB = '{0}' AND LimitType = '{1}' AND (BookingCountry = '{2}' OR BookingCountry Is null) AND PMCMatrixName = '{3}' GROUP BY MinimumSellPrice, MaximumSellPrice, MinimumLimit, MaximumLimit, ApprovalLevel".format(LOB,LimitType,BookingCountry,PMCApprovalMatrixName)
		ApprovalLevels = SqlHelper.GetList(SqlQuery2)

		# Sample data
		data = []
		for i in ApprovalLevels:
			a = {}
			a['ApprovalLevel'] = (i.ApprovalLevel)
			a['MaximumDiscount'] = (i.MaximumDiscount)
			a['MaximumSellPrice'] = (i.MaximumSellPrice)
			a['MinimumDiscount'] = (i.MinimumDiscount)
			a['MinimumSellPrice'] = (i.MinimumSellPrice)
			# Trace.Write(a)
			data.append(a)

		# Initialize a table to store maximum 'ApprovalLevel' values
		table = {}

		# Extract unique pairs of MinimumDiscount and MaximumDiscount
		discount_pairs = sorted(set((obj['MinimumDiscount'], obj['MaximumDiscount']) for obj in data))

		#Storing the Columns
		Columns = ["Sell Price(USD)"]
		for dp in discount_pairs:
			dp_range = "{}%-{}%".format(dp[0],dp[1])
			Columns.append(dp_range)

		# Extract unique pairs of MinimumSellPrice and MaximumSellPrice
		sell_price_pairs = sorted(set((obj['MinimumSellPrice'], obj['MaximumSellPrice']) for obj in data))

		# Initialize the table with None values
		for dr in discount_pairs:
			for sp in sell_price_pairs:
				table[(dr, sp)] = "none"

		# Populate the table with maximum 'ApprovalLevel' values
		for obj in data:
			approval_level = obj['ApprovalLevel']
			min_discount = obj['MinimumDiscount']
			max_discount = obj['MaximumDiscount']
			min_sell_price = obj['MinimumSellPrice']
			max_sell_price = obj['MaximumSellPrice']
			for dr in discount_pairs:
				for sp in sell_price_pairs:
					if min_discount == dr[0] and max_discount == dr[1] and min_sell_price == sp[0] and max_sell_price == sp[1]:
						table[(dr, sp)] = approval_level

		if Quote.GetCustomField("PMC Type").Content == "Services":
			PMCApprovalMatrixName = "PMC Services"
		for sp in sell_price_pairs:
			sp_dict = {}
			sp_range = "{}M-{}M".format(float(sp[0])/1000000,float(sp[1])/1000000)
			sp_dict['Sell Price(USD)'] = sp_range
			for dr in discount_pairs:
				dr_range = "{}%-{}%".format(dr[0],dr[1])
				sp_dict[dr_range] = table[(dr, sp)]
				if sp_dict not in Values:
					Values.append(sp_dict) # ----> H541049 (end)
	
Model = {}
Model['PMCApprovalMatrixName'] = PMCApprovalMatrixName  #---> Added for handling PMC Approval Matrix Table Name H541049
Model['ProposalType'] = ProposalType
Model['LimitType'] = LimitType if quoteType not in ['Contract New','Contract Renewal'] else "Regional Margin"

Model['ColumnIndex'] = colIdx
Model['RowIndex'] = rowIdx
Model['columns'] = Columns
Model['values'] = Values
Model['displayRecords'] = DisplayRecords
Model['ItemCount'] = Quote.Items.Count
'''Rejection Custom Fields'''
# Model['rejectedBy'] = RejectedBy
# Model['rejectionComment'] = RejectionComment
# Model['rejectionDate'] = RejectionDate
# Model['rejectionLevel'] = RejectionLevel
Model['LOB'] = LOB
# Trace.Write('approval model-'+str(Model))

Approval = Param.Approval if hasattr(Param, "Approval") else ''
if 1:
	if Approval=='Getapproval':
		import GS_R2Q_FunctionalUtil
		#Quote.GetCustomField('EGAP_Highest_Price_Margin_Approval_Level').Content='0'
		colval=['','Discount0','Discount1_25','Discount26_45','Discount46_54','Discount55','Discount66']
		Aprovalstatus = Model['values'][rowIdx-1].get(colval[colIdx], "")
		Trace.Write('adding in before '+str(Quote.GetCustomField('Is_Quote_Approval_Exempted').Content))
		Log.Info('Aprovalstatus out-->'+str([Aprovalstatus,LOB]))
		if Quote.GetCustomField('Is_Quote_Approval_Exempted').Content == 'Yes':
			Log.Info('Aprovalstatus in-->'+str([Aprovalstatus]))
			Quote.GetCustomField("EGAP_Highest_Approval_Level_for_the_Quote").Content='No Approval'
			if LOB == 'HCP':
				Quote.GetCustomField('EGAP_Highest_Price_Margin_Approval_Level').Content = Aprovalstatus
		else:
			Quote.GetCustomField("EGAP_Highest_Approval_Level_for_the_Quote").Content=Aprovalstatus
			Quote.GetCustomField('EGAP_Highest_Price_Margin_Approval_Level').Content = Aprovalstatus
		Quote.GetCustomField("CF_MaxApprovalLevel").Content=Aprovalstatus
		Trace.Write(str(Quote.GetCustomField("EGAP_Highest_Approval_Level_for_the_Quote").Content)+"--ApprovalApprovalApprovalApprovalApproval  "+str(Aprovalstatus))
		saveAction = Quote.GetCustomField("R2Q_Save").Content
		if (Quote.GetCustomField('IsR2QRequest').Content == 'Yes' and str(Aprovalstatus) == '2' and LOB == 'HCP') or (Quote.GetCustomField('Is_Quote_Approval_Exempted').Content == 'Yes' and LOB == 'HCP'):
			Quote.GetCustomField("EGAP_Highest_Approval_Level_for_the_Quote").Content='No Approval'
			#Quote.GetCustomField('EGAP_Highest_Price_Margin_Approval_Level').Content = 'No Approval'
			Quote.GetCustomField('Is_Quote_Approval_Exempted').Content == 'Yes'
		"""if Quote.GetCustomField("EGAP_Highest_Approval_Level_for_the_Quote").Content not in ['','NA','0','No Approval'] and saveAction != 'Save':
			GS_R2Q_FunctionalUtil.UpdateStatusMessage(Quote, "Egap Initiation", "Action", 'Quote submitted but egap approval required')
			Log.Info("ApprovalApprovalApprovalApprovalApproval  "+str(Aprovalstatus))"""
	elif Approval=='getstatus':
		colval=['','Discount0','Discount1_25','Discount26_45','Discount46_54','Discount55','Discount66']
		Aprovalstatus = Model['values'][rowIdx-1].get(colval[colIdx], "")
		if Quote.GetCustomField('Is_Quote_Approval_Exempted').Content == 'Yes':
			Quote.GetCustomField("EGAP_Highest_Approval_Level_for_the_Quote").Content='No Approval'
		else:
			Quote.GetCustomField("EGAP_Highest_Approval_Level_for_the_Quote").Content=Aprovalstatus
		Quote.GetCustomField("CF_MaxApprovalLevel").Content=Aprovalstatus
	else:
		ApiResponse = ApiResponseFactory.JsonResponse(Model)
	Log.Write("GS_ApprovalTabContent Success-->>")
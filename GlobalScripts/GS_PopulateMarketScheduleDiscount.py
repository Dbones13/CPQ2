def PopulateMarketScheduleDiscount(Quote):
	def getCustomFieldValue(cfName):
		return Quote.GetCustomField(cfName).Content

	def setCustomField(cfName,Value):
		Quote.GetCustomField(cfName).Content = Value

	def getCompititorValue(fieldValue):
		fieldValue = int(fieldValue)
		if fieldValue == 0 or fieldValue == '':
			competitorCount = "Low"
		elif fieldValue == 1:
			competitorCount = "Medium"
		elif fieldValue > 1:
			competitorCount = "High"
		return competitorCount

	def getEstimatedPriceScore(bookingLOB,estimatedSellPrice):
		score_estimatedSellPrice = 0
		query2 = SqlHelper.GetList("select * from MARKETDISCOUNT_SCHEDULE_SCORE where Field_Name = 'EstimatedSellPrice' and LOB = '"+bookingLOB+"'")
		for i in query2:
			if estimatedSellPrice > float(i.Field_Value) and estimatedSellPrice < float(i.Field_Value_2):
				score_estimatedSellPrice = int(i.Score)
		return score_estimatedSellPrice

	if getCustomFieldValue("Quote Type") == "Projects":
		competitorCount = getCompititorValue(getCustomFieldValue("CompetitorCount"))
		estimatedSellPrice = float(getCustomFieldValue("EstimatedSellPrice"))
		margetSegment = getCustomFieldValue("Market Segment")
		destinationCountry = getCustomFieldValue("Destination Country").title()
		businessModel = getCustomFieldValue("Business Model")
		proposalType = getCustomFieldValue("EGAP_Proposal_Type")
		bookingLOB = getCustomFieldValue("Booking LOB")
		score_competitorCount = 0
		score_margetSegment = 0
		score_destinationCountry = 0
		score_businessModel = 0
		score_proposalType = 0

		query1 = SqlHelper.GetList("Select * from MARKETDISCOUNT_SCHEDULE_SCORE where LOB = '"+bookingLOB+"'")
		for i in query1:
			if i.Field_Value == competitorCount:
				score_competitorCount = int(i.Score)
			elif i.Field_Value == margetSegment:
				score_margetSegment = int(i.Score)
			elif i.Field_Value == destinationCountry:
				score_destinationCountry = int(i.Score)
			elif i.Field_Value == businessModel:
				score_businessModel = int(i.Score)
			elif i.Field_Value == proposalType:
				score_proposalType = int(i.Score)

		score_estimatedSellPrice = getEstimatedPriceScore(bookingLOB,estimatedSellPrice)

		totalScore = str(score_competitorCount + score_margetSegment + score_destinationCountry + score_businessModel + score_proposalType + score_estimatedSellPrice)
		if int(totalScore) >= 11:
			totalScore = ">=11"

		query3 = SqlHelper.GetFirst("select Market_Discount_Schedule from MARKETDISCOUNT_SCHEDULE where Total_Score = '"+totalScore+"' and LOB = '"+bookingLOB+"'")
		if query3 is not None:
			if getCustomFieldValue("Recommended Discount Plan") != query3.Market_Discount_Schedule:
				setCustomField("Recommended Discount Plan",query3.Market_Discount_Schedule)
				setCustomField("Schedule Price Plan Updated	","True")
			if getCustomFieldValue("Selected Discount Plan") == '' and bookingLOB in ('LSS','PAS'):
				setCustomField("Selected Discount Plan",query3.Market_Discount_Schedule)
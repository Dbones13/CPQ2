if Session["prevent_execution"] != "true" and Quote.GetCustomField("Booking LOB").Content != 'CCC':
	PROS_Guidance = Quote.GetCustomField("PROS Guidance Recommendation").Content
	MPA = Quote.GetCustomField("MPA").Content

	for Item in Quote.Items:
		#Log.Info("-------------vs---------"+str(Item.ExtendedListPrice))
		if Item.QI_ProductLine.Value !='' and Item.QI_No_Discount_Allowed.Value == "0":
			if PROS_Guidance == "Target Discount" and MPA == '':
				#Quote.GetCustomField("PROS Guidance Recommendation").Content="Target Discount"
				Item.QI_Guidance_Discount_Percent.Value = Item.QI_TARGET_DISCOUNT.Value
				#Item.QI_MPA_Discount_Percent.Value = Item.QI_Guidance_Discount_Percent.Value

			if PROS_Guidance == "Floor Discount" and MPA == '':
				Item.QI_Guidance_Discount_Percent.Value = Item.QI_FLOOR_DISCOUNT.Value
				#Item.QI_MPA_Discount_Percent.Value = Item.QI_Guidance_Discount_Percent.Value

			if PROS_Guidance == "Expert Discount" and MPA == '':
				Item.QI_Guidance_Discount_Percent.Value = Item.QI_EXPERT_DISCOUNT.Value
				#Item.QI_MPA_Discount_Percent.Value = Item.QI_Guidance_Discount_Percent.Value

			if Item.QI_Guidance_Discount_Percent.Value != 0:
				Item.QI_PROS_Guidance_Recommended_Price.Value = Item.ExtendedListPrice*(100-Item.QI_Guidance_Discount_Percent.Value)/100
				#Item.QI_MPA_Discount_Amount.Value = Item.QI_PROS_Guidance_Recommended_Price.Value
				#Trace.Write("-->+-->aa" +str(Item.QI_PROS_Guidance_Recommended_Price.Value))
			if MPA != '':
				#Item.QI_MPA_Discount_Percent.Value = Item.QI_Guidance_Discount_Percent.Value
				#Item.QI_MPA_Discount_Amount.Value = Item.QI_PROS_Guidance_Recommended_Price.Value
				Item.QI_PROS_Guidance_Recommended_Price.Value = Item.ExtendedListPrice
				#Item.QI_MPA_Discount_Amount.Value = Item.QI_PROS_Guidance_Recommended_Price.Value
			#Trace.Write("-->+-->bb" +str(Item.QI_PROS_Guidance_Recommended_Price.Value))
		elif Item.QI_ProductLine.Value !='' and Item.QI_No_Discount_Allowed.Value == "1":
			Item.QI_PROS_Guidance_Recommended_Price.Value = Item.ExtendedListPrice
			#Item.QI_MPA_Discount_Amount.Value = Item.QI_PROS_Guidance_Recommended_Price.Value
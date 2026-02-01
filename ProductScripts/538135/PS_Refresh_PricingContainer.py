if Product.Name != "Service Contract Products":
	from GS_SC_CBM_PRICING_CALCULATIONS import reset_values,pricing_calc
	ConRows=Product.GetContainerByName('CBM_Pricing_Container').Rows
	if ConRows.Count>0:
		for row in ConRows:
			productFamily = row.Product.Attr("CBM_PRODUCT_FAMILY").GetValue()
			assetType = row.Product.Attr("CBM_ASSET_TYPE").GetValue()
			level = row.Product.Attr("CBM_Level").GetValue()
			count = row.Product.Attr("CBM_COUNT").GetValue()
			cycles = row.Product.Attr("CBM_PM/CBM_Cycles").GetValue()
			if productFamily is not None and productFamily != "" and assetType is not None and assetType != "":
				#CXCPQ-86942: Added new columns
				getPricingDetails = SqlHelper.GetFirst("select STD_Hours_LT,Remote_TT_NC,Remote_TT_C,Total_Tasks,Remote_T_NC,Remote_T_C,STD_Hours_LT_Quarterly,Remote_TT_NC_Quarterly,Remote_TT_C_Quarterly from SC_CT_CBM_Pricing where Product_Family = '"+str(productFamily)+"' and Asset_Type = '"+str(assetType)+"'")
			if assetType is None or assetType == "":
				reset_values(row.Product)
			else:
				lpmTask = ""
				if int(level) == 1:
					lpmTask = SqlHelper.GetFirst("select L_PMT_R_NLP from SC_CT_CBM_Pricing where Product_Family = '"+str(productFamily)+"' and Asset_Type = '"+str(assetType)+"'").L_PMT_R_NLP
				elif int(level) == 2:
					lpmTask = SqlHelper.GetFirst("select L_PMT_NR_NLP from SC_CT_CBM_Pricing where Product_Family = '"+str(productFamily)+"' and Asset_Type = '"+str(assetType)+"'").L_PMT_NR_NLP
				else:
					lpmTask = SqlHelper.GetFirst("select Local_TL3 from SC_CT_CBM_Pricing where Product_Family = '"+str(productFamily)+"' and Asset_Type = '"+str(assetType)+"'").Local_TL3
				resultCalc = pricing_calc(level,getPricingDetails,count,cycles,Quote,TagParserQuote,Session)
				row.Product.Attr("CBM_REMOTE_TIME").AssignValue(resultCalc["RemoteTime"])
				row.Product.Attr("CBM_LOCAL_TIME").AssignValue(resultCalc["LocalTime"])
				row.Product.Attr("CBM_TASK_PERCENTAGE").AssignValue(resultCalc["Tasks"])
				row.Product.Attr("CBM_PER_TIME").AssignValue(resultCalc["PerTime"])
				row.Product.Attr("CBM_REMOTE_TASKS").AssignValue(resultCalc["RemoteTask"])
				row.Product.Attr("CBM_LOCAL_TASKS").AssignValue(resultCalc["LocalTask"])
				row.Product.Attr("CBM_LIST_PRICE_PER_CYCLE").AssignValue(resultCalc["ListPricePerCycle"])
				row.Product.Attr("CBM_ANNUAL_PRICE").AssignValue(resultCalc["AnnualPrice"])
				row.Product.Attr('CBM_LPM_TASK').AssignValue(str(lpmTask))
				Trace.Write("SAnnualPrice = " + str(resultCalc))
			row.Product.ApplyRules()
			row.Calculate()
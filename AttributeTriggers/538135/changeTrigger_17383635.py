Trace.Write("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
Trace.Write(Product.Attr("CBM_PM/CBM_Cycles").GetValue())
#Trace.Write('before assigning ->'+Product.Attr("CBM_HIDDEN_CYCLES").GetValue())

#Trace.Write('after assigning - >'+Product.Attr("CBM_HIDDEN_CYCLES").GetValue())

from GS_SC_CBM_PRICING_CALCULATIONS import reset_values,pricing_calc
Trace.Write('triggered from hidden attribute..')
old_cycle = Product.Attr('CBM_HIDDEN_CYCLES').GetValue()
Trace.Write('old_cycle '+str(old_cycle))
new_cycle = Product.Attr('CBM_PM/CBM_Cycles').GetValue()
Trace.Write('new_cycle '+new_cycle)
if new_cycle != "":
    for row in Product.GetContainerByName('CBM_Pricing_Container').Rows:
    	annual_price = (float(row['Annual Price']) / float(old_cycle) ) * float(new_cycle)
    	row['Annual Price'] = str(annual_price)
    	row.Product.Attr("CBM_ANNUAL_PRICE").AssignValue(str(annual_price))
    	#row.Calculate()
    	row.ApplyProductChanges()
    Product.Attr("CBM_HIDDEN_CYCLES").AssignValue(str(Product.Attr("CBM_PM/CBM_Cycles").GetValue()))
else:
    Product.Attr("CBM_PM/CBM_Cycles").SelectValue(str(Product.Attr("CBM_HIDDEN_CYCLES").GetValue()))
#Change product status as incomplete
Product.Attr('SC_Product_Status').AssignValue("0")
"""Product.Attr("CBM_HIDDEN_CYCLES").AssignValue(str(Product.Attr('CBM_PM/CBM_Cycles').GetValue()))
	productFamily = row.Product.Attr("CBM_PRODUCT_FAMILY").GetValue()
	Trace.Write('productFamily - '+productFamily)
	assetType = row.Product.Attr("CBM_ASSET_TYPE").GetValue()
	Trace.Write('assetType - '+assetType)
	level = row.Product.Attr("CBM_Level").GetValue()
	Trace.Write('level - '+level)
	count = row.Product.Attr("CBM_COUNT").GetValue()
	Trace.Write('count - '+count)
	cycles = row.Product.Attr("CBM_PM/CBM_Cycles").GetValue()
	Trace.Write('cycles - '+cycles)
	if productFamily is not None and productFamily != "" and assetType is not None and assetType != "":
		getPricingDetails = SqlHelper.GetFirst("select Remote_T_C,Remote_T_NC,Total_Tasks,Remote_TT_C,Remote_TT_NC,STD_Hours_LT from SC_CT_CBM_PRICING where Product_Family = '"+str(productFamily)+"' and Asset_Type = '"+str(assetType)+"'")
	if assetType is None or assetType == "":
		reset_values(Product)
	else:
		resultCalc = pricing_calc(level,getPricingDetails,count,cycles)
		row.Product.Attr("CBM_REMOTE_TIME").AssignValue(resultCalc["RemoteTime"])
		row.Product.Attr("CBM_LOCAL_TIME").AssignValue(resultCalc["LocalTime"])
		row.Product.Attr("CBM_TASK_PERCENTAGE").AssignValue(resultCalc["Tasks"])
		row.Product.Attr("CBM_PER_TIME").AssignValue(resultCalc["PerTime"])
		row.Product.Attr("CBM_REMOTE_TASKS").AssignValue(resultCalc["RemoteTask"])
		row.Product.Attr("CBM_LOCAL_TASKS").AssignValue(resultCalc["LocalTask"])
		row.Product.Attr("CBM_LIST_PRICE_PER_CYCLE").AssignValue(resultCalc["ListPricePerCycle"])
		row.Product.Attr("CBM_ANNUAL_PRICE").AssignValue(resultCalc["AnnualPrice"])
		row.Calculate()"""
#Product.Attr("CBM_HIDDEN_CYCLES").AssignValue(str(Product.Attr("CBM_PM/CBM_Cycles").GetValue()))
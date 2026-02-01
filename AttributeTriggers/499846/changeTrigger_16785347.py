def getFloat(val):
	if val:
		return float(val)
	return 0.0
#CXCPQ-47391 : For WriteIns, list price is calculated based on cost and margin %
skidCon = Product.GetContainerByName("PRODUCTIZED _SKID_BOM")
if skidCon is not None:
    for Vrow in skidCon.Rows:
        if str(Vrow['Type'])=='W' and str(Vrow['Part Number'])!='':
            WriteIn_LP_VAL = SqlHelper.GetFirst("Select * from WriteIn_ListPriceValidation where Product ='{}'".format(str(Vrow["Part Number"])))
            V_GMargin = getFloat(TagParserProduct.ParseString('<* Value(PSkid Grossmargin in Percentage) *>'))
            if V_GMargin>0:
                lv_listPrice=round((getFloat(Vrow.GetColumnByName('Unit Cost').Value) * 100)/(100-V_GMargin),2)
                if WriteIn_LP_VAL is not None:
                    if getFloat(lv_listPrice) > getFloat(WriteIn_LP_VAL.MinimumListPrice) and getFloat(lv_listPrice) <= getFloat(WriteIn_LP_VAL.MaximumListPrice):
                        Vrow.GetColumnByName('Unit List Price').Value=str(lv_listPrice)
                        Vrow["Error Message"] =''
                    else:
                        Vrow.GetColumnByName('Unit List Price').Value=str(0)
                        Vrow["Error Message"] ='<label style="color:red">Calculated WriteIn List Price ' + str(lv_listPrice)+' not in Range.</label>'
                else:
                    Vrow.GetColumnByName('Unit List Price').Value=str(lv_listPrice)
                    Vrow["Error Message"] =''
    ScriptExecutor.Execute('Populate WriteIn Container')
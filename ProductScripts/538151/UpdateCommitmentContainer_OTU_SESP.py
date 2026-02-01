commitment_records = SqlHelper.GetList("select * from SC_COMMT_PRICES")
con =  Product.GetContainerByName('Commitment_OTU_SESP')
for i in commitment_records:
	row = con.AddNewRow(False)
	row['SESP_Commitment_OTU'] = i.Commitment.ToString()
	row['SESP_Prices_OTU'] = i.Price.ToString()
else:
	#serv_prod = SqlHelper.GetFirst("select Entitlement from CT_SC_ENTITLEMENTS_DATA where ServiceProduct = 'OTU'").Entitlement
	serv_prod = 'Software Upgrades'
	sesp_servProd = Product.Attr('SC_Service_Product').GetValue()
	Product.Attr('Service_Product_OTU_SESP').AssignValue(serv_prod)
	Product.Attr('Entitlement_OTU_SESP').AssignValue(serv_prod)
	Product.Attr('Contract_OTU_SESP').AssignValue(sesp_servProd)
	Product.Attr("Service_Product_OTU_SESP").Access = AttributeAccess.ReadOnly
	Product.Attr("Entitlement_OTU_SESP").Access = AttributeAccess.ReadOnly
	Product.Attr("Contract_OTU_SESP").Access = AttributeAccess.ReadOnly
Contract = Quote.GetCustomField("SC_CF_CONTRACTDURYR").Content
Contract_Years = 0
if Contract is not None or Contract != "":
	Contract_Years = Contract.Split(".")[0] if Contract.Split(".")[0] else 0
year_Check = "0"
if int(Contract_Years) == 0:
		pass
elif int(Contract_Years) < 3:
	year_Check = "1"
elif int(Contract_Years) < 5:
	year_Check = "3"
else:
	year_Check = "5"
for row in con.Rows:
	if int(row["SESP_Commitment_OTU"].split("-")[0]) == int(year_Check):
		row.IsSelected = True
	else:
		row.IsSelected = False
import GS_FME_CONFIG_MOD
import datetime

Session["IsHCIUpload"] = ""
items = arg.QuoteItemCollection
for item in items:
    item.Reconfigure()

def assignval(resp,prod):
	for atnm in list(resp):
		a = prod.Attributes.GetBySystemId(str(atnm["atnam"])).DisplayType
		if a == "DropDown":
			prod.Attributes.GetBySystemId(str(atnm["atnam"])).SelectValue(str(atnm["atwtb"]))
		else:
			prod.Attributes.GetBySystemId(str(atnm["atnam"])).AssignValue(str(atnm["atwtb"]))
			Trace.Write("name--->{}val--->{}".format(str(atnm["atnam"]),str(atnm["atwtb"])))
	prod.ApplyRules()
	return prod.IsComplete,prod.TotalPrice

#host = "it.api.honeywell.com"
hostquery = SqlHelper.GetFirst("Select HostName from CT_HOSTNAME where Domain in (select tenant_name from tenant_environments where is_current_environment = 1)")
host = hostquery.HostName
accessTkn = GS_FME_CONFIG_MOD.getAccessToken(host)
FME_Valid_Parts = Product.GetContainerByName("HPS_Valid_Parts")
invalidFME = []
if FME_Valid_Parts.Rows.Count>0:
	index = 0
	cont_length = FME_Valid_Parts.Rows.Count
	Session["prevent_execution"] = "true"
	part_lst = "'" + ("','".join([str(prow["Part Number"]) for prow in FME_Valid_Parts.Rows])) + "'"
	qry =("SELECT product_catalog_code,product_ID,version_number from (SELECT p.product_catalog_code, p.product_ID, pv.version_number, ROW_NUMBER() OVER ( PARTITION BY p.product_catalog_code ORDER BY pv.SAPEffectiveDate DESC, pv.version_number DESC ) AS rn FROM products p LEFT OUTER JOIN product_versions pv ON p.product_id = pv.product_id WHERE p.product_catalog_code IN ({}) AND p.PRODUCT_ACTIVE = 1 AND pv.is_active = 1) RankedProducts WHERE rn = 1".format(str(part_lst)))
	getprdid= SqlHelper.GetList(qry)
	prd_dict = {prd.product_catalog_code: prd.product_ID for prd in getprdid }

	#shortQuery
	fme_list = "'" + ("','".join([str(prow["FME"]) for prow in FME_Valid_Parts.Rows])) + "'"
	shortquery = SqlHelper.GetList("SELECT Short_model_code,Full_model_code FROM PMC_Short_FMC_Mapping WHERE Full_model_code in ({})".format(str(fme_list)))
	fme_dict = {i.Full_model_code : i.Short_model_code for i in shortquery}

	for prow in FME_Valid_Parts.Rows:
		Trace.Write("FME---->"+str(prow["Part Number"]))
		index += 1
		try:
			if prow["Message"]=='<label style="color:green">Valid</label>':
				product_id = prd_dict[prow["Part Number"]]
				prod = ProductHelper.CreateProduct(int(product_id))
				prod.SetGlobal('gv_short_fme','')
				if fme_dict.has_key(str(prow["FME"])):
					prod.SetGlobal('gv_short_fme',str(fme_dict[str(prow["FME"])]))
				prod.SetGlobal('BU_Extended_Desc', '')
				prod.SetGlobal('BU_ACE_Quote_ListPrice', '')
				prod.SetGlobal('BU_ACE_Quote_Cost', '')
				prod.SetGlobal('BU_Extended_Desc', str(prow["ExtendedDescription"]))
				prod.SetGlobal('BU_ACE_Quote_Cost', str(prow["Unit Cost Price"]))
				prod.SetGlobal('BU_ACE_Quote_ListPrice', str(prow["Unit List Price"]))
                #prod.SetGlobal('Yspec_Fme', str(prow["FME"]))

				if not prod.IsComplete:
					jsonConfig = GS_FME_CONFIG_MOD.fme2config(host, accessTkn,str(prow["Part Number"]),str(prow["FME"]))
					assignpart,assigntot = assignval(jsonConfig,prod)
				if prod.IsComplete:
					prod.AddToQuote(int(prow["Quantity"]))
				else:
					invalidFME.append({'Part Number': prow['Part Number'], 'FME': prow['FME']})
		except Exception as e:
			invalidFME.append({'Part Number': prow['Part Number'], 'FME': prow['FME']})
			Log.Info('Error in CPS Connection and moved to invalid parts : ' + str(e))

fme_invalid_tbl = Quote.QuoteTables["HPS_Invalid_Parts"]
if fme_invalid_tbl.Rows.Count:
	fme_invalid_tbl.Rows.Clear()
if invalidFME:
	Trace.Write("invalidFME --> " + str(invalidFME))
	for row in invalidFME:
		new_row = fme_invalid_tbl.AddNewRow()
		#Trace.Write("FME---->"+str(row["FME"]))
		new_row["FME"] = row["FME"]
		new_row["Part_Number"] = row["Part Number"]

PU_Invalid_Parts = Product.GetContainerByName("HPS_PU_Invalid_Parts")
for row in PU_Invalid_Parts.Rows:
	new_row = fme_invalid_tbl.AddNewRow()
	new_row["Part_Number"] = row["Part Number"]
fme_invalid_tbl.Save()
if str(FME_Valid_Parts.Rows.Count) =='1':
    Quote.ExecuteAction(18)
else:
    Quote.ExecuteAction(18)
    ScriptExecutor.Execute('GS_CheckNoPriceProducts')
'''fme_parts ={}
for i in Product.GetContainerByName("HPS_Valid_Parts").Rows:
    if i["FME"]:
        fme_parts[str(i["Part Number"])]=str(i["FME"])
#Trace.Write("-fme_parts->"+str(fme_parts))
for i in Quote.MainItems:
	if fme_parts.get(i.PartNumber):
		i["QI_FME"].Value = str(fme_parts.get(i.PartNumber)) '''
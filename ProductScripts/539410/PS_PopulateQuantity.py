import GS_FME_CONFIG_MOD

def assignval(resp,prod):
	# Log.Info(str(resp))
	for atnm in list(resp):
		a = prod.Attributes.GetBySystemId(str(atnm["atnam"])).DisplayType
		if a == "DropDown":
			prod.Attributes.GetBySystemId(str(atnm["atnam"])).SelectValue(str(atnm["atwtb"]))
		else:
			prod.Attributes.GetBySystemId(str(atnm["atnam"])).AssignValue(str(atnm["atwtb"]))
			Trace.Write("name--->{}val--->{}".format(str(atnm["atnam"]),str(atnm["atwtb"])))
	prod.ApplyRules()
	return prod.IsComplete,prod.TotalPrice

#CXCPQ-39700 - Replaced hardcoded host name : Start
#host = "it.api-beta.honeywell.com"
hostquery = SqlHelper.GetFirst("Select HostName from CT_HOSTNAME where Domain in (select tenant_name from tenant_environments where is_current_environment = 1)")
host = hostquery.HostName
Trace.Write('Host Name:'+hostquery.HostName)
#CXCPQ-39700 - Replaced hardcoded host name : End

accessTkn = GS_FME_CONFIG_MOD.getAccessToken(host)
FME_Valid_Parts = Product.GetContainerByName("FME_Valid_Parts")
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
			product_id = prd_dict[prow["Part Number"]]
			prod = ProductHelper.CreateProduct(int(product_id))
			yspecQuote = dict()
			eto = dict()
			#marine = dict()#CXCPQ-53124: Commented
			j=0
			YSpecial_Suboption = Product.GetContainerByName("YSpecial_Suboption")
			if YSpecial_Suboption.Rows.Count>0:
				for yrow in YSpecial_Suboption.Rows:
					if yrow["ID"] == prow["ID"]:
						if yrow["ETO_Marine_Yspec"] == "Yspecial":
							j+=1
							yspecQuote[j] = {"yspecRef" : yrow["YSpecial_Quote_Ref"], "yspecSubopt" : yrow["YSpecial_Suboption"]}
						if yrow["ETO_Marine_Yspec"] == "ETO":
							j+=1
							eto[j] = {"Eto_ref" : yrow["YSpecial_Quote_Ref"], "proposal_notes" : yrow["ETO proposal notes"], "production_notes" : yrow["ETO production notes"], "manufacturing_notes" : yrow["ETO manufacturing notes"], "net_price" : yrow["ETO Nett Price"]}
						#CXCPQ-53124:Start: Earlier there are two seperate quote tables for Gas and Marine ETO and now with this story it merged into one.
						''''if yrow["ETO_Marine_Yspec"] == "YspecMarine": 
							j+=1
							marine[j] = {"yspecmarine_ref" : yrow["YSpecial_Quote_Ref"], "proposal_notes" : yrow["ETO proposal notes"], "production_notes" : yrow["ETO production notes"], "manufacturing_notes" : yrow["ETO manufacturing notes"], "net_price" : yrow["ETO Nett Price"]}''' #CXCPQ-53124:End
			Trace.Write("yspecQuote----->"+str(yspecQuote))
			prod.SetGlobal('BU_Yspecial', str(yspecQuote))
			prod.SetGlobal('BU_ETO', str(eto))
			#prod.SetGlobal('BU_Marine', str(marine)) #CXCPQ-53124: Commented
			#Below global parameters are used in GS_PopulateFME Global script
			prod.SetGlobal('gv_short_fme','')
			if fme_dict.has_key(str(prow["FME"])):
				prod.SetGlobal('gv_short_fme',str(fme_dict[str(prow["FME"])]))
			prod.SetGlobal('BU_Extended_Desc', '')
			prod.SetGlobal('BU_ACE_Quote_Ref', '')
			prod.SetGlobal('BU_ACE_Quote_Desc', '')
			prod.SetGlobal('BU_ACE_Quote_ListPrice', '')
			prod.SetGlobal('BU_ACE_Quote_Cost', '')
			if prow["FME"][0].upper() == "Y":
				prod.Attributes.GetBySystemId("V_SPECIAL_OPTIONS").SelectValue("Y")
				#Log.Info("V_RMK_SPECIAL_LABOR_HOURS:" + str (prod.Attributes.GetBySystemId("V_RMK_SPECIAL_LABOR_HOURS").Required))
				prod.SetGlobal('Yspec_Fme', prow["FME"].upper())
				if prow["Labor Hours"]:
					if prod.Attributes.GetBySystemId("V_RMK_SPECIAL_LABOR_HOURS"):
						prod.Attributes.GetBySystemId("V_RMK_SPECIAL_LABOR_HOURS").AssignValue(str(prow("Labor Hours")))
				else:
					if prod.Attributes.GetBySystemId("V_RMK_SPECIAL_LABOR_HOURS"):
						prod.Attributes.GetBySystemId("V_RMK_SPECIAL_LABOR_HOURS").AssignValue("0")
				prod.SetGlobal('BU_AdderTotalETO',str({"adder":prow["AdderTotalETO"], "listprice":prow["Unit List Price"], "cost":prow["Unit Cost Price"]}))
			else:
				if str(prod.GetGlobal('Yspec_Fme')) != "":
					prod.SetGlobal('Yspec_Fme', '')
			prod.SetGlobal('BU_Extended_Desc', str(prow["ExtendedDescription"]))
			prod.SetGlobal('BU_ACE_Quote_Ref', str(prow["Ace Quote Reference Number"]))
			prod.SetGlobal('BU_ACE_Quote_Desc', str(prow["Ace Quote Description"]))
			prod.SetGlobal('BU_ACE_Quote_Cost', str(prow["Unit Cost Price"]))
			if str(prow["Ace Quote Reference Number"])!='':
				prod.SetGlobal('BU_ACE_Quote_ListPrice', str(prow["Unit List Price"]))

			if not prod.IsComplete:
				jsonConfig = GS_FME_CONFIG_MOD.fme2config(host, accessTkn,str(prow["Part Number"]),str(prow["FME"]))
				assignpart,assigntot = assignval(jsonConfig,prod)
			if prod.IsComplete:
				prod.AddToQuote(int(prow["Quantity"]))
			else:
				#invalidFME.append('Part Number: {}; FME: {}'.format(prow['Part Number'], prow['FME']))
				invalidFME.append({'Part Number': prow['Part Number'], 'FME': prow['FME']})
		except Exception as e:
			#invalidFME.append('Part Number: {}; FME: {}; '.format(prow['Part Number'], prow['FME']))
			invalidFME.append({'Part Number': prow['Part Number'], 'FME': prow['FME']})
			Log.Info('Error in CPS Connection and moved to invalid parts : ' + str(e))

fme_invalid_tbl = Quote.QuoteTables["FME_Invalid_Parts"]
if fme_invalid_tbl.Rows.Count:
	fme_invalid_tbl.Rows.Clear()
if invalidFME:
	# message = 'Below product configurations are incomplete and are not added to the quote. Please review and proceed.<br>'
	# message += '<br>'.join(invalidFME)
	# Quote.Messages.Add(message)
	Trace.Write("invalidFME --> " + str(invalidFME))
	for row in invalidFME:
		new_row = fme_invalid_tbl.AddNewRow()
		#Trace.Write("FME---->"+str(row["FME"]))
		new_row["FME"] = row["FME"]
		new_row["Part_Number"] = row["Part Number"]

PU_Invalid_Parts = Product.GetContainerByName("PU_Invalid_Parts")
for row in PU_Invalid_Parts.Rows:
	new_row = fme_invalid_tbl.AddNewRow()
	new_row["Part_Number"] = row["Part Number"]
fme_invalid_tbl.Save()
Quote.Calculate()
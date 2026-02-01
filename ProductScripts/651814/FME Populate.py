import GS_FME_CONFIG_MOD

def assignval(resp,prod):
	# Log.Info(str(resp))
	for atnm in list(resp):
		a = prod.Attributes.GetBySystemId(str(atnm["atnam"])).DisplayType
		if a == "DropDown":
			prod.Attributes.GetBySystemId(str(atnm["atnam"])).SelectValue(str(atnm["atwtb"]))
		else:
			prod.Attributes.GetBySystemId(str(atnm["atnam"])).AssignValue(str(atnm["atwtb"]))
			#Trace.Write("name--->{}val--->{}".format(str(atnm["atnam"]),str(atnm["atwtb"])))
	prod.ApplyRules()
	return prod.IsComplete,prod.TotalPrice

def delete_items(parts):
	for i in Quote.MainItems:
		if i.PartNumber==parts:
			i.Delete()
if (Quote.GetCustomField('R2Q_Save').Content == 'Submit' and Quote.GetCustomField('IsR2QRequest').Content == 'Yes') or Quote.GetCustomField('IsR2QRequest').Content != 'Yes':
    hostquery = SqlHelper.GetFirst("Select HostName from CT_HOSTNAME where Domain in (select tenant_name from tenant_environments where is_current_environment = 1)")
    host = hostquery.HostName
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
            Trace.Write(str(prow["Part Number"])+"<--FME--check123-->"+str(prd_dict))
            index += 1
            try:
                product_id = prd_dict[prow["Part Number"]]
                #if prow["Part Number"] == "AS-PHDAS":
                #	product_id = "16837"
                Trace.Write(str(prow["Part Number"])+"---product_id-recheck-->"+str(product_id))
                prod = ProductHelper.CreateProduct(int(product_id))
                #prod.SetGlobal('gv_short_fme',str(prow["FME"]))
                no_of_configuration = Product.Attr("Number_Of_Configurations_EDM").GetValue()
                prod.SetGlobal('gv_short_fme','')
                if fme_dict.has_key(str(prow["FME"])):
                    prod.SetGlobal('gv_short_fme',str(fme_dict[str(prow["FME"])]))
                prod.SetGlobal('BU_Extended_Desc', '')
                prod.SetGlobal('BU_ACE_Quote_Ref', '')
                prod.SetGlobal('BU_ACE_Quote_Desc', '')
                prod.SetGlobal('BU_ACE_Quote_ListPrice', '')
                prod.SetGlobal('BU_ACE_Quote_Cost', '')
                prod.SetGlobal('no_of_configuration', '')
                if prow["FME"][0].upper() == "Y":
                    prod.Attributes.GetBySystemId("V_SPECIAL_OPTIONS").SelectValue("Y")
                    #Log.Info("V_RMK_SPECIAL_LABOR_HOURS:" + str (prod.Attributes.GetBySystemId("V_RMK_SPECIAL_LABOR_HOURS").Required))
                    prod.SetGlobal('Yspec_Fme', prow["FME"].upper())
                #prod.Attributes.GetBySystemId("V_RMK_SPECIAL_LABOR_HOURS").AssignValue(0)
                else:
                    if str(prod.GetGlobal('Yspec_Fme')) != "":
                        prod.SetGlobal('Yspec_Fme', '')
                prod.SetGlobal('BU_Extended_Desc', str(prow["ExtendedDescription"]))
                prod.SetGlobal('BU_ACE_Quote_Ref', str(prow["Ace Quote Reference Number"]))
                prod.SetGlobal('BU_ACE_Quote_Desc', str(prow["Ace Quote Description"]))
                prod.SetGlobal('BU_ACE_Quote_Cost', str(prow["Unit Cost Price"]))
                prod.SetGlobal('no_of_configuration', str(no_of_configuration))
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
                Log.Info("Error in CPS Connection and moved to invalid parts "+str(prow['Part Number'])+" : "+ str(e))
                Log.Info("--Recheck-->"+str(prd_dict))

    '''fme_parts ={}
    for i in Product.GetContainerByName("HCI_PHD_PartSummary_Cont").Rows:
        if i["fme"]:
            fme_parts[str(i["PartNumber"])]=str(i["fme"])
    #Trace.Write("-fme_parts->"+str(fme_parts))
    for i in Quote.MainItems:
        if fme_parts.get(i.PartNumber):
            i["QI_FME"].Value = str(fme_parts.get(i.PartNumber))
            #Trace.Write(str(i.PartNumber)+"--QI_FME-->"+str(i["QI_FME"].Value)) '''

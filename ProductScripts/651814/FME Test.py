import GS_FME_CONFIG_MOD

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

hostquery = SqlHelper.GetFirst("Select HostName from CT_HOSTNAME where Domain in (select tenant_name from tenant_environments where is_current_environment = 1)")
host = hostquery.HostName
#if (Quote.GetCustomField('R2Q_Save').Content == 'Submit' and Quote.GetCustomField('IsR2QRequest').Content == 'Yes') or Quote.GetCustomField('IsR2QRequest').Content != 'Yes':
fme='AS-PHDAS-N-S-N-N-N-N-N-Y-H-N-N-N-N-N-0-00-00-00-00-0000-P-001-000000-000000'
#fme='STG73S-F1G000-1-C-BHS-13C-B-01A7-F1,FE-0000'
partno='AS-PHDAS'
#partno='STG73S'
accessTkn = GS_FME_CONFIG_MOD.getAccessToken(host)
jsonConfig = GS_FME_CONFIG_MOD.fme2config(host, accessTkn,str(partno),str(fme))
assignpart,assigntot = assignval(jsonConfig,Product)
Trace.Write(str(assignpart)+"--finall-->"+str(assigntot))


    # obj = GS_HPS_Product_Bulk_Upload.bulk_product_upload(Quote, Product, TagParserQuote, Workbook)
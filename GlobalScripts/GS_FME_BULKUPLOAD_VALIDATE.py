import GS_FME_CONFIG_MOD


def assignval(resp,prod):
	for atnm in list(resp):
		Trace.Write("name--->{}val--->{}".format(str(atnm["atnam"]),str(atnm["atwtb"])))
		a = prod.Attributes.GetBySystemId(str(atnm["atnam"])).DisplayType
		if a == "DropDown":
			prod.Attributes.GetBySystemId(str(atnm["atnam"])).SelectValue(str(atnm["atwtb"]))
		elif a == "Free Input, no Matching":
			prod.Attributes.GetBySystemId(str(atnm["atnam"])).AssignValue(str(atnm["atwtb"]))
		else:
			prod.Attributes.GetBySystemId(str(atnm["atnam"])).AssignValue(str(atnm["atwtb"]))
			Trace.Write("name--->{}val--->{}".format(str(atnm["atnam"]),str(atnm["atwtb"])))
	prod.ApplyRules()
	return prod.IsComplete,prod.TotalPrice


#CXCPQ-39700 - Replaced hardcoded host name : Start
hostquery = SqlHelper.GetFirst("Select HostName from CT_HOSTNAME where Domain in (select tenant_name from tenant_environments where is_current_environment = 1)")
host = hostquery.HostName
Trace.Write('Host Name:'+hostquery.HostName)
#CXCPQ-39700 - Replaced hardcoded host name : End

accessTkn = GS_FME_CONFIG_MOD.getAccessToken(host)

FME_Valid_Parts = Product.GetContainerByName("FME_Valid_Parts")
if FME_Valid_Parts.Rows.Count>0:
	for prow in FME_Valid_Parts.Rows:
		Trace.Write("FME---->"+str(prow["FME"]))
		getprdid = SqlHelper.GetFirst("SELECT top 1 p.product_ID from products p LEFT OUTER JOIN product_versions pv on p.product_id=pv.product_id where p.product_catalog_code= '{}' and p.PRODUCT_ACTIVE = 1 and pv.is_active = 1 order by pv.SAPEffectiveDate desc, pv.version_number desc".format(str(prow["Part Number"])))
		try:
			Trace.Write("In try FME---->"+str(prow["FME"]))
			Trace.Write("In try prow FME---->"+str(getprdid.product_ID))
			prod = ProductHelper.CreateProduct(int(getprdid.product_ID))
			Trace.Write("In try 2---->")
			jsonConfig = GS_FME_CONFIG_MOD.fme2config(host, accessTkn,str(prow["Part Number"]),str(prow["FME"]))
			Trace.Write("In try 3---->")
			assignpart,assigntot = assignval(jsonConfig,prod)
            #CXCPQ-44060: Setting Labor hours as zero
			if prod.Attributes.GetBySystemId("V_RMK_SPECIAL_LABOR_HOURS") is not None:
				prod.Attributes.GetBySystemId("V_RMK_SPECIAL_LABOR_HOURS").AssignValue("0")
			Trace.Write("assignpart---->"+str(assignpart))
			Trace.Write("assigntot---->"+str(assigntot))
		except Exception as e:
			#Trace.Write("Error--->:"+str(sys.exc_info()[1]))
			#Trace.Write("Error Line No--->:"+str(sys.exc_info()[-1].tb_lineno))
			Trace.Write("Error Detail--->:"+str(e))
			assignpart = None
			assigntot = 0
		if prow["Ace Quote Reference Number"]=='':
			prow["Unit List Price"]=str(assigntot)
		if assignpart:
			prow["Message"] = '<label style="color:green">Valid</label>'
		else:
			prow["Message"] = '<label style="color:red">InValid</label>'
#prod.AddToQuote(2)
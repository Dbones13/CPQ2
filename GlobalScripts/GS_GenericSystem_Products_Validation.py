import GS_FME_CONFIG_MOD

def getExgRate():
    cur_code = Quote.SelectedMarket.CurrencyCode
    rate = SqlHelper.GetFirst("SELECT Exchange_Rate FROM CURRENCY_EXCHANGERATE_MAPPING WHERE From_Currency = 'USD' AND To_Currency = '{}'".format(cur_code))
    if rate is not None:
        rate_amt = rate.Exchange_Rate
    else:
        rate_amt = 1
    return rate_amt

def assignval(resp,prod):
	Log.Info(str(resp))
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

lv_Generic_Parts_Con = Product.GetContainerByName("Generic_System_Part_Upload_Cont")
lv_Generic_yspec_Con = Product.GetContainerByName("Generic_BOM_YSpecial_Suboption")
if Quote.GetCustomField('Sales Area').Content == "1109":
    yspectable = "YSpecial_US"
else:
    yspectable = "YSpecial"

if lv_Generic_Parts_Con.Rows.Count>0:
    for prow in lv_Generic_Parts_Con.Rows:
        getprdid = SqlHelper.GetFirst("SELECT top 1 p.product_ID,p.IsSimple from products p LEFT OUTER JOIN product_versions pv on p.product_id=pv.product_id where p.product_catalog_code= '{}' and p.PRODUCT_ACTIVE = 1 and pv.is_active = 1 order by pv.SAPEffectiveDate desc, pv.version_number desc".format(str(prow["Part Number"])))
        if prow["FME"]!='':
            try:
                prod = ProductHelper.CreateProduct(int(getprdid.product_ID))
                jsonConfig = GS_FME_CONFIG_MOD.fme2config(host, accessTkn,str(prow["Part Number"]),str(prow["FME"]))
                assignpart,assigntot = assignval(jsonConfig,prod)
                Trace.Write("assignpart---->"+str(assignpart))
                Trace.Write("assigntot---->"+str(assigntot))
            except Exception as e:
                Trace.Write("Error Detail--->:"+str(e))
                prow["Message"] = '<label style="color:red">Error while Validating FME</label>'
                prow["FME_Error_Message"] = 'Error while Validating FME Configuration.'
                assignpart = None
                assigntot = 0
            if prow["Ace Quote Reference Number"]=='':
                prow["Unit List Price"]=str(assigntot)
            if assignpart:
                if lv_Generic_yspec_Con.Rows.Count>0:
                    prow["Message"] = '<label style="color:green">Valid</label>'
                    prow["FME_Error_Message"] = ''
                    prow["Valid_Part_ID"]=prow["ID"]
                    for yrow in lv_Generic_yspec_Con.Rows:
                        if yrow["ID"]==prow["ID"]:
                            ys_query = SqlHelper.GetFirst("Select Yspecial_Quote, Sub_Option,LP_Part from {} where Part_Number = '{}' and Yspecial_Quote ='{}' and Sub_Option='{}'".format(str(yspectable),str(prow["Part Number"]),str(yrow["YSpecial_Quote_Ref"]),str(yrow["YSpecial_Suboption"])))
                            if ys_query:
                                prow["Message"] = '<label style="color:green">Valid</label>'
                                prow["Valid_Part_ID"]=prow["ID"]
                                prow["FME_Error_Message"] = ''
                                ExRate=getExgRate()
                                Yspec_model_price = float(assigntot)+(float(ys_query.LP_Part)*float(ExRate))
                                prow["Unit List Price"]=str(Yspec_model_price)
                            else:
                                prow["Message"] = '<label style="color:red">InValid Yspec Reference</label>'
                                prow["Valid_Part_ID"]=''
                                prow["FME_Error_Message"] = 'InValid FME and Yspecial.Please correct.'
                                break
                else:
                    prow["Message"] = '<label style="color:green">Valid</label>'
                    prow["Valid_Part_ID"]=prow["ID"]
                    prow["FME_Error_Message"] = ''
            else:
                prow["Message"] = '<label style="color:red">InValid FME Configuration</label>'
                prow["FME_Error_Message"] = 'InValid FME Configuration.Please correct.'
                prow["Valid_Part_ID"]=''
        else:
            try:
                if getprdid is not None:
                    if getprdid.IsSimple == True:
                        Trace.Write("Simple product----->")
                        prow["Message"] = '<label style="color:green">Valid</label>'
                        prow["Valid_Part_ID"]=prow["ID"]
                        prow["FME_Error_Message"] = ''
                    else:
                        prow["Message"] = '<label style="color:red">InValid Part Number</label>'
                        prow["Valid_Part_ID"]=''
                        prow["FME_Error_Message"] = 'InValid Part Number.Please correct.'
                        

                else:
                    prow["Message"] = '<label style="color:red">Part Number Not found</label>'
                    prow["Valid_Part_ID"]=''
                    prow["FME_Error_Message"] = 'InValid Part Number.Please correct.'

            except Exception as e:
                prow["Message"] = '<label style="color:red">Error while validating Part Number</label>'
                prow["Valid_Part_ID"]=''
                prow["FME_Error_Message"] = 'Error while Validating Part Number.'
import GS_FME_CONFIG_MOD

prd = Param.PartNumber
yspec_qt=Param.PartNumber

def getfmeval(prd):
    #CXCPQ-39700 - Replaced hardcoded host name : Start
	#hostquery = SqlHelper.GetFirst("Select HostName from CT_HOSTNAME where Domain in (select tenant_name from tenant_environments where is_current_environment = 1)")
	host = "it.api-beta.honeywell.com"
	#host = hostquery.HostName
	#Trace.Write('Host Name:'+hostquery.HostName)
	#CXCPQ-39700 - Replaced hardcoded host name : End
	accessTkn = GS_FME_CONFIG_MOD.getAccessToken(host)

	jsonConfig = GS_FME_CONFIG_MOD.config2fme(host, accessTkn,prd)

	fmeval = ""
	keynum = ""
	ordrval = {}
	yspec = ""

	for attnm in list(jsonConfig):
		for attr in Product.Attributes:
			attname  = attr.Name
			attSystemId  = attr.SystemId
			if attSystemId == "V_SPECIAL_OPTIONS":
				for attval in attr.SelectedValues:
					yspec =  attval.Display
					break
			if attSystemId == str(attnm["charAttr"]):

				if "KEY_NUMBER" in str(attnm["charAttr"]):
					for value in attr.Values:
						#Trace.Write("attr--->"+str(value.Display))
						keynum =  str(value.Display)
						ordrval[str(attnm["charClassValue"])] = str(value.Display)
				else:
					for value in attr.Values:
						Trace.Write("attr--->"+str(value.Display))
						ordrval[str(attnm["charClassValue"])] = str(value.Display)
						fmeval +=  str(value.Display)
	if fmeval != "" and keynum != "":
		fmeval = keynum + fmeval
	fmeval = ""

	for k, v in sorted(ordrval.items()):
		fmeval += v
	if yspec  == "Yes":
		fmeval = "Y" + fmeval


	return fmeval

yspec=''
for attr in Product.Attributes:
	attname  = attr.Name
	attSystemId  = attr.SystemId
	if attSystemId == "V_SPECIAL_OPTIONS":
		for attval in attr.SelectedValues:
			yspec =  attval.Display
			break
itemFMEValue=""
lv_fme=""
lv_short_fme=""
if Quote and (Quote.GetCustomField('Booking LOB').Content == "PMC" or Quote.GetCustomField('Booking LOB').Content == "HCP"):

	qry = SqlHelper.GetFirst("SELECT 1 as flag from FME_PARTS WHERE PARTNUMBER = '{}'".format(str(prd)))
	if qry is not None:
		itemFMEValue = getfmeval(prd)
		if itemFMEValue: # Added if to avoid index out of range error
			if itemFMEValue[0] != 'Y':
				lv_fme=itemFMEValue
			else:
				lv_fme = itemFMEValue[1:]
		Trace.Write('getfmeval fmevalue:'+itemFMEValue)
	else:
		query = "select TOP 10 STANDARD_ATTRIBUTE_NAME from FME_ATTRIBUTE_ORDER fao join ATTRIBUTE_DEFN ad on fao.Attribute = ad.SYSTEM_ID where Material = '{}' order by ATTRIBUTE_Order asc".format(prd)
		res = SqlHelper.GetList(query)

		fme = ''
		attrDict = dict()

		for attr in Product.Attributes:
			for value in attr.Values:
				attrDict[attr.Name]= value.Display

		for attr in res:
			fme = '{}{}'.format(fme , attrDict[attr.STANDARD_ATTRIBUTE_NAME])
		if yspec == "Yes":
			itemFMEValue = "Y" + fme
			lv_fme=fme
		else:
			itemFMEValue = fme
			lv_fme=fme
		Trace.Write('full fme:'+fme)
	if lv_fme != '':
		if str(TagParserProduct.ParseString("<*CTX( Quote.CurrentItem.CustomField(QI_Short_FME_Code) )*>"))!='' and str(TagParserProduct.ParseString("<*CTX( Quote.CurrentItem.CustomField(QI_FME) )*>"))==itemFMEValue:
            #Below logic to send the short fme code from quote to configurator 
			lv_short_fme =str(TagParserProduct.ParseString("<*CTX( Quote.CurrentItem.CustomField(QI_Short_FME_Code) )*>"))
		else:
			res_smodel = SqlHelper.GetFirst("Select Short_model_code FROM PMC_Short_FMC_Mapping WHERE Full_model_code = '{}'".format(lv_fme))
			if res_smodel is not None:
				lv_short_fme = res_smodel.Short_model_code

	Trace.Write('short fme:'+lv_short_fme)
ret_val=[itemFMEValue,lv_short_fme]
ApiResponse = ApiResponseFactory.JsonResponse(ret_val)
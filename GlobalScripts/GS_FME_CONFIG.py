import GS_FME_CONFIG_MOD
fmeinput = Param.fmeinput

def assignval(resp):
    Log.Info(str(resp))
    for atnm in list(resp):
        Log.Info("name--->{}val--->{}===>{}".format(str(atnm["atnam"]),str(atnm["atwtb"]),str(dir(atnm["atnam"]))))
        a = Product.Attributes.GetBySystemId(str(atnm["atnam"])).DisplayType
        if a == "DropDown":
            Product.Attributes.GetBySystemId(str(atnm["atnam"])).SelectValue(str(atnm["atwtb"]))
        elif a == "Free Input, no Matching":
            Product.Attributes.GetBySystemId(str(atnm["atnam"])).AssignValue(str(atnm["atwtb"]))
        else:
            Product.Attributes.GetBySystemId(str(atnm["atnam"])).AssignValue(str(atnm["atwtb"]))
            Trace.Write("name--->{}val--->{}".format(str(atnm["atnam"]),str(atnm["atwtb"])))
    Product.ApplyRules()
#CXCPQ-39700 - Replaced hardcoded host name : Start
host = "it.api-beta.honeywell.com"
#hostquery = SqlHelper.GetFirst("Select HostName from CT_HOSTNAME where Domain in (select tenant_name from tenant_environments where is_current_environment = 1)")
#host = hostquery.HostName
#Trace.Write('Host Name:'+hostquery.HostName)
#CXCPQ-39700 - Replaced hardcoded host name : End

accessTkn = GS_FME_CONFIG_MOD.getAccessToken(host)
try:
    for i in Product.Attributes:
        if i.SystemId == "V_SPECIAL_OPTIONS":
            if fmeinput[0].upper() == "Y":
                Product.Attributes.GetBySystemId("V_SPECIAL_OPTIONS").SelectValue("Y")
                Quote.SetGlobal('Yspec_Fme', fmeinput.upper())
            else:
                Product.Attributes.GetBySystemId("V_SPECIAL_OPTIONS").SelectValue("N")
                if str(Quote.GetGlobal('Yspec_Fme')) != "":
                    Quote.SetGlobal('Yspec_Fme', '')
    Log.Info("fmeinput---{}---pn----{}".format(fmeinput,Product.PartNumber))
    jsonConfig = GS_FME_CONFIG_MOD.fme2config(host, accessTkn,Product.PartNumber,fmeinput)#fmeinput.split("-")[0],fmeinput)
    Log.Info("jsonConfig---{}---".format(jsonConfig))
except Exception as e:
    Product.ErrorMessages.Add('Please enter valid FME Code')
    jsonconfig=''
assignpart = assignval(jsonConfig)

ApiResponse = ApiResponseFactory.JsonResponse(str(jsonConfig))
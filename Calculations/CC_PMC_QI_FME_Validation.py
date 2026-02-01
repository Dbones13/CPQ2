
if Quote.GetCustomField('Booking LOB').Content == "PMC" and Item.IsFieldModified("QI_FME") and Item.PartNumber in Item.QI_FME.Value:
    import clr
    from System.Net import HttpWebRequest
    clr.AddReference("System.Xml")
    import sys
    from math import ceil
    from System.Text import Encoding
    import GS_FME_CONFIG_MOD
    Trace.Write('In CC_PMC_QI_FME_Validation')
    
    def assignval(resp,prod):
        Trace.Write(str(resp))
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
    #host = "it.api-beta.honeywell.com"
    try:
        hostquery = SqlHelper.GetFirst("Select HostName from CT_HOSTNAME where Domain in (select tenant_name from tenant_environments where is_current_environment = 1)")
        host = hostquery.HostName
        #CXCPQ-39700 - Replaced hardcoded host name : End
        accessTkn = GS_FME_CONFIG_MOD.getAccessToken(host)
        Trace.Write('In CC_PMC_QI_FME_Validation - In PMC:' + str(Item.PartNumber) + ':' +str(Item.QI_FME.Value))
        #Below logic checks whether entered FME code is valid or not
        Trace.Write('beforeJson')
        jsonConfig = GS_FME_CONFIG_MOD.fme2config(host, accessTkn,str(Item.PartNumber),str(Item.QI_FME.Value))
        Log.Write('json'+str(jsonConfig))
        getprdid = SqlHelper.GetFirst("SELECT top 1 p.product_ID from products p LEFT OUTER JOIN product_versions pv on p.product_id=pv.product_id where p.product_catalog_code= '{}' and p.PRODUCT_ACTIVE = 1 and pv.is_active = 1 order by pv.SAPEffectiveDate desc, pv.version_number desc".format(str(Item.PartNumber)))
        prod = ProductHelper.CreateProduct(int(getprdid.product_ID))
        assignpart,assigntot = assignval(jsonConfig,prod)
        Trace.Write("assignpart---->"+str(assignpart))
        Trace.Write("assigntot---->"+str(assigntot))
        if str(assignpart)=='True':
            Trace.Write("before GS_UpdateFME")
            Quote.SetGlobal('GV_QuoteItemGuid', Item.QuoteItemGuid)
            Quote.SetGlobal('GV_FMEValue', Item.QI_FME.Value)
            ScriptExecutor.ExecuteGlobal('GS_UpdateFME')
            Quote.SetGlobal('GV_QuoteItemGuid', '')
            Quote.SetGlobal('GV_FMEValue', '')
        else:
            Message = ''
            Message = 'Modified FME value is not Valid.:'+ Item.PartNumber +': Item Number:'+str(Item.RolledUpQuoteItem)
            if not Quote.Messages.Contains(Message):
                Quote.Messages.Add(Message)
    except:
        Message = ''
        Message = 'Modified FME value is not Valid.:'+ Item.PartNumber +': Item Number:'+str(Item.RolledUpQuoteItem)
        if not Quote.Messages.Contains(Message):
            Quote.Messages.Add(Message)

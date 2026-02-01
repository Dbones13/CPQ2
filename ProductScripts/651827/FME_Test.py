import GS_FME_CONFIG_MOD
pn = SqlHelper.GetFirst("Select PLANT_NAME from COUNTRY_SORG_PLANT_MAPPING(NOLOCK) where PLANT_CODE = '6649' ORDER BY CpqTableEntryId DESC")
Quote.GetCustomField("CF_Plant").Content = str(pn.PLANT_NAME)

def getPrdId(prdPartNum):
    datefilter='GETDATE()'
    prd=tuple([prdPartNum])
    prd=str(prd).replace(',','')
    productData="SELECT pv.SAPKBId as kbId,p.PRODUCT_ID as Id, p.PRODUCT_CATALOG_CODE as prodCode, (case when p.IsSimple='TRUE' then 'Yes' else 'No' end) as IsSimple,(CASE WHEN p.ConfigurationType = 0 THEN 'STANDARD' WHEN p.ConfigurationType = 1 THEN 'Variant' WHEN p.ConfigurationType = 2 THEN 'External' END) as ConfigurationType, p.product_name as Name, isnull(p.PRODUCT_CATALOG_CODE, '') as PartNumber FROM products p LEFT OUTER JOIN product_versions pv on p.product_id=pv.product_id WHERE p.PRODUCT_ACTIVE=1 AND (p.IsSyncedFromBackOffice = 0 OR ( p.IsSyncedFromBackOffice = 1 and pv.SAPEffectiveDate is null) OR (p.IsSyncedFromBackOffice = 1 AND pv.SAPEffectiveDate is not null AND pv.SAPEffectiveDate <= {1} AND pv.id = (select top 1 t1.id from product_versions t1 where t1.product_system_id = pv.product_system_id and t1.is_active = 1 and ((t1.IsRootItem=1 and (p.ConfigurationType=1 or p.ConfigurationType=2)) or p.ConfigurationType=0 or p.IsSimple=1) and t1.SAPEffectiveDate <= {1} order by SAPEffectiveDate desc, version_number desc))) and p.PRODUCT_CATALOG_CODE in {0}".format(prd,datefilter)
    prdID=SqlHelper.GetFirst(productData)
    return prdID

def assignval(resp,prod):
    for atnm in list(resp):
        a = prod.Attributes.GetBySystemId(str(atnm["atnam"])).DisplayType
        if a == "DropDown":
            prod.Attributes.GetBySystemId(str(atnm["atnam"])).SelectValue(str(atnm["atwtb"]))
        else:
            prod.Attributes.GetBySystemId(str(atnm["atnam"])).AssignValue(str(atnm["atwtb"]))
    prod.ApplyRules()
    return prod.IsComplete,prod.TotalPrice

if 1==1:
    hostquery = SqlHelper.GetFirst("Select HostName from CT_HOSTNAME where Domain in (select tenant_name from tenant_environments where is_current_environment = 1)")
    host = hostquery.HostName
    accessTkn = GS_FME_CONFIG_MOD.getAccessToken(host)
    Session["prevent_execution"] = "true"
    k1='AS-PHDAS'
    v1='AS-PHDAS-N-S-N-N-N-Y-N-N-N-N-H-N-N-N-0-00-00-00-00-0000-P-001-000000-000000'
    product_id=getPrdId(k1)
    try:
        Log.Info(str()+"---femtest---111--"+str(product_id.Id))
        prod = ProductHelper.CreateProduct(product_id.Id)
        if not prod.IsComplete:
            jsonConfig = GS_FME_CONFIG_MOD.fme2config(host, accessTkn,str(k1),str(v1))
            assignpart,assigntot = assignval(jsonConfig,prod)
        if prod.IsComplete:
            qty =1
            prod.AddToQuote(qty)
    except Exception as e:
        Log.Info("femtest--222-HCI_PHD_PartSummary_Cont--Error in CPS Connection and moved to invalid parts "+str(k1)+" : "+ str(e))

#Quote.Save(True)
#for i in Quote.MainItems:
#	i['QI_Plant'].Value = str(pn.PLANT_NAME)
Quote.ExecuteAction(3225)
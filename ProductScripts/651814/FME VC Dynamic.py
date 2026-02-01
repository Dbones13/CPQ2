import GS_FME_CONFIG_MOD

def getPrdId(prdPartNum):
    datefilter='GETDATE()'
    prd=tuple([prdPartNum])
    prd=str(prd).replace(',','')
    productData="SELECT pv.SAPKBId as kbId,p.PRODUCT_ID as Id, p.PRODUCT_CATALOG_CODE as prodCode, (case when p.IsSimple='TRUE' then 'Yes' else 'No' end) as IsSimple,(CASE WHEN p.ConfigurationType = 0 THEN 'STANDARD' WHEN p.ConfigurationType = 1 THEN 'Variant' WHEN p.ConfigurationType = 2 THEN 'External' END) as ConfigurationType, p.product_name as Name, isnull(p.PRODUCT_CATALOG_CODE, '') as PartNumber FROM products p LEFT OUTER JOIN product_versions pv on p.product_id=pv.product_id WHERE p.PRODUCT_ACTIVE=1 AND (p.IsSyncedFromBackOffice = 0 OR ( p.IsSyncedFromBackOffice = 1 and pv.SAPEffectiveDate is null) OR (p.IsSyncedFromBackOffice = 1 AND pv.SAPEffectiveDate is not null AND pv.SAPEffectiveDate <= {1} AND pv.id = (select top 1 t1.id from product_versions t1 where t1.product_system_id = pv.product_system_id and t1.is_active = 1 and ((t1.IsRootItem=1 and (p.ConfigurationType=1 or p.ConfigurationType=2)) or p.ConfigurationType=0 or p.IsSimple=1) and t1.SAPEffectiveDate <= {1} order by SAPEffectiveDate desc, version_number desc))) and p.PRODUCT_CATALOG_CODE in {0}".format(prd,datefilter)
    prdID=SqlHelper.GetFirst(productData)
    return prdID
if (Quote.GetCustomField('R2Q_Save').Content == 'Submit' and Quote.GetCustomField('IsR2QRequest').Content == 'Yes') or Quote.GetCustomField('IsR2QRequest').Content != 'Yes':
    fme_parts ={}
    hostquery = SqlHelper.GetFirst("Select HostName from CT_HOSTNAME where Domain in (select tenant_name from tenant_environments where is_current_environment = 1)")
    host = hostquery.HostName
    accessTkn = GS_FME_CONFIG_MOD.getAccessToken(host)
    for i in Product.GetContainerByName("HCI_PHD_PartSummary_Cont").Rows:
        if i["fme"]:
            fme_parts[str(i["PartNumber"])]=str(i["fme"])
            part_num = str(i["PartNumber"])
            fme_val = str(i["fme"])
            prdID=getPrdId(part_num)

            jsonConfig = GS_FME_CONFIG_MOD.fme2config(host, accessTkn,part_num,fme_val)
            config_lst = []
            for i in jsonConfig:
                #Trace.Write(str(i.atnam) + " : " + str(i.atwtb))
                config_lst.append({"id":str(i.atnam), "values":[{"value":str(i.atwtb),"selected":True}]})

            url="https://cpqtesthpspmthoneywell.authentication.us10.hana.ondemand.com/oauth/token"
            response = AuthorizedRestClient.Post('CPS',url,"grant_type=client_credentials",{},"application/x-www-form-urlencoded",False, False)
            bearer_token = response.access_token


            headers={"Authorization":"Bearer "+str(bearer_token)}
            url='https://cpservices-product-configuration.cfapps.us10.hana.ondemand.com/api/v2/configurations?autoCleanup=true'
            body={
                "productKey": part_num,
                "kbId": prdID.kbId
            }
            cpsPayload=RestClient.Post(url,body,headers)
            configId=str(cpsPayload.id)


            url="https://cpservices-product-configuration.cfapps.us10.hana.ondemand.com/closeSession"
            body={}
            cpsPayload=RestClient.Post(url,body,headers)

            headers={'Authorization':'Bearer '+str(bearer_token),'If-Match':'"1"'}
            url="""https://cpservices-product-configuration.cfapps.us10.hana.ondemand.com/api/v2/configurations/{}/items/1/""".format(configId)
            body = {"characteristics" : config_lst }


            cpsPayload=RestClient.Patch(url,body,headers,True)
            #Log.Info('Patch response'+str(cpsPayload))

            headers={'Authorization':'Bearer '+str(bearer_token)}
            url="""https://cpservices-product-configuration.cfapps.us10.hana.ondemand.com/api/v2/externalConfigurations/{}""".format(configId)
            finalCpsPayload=RestClient.Get(url,headers)
            #Log.Info("finalCpsPayload response:"+str(finalCpsPayload))

            prd=ProductHelper.CreateProduct(prdID.Id)
            prd.LoadVariantProductFromVariantConfiguration(str(finalCpsPayload), configId)
            if prd.IsComplete:
                qty = 1 #from uploaded excel 
                prd.AddToQuote(qty)

    for i in Quote.MainItems:
        if fme_parts.get(i.PartNumber):
            i["QI_FME"].Value = str(fme_parts.get(i.PartNumber))
            #Trace.Write(str(i.PartNumber)+"--QI_FME-->"+str(i["QI_FME"].Value))
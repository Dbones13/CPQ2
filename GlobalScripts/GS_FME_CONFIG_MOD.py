#StreamReader =StreamReader
#CXCPQ-39700 - getAccessToken function as been modiifed to replace hardcoded client credentials.Refer Credential Manager SAP_FME2Config_APIGEE : Start
def getAccessToken(host):
    url = "https://{}/v2/oauth/accesstoken".format(host)
    Trace.Write('URL:'+url)
    #with HttpClient() as api:
    #headers={'ContentType':'application/x-www-form-urlencoded'}
    response=AuthorizedRestClient.GetClientCredentialsGrantOAuthToken('SAP_FME2Config_APIGEE',url)
    Trace.Write('token_type in module:'+ str(response["token_type"]))
    Trace.Write('token_type in module:'+ str(response["access_token"]))
    
    return "{} {}".format(response["token_type"] , response["access_token"])

''''def getAccessToken(host):
    #set request URL
    url = "https://{}/v2/oauth/accesstoken".format(host)

    #define body
    #CXCPQ-39700 - Replaced hardcoded client credentials with credential manager : Start
    Get_Query_Res = SqlHelper.GetList("select Name, Identifier from sys_CredentialsStore where Name in ('SAP_CPS_Client_Id' , 'SAP_CPS_Client_Secret')")
    for i in Get_Query_Res:
        if i.Name=='SAP_CPS_Client_Id':
            lv_cliend_id=i.Identifier
        if i.Name=='SAP_CPS_Client_Secret':
            lv_cliend_secret=i.Identifier            
    #pre_request_body = "grant_type=client_credentials&client_id={0}&client_secret={1}".format("5g0lEVFPl69hYK3Hc0P2Y2pDB7qk1GoA","tTiduwxVQCS4pMD8")
    pre_request_body = "grant_type=client_credentials&client_id={0}&client_secret={1}".format(lv_cliend_id,lv_cliend_secret)
    #CXCPQ-39700 - End

    #encoding body
    en_body = Encoding.ASCII.GetBytes(pre_request_body)

    #set headers
    accessRequest = HttpWebRequest.Create(url)
    accessRequest.Method = "POST"
    accessRequest.ContentType = "application/x-www-form-urlencoded"
    accessRequest.ContentLength = en_body.Length


    requestStream = accessRequest.GetRequestStream()
    requestStream.Write(en_body , 0 , en_body.Length)

    response = accessRequest.GetResponse()

    responseStream = response.GetResponseStream()

    jsonData = StreamReader(responseStream).ReadToEnd()

    json = RestClient.DeserializeJson(jsonData)

    return "{} {}".format(json.token_type , json.access_token)'''
#CXCPQ-39700 - End

def fme2config(host, accessTkn,material,fullModelCode):
    #material = "ACM"
    #fullModelCode = "ACM-032-004-010-000-01-02-11,12,83"

    fmeUrl = "https://{0}/ecommerce/services/fme/sap/v1/fmetoconfig?material={1}&fullModel={2}".format(host,material,fullModelCode)

    headers = {"HON-Org-Id":"PMT-HPS", "Authorization":accessTkn}

    fmeResponse = RestClient.Get(fmeUrl,headers)


    #return "{}".format(fmeResponse)
    return fmeResponse
def config2fme(host, accessTkn,material):
    #material = "ACM"
    #fullModelCode = "ACM-032-004-010-000-01-02-11,12,83"

    fmeUrl = "https://{0}/ecommerce/services/fme/sap/v1/configtofme?material={1}".format(host,material)

    headers = {"HON-Org-Id":"PMT-HPS", "Authorization":accessTkn}

    fmeResponse = RestClient.Get(fmeUrl,headers)

    #return "{}".format(fmeResponse)
    return fmeResponse
"""host = "it.api-beta.honeywell.com"

accessTkn = getAccessToken(host)
jsonConfig = fme2config(host, accessTkn)

ApiResponse = ApiResponseFactory.JsonResponse(str(jsonConfig))"""
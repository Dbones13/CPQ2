#---------------------------------------------------------------------------------------------------------
#					Change History Log
#---------------------------------------------------------------------------------------------------------
# Description: Base URL & Bearer Token Headers Generation For APIGEE.
# JIRA Ref.  : CXCPQ-54881
# HID        : H542824
#----------------------------------------------------------------------------------------------------------
# Date 			Name					Version   Comment
# 07-03-2023	Pratik Sanghani			10		  Initial Creation
#

def GetAPIGEEAuthHeader():
    APIGEE_Credentials = SqlHelper.GetFirst("Select Value from HPS_INTEGRATION_PARAMS Where [Key]='APIGEE_Credentials'").Value
    APIGEE_URL = SqlHelper.GetFirst("Select Value from HPS_INTEGRATION_PARAMS Where [Key]='APIGEE_URL'").Value
    url = "{}/v2/oauth/accesstoken".format(APIGEE_URL)
    Trace.Write('URL:'+url)
    
    response=AuthorizedRestClient.GetClientCredentialsGrantOAuthToken(APIGEE_Credentials,url)
    
    Req_Token = "{} {}".format(response["token_type"] , response["access_token"])

    headers = {"HON-Org-Id":"PMT-HPS", "Authorization":Req_Token}
    
    return headers

def GetAPIGEEBaseURL():
    APIGEE_URL= SqlHelper.GetFirst("Select Value from HPS_INTEGRATION_PARAMS Where [Key]='APIGEE_URL'")
    return APIGEE_URL.Value


def GetR2QAPIGEEAuthDetails():
    APIGEE_Credentials = SqlHelper.GetFirst("Select Value from HPS_INTEGRATION_PARAMS Where [Key]='APIGEE_Credentials'").Value
    APIGEE_R2Q_URL = SqlHelper.GetFirst("Select Value from HPS_INTEGRATION_PARAMS Where [Key]='APIGEE_R2Q_URL'").Value
    tokenUrl = "{}/v2/oauth/accesstoken".format(APIGEE_R2Q_URL)
						   
	
    responseToken=AuthorizedRestClient.GetClientCredentialsGrantOAuthToken(APIGEE_Credentials,tokenUrl)
    Req_Token = "{} {}".format(responseToken["token_type"] , responseToken["access_token"])
    excel_Url="https://it.api-beta.honeywell.com/cpq/r2q/sfdc/v1/cpqtor2q/tas"
    header = {"Content-Type" : "application/json","Authorization" : "{}".format(Req_Token),"HON-Org-Id" : "PMT-HPS" }
    return excel_Url, header

def GetR2QVirtualizationAPIGEEAuthDetails():
    APIGEE_Credentials = SqlHelper.GetFirst("Select Value from HPS_INTEGRATION_PARAMS Where [Key]='APIGEE_Credentials'").Value
    APIGEE_R2Q_URL = SqlHelper.GetFirst("Select Value from HPS_INTEGRATION_PARAMS Where [Key]='APIGEE_R2Q_URL'").Value
    tokenUrl = "{}/v2/oauth/accesstoken".format(APIGEE_R2Q_URL)
    responseToken=AuthorizedRestClient.GetClientCredentialsGrantOAuthToken(APIGEE_Credentials,tokenUrl)
    Req_Token = "{} {}".format(responseToken["token_type"] , responseToken["access_token"])
    excel_Url="https://it.api-beta.honeywell.com/cpq/r2q/sfdc/v1/cpqtor2q/virtualization"
    header = {"Content-Type" : "application/json","Authorization" : "{}".format(Req_Token),"HON-Org-Id" : "PMT-HPS" }
    return excel_Url, header
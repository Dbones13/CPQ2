from CPQ_SF_IntegrationModules import CL_SalesforceIntegrationModules
###############################################################################################
# Class CL_CustomerModules:
#       Class to fetch Service Contract Products from SFDC Rst API Service
###############################################################################################
class CL_SC_Modules(CL_SalesforceIntegrationModules):
	###############################################################################################
	# Function to get the Assets(MSID's) of the Quote Account site
	###############################################################################################

	def get_site_assets(self, AccountName, AccountSite, MSIDsList = None, isParent = False):
		soql =  """?q=SELECT+Name,ProductCode,SiteLicSeqSys__c,Account.Site+FROM+Asset+where+(Account{pName}.name+=+'{accName}'+OR+Account.name+=+'{accName}')+AND+Account.Site+IN+{accSite}+AND+Parent.name+=+null+AND+Status+IN+('Deployed')"""
		if MSIDsList:
			soql =  """?q=SELECT+AccountId,Name,Quantity,SiteLicSeqSys__c,+ProductCode,+Parent.name,+Parent.ProductCode,Account.Site+FROM+Asset+where+Account{pName}.name+=+'{accName}'+AND+Account.Site+IN+{accSite}+AND+Parent.name+IN+{MSIDs}+AND+Status+IN+('Deployed')"""
		apiResponse = self.call_soql_api(self.get_authorization_header(self.get_admin_auth2_token()), soql.format(pName = '.Parent' if isParent else '', accName = AccountName.replace(' ', '+').replace('&','%26'), accSite = str(tuple(AccountSite)).replace(',)',')').replace(' ', '+') if type(AccountSite) is list else str(tuple(AccountSite.split('<,>'))).replace(',)',')').replace(' ', '+'), MSIDs = str(tuple(MSIDsList)).replace(',)',')').replace(' ', '+') if MSIDsList else ""))
		return apiResponse

	def get_site_assets_HRHW(self, AccountName, AccountSite, MSIDsList = None, isParent = False):
		soql =  """?q=SELECT+Name,ProductCode,SiteLicSeqSys__c,Account.Site+FROM+Asset+where+(Account{pName}.name+=+'{accName}'+OR+Account.name+=+'{accName}')+AND+Account.Site+IN+{accSite}+AND+Parent.name+=+null+AND+Status+IN+('Deployed','Active')"""
		if MSIDsList:
			soql =  """?q=SELECT+AccountId,Name,Quantity,SiteLicSeqSys__c,+ProductCode,+Parent.name,+Parent.ProductCode,Account.Site+FROM+Asset+where+Account{pName}.name+=+'{accName}'+AND+Account.Site+IN+{accSite}+AND+Parent.name+IN+{MSIDs}+AND+Status+IN+('Deployed','Active')"""
		apiResponse = self.call_soql_api(self.get_authorization_header(self.get_admin_auth2_token()), soql.format(pName = '.Parent' if isParent else '', accName = AccountName.replace(' ', '+'), accSite = str(tuple(AccountSite)).replace(',)',')').replace(' ', '+') if type(AccountSite) is list else str(tuple(AccountSite.split('<,>'))).replace(',)',')').replace(' ', '+'), MSIDs = str(tuple(MSIDsList)).replace(',)',')').replace(' ', '+') if MSIDsList else ""))
		return apiResponse

	def get_siteID_assets(self, AccountName, AccountSite, MSIDsList = None, isParent = False):
		soql =  """?q=SELECT+Name,ProductCode,SiteLicSeqSys__c,Account.Site,Account.Id+FROM+Asset+where+(Account{pName}.Id+=+'{accName}'+OR+Account.Id+=+'{accName}')+AND+Account.Id+IN+{accSite}+AND+Parent.name+=+null+AND+Status+IN+('Deployed')"""
		if MSIDsList:
			soql =  """?q=SELECT+AccountId,Id,Name,Quantity,SiteLicSeqSys__c,+ProductCode,+Parent.Id,+Parent.name,+Parent.ProductCode,Account.Site,Account.Id+FROM+Asset+where+(Account{pName}.Id+=+'{accName}'+OR+Account.Id+=+'{accName}')+AND+Account.Id+IN+{accSite}+AND+Parent.name+IN+{MSIDs}+AND+Status+IN+('Deployed')"""
		apiResponse = self.call_soql_api(self.get_authorization_header(self.get_admin_auth2_token()), soql.format(pName = '.Parent' if isParent else '', accName = AccountName.replace(' ', '+'), accSite = str(tuple(AccountSite)).replace(',)',')').replace(' ', '+') if type(AccountSite) is list else str(tuple(AccountSite.split('<,>'))).replace(',)',')').replace(' ', '+'), MSIDs = str(tuple(MSIDsList)).replace(',)',')').replace(' ', '+') if MSIDsList else ""))
		return apiResponse

	def get_sites(self, pAccountName):
		soql =  """?q=select+Site,+Id,+Name,+Parent.Name,+Status__C+from+Account+where+Status__c+=+'Active'+AND+(Parent.Name+=+'{pAccount}'+OR+Name+=+'{pAccount}')"""
		apiResponse = self.call_soql_api(self.get_authorization_header(self.get_admin_auth2_token()), soql.format(pAccount = pAccountName.replace(' ', '+')))
		return apiResponse

	def get_sitesByID(self, pAccountID):
		soql =  """?q=select+Site,+Id,+Name,+Parent.Name,+Status__C+from+Account+where+Parent.Id+=+'{pAccount}'+OR+Id+=+'{pAccount}'"""
		apiResponse = self.call_soql_api(self.get_authorization_header(self.get_admin_auth2_token()), soql.format(pAccount = pAccountID.replace(' ', '+')))
		return apiResponse

	def get_TeamRoles_Data(self, opportunityID):
		soql =  """?q=select+User__r.id,+User__r.Name,+User__r.Email,+User__r.Business_Role__c,+User__r.Phone,+User__r.MobilePhone,+User__r.manager.Email+from+Honeywell_Sales_Team__c+where+Opportunity__c+=+'{oppID}'"""
		#apiResponse = self.call_soql_api(self.get_authorization_header(self.get_admin_auth2_token()), soql.format(roleList = str(tuple(TeamRoleList)).replace(',)',')').replace(' ', '+'), oppID = opportunityID.replace(' ', '+')))
		apiResponse = self.call_soql_api(self.get_authorization_header(self.get_admin_auth2_token()), soql.format(oppID = opportunityID.replace(' ', '+')))
		return apiResponse

	def get_RenewalTeamRoles_Data(self, opportunityID,WhereCond):
		soql ="""?q=select+id,+User__c,+User__r.Name,+User__r.Email,+Team_role__c,+User__r.Phone,+User__r.manager.Email+from+Service_Contract_Team__c+where+Service_Contract__r.{WhereCondition}+=+'{oppID}'+AND+Service_Contract__r.Status+=+'Active'+AND+Service_Contract__r.RecordType.DeveloperName+=+'Service_Contract'"""
		#soql =   """?q=select+id,+User__c,+User__r.Name,+User__r.Email,+Team_role__c,+User__r.Phone+from+Service_Contract_Team__c+where+Service_Contract__r.Renewal_Opportunity__c+=+'{oppID}'"""
		apiResponse = self.call_soql_api(self.get_authorization_header(self.get_admin_auth2_token()), soql.format(oppID = opportunityID.replace(' ', '+'),WhereCondition = WhereCond))
		return apiResponse

	def get_Topology_aggregate_Data(self, MSIDsList):
		soql =  """?q=select+Product__r.Name+TopologyName,+System_ID_MSID__c MISD,+SUM(Quantity__c)+Quantity+from+Asset_Audited__c+where+Parent_Asset__c+!=+null+AND+Latest_Audited_Asset__c+=+true+AND+RecordType.DeveloperName+=+'Audited_Hardware'+AND+System_ID_MSID__c+IN+{MSIDs}+group+by+Product__r.Name,+System_ID_MSID__c"""
		apiResponse = self.call_soql_api(self.get_authorization_header(self.get_admin_auth2_token()), soql.format(MSIDs = str(tuple(MSIDsList)).replace(',)',')').replace(' ', '+') if MSIDsList else ""))
		return apiResponse

	def get_ContractRenewalQuote_Data(self, opportunityID,WhereCond):
		soql =  """?q=select+Id,+Opportunity_No__c,+Opportunity_No_renewal__c,+Name,+ContractNumber,+Local_Ref__c,+ERP_Contract_Reference__c,+Purchasing_Agreement_Type__c,+Multi_Year_Start_Date__c,+Multi_Year_End_Date__c,+EndDate,+Status,+Renewal_Opportunity__r.Previous_Year_CPQ_Quote__c,+CurrencyIsoCode+from+ServiceContract+where+Status+=+'Active'+AND+{WhereCondition}+=+'{oppID}'"""
		apiResponse = self.call_soql_api(self.get_authorization_header(self.get_admin_auth2_token()), soql.format(oppID = opportunityID.replace(' ', '+'),WhereCondition = WhereCond))
		return apiResponse
	def get_ContractRenewalQuote_lineitemdata(self, ContractLineItemId):
		soql =  """?q=select+Id,Product_Code__c+from+ProductItem++where+LocationId+in+(SELECT+Source_Location__c+FROM+Entitlement+WHERE+ContractLineItemId+=+'{citemID}')"""
		apiResponse = self.call_soql_api(self.get_authorization_header(self.get_admin_auth2_token()), soql.format(citemID =ContractLineItemId))
		return apiResponse
	def get_ServiceContract_QuoteLine_Data(self, ContractNumber, serviceProduct = None):
		if serviceProduct:
			serviceProductList = [prd.ServiceProduct for prd in SqlHelper.GetList("SELECT distinct ServiceProduct FROM CT_SC_Entitlements_Data WHERE Module_Name='{0}' or Module_Name_GN='{0}'".format(serviceProduct))]
		soql =  """?q=select+Id,+Product_Name__c,+CurrencyIsoCode,+Sell_Price__c,+List_Price__c,+Booked_Value__c,+Booked_Margin__c,+Gross_Margin__c,+Target_Price__c,+Quantity,+UnitPrice+from+ContractLineItem+where+Status+=+'Active'+AND+ServiceContract.ContractNumber+=+'{ContractNo}'{withCondition}"""
		apiResponse = self.call_soql_api(self.get_authorization_header(self.get_admin_auth2_token()),soql.format(ContractNo=ContractNumber, withCondition = ' AND Product_Name__c in ' + str(tuple(serviceProductList)).replace(',)',')').replace('&','%26') if serviceProduct else ''))
		return apiResponse

	'''def get_AssetValidationHeader_Data(self, LocalRef,StartDate,EndDate):
		soql =   """?q=select+Asset_Comments__c,+Clear_Estimator_Comments__c,+MSID__r.Id,+MSID__r.Name,+MSID__r.Quantity,+MSID__r.SiteLicSeqSys__c,+MSID__r.ProductCode,+ContractRenewalHeaderId__r.LocalRef__c+from+Contract_Renewal_Line_Items__c+where+ContractRenewalHeaderId__r.LocalRef__c+=+'{lr}'+AND+ContractRenewalHeaderId__r.StartDate__c+=+'{EdDate}'+AND+ContractRenewalHeaderId__r.EndDate__c+=+'{StDate}'+AND+ContractRenewalHeaderId__r.Status__c+IN+('Asset+Validation+Completed','Amedment+completed')"""
		apiResponse = self.call_soql_api(self.get_authorization_header(self.get_admin_auth2_token()),soql.format(lr=LocalRef,StDate=StartDate,EdDate=EndDate))
		return apiResponse'''
	def get_AssetValidationHeader_Data(self):
		soql =   """?q=select+Asset_Comments__c,+ContractRenewalHeaderId__r.Status__c,+Renewal_Quantity__c,+Name,+Asset_Status__c,+MSID__r.Id,+SysName__c,+SystemNumber__c,+Platform__c,+SESP_Model_Num__c,+MSID__r.Name,+MSID__r.Quantity,+MSID__r.SiteLicSeqSys__c,+MSID__r.ProductCode,+ContractRenewalHeaderId__r.LocalRef__c+from+Contract_Renewal_Line_Items__c"""
		apiResponse = self.call_soql_api(self.get_authorization_header(self.get_admin_auth2_token()),soql)
		return apiResponse

	def get_AssetValidationHeader_Data1(self,LocalRef__c1,Account_Site__c):
		assetHearderId = self.get_AssetValidationHeader_ID(LocalRef__c1,Account_Site__c)
		soql =   """?q=select+Asset_Comments__c,+ContractRenewalHeaderId__r.Status__c,+ContractRenewalHeaderId__r.StartDate__c,+ContractRenewalHeaderId__r.EndDate__c,+Renewal_Quantity__c,+Name,+Asset_Status__c,+MSID__r.Id,+SysName__c,+SystemNumber__c,+Platform__c,+SESP_Model_Num__c,+MSID__r.Name,+MSID__r.Quantity,+MSID__r.SiteLicSeqSys__c,+MSID__r.ProductCode,+ContractRenewalHeaderId__r.LocalRef__c,+Quantity__c+from+Contract_Renewal_Line_Items__c +where+ ContractRenewalHeaderId__r.LocalRef__c+= +'{lf}'+AND+Account_Site__c+=+'{account_site}'+AND+ContractRenewalHeaderId__r.Id+IN+{AssetIDs}+Order+By+ContractRenewalHeaderId__r.EndDate__c+Desc"""
		apiResponse = self.call_soql_api(self.get_authorization_header(self.get_admin_auth2_token()),soql.format(lf=LocalRef__c1,account_site=Account_Site__c, AssetIDs = assetHearderId))
		return apiResponse

	def get_AssetValidationHeader_Data_With_HeaderID(self,LocalRef__c1,Account_Site__c,assetHearderId, AccountID):
		accountSites = self.get_AccountSites_ID(AccountID)
		soql = """?q=select+Asset_Comments__c,+ContractRenewalHeaderId__r.Status__c,+ContractRenewalHeaderId__r.StartDate__c,+ContractRenewalHeaderId__r.EndDate__c,+Renewal_Quantity__c,+Name,+Asset_Status__c,+MSID__r.Id,+SysName__c,+SystemNumber__c,+Platform__c,+SESP_Model_Num__c,+MSID__r.Name,+MSID__r.Quantity,+MSID__r.SiteLicSeqSys__c,+MSID__r.ProductCode,+ContractRenewalHeaderId__r.LocalRef__c,+Quantity__c+from+Contract_Renewal_Line_Items__c +where+ ContractRenewalHeaderId__r.LocalRef__c+= +'{lf}'+AND+Account_Site__c+IN+{account_site}+AND+ContractRenewalHeaderId__r.Id+=+'{AssetID}'+Order+By+ContractRenewalHeaderId__r.EndDate__c+Desc"""
		apiResponse = self.call_soql_api(self.get_authorization_header(self.get_admin_auth2_token()),soql.format(lf=LocalRef__c1,account_site=accountSites, AssetID = assetHearderId))
		return apiResponse

	def get_AssetValidationHeader_Details(self,LocalRef__c1,Account_Site__c):
		#"""?q=select+id,+Name+from+Contract_Renewal_Header__c+where+LocalRef__c+=+'{lf}'+and+Status__c+!=+'Draft'+order+by+StartDate__c+desc"""
		soql ="""?q=select+id,+Name+from+Contract_Renewal_Header__c+where+LocalRef__c+=+'{lf}'+and+Service_Contract__c+!=+null+and+Status__c+!=+'Draft'+order+by+StartDate__c+desc"""
		apiResponse = self.call_soql_api(self.get_authorization_header(self.get_admin_auth2_token()),soql.format(lf=LocalRef__c1,account_site=Account_Site__c))
		return apiResponse

	def get_AssetValidationHeader_ID(self,LocalRef__c1,Account_Site__c):
		soql =   """?q=select+id+from+Contract_Renewal_Header__c+where+Status__c+=+'{ss}'+and+LocalRef__c+=+'{lf}'+and+Service_Contract__c+!=+null+order+by+StartDate__c+desc+limit+1"""
		apiResponse = self.call_soql_api(self.get_authorization_header(self.get_admin_auth2_token()),soql.format(lf=LocalRef__c1,account_site=Account_Site__c,ss='Asset Validation Completed'))

		assetHeaderIdList = []
		if apiResponse:
			if apiResponse and str(apiResponse).Contains('totalSize') and apiResponse.totalSize > 0:
				for hd in apiResponse.records:
					assetHeaderIdList.append(str(hd.Id))
		return str(tuple(assetHeaderIdList)).replace(',)',')').replace(' ', '+') if assetHeaderIdList else ""

	def get_AccountSites_ID(self, AccountID):
		soql = """?q=select+Name,+Site+from+Account+where+ParentID=+'{accId}'+or+Id+=+'{accId}'"""
		apiResponse = self.call_soql_api(self.get_authorization_header(self.get_admin_auth2_token()),soql.format(accId=AccountID))

		actNameList = []
		if apiResponse:
			if apiResponse and str(apiResponse).Contains('totalSize') and apiResponse.totalSize > 0:
				for acct in apiResponse.records:
					actNameList.append(str(acct.Site))
		return '(' + ",".join(["'{}'".format(n.replace("'", "\'")) for n in actNameList]) + ')' if actNameList else "('')"

	def get_ContractRenewalLineItem_Data(self, ContractID):
		soql =  """?q=select+Id,+ContractLineItemId,+Service_Product_Name__c,+Name+from+Entitlement+where+Service_Contract_Link__r.ContractNumber+=+'{CID}'"""
		apiResponse = self.call_soql_api(self.get_authorization_header(self.get_admin_auth2_token()), soql.format(CID = ContractID.replace(' ', '+')))
		return apiResponse

	def get_Training_Match_Data(self, ContractNumber):
		soql =  """?q=select+Id,+ContractLineItemId,+Service_Product__c,+Name,+CurrencyIsoCode,+Budgeted_Quota__c,+AssetName__c+from+Entitlement+where+Status+=+'Active'+AND+Service_Contract_Link__r.ContractNumber+=+'{ContractNo}'+AND+Name+=+'Training Match'"""
		apiResponse = self.call_soql_api(self.get_authorization_header(self.get_admin_auth2_token()),soql.format(ContractNo=ContractNumber.replace(' ', '+')))
		return apiResponse
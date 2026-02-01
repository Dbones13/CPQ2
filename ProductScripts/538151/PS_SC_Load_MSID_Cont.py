# To load the Entitlement Container -----Udhaya - 23/8/23
Ent = Product.GetContainerByName('SC_Entitlements')
#Ent.Clear()
Service = Product.Attr('SC_Service_Product').GetValue()
if not Service:
    setDefaultValues = SqlHelper.GetList("select top 1 ServiceProduct, Service_Hours from CT_SC_ENTITLEMENTS_DATA where Product_Type = '{}' and Status='Active'".format('SESP'))
    if setDefaultValues:
        Product.Attr('SC_Service_Product').SelectDisplayValue(setDefaultValues[0].ServiceProduct, False)
        Product.Attr('SC_Coverage').SelectDisplayValue(setDefaultValues[0].Service_Hours, False)
        #Product.Attr('SC_Service_Product').AssignValue(setDefaultValues[0].ServiceProduct)
        #Product.Attr('SC_Coverage').AssignValue(setDefaultValues[0].Service_Hours)
a = SqlHelper.GetList("select distinct Top 1000 Entitlement,IsMandatory,ServiceProduct,Asset_Level from CT_SC_ENTITLEMENTS_DATA where ServiceProduct = '{}' and IsMandatory = 'False'".format(Service))
if Ent.Rows == 0:
    for row in a:
        if row.IsMandatory == 'FALSE':
            i = Ent.AddNewRow(False)
            i['Entitlement'] = row.Entitlement
            i['ServiceProduct'] = str(row.ServiceProduct)
            i['ProductLevel'] = str(row.Asset_Level)
Ent.Calculate()
# to Load MSID Container ----Udhaya---31/8/23
from CPQ_SF_SC_Modules import CL_SC_Modules
class_contact_modules = CL_SC_Modules(Quote, TagParserQuote, None, Session)
AccountId = Quote.GetCustomField('AccountId').Content
AccountName = Quote.GetCustomField('Account Name').Content
AccountSite = Quote.GetCustomField('Account Site').Content
pAccountName = Quote.GetCustomField('SC_CF_PARENT_ACCOUNT_NAME').Content
mSites=class_contact_modules.get_sitesByID(AccountId)
mSites_Cont = Product.GetContainerByName('SC_SESP_MultiSites')
updateSites = []
for site in mSites.records:
    sRow = mSites_Cont.AddNewRow(False)
    if site.Parent == None:
        sRow['SiteType'] = 'Parent Site'
    else:
        sRow['SiteType'] = 'Child Site'
    sRow['Sites'] = str(site.Site)
    sRow['AccountId'] = str(site.Id)
    sRow['AccountName'] = str(site.Name)
    if AccountSite == str(site.Site) and (AccountName == str(site.Name) or AccountName == ""):
        sRow['IsDefault'] = 'True'
        #sRow.IsSelected = True
        #updateSites.append(str(site.Id))
    else:
        sRow['IsDefault'] = 'False'
Product.Attr('SC_SESP_MultiSites').Allowed = True
Product.Attr('SC_SESP_MultiSites_Button').Allowed = True

"""
if not pAccountName:
    mSites=class_contact_modules.get_sites(AccountName)
    mSites_Cont = Product.GetContainerByName('SC_SESP_MultiSites')
    for site in mSites.records:
        sRow = mSites_Cont.AddNewRow()
        sRow['Sites'] = str(site.Site)
        sRow['AccountId'] = str(site.Id)
        sRow['AccountName'] = str(site.Name)
else:
    Product.Attr('SC_SESP_MultiSites').Allowed = False
    Product.Attr('SC_SESP_MultiSites_Button').Allowed = False
    MSID_Cont = Product.GetContainerByName('SC_Select_MSID_Cont')
    Hid_Cont = Product.GetContainerByName('SC_Select_MSID_Cont_Hidden')
    MSIDTable=class_contact_modules.get_site_assets(AccountName, AccountSite)
    if Hid_Cont.Rows.Count is 0:
        for asset in MSIDTable.records:
            msid = asset.Name
            SystemName = asset.ProductCode
            Systemnum = asset.SiteLicSeqSys__c
            i = MSID_Cont.AddNewRow(False)
            hrow = Hid_Cont.AddNewRow(False)
            i['MSIDs'] = str(msid)
            i['System Name'] = str(SystemName)
            i['System Number'] = str(Systemnum)
            hrow['MSIDS'] = str(msid)
            hrow['System Name'] = str(SystemName)
            hrow['System Number'] = str(Systemnum)
    MSID_Cont.Calculate()
    Hid_Cont.Calculate()
"""
#CXCPQ-62215 To set Default Value to Training Match Percent Attribute.
container_Entitlements = Product.GetContainerByName("SC_Entitlements")
Training_Match_Value = Product.Attr('SC_Training_Match_Contract_Value')
Training_Match_Value_Per = Product.Attr('SC_Training_Match_Contract_Value_Percent')

Training_Match_Value.Allowed = False
Training_Match_Value_Per.Allowed = False

if container_Entitlements is not None:
    for row in container_Entitlements.Rows:
        if row['Entitlement'] == 'Training Match':
            if row.IsSelected:
                Trace.Write('****************')
                Training_Match_Value.Allowed = True
                Training_Match_Value_Per.Allowed = True
                Training_Match_Value.Access = AttributeAccess.Editable
                Training_Match_Value_Per.Access = AttributeAccess.Editable
                P = Product.Attr('SC_Training_Match_Contract_Value_Percent').GetValue()
                if not P:
                    Product.Attr('SC_Training_Match_Contract_Value_Percent').AssignValue("10")
            else:
                Training_Match_Value.Allowed = False
                Training_Match_Value_Per.Allowed = False
            break
#container_Entitlements.Calculate()
if updateSites:
    MSID_Cont = Product.GetContainerByName('SC_Select_MSID_Cont')
    Hid_Cont = Product.GetContainerByName('SC_Select_MSID_Cont_Hidden')
    class_contact_modules = CL_SC_Modules(Quote, TagParserQuote, None, Session)
    #AccountName = Quote.GetCustomField('Account Name').Content
    AccountSite = updateSites
    MSIDTable=class_contact_modules.get_siteID_assets(AccountId, AccountSite, isParent = True)
    if MSIDTable:
        for asset in MSIDTable.records:
            msid = asset.Name
            SystemName = asset.ProductCode
            Systemnum = asset.SiteLicSeqSys__c
            i = MSID_Cont.AddNewRow(False)
            hrow = Hid_Cont.AddNewRow(False)
            i['MSIDs'] = str(msid)
            i['System Name'] = str(SystemName)
            i['System Number'] = str(Systemnum)
            i['siteName'] = str(asset.Account.Site)
            i['SiteID'] = str(asset.Account.Id)
            hrow['MSIDS'] = str(msid)
            hrow['System Name'] = str(SystemName)
            hrow['System Number'] = str(Systemnum)
            hrow['siteName'] = str(asset.Account.Site)
            hrow['SiteID'] = str(asset.Account.Id)
        MSID_Cont.Calculate()
        Hid_Cont.Calculate()
Product.Attr('SC_MultiSites_Selected').AssignValue('<,>'.join(set(updateSites)).strip('<,>'))
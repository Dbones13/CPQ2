def getFloat(n):
    try:
        return float(n)
    except:
        return 0
    
'''
Load SC_Entitlements_Exp_Ext_Supp i.e Entitlements(Summary tab)
'''
SERVICE_PROD = 'Experion Extended Support - RQUP ONLY'
entitlement_cont = Product.GetContainerByName("SC_Entitlements_Exp_Ext_Supp")
entitlement_cont.Rows.Clear()

Entitlement_query = SqlHelper.GetList("select Entitlement from CT_SC_ENTITLEMENTS_DATA where ServiceProduct='{}' and IsMandatory='TRUE'".format(SERVICE_PROD))
for query in Entitlement_query:
    cont = entitlement_cont.AddNewRow(False)
    cont["Entitlement"] = query.Entitlement
    cont["Type"] = 'Mandatory'

'''
Load SC_SESP_MultiSites container i.e. Sites Container
'''
from CPQ_SF_SC_Modules import CL_SC_Modules
class_contact_modules = CL_SC_Modules(Quote, TagParserQuote, None, Session)
AccountName = Quote.GetCustomField('Account Name').Content
AccountSite = Quote.GetCustomField('Account Site').Content
pAccountName = Quote.GetCustomField('SC_CF_PARENT_ACCOUNT_NAME').Content
mSites=class_contact_modules.get_sites(AccountName)
mSites_Cont = Product.GetContainerByName('SC_SESP_MultiSites')
updateSites = []
for site in mSites.records:
    sRow = mSites_Cont.AddNewRow()
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
        updateSites.append(str(site.Site))
    else:
        sRow['IsDefault'] = 'False'
        
'''
Load SC_MSID_Container i.e. MSID container
'''
mSites_Cont = Product.GetContainerByName('SC_SESP_MultiSites')
selectedSites = Product.Attr('SC_MultiSites_Selected').GetValue()
sitesList = selectedSites.split('<,>')
updateSites = []
removeSites = []
for row in mSites_Cont.Rows:
    if row.IsSelected and row['Sites'] not in sitesList:
        updateSites.append(row['Sites'])
    elif row.IsSelected == False and row['Sites'] in sitesList:
        removeSites.append(row['Sites'])
MSID_Cont = Product.GetContainerByName('SC_MSID_Container')
Hid_Cont = Product.GetContainerByName('SC_MSID_Container_Hidden')
if removeSites:
    sitesList = list(set(sitesList) - set(removeSites))
    removeIndexList = []
    for row in MSID_Cont.Rows:
        if row['Site'] in removeSites:
            removeIndexList.append(row.RowIndex)
    removeIndexList.reverse()
    for i in removeIndexList:
        MSID_Cont.DeleteRow(i)
        Hid_Cont.DeleteRow(i)
    MSID_Cont.Calculate()
    Hid_Cont.Calculate()
if updateSites:
    MSID_Cont = Product.GetContainerByName('SC_MSID_Container')
    Hid_Cont = Product.GetContainerByName('SC_MSID_Container_Hidden')
    class_contact_modules = CL_SC_Modules(Quote, TagParserQuote, None, Session)
    AccountSite = updateSites
    MSIDTable=class_contact_modules.get_site_assets(AccountName, AccountSite, isParent = True)
    py_msid = []
    if MSID_Cont.Rows.Count:
        for row in MSID_Cont.Rows:
            py_msid.append(row['MSIDs'])
    if MSIDTable:
        for asset in MSIDTable.records:
            msid = asset.Name
            if msid in py_msid:
                continue
            SystemName = asset.ProductCode
            Systemnum = asset.SiteLicSeqSys__c
            i = MSID_Cont.AddNewRow()
            hrow = Hid_Cont.AddNewRow()
            i['MSIDs'] = str(msid)
            i['System Name'] = str(SystemName)
            i['System Number'] = str(Systemnum)
            i['Site'] = str(asset.Account.Site)
            hrow['MSIDs'] = str(msid)
            hrow['System Name'] = str(SystemName)
            hrow['System Number'] = str(Systemnum)
            hrow['Site'] = str(asset.Account.Site)
        MSID_Cont.Calculate()
        Hid_Cont.Calculate()
        MSIDRows = MSID_Cont.Rows.Count
        #SC_Num_of_MSID
        #Product.Attr('SC_Num_of_MSID').AssignValue(str(MSIDRows))
Product.Attr('SC_MultiSites_Selected').AssignValue('<,>'.join(set(updateSites)).strip('<,>'))
import math as m

def getFloat(n):
    try:
        return float(n)
    except:
        return 0
'''
Load Entitlement Container i.e. SC_Entitlements
'''
Ent = Product.GetContainerByName('SC_Entitlements')
Service = Product.Attr('SC_Honeywell_Digital_Prime').GetValue()

a = SqlHelper.GetList("select Entitlement,IsMandatory from CT_SC_ENTITLEMENTS_DATA where IsMandatory = 'False' and ServiceProduct = '{}'".format(Service))
if Ent.Rows.Count == 0:
    for row in a:
        if row.IsMandatory == 'FALSE':
            i = Ent.AddNewRow()
            i['Entitlement'] = row.Entitlement
Ent.Calculate()


'''
Load SC_SESP_MultiSites container i.e. Sites Container
'''
from CPQ_SF_SC_Modules import CL_SC_Modules
class_contact_modules = CL_SC_Modules(Quote, TagParserQuote, None, Session)
AccountId = Quote.GetCustomField('AccountId').Content
AccountName = Quote.GetCustomField('Account Name').Content
AccountSite = Quote.GetCustomField('Account Site').Content
pAccountName = Quote.GetCustomField('SC_CF_PARENT_ACCOUNT_NAME').Content
#mSites=class_contact_modules.get_sites(AccountName)
mSites=class_contact_modules.get_sitesByID(AccountId) #updated get site function to get data from account id instade of account name (5/8/2024)
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
    if MSIDTable:
        for asset in MSIDTable.records:
            msid = asset.Name
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

'''
Contract Duration logic
'''
contract = Quote.GetCustomField('SC_CF_CONTRACTDURYR').Content
contractDuration = contract.split(' ')[0]
#contractDuration1 = contract.split(' ')[0]
if Product.Attr('SC_Product_Type').GetValue() == "New":
    if contractDuration=='0.10':
        contractDuration = int(m.ceil(float(contractDuration)))
        Product.Attr('SC_Contract_Duration').AssignValue(str(contractDuration))
    elif float(contractDuration) < 0.5 or float(contractDuration) > 3:
        if float(contractDuration) > 3:
            incompleteMessage = "Contract Duration greater than 3 years not allowed."
        else:
            incompleteMessage = "Contract Duration less than 6 months not allowed."
        Product.Attr('SC_Digital_Prime_Contract_invalid').AssignValue(incompleteMessage)
    else:
        contractDuration = int(m.ceil(float(contractDuration)))
        #contractYears = str(contractDuration)+" year"
        Product.Attr('SC_Contract_Duration').AssignValue(str(contractDuration))
ContDur = Product.Attr('SC_Contract_Duration').GetValue()
Trace.Write("ContDure MSID" + str(ContDur))
from CPQ_SF_SC_Modules import CL_SC_Modules
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
    class_contact_modules = CL_SC_Modules(Quote, TagParserQuote, None, Session)
    AccountName = Quote.GetCustomField('Account Name').Content
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
            hrow['MSIDS'] = str(msid)
            hrow['System Name'] = str(SystemName)
            hrow['System Number'] = str(Systemnum)
            hrow['Site'] = str(asset.Account.Site)
        MSID_Cont.Calculate()
        Hid_Cont.Calculate()
    sitesList.extend(updateSites)
Product.Attr('SC_MultiSites_Selected').AssignValue('<,>'.join(set(sitesList)).strip('<,>'))
#Change product status as incomplete
#Product.Attr('SC_Product_Status').AssignValue("0")
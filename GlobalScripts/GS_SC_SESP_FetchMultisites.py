from CPQ_SF_SC_Modules import CL_SC_Modules
mSites_Cont = Product.GetContainerByName('SC_SESP_MultiSites')
selectedSites = Product.Attr('SC_MultiSites_Selected').GetValue()
sitesList = selectedSites.split('<,>')
updateSites = []
removeSites = []
for row in mSites_Cont.Rows:
    if row.IsSelected and row['AccountID'] not in sitesList:
        updateSites.append(row['AccountId'])
    elif row.IsSelected == False and row['AccountId'] in sitesList:
        removeSites.append(row['AccountId'])
MSID_Cont = Product.GetContainerByName('SC_Select_MSID_Cont')
Hid_Cont = Product.GetContainerByName('SC_Select_MSID_Cont_Hidden')

es = Product.Attr('EnableSelection_SESP').SelectedValue
if es: #Enabled Service is selected
    asset_cont	= Product.GetContainerByName('Asset_details_ServiceProd')
    asset_cont2	= Product.GetContainerByName('Asset_details_ServiceProd_ReadOnly')
def deleteAsset(msid):
    indexes = [row.RowIndex for row in	asset_cont.Rows if row['MSID'] == msid]
    start_index = 0
    for indx in indexes:
        asset_cont.DeleteRow(indx - start_index)
        start_index += 1
    indexes = [row.RowIndex for row in	asset_cont2.Rows if row['MSID'] == msid]
    start_index = 0
    for indx in indexes:
        asset_cont2.DeleteRow(indx - start_index)
        start_index += 1

if removeSites:
    sitesList = list(set(sitesList) - set(removeSites))
    removeIndexList = []
    for row in Hid_Cont.Rows:
        if row['SiteID'] in removeSites:
            removeIndexList.append(row.RowIndex)
    removeIndexList.reverse()
    for i in removeIndexList:
        r = Hid_Cont.Rows[i]
        msid = r['MSIDs']
        #MSID_Cont.DeleteRow(i)
        Hid_Cont.DeleteRow(i)
        if es: #Enabled Service is selected
            deleteAsset(msid)
    #MSID_Cont.Calculate()
    Hid_Cont.Calculate()

if updateSites:
    class_contact_modules = CL_SC_Modules(Quote, TagParserQuote, None, Session)
    AccountName = Quote.GetCustomField('Account Name').Content
    AccountId = Quote.GetCustomField('AccountId').Content
    AccountSite = updateSites
    MSIDTable=class_contact_modules.get_siteID_assets(AccountId, AccountSite, isParent = True)
    if MSIDTable:
        for asset in MSIDTable.records:
            msid = asset.Name
            SystemName = asset.ProductCode
            Systemnum = asset.SiteLicSeqSys__c
            #i = MSID_Cont.AddNewRow()
            hrow = Hid_Cont.AddNewRow(False)
            # i['MSIDs'] = str(msid)
            # i['System Name'] = str(SystemName)
            # i['System Number'] = str(Systemnum)
            # i['siteName'] = str(asset.Account.Site)
            # i['SiteID'] = str(asset.Account.Id)
            hrow['MSIDS'] = str(msid)
            hrow['System Name'] = str(SystemName)
            hrow['System Number'] = str(Systemnum)
            hrow['siteName'] = str(asset.Account.Site)
            hrow['SiteID'] = str(asset.Account.Id)
        ##MSID_Cont.Calculate()
        ##Hid_Cont.Calculate()
    sitesList.extend(updateSites)
Product.Attr('SC_MultiSites_Selected').AssignValue('<,>'.join(set(sitesList)).strip('<,>'))
#ScriptExecutor.Execute('GS_MSIDs_OTU_SESP') # OTU update
if es: #Enabled Service is selected
    asset_cont.Calculate()
    asset_cont2.Calculate()

SearchText = Product.Attr('SC_MSID_Search_Field_Scope_Select').GetValue()
MSID_Cont.Clear()
if SearchText == "" or SearchText == None:
    for row in Hid_Cont.Rows:
        i = MSID_Cont.AddNewRow(False)
        i['MSIDS'] = row['MSIDs']
        i['System Name'] = row['System Name']
        i['System Number'] = row['System Number']
        i['siteName'] = row['siteName']
        i['SiteID'] = row['SiteID']
        i['HiddenRowIndex'] = str(row.RowIndex)
        i.IsSelected = row.IsSelected
else:
    for row in Hid_Cont.Rows:
        if SearchText.lower() in row['MSIDs'].lower():
            i = MSID_Cont.AddNewRow(False)
            i['MSIDS'] = row['MSIDs']
            i['System Name'] = row['System Name']
            i['System Number'] = row['System Number']
            i['siteName'] = row['siteName']
            i['SiteID'] = row['SiteID']
            i['HiddenRowIndex'] = str(row.RowIndex)
            i.IsSelected = row.IsSelected
from CPQ_SF_SC_Modules import CL_SC_Modules
class_contact_modules = CL_SC_Modules(Quote, TagParserQuote, None, Session)
AccountName = Quote.GetCustomField('Account Name').Content
AccountSite = Quote.GetCustomField('Account Site').Content
#Quote.GetCustomField('SC_CF_PARENT_ACCOUNT_NAME').Content = 'Exxon Parent'
pAccountName = Quote.GetCustomField('SC_CF_PARENT_ACCOUNT_NAME').Content
Log.Info('----pAccountName['+str(pAccountName)+']')
if  not pAccountName:
    Log.Info('----pAccountName inside sites ['+str(pAccountName)+']')
    mSites=class_contact_modules.get_sites(AccountName)
    #mSites=class_contact_modules.get_sites(pAccountName)
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
            i = MSID_Cont.AddNewRow()
            hrow = Hid_Cont.AddNewRow()
            i['MSIDs'] = str(msid)
            i['System Name'] = str(SystemName)
            i['System Number'] = str(Systemnum)
            hrow['MSIDS'] = str(msid)
            hrow['System Name'] = str(SystemName)
            hrow['System Number'] = str(Systemnum)
    MSID_Cont.Calculate()
    Hid_Cont.Calculate()
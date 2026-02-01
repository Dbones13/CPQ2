from GS_ITEMCREATE_UPDATE_Functions import populateSetPointAttrs,populateVCwithcond,deleteRows
Bookinglob = Quote.GetCustomField("Booking LOB").Content
cartitem = sender
prd=''
#IsR2QRequest =  Quote.GetCustomField('IsR2QRequest').Content
#pn = SqlHelper.GetFirst("Select PLANT_NAME from COUNTRY_SORG_PLANT_MAPPING(NOLOCK) where PLANT_CODE = '6649' ORDER BY CpqTableEntryId DESC")
## CXCPQ-111107 # R2Q HCI Bundle set default plant
#if Bookinglob!="PMC" and IsR2QRequest == "Yes" and pn:
#    Quote.GetCustomField("CF_Plant").Content = str(pn.PLANT_NAME)
#    cartitem['QI_Plant'].Value = str(pn.PLANT_NAME)

## GS_Manual_Entry_3rdParty_WriteIn_Parts ##
if cartitem.ProductTypeName  == 'Write-In' and Bookinglob != 'CCC':
    from GS_Manual_Entry_3rdParty_WriteIn_Parts import Manual_Entry_3rdParty
    Manual_Entry_3rdParty(cartitem)

if Bookinglob == "PMC" or Bookinglob in ["HCP", "LSS", "PAS"]:
    from GS_Validate_Product_Type import IsVCitem
    ##GS_Skid_VC_Items##
    if cartitem.ProductName=='Productized Skid Quote Item':
        from GS_Skid_VC_Items import Skid_items
        Skid_items(cartitem)
    if IsVCitem(cartitem.PartNumber) ==True:
        ##GS_PopulateFME 
        tableInfo = SqlHelper.GetTable("PMC_ACE_QUOTE")
        from GS_PopulateFME import Populate_FME
        from GS_PopulateAceTable import PopulateAceTable
        Trace.Write(str()+'--rechecking--111-->'+str(cartitem.QI_FME.Value))
        Populate_FME(cartitem,cartitem.PartNumber,Quote)
        Trace.Write(str()+'--rechecking--222-->'+str(cartitem.QI_FME.Value))
        ##GS_PopulateAceTable
        PopulateAceTable(cartitem,tableInfo)
        VCModelConfiguration = Quote.QuoteTables["VCModelConfiguration"]
        guId = cartitem.QuoteItemGuid
        toBeDeleted = list()
        for row in VCModelConfiguration.Rows:
            if row['CartItemGUID'] == guId:
                toBeDeleted.append(row.Id)
        #GS_VCSetPointAttrs
        populateSetPointAttrs(VCModelConfiguration , cartitem, Product)
        #GS_PopulateVCConfigQuoteTable
        populateVCwithcond(VCModelConfiguration , cartitem,Product)
        deleteRows(VCModelConfiguration , toBeDeleted)
        VCModelConfiguration.Save()
        ## GS_Add_ETO_QTable##
        if str(cartitem.ProductName) != 'Write-in Products':
            from GS_Add_ETO_QTable import Add_ETO_QTable
            Add_ETO_QTable(Quote,cartitem)
            
        ##GS_ETO_ListPrice_CAL##
        from GS_ETO_ListPrice_CAL import ETO_ListPrice_CAL
        ETO_ListPrice_CAL(Quote,cartitem) 
    
        ## GS_delete_invalid_parts##
        tbl = Quote.QuoteTables['FME_Invalid_Parts']
        if tbl.Rows.Count:
            for row in tbl.Rows:
                if row["Part_Number"] == str(prd):
                    tbl.DeleteRow(row.Id)

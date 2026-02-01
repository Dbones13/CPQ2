import GS_CommonModule

#Quote Type is selected based on Oppurtunity type
opp_type = GS_CommonModule.getCFValue(Quote , "Opportunity Type")
lob = GS_CommonModule.getCFValue(Quote , "Booking LOB")
Log.Info('GS_SetQuoteType')
Trace.Write(lob)

if opp_type in ['Project','Change Order','Contract New'] and lob in ['PAS','LSS','PMC','CCC','HCP'] :
    GS_CommonModule.setCFValue(Quote, "Quote Type",'Projects')
if opp_type in ['Spot Service','Parts/Hardware/K&E','Products','Software Only','Automation College','Run Rate'] and lob in ['LSS','PMC','CCC','HCP']:
    GS_CommonModule.setCFValue(Quote, "Quote Type",'Parts and Spot')

if Quote.GetCustomField('Quote Type').Content == 'Projects':
    GS_CommonModule.setCFValue(Quote, "Quote Expiration Date",TagParserQuote.ParseString("<*CTX(Date.AddDays(1000))*>"))
    #Quote.GetCustomField('Quote Expiration Date').Content = TagParserQuote.ParseString("<*CTX(Date.AddDays(1000))*>")
elif Quote.GetCustomField('Quote Type').Content == 'Parts and Spot':
    GS_CommonModule.setCFValue(Quote, "Quote Expiration Date",TagParserQuote.ParseString("<*CTX( Date.AddDays(30) )*>"))
    #Quote.GetCustomField('Quote Expiration Date').Content = TagParserQuote.ParseString("<*CTX( Date.AddDays(30) )*>")
#Log.Info("QCF-->2"+str(Quote.GetCustomField('Quote Expiration Date').Content))
#import GS_CommonModule

'''quoteTypeDict = {
    "LSSC" : "Parts and Spot" ,
    "LSSD" : "Parts and Spot" ,
    "PMCC" : "Parts and Spot" ,
    "PMCD" : "Parts and Spot" ,
    "LSSA" : "Projects" ,
    "LSSB" : "Projects" ,
    "PASA" : "Projects" ,
    "PASB" : "Projects" ,
    "PMCB" : "Projects" ,
    "PMCA" : "Projects" ,
}
#added code for service contract --nilesh 31082023--
if GS_CommonModule.getCFValue(Quote , "Opportunity Type") not in ("Contract New", "Contract Renewal"):
    oppCategory = GS_CommonModule.getCFValue(Quote , "Opportunity Category")
    lob			= GS_CommonModule.getCFValue(Quote , "Booking LOB")
    if oppCategory and lob:
        GS_CommonModule.setCFValue(Quote, "Quote Type", quoteTypeDict["{}{}".format(lob , oppCategory)])'''
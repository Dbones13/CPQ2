#---------------------------------------------------------------------------------------------------------
#					Change History Log
#---------------------------------------------------------------------------------------------------------
# Description: To Populate Year in All Quote Line Items.
# JIRA Ref.  : CXCPQ-63375
# Author     : H542824
# Created Date : 13-09-2023
#----------------------------------------------------------------------------------------------------------
# Date 			Name					    Version     Comment
# 27-10-2023	Pratik Sanghani    			2  	        Initial Version
#----------------------------------------------------------------------------------------------------------

ITEMS = arg.QuoteItemCollection

def populateYears(SuperParentRolledUpQuoteItem,Year):
    for item in Quote.MainItems:
        if item.RolledUpQuoteItem == SuperParentRolledUpQuoteItem:
            item["QI_Year"].Value = Year
            item["QI_Year_Visibility"].Value = "0"
            continue
            
        if item.RolledUpQuoteItem.startswith(SuperParentRolledUpQuoteItem + '.'):
            item["QI_Year"].Value = Year
            item["QI_Year_Visibility"].Value = "0"


if Quote.GetCustomField("Quote Type").Content == 'Projects':
    for item in ITEMS:
        IsMultiYear = False
        if item.PartNumber == "Migration" :
            for selAttr in item.SelectedAttributes:
                if selAttr.Name == "LCM_Multiyear_Selection":
                    IsMultiYear = True
                    for val in selAttr.Values:
                        populateYears(item.RolledUpQuoteItem,(val.ValueCode))
        
            if IsMultiYear == False:
                populateYears(item.RolledUpQuoteItem,'')
            
            break
    
    Quote.Save(False)
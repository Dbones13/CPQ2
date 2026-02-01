#---------------------------------------------------------------------------------------------------------
#					Change History Log
#---------------------------------------------------------------------------------------------------------
# Description: To Populate Year in All Quote Line Items.
# JIRA Ref.  : CXCPQ-63663
# Author     : H542824
# Created Date : 13-09-2023
#----------------------------------------------------------------------------------------------------------
# Date 			Name					    Version     Comment
# 01-10-2023	Pratik Sanghani    			1  	        Initial Version
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
    for item in arg.QuoteItemCollection:
        IsMultiYear = False
        if item.PartNumber == "Trace Software":
            for selAttr in item.SelectedAttributes:
                if selAttr.Name == "LCM_Multiyear_Selection":                    
                    for val in selAttr.Values:
                        if val.ValueCode != "No Multi-year":
                            IsMultiYear = True
                            populateYears(item.RolledUpQuoteItem,val.ValueCode)
                    
            if IsMultiYear == False:
                populateYears(item.RolledUpQuoteItem,'')

            break
    
    Quote.Save(False)
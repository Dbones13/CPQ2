#---------------------------------------------------------------------------------------------------------
#                    Change History Log
#---------------------------------------------------------------------------------------------------------
# Description: To Populate Year in All Quote Line Items.
# JIRA Ref.  : CXCPQ-63376
# Author     : H542824
# Created Date : 13-09-2023
#----------------------------------------------------------------------------------------------------------
# Date             Name                        Version     Comment
# 27-10-2023    Pratik Sanghani               1            Initial Version
#----------------------------------------------------------------------------------------------------------

def populate_years(super_parent_rolled_up_quote_item, year):
    """Populate year and visibility for quote items."""
    for item in Quote.MainItems:
        if item.RolledUpQuoteItem == super_parent_rolled_up_quote_item or item.RolledUpQuoteItem.startswith(super_parent_rolled_up_quote_item + '.'):
            item["QI_Year"].Value = year
            item["QI_Year_Visibility"].Value = "0"

def process_project_items(items):
    """Process project items to populate years."""
    for item in items:
        if item.PartNumber == "PRJT":
            is_multi_year = False
            for sel_attr in item.SelectedAttributes:
                if sel_attr.Name == "LCM_Multiyear_Selection":
                    is_multi_year = True
                    for val in sel_attr.Values:
                        populate_years(item.RolledUpQuoteItem, val.ValueCode)
            if not is_multi_year:
                populate_years(item.RolledUpQuoteItem, '')
            break

if Quote.GetCustomField("Quote Type").Content == 'Projects':
    process_project_items(arg.QuoteItemCollection)
    Quote.Save(False)

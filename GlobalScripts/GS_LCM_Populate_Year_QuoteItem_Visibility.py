#---------------------------------------------------------------------------------------------------------
#					Change History Log
#---------------------------------------------------------------------------------------------------------
# Description: To Populate Year Visibility in All Quote Line Items.
# JIRA Ref.  : CXCPQ-63663
# Author     : H542824
# Created Date : 20-10-2023
#----------------------------------------------------------------------------------------------------------
# Date 			Name					    Version     Comment
# 20-10-2023	Pratik Sanghani    			7 	        Initial Version
# 10-11-2023	Pratik Sanghani    			13 	        Event change
#----------------------------------------------------------------------------------------------------------

Multi_Year = Quote.GetCustomField("CF_Multiyear_Project").Content

for item in Quote.MainItems:
    if Multi_Year == 'Yes':
        if (len(list(item.AsMainItem.Children)) > 0) or (item.ParentItemGuid):
            item["QI_Year_Visibility"].Value = "0"
        else:
            item["QI_Year_Visibility"].Value = "1"
    else:
        item["QI_Year_Visibility"].Value = "0"

Quote.Save(False)
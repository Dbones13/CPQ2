#---------------------------------------------------------------------------------------------------------
#					Change History Log
#---------------------------------------------------------------------------------------------------------
# Description: To Populate Year in WriteIn Quote Line Items.
# JIRA Ref.  : CXCPQ-63379,CXCPQ-63380
# Author     : H542824
# Created Date : 20-10-2023
#----------------------------------------------------------------------------------------------------------
# Date 			Name					    Version     Comment
# 1-11-2023	 	Pratik Sanghani    			1 	        Initial Version
#----------------------------------------------------------------------------------------------------------

#Log.Write("Populate_LCM_Year : Start")
if Quote.GetCustomField("Booking LOB").Content != 'PMC':
	items = arg.QuoteItemCollection

	for item in items:
		for SelAttr in item.SelectedAttributes:
			for val in SelAttr.Values:
				if SelAttr.Name == "LCM_WriteIn_Year":
					item["QI_Year"].Value = val.Display
				elif SelAttr.Name == "LCM_WriteIn_Area":
					item["QI_Area"].Value = val.Display


#Quote.Save(False)
#Log.Write("Populate_LCM_Year : End")
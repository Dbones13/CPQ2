#This requirement Bypass to SAP validation for Incomplete configuration.
if (Quote.GetCustomField('Booking LOB').Content in ("PAS", "LSS") and Quote.GetCustomField('Quote Type').Content == "Projects"):
    for item in Quote.MainItems:
        if item.IsMainItem == True and item.IsComplete == False:
        #if item.IsComplete == False:
            item.IsComplete = True
if Session["prevent_execution"] != "true" and Quote.GetGlobal('PerformanceUpload') != 'Yes' and Quote.GetCustomField('Booking LOB').Content == "PMC":
    from GS_ExtendedETOCal import ExtendedETOCal
    ExtendedETOCal(Quote,Item)
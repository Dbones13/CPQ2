#This request is to set Default  execution country based on Booking Country
query1 = SqlHelper.GetFirst("SELECT Service_Team FROM MIQ_BCOUNTRY_SERVICETEAM_MAPPING WHERE Booking_Country = '{}' ".format(str(Quote.GetCustomField("Booking Country").Content)))
if query1 is not None:
    for value in Product.Attributes.GetByName("MIQ_Execution_Country").Values:
        if value.Display == query1.Service_Team:
            value.Display =query1.Service_Team
            value.IsSelected = True
            break
    for avalue in Product.Attributes.GetByName("MIQ_ACD_Execution_Country").Values:
        if avalue.Display == query1.Service_Team:
            avalue.Display =query1.Service_Team
            avalue.IsSelected = True
            break
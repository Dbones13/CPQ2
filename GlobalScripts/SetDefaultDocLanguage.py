query = "select Default_Language from COUNTRY_LANGUAGE_MAPPING where country='{}'".format(Quote.GetCustomField("Booking Country").Content)
country = SqlHelper.GetFirst(query).Default_Language

Quote.GetCustomField("Language").Content = country
import GS_CommonModule as cm

def setDefaultLanguage():
	query = TagParserQuote.ParseString("select Default_Language from COUNTRY_LANGUAGE_MAPPING where country='<*CTX(Quote.CustomField(Booking Country))*>'")

	res = SqlHelper.GetList(query)
	if res and len(res) > 0:
		cm.setCFValue(Quote , 'Language' , res[0].Default_Language)

if not cm.getCFValue(Quote , 'Language'):
	setDefaultLanguage()

#ScriptExecutor.ExecuteGlobal('GS_calculateParent')
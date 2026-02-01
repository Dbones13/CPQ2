if Quote.GetCustomField("Quote Tab Booking LOB").Content in ["PAS","LSS","HCP","CCC","PMC"] and Quote.GetCustomField("Quote Type").Content not in ["Contract New","Contract Renewal"]:
    #DocData = SqlHelper.GetList("Select TemplateName, TemplateCondition, UserType from Document_Conditions where TemplateStatus = 'Active'")
    DocData= SqlHelper.GetList("Select Template_Name, Condition, UserType from DOCUMENT_GENERATION_TEMPLATE_MAPPING where TemplateStatus = 'Active'")
    templateList=[dData.Template_Name for dData in DocData if (dData.UserType.lower() == 'all' or User.UserType.Name.lower() in list(map(str.strip, dData.UserType.lower().split(',')))) and TagParserQuote.ParseString(dData.Condition) =='1']
    Quote.SetGlobal('DocTempValues', str(tuple(templateList)).replace(",)",")"))
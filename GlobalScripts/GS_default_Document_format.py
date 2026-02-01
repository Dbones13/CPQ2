DocType = Quote.GetCustomField('Generate_document_Selection').Content
query = TagParserQuote.ParseString("select DocFormat from DOCUMENT_GENERATION_TEMPLATE_MAPPING where Template_Name='{}'".format(DocType))
res=SqlHelper.GetList(query)

if str(len(res))=='1':
    Quote.GetCustomField('Document_Generation_Format').Content = res[0].DocFormat
else:
    Quote.GetCustomField('Document_Generation_Format').Content = ''
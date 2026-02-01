FormatType = Quote.GetCustomField('Document_Generation_Format').Content
DocType = Quote.GetCustomField('Generate_document_Selection').Content
Formats={"EXCEL":GenDocFormat.EXCEL,"DOC":GenDocFormat.DOC,"PDF":GenDocFormat.PDF,"DOCX":GenDocFormat.DOCX}

if FormatType !=''and DocType !='':
	jsonObject = {}
	if DocType:
		templateName = DocType
		query = SqlHelper.GetFirst("select ScriptsName from DOCUMENT_GENERATION_TEMPLATE_MAPPING where Template_Name = '{}'".format(DocType))
		ScriptName=str(query.ScriptsName)

	if templateName:
		#added logic for Multilangauge --->> Start
		language_dict = {
				"English": "102",
				"French": "108",
				"German (HW)": "103",
				"Spanish": "107",
				"Portuguese": "106",
				"Korean": "105",
				"Chinese": "104"
			}

		# Set the "Customer's Language" custom field based on the lookup
		Lang= Quote.GetCustomField('Language').Content
		Quote.GetCustomField("Customer's Language").Content = language_dict.get(Lang, language_dict["English"])
		#added logic for Multilangauge --->> END
		if ScriptName not in ['None','']:
			ScriptExecutor.Execute(ScriptName)
		Quote.GenerateDocument(templateName, Formats[FormatType])
		#jsonObject['href'] = TagParserQuote.ParseString('<*CTX( Quote.LastGeneratedDocument.Link )*>').replace('http','https')
	#ApiResponse = ApiResponseFactory.JsonResponse(jsonObject)
else:
	Quote.Messages.Add('Please Select categary, Document & Format Option')
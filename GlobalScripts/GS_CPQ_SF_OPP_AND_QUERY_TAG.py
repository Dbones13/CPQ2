def CPQ_SF_OPP_AND_QUERY_TAG(Quote):
	Quote.GetCustomField('CF_RecordTypeId').Content = ScriptExecutor.Execute('CPQ_SF_OPP_TAG', {"PROPERTY": "RecordTypeId"})
	Quote.GetCustomField('CF_Opprtunity_Sales_Field_Value').Content = ScriptExecutor.Execute('CPQ_SF_QUERY_TAG', {"QUERY": "SELECT+Name+FROM+RecordType+WHERE+Id='"+Quote.GetCustomField('CF_RecordTypeId').Content+"'"})
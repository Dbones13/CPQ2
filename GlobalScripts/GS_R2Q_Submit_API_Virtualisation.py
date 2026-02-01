Log.Info('R2Q Virtualisation API =>> Payload: {}'.format(str(JsonHelper.Serialize(Param).encode("ascii", "replace").replace('?','')).strip()))
try:
	param = eval(str(JsonHelper.Serialize(Param).encode("ascii", "replace").replace('?','')).strip().replace('null', '""'))
	if param.get('DataType', '') == 'Virtualization Data':
		ScriptExecutor.ExecuteGlobal('GS_R2Q_Virtualization_Mapping', JsonHelper.Serialize(Param))
	elif param.get('DataType', '') == 'TAS Data':
		Log.Info('R2Q TAS API =>> Payload: {}'.format(str(JsonHelper.Serialize(Param).encode("ascii", "replace").replace('?','')).strip()))
		ScriptExecutor.ExecuteGlobal('GS_R2Q_TAS_Parts_LineItem', JsonHelper.Serialize(Param))
	elif param.get('DataType', '') == 'Bom Generated':
		Log.Info('R2Q Bom Generated API =>> Payload: {}'.format(str(JsonHelper.Serialize(Param).encode("ascii", "replace").replace('?','')).strip()))
		param = eval(JsonHelper.Serialize(Param).replace('null', '""'))
		Quote = QuoteHelper.Edit(str(param["CPQQuoteNumber"]))
		import GS_R2Q_FunctionalUtil
		GS_R2Q_FunctionalUtil.UpdateStatusMessage(Quote, "Egap Initiation" if "Quote submitted but egap approval required" in str(param["Messagetext"]) else "Final", "Action", str(param["Messagetext"]))
	elif param.get('DataType', '') == 'Marshalling':
		Log.Info('R2Q Marshalling =>> Payload: {}'.format(str(JsonHelper.Serialize(param))))
		ScriptExecutor.ExecuteGlobal('GS_R2QPRJT_PS_Marshalling_Update', JsonHelper.Serialize(param))
	else:
		Log.Info('R2Q Invalid DataType API =>> Payload: {}'.format(str(JsonHelper.Serialize(Param).encode("ascii", "replace").replace('?','')).strip()))
except Exception as ex:
	Log.Info('R2Q Virtualisation API =>> Error: {}'.format(str(ex)))
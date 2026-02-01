if Quote.GetGlobal('PerformanceUpload') != 'Yes':
	import GS_CalculateTotals as tcUtil
	if Session["prevent_execution"] != "true":
		tcUtil.calculateParent(Quote)
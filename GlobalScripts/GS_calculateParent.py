import GS_CalculateTotals as tcUtil
#ScriptExecutor.ExecuteGlobal('GS_GetQuoteStatus')
if Session["prevent_execution"] != "true":
	tcUtil.calculateParent(Quote)
def check_approval_status(quote):
	quote.GetCustomField('Is_pendingApprovalProcess').Content = ''
	revisionQuery = SqlHelper.GetFirst("Select OrderStatus from Quotes(nolock) where cartID = '{}' and OrderStatus in ('Ready for Approval','Awaiting Approval') Order By OrderStatus DESC ".format(quote.CompositeNumber))
	if revisionQuery:
		quote.GetCustomField('Is_pendingApprovalProcess').Content = '1'

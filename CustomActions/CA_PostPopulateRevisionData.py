if Quote.GetCustomField('EGAP_Proposal_Type').Content == 'Firm' and Quote.GetCustomField('Revised proposal type').Content == 'Booking':
    query = "select TOP 1000 * from cart_revisions where parent_id = '{}' and VISITOR_ID = '{}' order by CART_ID desc".format(Quote.QuoteId , Quote.UserId)
    res = SqlHelper.GetFirst(query)

    Quote.CustomFields.AssignValue('Booking Revision' , "Revision - {}".format(res.REVISION_ID))
    Quote.Save(False)
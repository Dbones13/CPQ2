###############################################################################################
#       Class CL_QuoteHandler:
#       Class to get Quote Custom Field data by Quote Number
###############################################################################################
class CL_QuoteHandler:

	def __init__(self, QuoteNumber):
		QuoteNumber = self.GetRevisionQuote(QuoteNumber)
		self.QuoteNumber = QuoteNumber
		self.CartID = int(self.QuoteNumber[4:])
		self.UserID = int(self.QuoteNumber[:4])

	###############################################################################################
	# Function to Get Quote Custom Field Data using Strong Name
	###############################################################################################
	def GetFieldValues(self, FieldList):
		FieldData = SqlHelper.GetList("select s.PARAMID as ID, d.StrongName as Name, s.Content as Value from scparams s (NOLOCK) INNER JOIN ScParamDefnNew d on s.PARAMID = d.ScParamId where s.Cart_ID={} and s.UserID= {} and d.StrongName in {}".format(self.CartID, self.UserID, str(tuple(FieldList)).replace(',)',')')))
		return FieldData

	###############################################################################################
	# Function to Get the Quote Composite Number based on Revision
	###############################################################################################
	def GetRevisionQuote(self, QuoteNumber):
		if('-' in QuoteNumber):
			QuoteNo = QuoteNumber.split('-')
			if len(QuoteNumber)>0:
				CartID = QuoteNo[0][4:]
				UserID = QuoteNo[0][:4]
				revisionData = SqlHelper.GetList('''SELECT cr.*, cart.ACTIVE_REV, cart.DATE_CREATED, cart.DATE_MODIFIED, cart.ORDER_STATUS, (osd.ORDER_STATUS_NAME) as OrderStatusName FROM CART_REVISIONS cr JOIN CART cart ON cr.VISITOR_ID=cart.USERID AND cr.CART_ID=cart.CART_ID JOIN ORDER_STATUS_DEFN osd ON cart.ORDER_STATUS = osd.ORDER_STATUS_ID WHERE VISITOR_ID={} AND MASTER_ID={}'''.format(UserID,CartID))
				if revisionData:
					for row in revisionData:
						if str(row.REVISION_ID) == QuoteNo[1]:
							CartID = row.CART_ID
							break
					return "{}{}".format(str(UserID).zfill(4), str(CartID).zfill(4))
				else:
					return QuoteNo[0]
			else:
				return QuoteNo[0]
		else:
			return QuoteNumber

	###############################################################################################
	# Function to Get Quote Line Item's Discounts
	###############################################################################################
	def GetQuoteLineItemDiscounts(self):
		pQuoteDiscounts = {}
		ptable = SqlHelper.GetList("SELECT ct.ID, ct.CART_ITEM, ct.CATALOGCODE, ct.DESCRIPTION, c.cart_id, c.userid, c.QI_SC_StartDate, c.QI_SC_ItemFlag, c.QI_MPA_Discount_Percent, c.QI_Additional_Discount_Percent FROM CartItemCustomFields c join CART_ITEM ct on c.CART_ITEM_id = ct.id where c.cart_id = '{CartID}' and c.userid = '{UserID}' and c.QI_SC_ItemFlag <> '0000' and c.QI_SC_StartDate = (SELECT MIN(QI_SC_StartDate) FROM CartItemCustomFields where cart_id = '{CartID}' and userid = '{UserID}')".format(CartID = self.CartID, UserID = self.UserID))
		for row in ptable:
			qDiscounts = {}
			Trace.Write("{}, {}".format(row.ID, row.QI_SC_StartDate))
			qDiscounts['PartNumber'] = row.CATALOGCODE
			qDiscounts['Description'] = row.DESCRIPTION
			qDiscounts['UniqueText'] = row.CATALOGCODE + '-#-' + row.DESCRIPTION
			qDiscounts['QI_MPA_Discount_Percent'] = row.QI_MPA_Discount_Percent
			qDiscounts['QI_Additional_Discount_Percent'] = row.QI_Additional_Discount_Percent
			pQuoteDiscounts[row.CATALOGCODE + '-#-' + row.DESCRIPTION] = qDiscounts
		return pQuoteDiscounts
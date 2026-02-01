def traceEvent(scriptName , msg):
	Trace.Write("script executed {} : {}".format(scriptName , msg))

def getCF(quote, cfName):
	return quote.GetCustomField(cfName)

def hideCF(customField):
	customField.Visible = False

def showCF(customField):
	customField.Visible = True

def getCFValue(Quote, CF_Name):
	return Quote.GetCustomField(CF_Name).Content

def setCFValue(Quote, CF_Name, CF_Value):
	Quote.GetCustomField(CF_Name).Content = CF_Value

def getFloat(Var):
	if Var:
		return float(Var)
	return 0

def GetQuoteTable(Quote,Name):
	return Quote.QuoteTables[Name]


def setAccessReadonly(table):
	table.AccessLevel = table.AccessLevel.ReadOnly
	table.Save()

# def setAccessEditable(table):
#     table.AccessLevel = table.AccessLevel.Editable

def hideQuoteTableColumn(table,column):
	table.GetColumnByName(column).AccessLevel = table.AccessLevel.Hidden

def hideQuoteTable(Quote,tableName):
	table = Quote.QuoteTables[tableName]
	table.AccessLevel = table.AccessLevel.Hidden

def showQuoteTableColumn(table,column,isEditable):
	if isEditable:
		table.GetColumnByName(column).AccessLevel = table.AccessLevel.Editable
	else:
		table.GetColumnByName(column).AccessLevel = table.AccessLevel.ReadOnly

def setCFReadonly(customField):
	customField.Editable = False

def updateExpirationDate(Quote , TagParserQuote):
	validity = getCFValue(Quote , "Proposal Validity")
	validity = validity.split(' ')[0]

	expirationDate = TagParserQuote.ParseString("<*CTX( Date.AddDays({}) )*>".format(validity))

	setCFValue(Quote , 'Quote Expiration Date' , expirationDate)


def GetApprovalLevel(quoteType, LOB, targetSellPrice, discount, proposalType='Parts & Spots', limitType='Discount',bookingCountry='',sfdcquotetype =''):
	#Trace.Write("Here Goes")
	result = None
	if discount < 0:
		discount = 0
	'''elif discount < 1:
		discount = 1'''
	# if (LOB in ["LSS", "PAS", "CCC","HCP"]):
	if(sfdcquotetype == 'Software Only') and LOB == 'HCP':
		Sql_Stmt_Lst = ["SELECT TOP 1000 ISNULL(ApprovalLevel,'{5}') as ApprovalLevel FROM SEA_APPROVAL_DISCOUNT_MATRIX_SWONLY ",
                    "WHERE (Cast(MinimumSellPrice  as Float) <= {0} AND Cast(MaximumSellPrice as Float) >= {0}) AND ",
                    " (Cast(MinimumLimit as Float) <= {1} AND Cast(MaximumLimit as Float) >= {1}) AND ",
                    " LOB = '{2}' AND ProposalType ='{3}' AND LimitType ='{4}' AND coalesce(BookingCountry,'') in ('{6}','')",
                    " Order By BookingCountry DESC"
                    ]
	else:
		Sql_Stmt_Lst = ["SELECT TOP 1000 IIF(ApprovalLevel !='', ApprovalLevel , '{5}') as ApprovalLevel FROM SEA_APPROVAL_DISCOUNT_MATRIX ",
                    "WHERE (Cast(MinimumSellPrice  as Float) <= {0} AND Cast(MaximumSellPrice as Float) >= {0}) AND ",
                    " (Cast(MinimumLimit as Float) <= {1} AND Cast(MaximumLimit as Float) >= {1}) AND ",
                    " LOB = '{2}' AND ProposalType ='{3}' AND LimitType ='{4}' AND coalesce(BookingCountry,'') in ('{6}','')",
                    " Order By BookingCountry DESC"
                    ]
	approvalLevel = 'No P&M Approval'
	if LOB in ["PAS", "CCC", "LSS"]:
		approvalLevel = 'Functional Approvals Only'
        if proposalType == 'Budgetary':
            approvalLevel = 'No Approval'
	sqlQuery = "".join(Sql_Stmt_Lst).format(targetSellPrice, discount, LOB, proposalType, limitType, approvalLevel,bookingCountry)
	Trace.Write(sqlQuery)
	result = SqlHelper.GetFirst(sqlQuery)
	return result

def exchangerate(Quote):
	if getCFValue(Quote, 'Booking LOB') == 'CCC':
		res = SqlHelper.GetFirst("SELECT Exchange_Rate FROM CURRENCY_EXCHANGERATE_MAPPING_CCC WHERE From_Currency = 'USD' AND To_Currency = '"+str(Quote.GetCustomField('Currency').Content)+"'")
	else:
		res = SqlHelper.GetFirst("SELECT Exchange_Rate FROM Currency_ExchangeRate_Mapping WHERE From_Currency = 'USD' AND To_Currency = '"+str(Quote.GetCustomField('Currency').Content)+"'")
	if res:
		Quote.GetCustomField('Exchange Rate').Content = res.Exchange_Rate
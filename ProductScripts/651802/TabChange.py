if(str(arg.NameOfCurrentTab) == 'Part Summary'):
	Product.ParseString('<*CTX( Container(AR_Cyber_PartsSummary).Column(Adj Quantity).SetPermission(ReadOnly) )*>')
	Product.ParseString('<*CTX( Container(AR_Cyber_PartsSummary).Column(Comments).SetPermission(ReadOnly) )*>')
if sender.StrongName == 'EGAP_Proposal_Type':
	from GS_PopulateMarketScheduleDiscount import PopulateMarketScheduleDiscount
	GS_PopulateMarketScheduleDiscount.PopulateMarketScheduleDiscount(Quote)
elif sender.StrongName == 'SC_CF_AGREEMENT_TYPE':
	from GS_SC_QUOTE_TABLE_VIEW_CONTROL import SC_QUOTE_TABLE_VIEW_CONTROL
	from GS_SC_Custom_Field_Visibility import GS_SC_Custom_Field_Visibility
	SC_QUOTE_TABLE_VIEW_CONTROL(Quote)
	GS_SC_Custom_Field_Visibility(Quote,User)
elif sender.StrongName == 'SC_CF_ORDER_REASON':
	from GS_SC_AllowEGAPCustomFields import SC_AllowEGAPCustomFields
	SC_AllowEGAPCustomFields(Quote)
elif sender.StrongName == 'Change Proposal Type':
	from GS_SetEgapProposalType import SetEgapProposalType
	SetEgapProposalType(Quote)
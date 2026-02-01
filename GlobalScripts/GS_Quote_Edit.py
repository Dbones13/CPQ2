#-- This Script is responsible for Quote Edit Event
from GS_CommonModule import GetQuoteTable,setAccessReadonly,hideQuoteTableColumn,getCFValue,exchangerate,hideCF,getCF,showCF,setCFValue,setCFReadonly
from GS_GetOpportunityDetails import GetOpportunityDetails
from GS_Display_Warning_Message import Laborwarningmessage
from GS_Set_Default_Plant import Set_Default_Plant

if Quote.OrderStatus.Name == 'Preparing':
	exchangerate(Quote)
from GS_MarketModule import marketinit
marketinit(Quote) #This function will set the market and Pricebook.

if getCFValue(Quote , 'CF_RecordTypeId') =='':
	from GS_CPQ_SF_OPP_AND_QUERY_TAG import CPQ_SF_OPP_AND_QUERY_TAG
	CPQ_SF_OPP_AND_QUERY_TAG(Quote) #This function is setting the recordId

#GS_GetOpportunityDetails
GetOpportunityDetails(Quote,TagParserQuote,Session)

if Quote.OrderStatus.Name == 'Ready for Approval':
	from GS_BackToPreparing import BackToPreparing
	BackToPreparing(Quote)
elif Quote.OrderStatus.Name == 'Awaiting Approval':
	from GS_CheckApprovalStatus import check_approval_status
	check_approval_status(Quote)
elif Quote.OrderStatus.Name == 'Preparing':
	if getCFValue(Quote , "Booking LOB") in ('PMC','LSS', 'HCP') and getCFValue(Quote , "Quote Type") not in ('Contract New','Contract Renewal'):
		Set_Default_Plant(Quote)
	if getCFValue(Quote , "Quote Type") == "Projects" and getCFValue(Quote , "MPA") == "" and getCFValue(Quote , "Booking LOB") in ('PAS','LSS'):
		from GS_PopulateMarketScheduleDiscount import PopulateMarketScheduleDiscount
		PopulateMarketScheduleDiscount(Quote)
	#GS_PROS_Column_Visibility
	if User.BelongsToPermissionGroup('Estimator-ProsGuidanceAccess'):
		from GS_PROS_Column_Visibility import user_epga
		user_epga(Quote,User)
	else:
		from GS_PROS_Column_Visibility import hideqtcolumn
		hideqtcolumn(Quote)
#	if getCFValue(Quote , "MPA") != "":
	if getCFValue(Quote , "MPA") != "" and getCFValue(Quote , "MPA Price Plan") == '':
		#Log.Info("Before--->"+str(getCFValue(Quote , "MPA Price Plan")))
		#Log.Info("Before--->"+str(getCFValue(Quote , "MPA")))
		from GS_SetDefaultPricePlan import setDefaultMpa
		setDefaultMpa(Quote, TagParserQuote)
		#Log.Info("After--->"+str(getCFValue(Quote , "MPA Price Plan")))
		#Log.Info("After--->"+str(getCFValue(Quote , "MPA")))
		
	#SC Scripts
	if getCFValue(Quote , "Quote Type") in ['Contract New','Contract Renewal']:
		from GS_SC_QUOTE_TABLE_VIEW_CONTROL import SC_QUOTE_TABLE_VIEW_CONTROL
		from GS_SC_Custom_Field_Visibility import GS_SC_Custom_Field_Visibility
		from GS_SC_AllowEGAPCustomFields import SC_AllowEGAPCustomFields

		if Quote.OrderStatus.Name in ("Accepted by Customer","GCC Handover","ERP Contract Created","Booked") and not getCFValue(Quote , "CF_Plant") :
			Set_Default_Plant(Quote)
        #GS_SC_QUOTE_TABLE_VIEW_CONTROL
		SC_QUOTE_TABLE_VIEW_CONTROL(Quote)

		#GS_SC_Custom_Field_Visibility
		GS_SC_Custom_Field_Visibility(Quote,User)

		#GS_SC_AllowEGAPCustomFields
		SC_AllowEGAPCustomFields(Quote)

		#GS_SC_SFDC_Role_Validation
		from GS_SC_SFDC_Role_Validation import SC_SFDC_Role_Validation
		SC_SFDC_Role_Validation(Quote)

#GS_PopulateOrderBookingErrorQuoteTable
elif Quote.OrderStatus.Name in ('Pending Project Creation','Pending Order Confirmation','Accepted by Customer', 'Project Created'):# and Quote.QuoteTables["Order_Booking_Error"].Rows.Count > 0:
	from GS_PopulateOrderBookingErrorQuoteTable import PopulateOrderBookingErrorQuoteTable
	PopulateOrderBookingErrorQuoteTable(Quote)

#GS_Make ReadOnly Fields
elif Quote.OrderStatus.Name != 'Preparing':
	from GS_Make_ReadOnlyFields import readonly
	readonly(Quote)
if getCFValue(Quote , "Quote Tab Booking LOB") == "PMC" and getCFValue(Quote , "Quote Type") == "Parts and Spot":
	from GS_Make_ReadOnlyFields import hidecol
	hidecol(Quote,User)
#from GS_UpdateRevisionData import UpdateRevisionData
#UpdateRevisionData(Quote)

'''if Quote.Items.Count > 0:
	if getCFValue(Quote , "Booking LOB") in ["LSS", "PAS"] and Quote.GetCustomField('Quote Type').Content == "Projects" and Quote.OrderStatus.Name in ['Preparing', 'Ready for Approval', 'Rejected']:
		from GS_CommonConfig import CL_CommonSettings as CS
		from GS_Execution_Year_Error_Message import Quote_Items
		Quote_Items(CS, Quote)'''

'''from Gs_BeforeRendering import BeforeRendering
BeforeRendering(Quote)'''
"""if Quote.GetCustomField("isR2QRequest").Content in ('yes','Yes','YES','True','true','True'):
	from GS_R2Q_Gendocrecal import R2qrecall
	editval=Session['editsession']
	mir2qedi=Session['r2qreprice']
	Log.Info("mir2qedi"+str(mir2qedi)+str(editval))
	R2qrecall(Quote,editval,mir2qedi)
	Session['editsession']=''
	Session['r2qreprice']=''"""
#Field Visibility
if getCFValue(Quote, "Booking LOB") in ('LSS', 'PAS', 'HCP'):
	if getCFValue(Quote , "MPA") != '' and getCFValue(Quote , "MPA Price Plan") != '':
		hideCF(getCF(Quote, "Recommended Discount Plan"))
		hideCF(getCF(Quote, "Selected Discount Plan"))
		hideCF(getCF(Quote, "Schedule Price Plan Updated"))
	else:
		showCF(getCF(Quote, "Recommended Discount Plan"))
		showCF(getCF(Quote, "Selected Discount Plan"))
		showCF(getCF(Quote, "Schedule Price Plan Updated"))
		hideCF(getCF(Quote, "MPA Price Plan"))
		hideCF(getCF(Quote, "MPA Validity"))
		hideCF(getCF(Quote, "MPA Threshold"))
		hideCF(getCF(Quote, "MPA Honeywell Ref"))
		setCFValue(Quote, "Schedule Price Plan Updated", "True")
if getCFValue(Quote, "Booking LOB") != 'CCC':
	hideCF(getCF(Quote, 'Exchange Rate'))
if getCFValue(Quote, "Booking LOB") == 'HCP' and getCFValue(Quote, "Quote Type") == "Parts and Spot":
	hideCF(getCF(Quote, 'CF_ProjectId'))
if getCFValue(Quote, "Booking LOB") != "PMC":
	hideCF(getCF(Quote, "PMC Type"))
	hideCF(getCF(Quote, "PMC Product Family"))
	hideCF(getCF(Quote, "PMC Product Line"))
elif getCFValue(Quote, "Booking LOB") == "PMC":
	hideCF(getCF(Quote, "MPA Threshold"))
	hideCF(getCF(Quote, "MPA Price Plan"))
	hideCF(getCF(Quote, "MPA Validity"))
	hideCF(getCF(Quote, "MPA Honeywell Ref"))
	setCFReadonly(getCF(Quote, "PMC Type"))
	setCFReadonly(getCF(Quote, "PMC Product Family"))
	setCFReadonly(getCF(Quote, "PMC Product Line"))
	if getCFValue(Quote, "Quote Type") == "Projects":
		showCF(getCF(Quote, "EGAP_Proposal_Type"))
	elif getCFValue(Quote, "Quote Type") == "Parts and Spot":
		hideCF(getCF(Quote, 'Discount Request Reason'))
		if not User.BelongsToPermissionGroup('PMC WTW Cost Access Group'):
			hideCF(getCF(Quote, "TotalwtwMarginPercent"))
Laborwarningmessage(Quote)
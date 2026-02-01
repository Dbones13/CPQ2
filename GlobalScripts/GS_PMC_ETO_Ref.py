# ========================================================================================================
#   Component: GS_PMC_ETO_Ref
#   Copyright: Honeywell Inc
#   Purpose: - This script is called from Header Template.Returns unique ETO reference IDs based on PartNumber.
# ========================================================================================================
def fn_get_eto_ref(yetotable):
	if yetotable=='QT__PMC_ETO_Selection':
		col_ref='ETO_Ref_No'
		col_pnotes='ETO_Proposal_Notes'
	else:
		col_ref=''
		col_pnotes=''
	if col_ref!='' and col_pnotes!='':
		yspec_quote = SqlHelper.GetList("SELECT DISTINCT {} as 'ETO_REF' FROM {} where PartNumber = '{}'".format(col_ref,yetotable,Product.PartNumber))
		if yspec_quote:
			st_it = '<select id="eto_refnos"><option value="none" selected disabled hidden>Select an Option</option>'
			for qt in yspec_quote:
				st_it +='<option value="'+ qt.ETO_REF +'">'+ qt.ETO_REF +'</option>'
		else:
			st_it='<select id="eto_refnos"><option value="none" selected disabled hidden>Select an Option</option>'
	else:
		st_it='<select id="eto_refnos"><option value="none" selected disabled hidden>Select an Option</option>'
	refNumObj = SqlHelper.GetList("SELECT * FROM CUSTOMIZED_SPECIAL_REFERENCE_NUMBER where PartNumber = '{}'".format(Product.PartNumber))
	refNum = []
	if refNumObj:
		for row in refNumObj:
			for i in range(1,11):
				ref = eval("row.Reference"+str(i))
				if ref != '':
					st_it +='<option value="'+ ref +'">'+ ref +'</option>'
				else:
					break
	return st_it

lv_FamilyCode = Param.FamilyCode
yetotable = "QT__PMC_ETO_Selection"

lv_eto_ref = fn_get_eto_ref(yetotable)
ApiResponse = ApiResponseFactory.JsonResponse(str(lv_eto_ref))
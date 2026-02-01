try:
    prev_c_start_date = Product.Attr('PreviousQuoteCStartDate_EnabledServices').GetValue()
    prev_c_end_date = Product.Attr('PreviousQuoteCEndDate_EnabledServices').GetValue()
    currnt_start_date = Product.Attr('ContractStartDate_EnabledService').GetValue()
    current_end_date = Product.Attr('ContractEndDate_EnabledService').GetValue()
    dummy_start_date = Product.Attr('Compare_StartDate_SESP').GetValue()
    dummy_end_date = Product.Attr('Compare_EndDate_SESP').GetValue()
    if prev_c_start_date:
        ps = DateTime.ParseExact(prev_c_start_date,"M/d/yyyy",CultureInfo.InvariantCulture)
    if prev_c_end_date:
        pe = DateTime.ParseExact(prev_c_end_date,"M/d/yyyy",CultureInfo.InvariantCulture)
    ds = DateTime.ParseExact(dummy_start_date,"M/d/yyyy",CultureInfo.InvariantCulture)
    de = DateTime.ParseExact(dummy_end_date,"M/d/yyyy",CultureInfo.InvariantCulture)
    com_be_PS_DS = DateTime.Compare(ps,ds)
    com_be_PE_DE = DateTime.Compare(pe,de)
    if com_be_PS_DS != 0:
        Product.Attr('PreviousQuoteCStartDate_EnabledServices').AssignValue(dummy_start_date)
        Product.Attr('ContractStartDate_EnabledService').AssignValue(dummy_start_date)
    if com_be_PE_DE != 0:
        prev_c_end_date = Product.Attr('PreviousQuoteCEndDate_EnabledServices').AssignValue(dummy_end_date)
        current_end_date = Product.Attr('ContractEndDate_EnabledService').AssignValue(dummy_end_date)
except:
	Trace.Write('====Error Occured in AssignConfigPrevDate Enabled Service Model======')
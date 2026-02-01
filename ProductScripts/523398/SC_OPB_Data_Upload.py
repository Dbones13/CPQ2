if Quote.GetCustomField("Quote Type").Content=="Contract Renewal" and Quote.GetCustomField("SC_CF_PREVIOUS_QUOTE_NO").Content=='':
    Product.Attr('SC_OPB_Data_upload_flag_renewal').AssignValue('True')
    if Product.Attr('SC_OBP_upload_flag').GetValue() !='OPB_Applied':
        Product.Attr('SC_OPB_Data_upload_flag_renewal_msg').AssignValue('True')
    else:
        Product.Attr('SC_OPB_Data_upload_flag_renewal_msg').AssignValue('False')
else:
    Product.Attr('SC_OPB_Data_upload_flag_renewal').AssignValue('False')
def calc_profib_conn(parts_dict, attrs):
    #CXCPQ-21360
	parts_dict['6ES7972-0BA42-0XA0'] = attrs.profib_conn_rs485
	parts_dict['6ES7972-0BB42-0XA0'] = attrs.profib_conn_rs485_PGSST
	parts_dict['6ES7972-0BA52-0XA0'] = attrs.profib_fastconn_rs485
	parts_dict['6ES7972-0BB52-0XA0'] = attrs.profib_fastconn_rs485_PGSST
	
    #CXCPQ-21369
	parts_dict['6ES7153-2BA70-0XB0'] = attrs.dp_pa_link
	parts_dict['6ES7157-0AC85-0XA0'] = attrs.dp_pa_coupler
    
    #CXCPQ-21363
	parts_dict['6ES7972-0DA00-0AA0'] = attrs.active_te
    
	return parts_dict
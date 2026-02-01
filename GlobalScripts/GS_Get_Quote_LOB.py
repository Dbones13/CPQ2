if Quote is not None:
    ret_val=Quote.GetCustomField('Booking LOB').Content
    Trace.Write('ret_val:'+str(ret_val))
    #Send the response to the API Called
    ApiResponse = ApiResponseFactory.JsonResponse(ret_val)
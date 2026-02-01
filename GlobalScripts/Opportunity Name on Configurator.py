if Quote is not None:
    oppty_name = Quote.GetCustomField('Opportunity Name').Content

    if oppty_name != "":
        ApiResponse = ApiResponseFactory.JsonResponse(oppty_name)
else:
    ApiResponse = ApiResponseFactory.JsonResponse("New / Expansion Project")
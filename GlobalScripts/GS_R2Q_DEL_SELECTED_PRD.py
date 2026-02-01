#if Product.Attr("R2QRequest").GetValue() == "Yes":
selc_prod = Product.GetContainerByName('AR_HCI_SUBPRD')
no_popup = 0
if Param.action == 'change':
    if selc_prod.Rows.Count > 0:
        no_popup = 1
        ApiResponse = ApiResponseFactory.JsonResponse(no_popup)
elif Param.action == 'ok':
    if selc_prod.Rows.Count > 0:
        delprd = []
        for prd in selc_prod.Rows:
            delprd.append(prd.RowIndex)
        delprd.reverse()
        for row in delprd:
            selc_prod.DeleteRow(row)
elif Param.action == 'cancel':
    Trace.Write('cancel---'+str(Product.Attr('AR_HCI_SCOPE').GetValue()))
    swap_scope = {"Software":"Software + Labor","Software + Labor":"Software"}
    Product.Attr('AR_HCI_SCOPE').SelectDisplayValue(swap_scope.get(Product.Attr('AR_HCI_SCOPE').GetValue()),'')
scope = Product.Attr('AR_HCI_SCOPE').GetValue()
if scope == "Software" and Param.action != 'change':
    Product.Attr("Header_02_open").Access = AttributeAccess.Hidden
    Product.Attr("ATTCON_02_open").Access = AttributeAccess.Hidden
    Product.Attr("AR_HCI_GES Participation %").Access = AttributeAccess.Hidden
    Product.Attr("AR_HCI_GES Location").Access = AttributeAccess.Hidden
    Product.Attr("R2Q_Alternate_Execution_Country").Access = AttributeAccess.Hidden
    Product.Attr("Project_Execution_Year").Access = AttributeAccess.Hidden
    Product.Attr("ATTCON_02_close").Access = AttributeAccess.Hidden
    Product.Attr("Header_02_close").Access = AttributeAccess.Hidden
elif scope == "Software + Labor" and Param.action != 'change':
    Product.Attr("Header_02_open").Access = AttributeAccess.Editable
    Product.Attr("ATTCON_02_open").Access = AttributeAccess.Editable
    Product.Attr("AR_HCI_GES Participation %").Access = AttributeAccess.Editable
    Product.Attr("AR_HCI_GES Location").Access = AttributeAccess.Editable
    Product.Attr("R2Q_Alternate_Execution_Country").Access = AttributeAccess.Editable
    Product.Attr("Project_Execution_Year").Access = AttributeAccess.Editable
    Product.Attr("ATTCON_02_close").Access = AttributeAccess.Editable
    Product.Attr("Header_02_close").Access = AttributeAccess.Editable
Product.ApplyRules()
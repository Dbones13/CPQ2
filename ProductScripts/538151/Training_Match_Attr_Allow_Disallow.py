container_Entitlements = Product.GetContainerByName("SC_Entitlements")
if container_Entitlements is not None:
    for row in container_Entitlements.Rows:
        if row['Entitlement'] == 'Training Match':
            if row.IsSelected:
                Product.Attr('SC_Training_Match_Contract_Value').Allowed = True
                Product.Attr('SC_Training_Match_Contract_Value_Percent').Allowed = True
                Product.Attr('SESP_Training_Match_Flag').AssignValue("1")
            else:
                Product.Attr('SC_Training_Match_Contract_Value').Allowed = False
                Product.Attr('SC_Training_Match_Contract_Value_Percent').Allowed = False
                Product.Attr('SESP_Training_Match_Flag').AssignValue("0")
if container_Entitlements and container_Entitlements.Rows.Count == 0:
    Product.Attr('SC_Training_Match_Contract_Value').Allowed = False
    Product.Attr('SC_Training_Match_Contract_Value_Percent').Allowed = False

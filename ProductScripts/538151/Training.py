container_Entitlements = Product.GetContainerByName("SC_Entitlements")
Training_Match_Value = Product.Attr('SC_Training_Match_Contract_Value')
Training_Match_Value_Per = Product.Attr('SC_Training_Match_Contract_Value_Percent')

Training_Match_Value.Allowed = False
Training_Match_Value_Per.Allowed = False

if container_Entitlements is not None:
    for row in container_Entitlements.Rows:
        if row['Entitlement'] == 'Training Match':
            if row.IsSelected:
                Trace.Write('****************')
                Training_Match_Value.Allowed = True
                Training_Match_Value_Per.Allowed = True
                Training_Match_Value.Access = AttributeAccess.Editable
                Training_Match_Value_Per.Access = AttributeAccess.Editable
                P = Product.Attr('SC_Training_Match_Contract_Value_Percent').GetValue()
                if not P:
                    Product.Attr('SC_Training_Match_Contract_Value_Percent').AssignValue("10")
            else:
                Training_Match_Value.Allowed = False
                Training_Match_Value_Per.Allowed = False
            break
        Product.Attr('Training_Match_Test').AssignValue('Test')
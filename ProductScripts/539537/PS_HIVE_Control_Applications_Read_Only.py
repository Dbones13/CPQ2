for attr in Product.Attributes:
    if attr.DisplayType=="DropDown" and attr.Required:
        if not attr.GetValue():
            for val in attr.Values:
                attr.SelectValue(val.ValueCode)
                break
Product.Attr('SerC_CG_Number_of_HIVE_Control_Applications(HCA)').Access = AttributeAccess.ReadOnly
Product.Attr('SerC_CG_HIVE_Number_of_Controller_Required').Access = AttributeAccess.ReadOnly
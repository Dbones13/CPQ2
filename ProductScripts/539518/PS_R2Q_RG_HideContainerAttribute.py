if Quote.GetCustomField("isR2QRequest").Content != 'Yes':
    Product.ParseString('<*CTX( Container(SM_RG_Cabinet_Details_Cont_Left).Column(SM_RG_Percentage_SSM_Cabinet(0-100%)).SetPermission(Hidden) )*>')
    Product.ParseString('<*CTX( Container(SM_RG_Cabinet_Details_Cont_Left).Column(SM_RG_RelayTypeForESD).SetPermission(Hidden) )*>')
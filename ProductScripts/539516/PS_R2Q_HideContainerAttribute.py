if Quote.GetCustomField("isR2QRequest").Content != 'Yes':
    Product.ParseString('<*CTX( Container(SM_CG_Cabinet_Details_Cont_Left).Column(SM_CG_RelayTypeForESD).SetPermission(Hidden) )*>')
    Product.ParseString('<*CTX( Container(SM_CG_Cabinet_Details_Cont_Left).Column(SM_CG_Percentage_SSM_Cabinet(0-100%)).SetPermission(Hidden) )*>')
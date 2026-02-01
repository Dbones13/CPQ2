if Quote.GetCustomField('EGAP_Proposal_Type').Content == "Budgetary":
    Product.Attr('ELEPIU_Total_numberof_Scada_points_for_controllers').Access = AttributeAccess.ReadOnly
    Product.Attr('ELEPIU_Total_number_of_Process_points_controllers').Access = AttributeAccess.ReadOnly
    Product.Attr('ELEPIU_Total_number_of_graphics_affected_by_ELPIU').Access = AttributeAccess.ReadOnly
else:
    Product.Attr('ELEPIU_Total_numberof_Scada_points_for_controllers').Access = AttributeAccess.Editable
    Product.Attr('ELEPIU_Total_number_of_Process_points_controllers').Access = AttributeAccess.Editable
    Product.Attr('ELEPIU_Total_number_of_graphics_affected_by_ELPIU').Access = AttributeAccess.Editable
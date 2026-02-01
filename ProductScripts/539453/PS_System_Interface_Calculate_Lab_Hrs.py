def isFloat(val):
    if val is not None and val != '':
        try:
            float(val)
            return True
        except:
            return False
    return False

scope = Product.Attr('CE_Scope_Choices').GetValue()
if Product.Attr('isProductLoaded').GetValue() == 'True' and scope == 'HW/SW + LABOR':
    tableLabor = SqlHelper.GetList('Select Deliverable,Calculated_Hrs from SYSTEM_INTERFACE_LABOR')
    laborCont = Product.GetContainerByName('System_Interface_Engineering_Labor_Container')
    calc_dict = {}
    for x in tableLabor:
        calc_dict[x.Deliverable] = x.Calculated_Hrs
    for row in laborCont.Rows:
        deliverable = row.GetColumnByName("Deliverable").Value
        if deliverable in calc_dict.keys() and not isFloat(calc_dict[deliverable]):
            calc_name = calc_dict[deliverable]
            try:
                row.GetColumnByName("Calculated Hrs").Value = Product.Attr(calc_name).GetValue()
            except Exception,e:
                pass
    laborCont.Calculate()
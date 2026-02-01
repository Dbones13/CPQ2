scope = Product.Attr('CE_Scope_Choices').GetValue()
if Product.Attr('isProductLoaded').GetValue() == 'True' and scope == 'HW/SW + LABOR':
    tableLabor = SqlHelper.GetList("Select Deliverable,Calculated_Hrs from LIQUID_METERINGSUITE_ENGINEERING_LABOR_CUSTOM_TABLE where Calculated_Hrs <> 'NA'")
    laborCont = Product.GetContainerByName('LMS_Labor_Container')
    calc_dict = {}
    for x in tableLabor:
        calc_dict[x.Deliverable] = x.Calculated_Hrs
    for row in laborCont.Rows:
        deliverable = row.GetColumnByName("Deliverable").Value
        if deliverable in calc_dict.keys() and not calc_dict[deliverable].isnumeric():
            calc_name = calc_dict[deliverable]
            try:
                row.GetColumnByName("Calculated Hrs").Value = Product.Attr(calc_name).GetValue()
            except Exception:
                pass
    laborCont.Calculate()
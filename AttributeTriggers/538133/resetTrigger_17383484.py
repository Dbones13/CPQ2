if Product.Attr("SC_P1P2_LPDA_PY_ListPrice").GetValue() == "":
    Product.Attr("SC_P1P2_LPDA_PY_ListPrice").AssignValue("0")
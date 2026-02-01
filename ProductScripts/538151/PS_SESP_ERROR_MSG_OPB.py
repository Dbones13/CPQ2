prev_quote = Quote.GetCustomField("SC_CF_Parent_Quote_Number_Link").Content
active_contract = Quote.GetCustomField("SC_CF_Parent_Contract_Number_Link").Content
# OBP Changes Error Msg.
if active_contract and prev_quote in ("None","") and Product.Attr('SC_Product_Type').GetValue() == "Renewal":
    SC_Service_Product = Product.Attr("SC_Service_Product").GetValue()
    Comp_summ = Product.GetContainerByName("ComparisonSummary")
    if Comp_summ.Rows.Count:
        for com_row in Comp_summ.Rows:
            if com_row["Service_Product"] != str(SC_Service_Product):
                if not com_row.IsSelected:
                    Product.Attr('SC_SESP_Popup_Msg').AssignValue('True')
                else:
                    Product.Attr('SC_SESP_Popup_Msg').AssignValue('')
            else:
                Product.Attr('SC_SESP_Popup_Msg').AssignValue('')
    Product.Attr('SC_OPB_Check_SP_Ent').AssignValue('1')
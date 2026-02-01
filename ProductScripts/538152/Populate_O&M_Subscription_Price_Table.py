Sub_Cont = Product.GetContainerByName("SC_WEP_Subscription_Price_OM")
Add_Cont = Product.GetContainerByName("SC_WEP_Add_On_Fees_OM")
Sub_Cont.Rows.Clear()
Add_Cont.Rows.Clear()

sub_list = ["Enter max # of Pipeline Operator (5-450)","Enter max # of Gas Plant Operator (5-450)","Enter max # of Refinery / Petrochem Plant Operator (5-450)","Enter max # of Inst Techs (5-450)","Enter max # of Electricians (5-450)","Enter max # of ROT Equip Mechanics (5-450)","Enter max # of EH&S Learners (5-450)"]
add_list = ["New Customer eLearning Set-Up Fee","New Customer Software Set-Up Fee"]

for i in sub_list:
    sub_row = Sub_Cont.AddNewRow(False)
    sub_row["Type"] = i

for j in add_list:
    add_row = Add_Cont.AddNewRow(False)
    add_row["Add_on_Fees"] = j
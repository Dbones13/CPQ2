current_score = Product.Attr("SC_WEP_Current_Score_OCP_PY").GetValue()
if current_score == "1":
    Product.Attr("SC_WEP_Effort_Loading_OCP_PY").AssignValue("95")
    Product.Attr("SC_WEP_Skill_Assessment_Level_OCP_PY").AssignValue("AWARENESS")
elif current_score == "2":
    Product.Attr("SC_WEP_Effort_Loading_OCP_PY").AssignValue("90")
    Product.Attr("SC_WEP_Skill_Assessment_Level_OCP_PY").AssignValue("AWARENESS")
elif current_score == "3":
    Product.Attr("SC_WEP_Effort_Loading_OCP_PY").AssignValue("80")
    Product.Attr("SC_WEP_Skill_Assessment_Level_OCP_PY").AssignValue("AWARENESS")
elif current_score == "4":
    Product.Attr("SC_WEP_Effort_Loading_OCP_PY").AssignValue("70")
    Product.Attr("SC_WEP_Skill_Assessment_Level_OCP_PY").AssignValue("AWARENESS")
elif current_score == "5":
    Product.Attr("SC_WEP_Effort_Loading_OCP_PY").AssignValue("60")
    Product.Attr("SC_WEP_Skill_Assessment_Level_OCP_PY").AssignValue("FUNDAMENTAL")
elif current_score == "6":
    Product.Attr("SC_WEP_Effort_Loading_OCP_PY").AssignValue("50")
    Product.Attr("SC_WEP_Skill_Assessment_Level_OCP_PY").AssignValue("FUNDAMENTAL")
elif current_score == "7":
    Product.Attr("SC_WEP_Effort_Loading_OCP_PY").AssignValue("40")
    Product.Attr("SC_WEP_Skill_Assessment_Level_OCP_PY").AssignValue("FUNDAMENTAL")
elif current_score == "8":
    Product.Attr("SC_WEP_Effort_Loading_OCP_PY").AssignValue("30")
    Product.Attr("SC_WEP_Skill_Assessment_Level_OCP_PY").AssignValue("FUNDAMENTAL")
elif current_score == "9":
    Product.Attr("SC_WEP_Effort_Loading_OCP_PY").AssignValue("20")
    Product.Attr("SC_WEP_Skill_Assessment_Level_OCP_PY").AssignValue("SKILLED")
elif current_score == "10":
    Product.Attr("SC_WEP_Effort_Loading_OCP_PY").AssignValue("20")
    Product.Attr("SC_WEP_Skill_Assessment_Level_OCP_PY").AssignValue("EXPERT")
ScriptExecutor.Execute('PS_Populate_Prices_OCP')
Product.Attr('SC_Product_Status').AssignValue("0")
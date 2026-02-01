current_score = Product.Attr("SC_WEP_Current_Score_OCP").GetValue()
if current_score == "1":
    Product.Attr("SC_WEP_Effort_Loading_OCP").AssignValue("95")
    Product.Attr("SC_WEP_Skill_Assessment_Level_OCP").AssignValue("AWARENESS")
elif current_score == "2":
    Product.Attr("SC_WEP_Effort_Loading_OCP").AssignValue("90")
    Product.Attr("SC_WEP_Skill_Assessment_Level_OCP").AssignValue("AWARENESS")
elif current_score == "3":
    Product.Attr("SC_WEP_Effort_Loading_OCP").AssignValue("80")
    Product.Attr("SC_WEP_Skill_Assessment_Level_OCP").AssignValue("AWARENESS")
elif current_score == "4":
    Product.Attr("SC_WEP_Effort_Loading_OCP").AssignValue("70")
    Product.Attr("SC_WEP_Skill_Assessment_Level_OCP").AssignValue("AWARENESS")
elif current_score == "5":
    Product.Attr("SC_WEP_Effort_Loading_OCP").AssignValue("60")
    Product.Attr("SC_WEP_Skill_Assessment_Level_OCP").AssignValue("FUNDAMENTAL")
elif current_score == "6":
    Product.Attr("SC_WEP_Effort_Loading_OCP").AssignValue("50")
    Product.Attr("SC_WEP_Skill_Assessment_Level_OCP").AssignValue("FUNDAMENTAL")
elif current_score == "7":
    Product.Attr("SC_WEP_Effort_Loading_OCP").AssignValue("40")
    Product.Attr("SC_WEP_Skill_Assessment_Level_OCP").AssignValue("FUNDAMENTAL")
elif current_score == "8":
    Product.Attr("SC_WEP_Effort_Loading_OCP").AssignValue("30")
    Product.Attr("SC_WEP_Skill_Assessment_Level_OCP").AssignValue("FUNDAMENTAL")
elif current_score == "9":
    Product.Attr("SC_WEP_Effort_Loading_OCP").AssignValue("20")
    Product.Attr("SC_WEP_Skill_Assessment_Level_OCP").AssignValue("SKILLED")
elif current_score == "10":
    Product.Attr("SC_WEP_Effort_Loading_OCP").AssignValue("20")
    Product.Attr("SC_WEP_Skill_Assessment_Level_OCP").AssignValue("EXPERT")
ScriptExecutor.Execute('PS_Populate_Prices_OCP')
Product.Attr('SC_Product_Status').AssignValue("0")
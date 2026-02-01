import GS_PS_Exp_Ent_BOM
import GS_EXP_ENT_EBR_Parts

def EBRParts(Product):
    #Product.ExecuteRulesOnce = True
    qnt=GS_EXP_ENT_EBR_Parts.getebrparts(Product)
    addall=GS_EXP_ENT_EBR_Parts.getebrpartsNode(Product)
    #CXCPQ-46574
    if qnt>0 and Product.Attributes.GetByName("Experion Backup Restore Software Release").GetValue()=="R520":
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-BRWE06",qnt)
    else:
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-BRWE06",0)
    #CXCPQ-46569
    if qnt>0 and Product.Attributes.GetByName("Experion Backup Restore Software Release").GetValue()=="R501":
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-BRWE05",qnt)
    else:
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-BRWE05",0)
    #CXCPQ-46504
    if addall>0 and Product.Attributes.GetByName("Experion Backup Restore Software Release").GetValue()=="R501":
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-BRSE05",addall)
    else:
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-BRSE05",0)
    #CXCPQ-46553
    if addall>0 and Product.Attributes.GetByName("Experion Backup Restore Software Release").GetValue()=="R520":
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-BRSE06",addall)
    else:
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-BRSE06",0)
    Product.ApplyRules()
    #Product.ExecuteRulesOnce = False
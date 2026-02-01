Power_System_Type = Product.Attr('SerC_CG_Power_System_Type').GetValue()
#Power_System_Type = Product.Attr('SerC_CG_Power_System_Type').SelectValue('Locally Supplied Power')
Trace.Write(Power_System_Type)
RQUP_Approval_Value = Product.Attr('SerC_CG_RQUP_Approval_Value').GetValue()
list1=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
#list2=["K","L","M","N","O","P","Q","R","S","T"]
#list3=["U","V","W","X","Y","Z"]
#list4=["0","1","2","3","4","5","6","7","8","9"]
if Power_System_Type =='Locally Supplied Power' and (len(str(RQUP_Approval_Value)) >0 and len(str(RQUP_Approval_Value))<17):
    Trace.Write(RQUP_Approval_Value)
    for i in RQUP_Approval_Value:
        if i not in list1:
            #Trace.Write()
            Product.ResetAttr('SerC_CG_RQUP_Approval_Value')
elif Power_System_Type =='Locally Supplied Power' and (len(str(RQUP_Approval_Value)) <1 or len(str(RQUP_Approval_Value))>16):
    Product.ResetAttr('SerC_CG_RQUP_Approval_Value')
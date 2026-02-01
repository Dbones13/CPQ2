if Quote.GetCustomField("isR2QRequest").Content in ('yes','Yes','YES','True','true','TRUE'):
    Session['editsession']="True"
    from GS_R2Q_Gendocrecal import R2qrecall
    editval=Session['editsession']
    R2qrecall(Quote,editval)
    Session['editsession']=''
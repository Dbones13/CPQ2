if Product.Attr('PERF_ExecuteScripts').GetValue() != '':
    import GS_PS_Exp_Ent_BOM
    lst1=['ServerLocation_Cluster/Network_Group','DMS Desk Station Location Cluster Network Group','Orion Station Location/Cluster/Network Group']
    lst2=['IKBorOEP_FlexServer','DMS IKB or OEP','Orion Console Membrane KB Type']
    lst=[]
    for i,k in zip(lst1,lst2):
         val1=Product.Attributes.GetByName(str(i)).GetValue()
         val2=Product.Attributes.GetByName(str(k)).GetValue()
         if val2=='':
            val2='None'
         if val1=='':
            val1='abc'
         #Trace.Write(val1)
         if val2=='Operator Touch Panel':
            lst.append(val1)
            #Trace.Write(str(lst))
    b={i:lst.count(i) for i in lst if i !="abc"}
    Trace.Write(str(b))
    def countdupblicate(b):
      count =0
      for ele in b:
         count = count + 1
      return count
    count=countdupblicate(b)
    if count >0:
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-ADSP01",count)
    else:
        GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Exp_Ent_Grp_Part_Summary","EP-ADSP01",0)
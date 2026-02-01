if sender.PartNumber=="PRJT" :
    from GS_CommonConfig import CL_CommonSettings as CS
    from GS_Display_Warning_Message import Laborwarningmessage
    Labor_Execution_Year_List=''
    quoteTotalTable = Quote.QuoteTables["Quote_Details"]
    if quoteTotalTable.Rows.Count > 0:
        row = quoteTotalTable.Rows[0]
        Labor_Execution_Year_List=row['Labor_Execution_Year']
    Systemgroup_cont=Product.GetContainerByName('CE_SystemGroup_Cont')
    Guid=TagParserQuote.ParseString('<*CTX( Quote.CurrentItem.CartItemGuid )*>')
    Execution_Year_list=[]
    Quote_Guid=dict()
    if Labor_Execution_Year_List!='':
        Quote_Guid=eval(Labor_Execution_Year_List)

    def CheckExecutionYear(product,productName,CS):

        if productName in CS.conNames:
            for conName in CS.conNames.get(productName):
                con=product.GetContainerByName(conName)
                if con is None:
                    continue
                else:
                    for row in con.Rows:
                        if row["Execution Year"]!='' and row["Final Hrs"]!='' and float(row["Final Hrs"])>0:
                            Execution_Year_list.append(row["Execution Year"])

    for row in Systemgroup_cont.Rows:
        if row["Scope"] in ["HWSWLABOR","LABOR"]:
            product_list=row.Product.GetContainerByName("CE_System_Cont")
            for row1 in product_list.Rows:
                productName=row1.Product.Name
                CheckExecutionYear(row1.Product,productName,CS)
        else:
            Execution_Year_list.append("No Labor")

    productName=Product.Name
    if productName == "New / Expansion Project":
        CheckExecutionYear(Product,productName,CS)

    if quoteTotalTable.Rows.Count > 0 and len(Execution_Year_list)>0:
        row = quoteTotalTable.Rows[0]
        Quote_Guid[Guid]=(',').join(set(Execution_Year_list))
        row['Labor_Execution_Year']=str(Quote_Guid)
    elif quoteTotalTable.Rows.Count > 0:
        if Guid in Quote_Guid:
            Quote_Guid.pop(Guid)
        row = quoteTotalTable.Rows[0]
        row['Labor_Execution_Year']=str(Quote_Guid)
    quoteTotalTable.Save()

Laborwarningmessage(Quote)
isR2Qquote = True if Quote.GetCustomField("isR2QRequest").Content else False
if not isR2Qquote:
    msid_scope=Product.Attr('MIgration_Scope_Choices').GetValue()
    for frow in Product.GetContainerByName("CONT_MSID_SUBPRD").Rows:
        #selectedProducts.add(row["Selected_Products"])
        if frow["Selected_Products"] == 'Graphics Migration' and msid_scope in ('HW/SW/LABOR','LABOR') :

            containers = Product.GetContainerByName("MSID_Labor_Graphics_Migration_con")
            if Product.Attr("MSID_GES_Location").GetValue() != 'None':
                for row in containers.Rows:
                    if Session['gap_analysis'] != '' :
                        if row["Deliverable"] == "GAP Analysis":
                            if Session['gap_analysis'] == "Limitations to use GES":
                                row["FO_Eng_Percentage_Split"] = "70"
                                row["GES_Eng_Percentage_Split"] = "30"
                                row.Calculate()
                            elif Session['gap_analysis'] == "No limitation to use GES":
                                row["FO_Eng_Percentage_Split"] = "30"
                                row["GES_Eng_Percentage_Split"] = "70"
                    if Session['FAT_required'] != '':
                        if row["Deliverable"] == "FAT Support":
                            if row['Deliverable_Type'] in ('Onsite','Offsite'):
                                if Session['FAT_required'] == "Yes via VEP/Remote GES":
                                    row["FO_Eng_Percentage_Split"] = "50"
                                    row["GES_Eng_Percentage_Split"] = "50"
                                else :
                                    row["FO_Eng_Percentage_Split"] = "100"
                                    row["GES_Eng_Percentage_Split"] = "0"


                    #ScriptExecutor.Execute('PS_PopulatePartNumberContainer')
                    containers.Calculate()

        if frow["Selected_Products"] == 'TPA/PMD Migration' and msid_scope in ('HW/SW/LABOR','LABOR') :
            container = Product.GetContainerByName("MSID_Labor_TPA_con")
            for containerrow in container.Rows:

                if Session['TPA_System_migrating'] != '':
                    if containerrow["Deliverable"] == "Block Engineering":
                        if Session['TPA_System_migrating'] not in ( "TPA Alcont", 'PMD R61x or older') :

                            containerrow["FO_Eng_Percentage_Split"] = '100'
                            containerrow["GES_Eng_Percentage_Split"] = '0'
                        else:
                            containerrow["FO_Eng_Percentage_Split"] = '45'
                            containerrow["GES_Eng_Percentage_Split"] = '55'
                        containerrow.Calculate()
    Session['gap_analysis'] = ''	
    Session['FAT_required'] = ''	
    Session['TPA_System_migrating'] =''
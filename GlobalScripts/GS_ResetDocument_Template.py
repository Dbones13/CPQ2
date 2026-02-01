if EventArgs.CurrentTabName=="DOCUMENTS":
    Doc_Tmp=Quote.GetCustomField('Generate_document_Selection')
    if Doc_Tmp.Content=="Functional Questions":
        Doc_Tmp.Content='Cyber Costing Template'
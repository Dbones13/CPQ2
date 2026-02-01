gesLocation = TagParserProduct.ParseString('<* Value(SCADA_Ges_Location_Labour) *>')
laborCont = Product.GetContainerByName('SCADA_Engineering_Labor_Container')
tableLabor = SqlHelper.GetList('select Deliverable,Productivity,GES_Eng_1_No,GES_Eng,FO_Eng_1_NoGES,FO_Eng_1_GES_None,FO_Eng_1_GES,FO_Eng_2_NoGES,FO_Eng_2_GES_None,FO_Eng_2_GES,Rank,Execution_Country from SCADA_LABOR_DELIVERABLES')
set_default = {'GES China':'SYS GES Eng-BO-CN', 'GES India':'SYS GES Eng-BO-IN', 'GES Romania':'SYS GES Eng-BO-RO', 'GES Uzbekistan':'SYS GES Eng-BO-UZ','GES Egypt':'SYS GES Eng-BO-EG'}
if laborCont.Rows.Count > 0:
    for new_row in laborCont.Rows:
        new_row.GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue(set_default.get(gesLocation))
        new_row['GES Eng'] = set_default.get(gesLocation)
        new_row.Calculate()
    laborCont.Calculate()

    custom_deliverables = Product.GetContainerByName('SCADA_Additional_Custom_Deliverables_Container')
    for row in custom_deliverables.Rows:
        row.GetColumnByName('GES Eng').ReferencingAttribute.SelectDisplayValue(set_default.get(gesLocation))
        row['GES Eng'] = set_default.get(gesLocation)
        row.Calculate()
    custom_deliverables.Calculate()
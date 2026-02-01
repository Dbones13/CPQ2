if Product.Name != "Service Contract Products":
    currentTab = "".join([tab.Name for tab in Product.Tabs if tab.IsSelected])
    es = Product.Attr('EnableSelection_SESP').SelectedValue
    if currentTab in ['Scope Summary', 'Enabled Services'] and es:
        ScriptExecutor.Execute('GS_SC_ES_Scope_Removal')
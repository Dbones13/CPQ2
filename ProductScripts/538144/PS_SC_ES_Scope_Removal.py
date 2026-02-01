if Product.Name != "Service Contract Products":
    currentTab = "".join([tab.Name for tab in Product.Tabs if tab.IsSelected])
    if currentTab == 'Scope Summary':
        ScriptExecutor.Execute('GS_SC_ES_Scope_Removal')
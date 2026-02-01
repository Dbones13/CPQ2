tabs = [tab.Name for tab in Product.Tabs if tab.IsSelected]
if 'Parts Replacement' in tabs:
    ScriptExecutor.Execute('PS_Populate_PartListSummary')
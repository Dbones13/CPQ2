Contract = ['Contract New','Contract Renewal']
if Quote.GetCustomField('Quote Type').Content in Contract:
	import GS_SC_MilestoneTablePopulation_Module as gsmm
	gsmm.Main_function(Quote,'QTab')
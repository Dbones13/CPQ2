def GS_UOC_Batch_Application_Configuration_Calcs(attrs):
	Hrs = 0
	if attrs.process_type in ['Batch - Pharma', 'BatchPharma', 'Batch - Chemical','BatchChemical']:
		bmu = int(attrs.batch_unit)
		bcscm = int(attrs.complex_scms)
		bmr = int(attrs.product_master_recipes)
		bco = int(attrs.complex_ops)
		bru = int(attrs.batch_unit_copies)
		bpr = int(attrs.product_replicated)
		masterHrs = bmu * (30.26 + 47.06 + 8 + bcscm * 26.212) + bmr * (23.3 + bco * 11.55 + 8.9)
		instanceHrs = bru * (5.06 + 5.06 + 6 + bcscm * 1.012) + bpr * (4.75 + bco * 0.95 + 0.95)
		Hrs = masterHrs + instanceHrs
	return Hrs
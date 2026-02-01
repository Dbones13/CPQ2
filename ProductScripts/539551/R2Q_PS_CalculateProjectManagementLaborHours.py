isR2Qquote = True if Quote.GetCustomField("isR2QRequest").Content else False
if isR2Qquote:
	def getContainer(Product, Name):
		return Product.GetContainerByName(Name)

	def calculateFinalHours(row):
		return str(round(getFloat(row["Calculated_Hrs"]) * getFloat(row["Adjustment_Productivity"])))

	def getFloat(Var):
		if Var:
			return float(Var)
		return 0

	def getTotalEngHours(Product, container):
		totalFinalHours = 0
		if getContainer(Product, container):
			for row in getContainer(Product, container).Rows:
				if row["Deliverable"] == "Total":
					totalFinalHours += getFloat(row["Final_Hrs"])
		return totalFinalHours

	def getProjectMangementHours(Product):
		selectedProducts = Product.Attr('MSID_Selected_Products').GetValue().split('<br>')
		totalOpmFinalHours = getTotalEngHours(Product, "MSID_Labor_OPM_Engineering") if "OPM" in selectedProducts else 0
		totalLcnFinalHours = getTotalEngHours(Product, "MSID_Labor_LCN_One_Time_Upgrade_Engineering") if "LCN One Time Upgrade" in selectedProducts else 0
		totalEbrFinalHours = getTotalEngHours(Product, "MSID_Labor_EBR_Con") if "EBR" in selectedProducts else 0
		totalElcnFinalHours = getTotalEngHours(Product, "MSID_Labor_ELCN_Con") if "ELCN" in selectedProducts else 0
		totalOrionConsoleHours = getTotalEngHours(Product, "MSID_Labor_Orion_Console_Con") if "Orion Console" in selectedProducts else 0
		totalEHPMHours = getTotalEngHours(Product, "MSID_Labor_EHPM_C300PM_Con") if "EHPM/EHPMX/ C300PM" in selectedProducts else 0
		totalTPSHours = getTotalEngHours(Product, "MSID_Labor_TPS_TO_EXPERION_Con") if "TPS to Experion" in selectedProducts else 0
		totalTCMIHours = getTotalEngHours(Product, "MSID_Labor_TCMI_Con") if "TCMI" in selectedProducts else 0
		totalEHPMHARTIOHours = getTotalEngHours(Product, "MSID_Labor_EHPM_HART_IO_Con") if "EHPM HART IO" in selectedProducts else 0
		totalC200Hours = getTotalEngHours(Product, "MSID_Labor_C200_Migration_Con") if "C200 Migration" in selectedProducts else 0
		totalcbecHours = getTotalEngHours(Product, "MSID_Labor_CB-EC_Upgrade_to_C300-UHIO_con") if "CB-EC Upgrade to C300-UHIO" in selectedProducts else 0
		totalfsctosmhours = getTotalEngHours(Product, "MSID_Labor_FSC_to_SM_con") if "FSC to SM" in selectedProducts else 0
		totalfsctosmaudithours = getTotalEngHours(Product, "MSID_Labor_FSC_to_SM_audit_Con") if "FSC to SM" in selectedProducts else 0
		#totalfdmHours = getTotalEngHours("MSID_Labor_FDM_Upgrade_Con") if ["FDM Upgrade 1","FDM Upgrade 2","FDM Upgrade 3"] in selectedProducts else 0
		totalfdmHours = getTotalEngHours(Product, "MSID_Labor_FDM_Upgrade_Con") if (("FDM Upgrade 1" in selectedProducts) or ("FDM Upgrade 2" in selectedProducts) or ("FDM Upgrade 3" in selectedProducts)) else 0
		totalxPMHours = getTotalEngHours(Product, "MSID_Labor_xPM_to_C300_Migration_Con") if "xPM to C300 Migration" in selectedProducts else 0
		totalXP10Hours = getTotalEngHours(Product, "MSID_Labor_XP10_Actuator_Upgrade_con") if "XP10 Actuator Upgrade" in selectedProducts else 0
		totallmHours = getTotalEngHours(Product, "MSID_Labor_LM_to_ELMM_Con") if "LM to ELMM ControlEdge PLC" in selectedProducts else 0
		totalGraphicsHours = getTotalEngHours(Product, "MSID_Labor_Graphics_Migration_con") if "Graphics Migration" in selectedProducts else 0
		totalCDActuatorHours = getTotalEngHours(Product, "MSID_Labor_CD_Actuator_con") if "CD Actuator I-F Upgrade" in selectedProducts else 0
		totalfscsmioHours = getTotalEngHours(Product, "MSID_Labor_FSCtoSM_IO_con") if "FSC to SM IO Migration" in selectedProducts else 0
		totalfscsmioauditHours = getTotalEngHours(Product, "MSID_Labor_FSC_to_SM_IO_Audit_Con") if "FSC to SM IO Migration" in selectedProducts else 0
		totalCWSRAEHours = getTotalEngHours(Product, "MSID_Labor_CWS_RAE_Upgrade_con") if "CWS RAE Upgrade" in selectedProducts else 0
		totalplcuocHours = getTotalEngHours(Product, "3rd_Party_PLC_UOC_Labor") if "3rd Party PLC to ControlEdge PLC/UOC" in selectedProducts else 0
		totalVirtualizationHours = getTotalEngHours(Product, "MSID_Labor_Virtualization_con") if "Virtualization System" in selectedProducts else getTotalEngHours(Product, "MSID_Labor_Virtualization_con") if "Virtualization System Migration" in selectedProducts else 0
		totalQCSHours = getTotalEngHours(Product, "MSID_Labor_QCS_RAE_Upgrade_con") if "QCS RAE Upgrade" in selectedProducts else 0
		totalGS1Hours = getTotalEngHours(Product, "MSID_Labor_Generic_System1_Cont") if "Generic System 1" in selectedProducts else 0
		totalGS2Hours = getTotalEngHours(Product, "MSID_Labor_Generic_System2_Cont") if "Generic System 2" in selectedProducts else 0
		totalGS3Hours = getTotalEngHours(Product, "MSID_Labor_Generic_System3_Cont") if "Generic System 3" in selectedProducts else 0
		totalGS4Hours = getTotalEngHours(Product, "MSID_Labor_Generic_System4_Cont") if "Generic System 4" in selectedProducts else 0
		totalGS5Hours = getTotalEngHours(Product, "MSID_Labor_Generic_System5_Cont") if "Generic System 5" in selectedProducts else 0
		totalTPAHours = getTotalEngHours(Product, "MSID_Labor_TPA_con") if "TPA/PMD Migration" in selectedProducts else 0
		# Extended Logic for ELEPIU Module for Project Management Labor Hrs -- Dipak Shekokar : CXCPQ-60175
		totalELEPIUHours = getTotalEngHours(Product, "MSID_Labor_ELEPIU_con") if "ELEPIU ControlEdge RTU Migration Engineering" in selectedProducts else 0
		totaltracehours = getTotalEngHours(Product, "Trace_Software_Labor_con") if "Trace Software" in selectedProducts else 0
		EngHours = totalOpmFinalHours + totalLcnFinalHours + totalEbrFinalHours + totalElcnFinalHours + totalOrionConsoleHours + totalEHPMHours + totalTPSHours + totalTCMIHours + totalEHPMHARTIOHours + totalC200Hours + totalcbecHours + totalxPMHours + totalfsctosmhours + totalfdmHours + totallmHours + totalfsctosmaudithours + totalXP10Hours + totalGraphicsHours + totalfscsmioHours + totalCDActuatorHours + totalCWSRAEHours + totalplcuocHours + totalVirtualizationHours + totalQCSHours + totalGS1Hours + totalGS2Hours + totalGS3Hours + totalGS4Hours + totalGS5Hours + totalTPAHours + totalfscsmioauditHours + totalELEPIUHours + totaltracehours

		pmOtherActivities = 0
		if EngHours > 0:
			pmOtherActivities = 24
		else:
			pmOtherActivities = 0

		paOtherActivities = 0
		if EngHours > 0:
			paOtherActivities = 8
		else:
			paOtherActivities = 0

		paMonthlyProjectManagement = 0
		if EngHours <= 160:
			paMonthlyProjectManagement = 0
		else:
			paMonthlyProjectManagement = 16

		pmEngineeringManagement = 0
		if EngHours <= 160:
			pmEngineeringManagement = 0
		elif EngHours > 160 and EngHours <= 2000:
			pmEngineeringManagement = round((EngHours -160) * 0.1)
		else:
			pmEngineeringManagement = 176 + round((EngHours - 2000 -160) * 0.05)

		return pmOtherActivities,paOtherActivities,paMonthlyProjectManagement,pmEngineeringManagement
	migration_new_cont = Product.GetContainerByName('CONT_Migration_MSID_Selection')
	for MigrationNew in migration_new_cont.Rows:
		opmEngineeringCon = getContainer(MigrationNew.Product, "MSID_Labor_OPM_Engineering")
		lcnOneTimeUpgradeCon = getContainer(MigrationNew.Product, "MSID_Labor_LCN_One_Time_Upgrade_Engineering")
		projectManagementCon = getContainer(MigrationNew.Product, "MSID_Labor_Project_Management")
		if projectManagementCon.Rows.Count > 0:
			pmOtherActivities,paOtherActivities,paMonthlyProjectManagement,pmEngineeringManagement = getProjectMangementHours(MigrationNew.Product)
			for row in projectManagementCon.Rows:
				if row["Deliverable"] == "PM Engineering Management":
					row["Calculated_Hrs"] = str(pmEngineeringManagement)
					if getFloat(row["Calculated_Hrs"]) == 0:
						row["Adjustment_Productivity"] = str(1)    
					row["Final_Hrs"] = calculateFinalHours(row)
				elif row["Deliverable"] == "PM Other activities":
					row["Calculated_Hrs"] = str(pmOtherActivities)
					if getFloat(row["Calculated_Hrs"]) == 0:
						row["Adjustment_Productivity"] = str(1)
					row["Final_Hrs"] = calculateFinalHours(row)
				elif row["Deliverable"] == "PA Monthly Project Management":
					row["Calculated_Hrs"] = str(paMonthlyProjectManagement)
					if getFloat(row["Calculated_Hrs"]) == 0:
						row["Adjustment_Productivity"] = str(1)
					row["Final_Hrs"] = calculateFinalHours(row)
				elif row["Deliverable"] == "PA Other activities":
					row["Calculated_Hrs"] = str(paOtherActivities)
					if getFloat(row["Calculated_Hrs"]) == 0:
						row["Adjustment_Productivity"] = str(1)
					row["Final_Hrs"] = calculateFinalHours(row)
			projectManagementCon.Calculate()

		if projectManagementCon.Rows.Count > 0:
			'''for row in projectManagementCon.Rows:
				if row["Deliverable"] not in ('Total'):
					row["Adjustment_Productivity"] = AdjustmentProductivity
					row["Final_Hrs"] = str(round(getFloat(row["Calculated_Hrs"]) * getFloat(AdjustmentProductivity)))'''
			totalCalculatedHrs = 0
			totalFinalHrs = 0
			for row in projectManagementCon.Rows:
				if row["Deliverable_Type"] in ("Offsite","Off-Site","On-Site","Onsite"):
					if row["Calculated_Hrs"] != "0":
						totalCalculatedHrs = totalCalculatedHrs + getFloat(row["Calculated_Hrs"])
					totalFinalHrs = totalFinalHrs + getFloat(row["Final_Hrs"])
			for row in projectManagementCon.Rows:
				if row["Deliverable"] == "Total":
					row["Calculated_Hrs"] = str(totalCalculatedHrs)
					row["Final_Hrs"] = str(totalFinalHrs)
			projectManagementCon.Calculate()
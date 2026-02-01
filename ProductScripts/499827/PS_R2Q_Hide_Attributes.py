nonR2QContColumn = {
	"CE_Project_Questions_Cont": ["MIB Configuration Required?","Languages","R2Q_Alternate_Execution_Country","Is HMI Engineering in Scope?","Project_Execution_Year","R2Q_PRJT_Proposal Language"]
}
for contColumn in nonR2QContColumn:
		for col in nonR2QContColumn[contColumn]:
			TagParserProduct.ParseString('<*CTX( Container({0}).Column({1}).SetPermission(Hidden) )*>'.format(contColumn,col))
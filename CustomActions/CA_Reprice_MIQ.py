#CXCPQ-50830: Add "Write-In MIQ Optimize Annual Update Fee" when "Measurement IQ System" System is added in the new expansion project and attribute MIQ_Perpetual_Contract is Yes.

#write in Price = 18% of Total Price * Years of Annual Fee.  Cost = 45% of the write in Price
#If "Perpetual Contract" = Yes, Years of Annual Fee = "Contract Length" - 1


#ScriptExecutor.ExecuteGlobal('GS_MIQ_WriteIn')
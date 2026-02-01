import math
qf = ((int(Product.Attr('MSASE_Total_Number_of_Analyser_Systems_(1-20)').GetValue())*1)+(int(Product.Attr('MSASE_Number_of_Redundant_Analyser_Systems').GetValue())*0.3)+(int(Product.Attr('MSASE_Total_Number_of_Analysers_require_for_all_Systems_(1-300)').GetValue())*0.2)+(int(Product.Attr('MSASE_Number_of_Houses/Enclosures_Included_in_the_Scope').GetValue())*0.2)+(int(Product.Attr('MSASE_Number_of_Enclosures_with_Air_Conditioning').GetValue())*0.2)+(int(Product.Attr('MSASE_Number_of_Enclosures_with_Space_Heaters').GetValue())*0.1)+(int(Product.Attr('MSASE_Number_of_Enclosures_with_Force_Ventilation').GetValue())*0.1)+(int(Product.Attr('MSASE_Number_of_Enclosures_with_F&G_Detection/Alarms').GetValue())*0.1))

qfu = ((int(Product.Attr('MSASE_Number_of_Unique_Analyser_System_Designs_(1-20)').GetValue())*1)+(int(Product.Attr('MSASE_Number_of_Different_Types_of_Analysers_(1-10)').GetValue())*0.5)+(int(Product.Attr('MSASE_Number_of_Unique_Houses/Enclosures').GetValue())*0.3)+(int(Product.Attr('MSASE_Number_of_Unique_Enclosures_with_Air_Conditioning').GetValue())*0.1)+(int(Product.Attr('MSASE_Number_of_Unique_Enclosures_with_Space_Heaters').GetValue())*0.1)+(int(Product.Attr('MSASE_Number_of_Unique_Enclosures_with_Force_Ventilation_').GetValue())*0.1)+(int(Product.Attr('MSASE_Number_of_Unique_Enclosures_F&G_Detection/Alarms').GetValue())*0.1))

#Deliverable 1
x=2 if Product.Attr('MSASE_Analyser_System_Part_of_Metering_Package').GetValue() == "No" else 1
Deliverable_1 = 2*(1+qf*0.5)*(0.5*x)
Product.Attr('MS Sales Handover Meeting').AssignValue(str(Deliverable_1))

#Deliverable 2
Deliverable_2 = qfu*2
Product.Attr('MS Project Specification Review').AssignValue(str(Deliverable_2))

#Deliverable 3
Deliverable_3 = (2+(qfu*3)+(qf-qfu))*(0.5*x)
Product.Attr('MS Define Document Requirements').AssignValue(str(Deliverable_3))

#Deliverable 4
Deliverable_4 = 48 if Product.Attr('MSASE_Analyser_System_Part_of_Metering_Package').GetValue() == "No" else 0.2*qfu
Product.Attr('MS Kick-Off Meeting with Client (at Client Location)').AssignValue(str(Deliverable_4))

#Deliverable 5
Deliverable_5 = (int(Product.Attr('MSASE_Number_of_Client_Meetings_at_Client_Location_(1-99)').GetValue())-1)*48 if Product.Attr('MSASE_Analyser_System_Part_of_Metering_Package').GetValue() == "No" else 0
Product.Attr('MS Progress Meeting with Client (at Client Location)').AssignValue(str(Deliverable_5))

#Deliverable 6
Deliverable_6 = (int(Product.Attr('MSASE_Number_of_Client_Meetings_at_Home_Location_(4-99)').GetValue()))*2 if Product.Attr('MSASE_Analyser_System_Part_of_Metering_Package').GetValue() == "No" else 0
Product.Attr('MS Progress Meeting with Client (at Home Location)').AssignValue(str(Deliverable_6))

#Deliverable 7
Deliverable_7 = int(Product.Attr('MSASE_Estimated_Delivery_of_Scope_(16-500)').GetValue())*2*0.5
Product.Attr('MS Regular Communications with Client').AssignValue(str(Deliverable_7))

#Deliverable 8
Deliverable_8 = 8+(qfu*0.2)
Product.Attr('MS Technical Requirement Specifications').AssignValue(str(Deliverable_8))

#Deliverable 9
Deliverable_9 = 2*(16+8*math.floor(1.6+(qfu*0.3)))
Product.Attr('MS Kick-Off Meeting with Subcontractor').AssignValue(str(Deliverable_9))

#Deliverable 10
Deliverable_10 = 24*(1+math.floor(qfu*0.5))
Product.Attr('MS Progress Meeting with Subcontractor').AssignValue(str(Deliverable_10))

#Deliverable 11
Deliverable_11 = 2*(16*math.floor(float(1+(1+(qfu*1)+((qf-qfu)*0.5))/12)) + 8*math.ceil(1+(qfu*1)+(qf-qfu)*0.5))
Product.Attr('MS Pre-FAT at Subcontractor Location').AssignValue(str(Deliverable_11))

#Deliverable 12
Deliverable_12 = 2*(16*math.floor(float(1+(1+(qfu*0.5)+((qf-qfu)*0.25))/12)) + 8*math.ceil(1+(qfu*0.5)+(qf-qfu)*0.25))
Product.Attr('MS FAT at Subcontractor Location').AssignValue(str(Deliverable_12))

#Deliverable 13
Deliverable_13 = 2*math.ceil(16+4*qfu+(qf-qfu)*1)
Product.Attr('MS Document Review (Subcontractor)').AssignValue(str(Deliverable_13))

#Deliverable 14
Deliverable_14 = 14+(13*qfu)+(qf-qfu)*4
Product.Attr('MS Project Design Documents').AssignValue(str(Deliverable_14))

#Deliverable 15
Deliverable_15 = 26+(8*qfu)+(qf-qfu)*4
Product.Attr('MS Project Procedures (PEP_ FAT_ IOM)').AssignValue(str(Deliverable_15))

#Deliverable 16
Deliverable_16 =  2*int(Product.Attr('MSASE_Estimated_Delivery_of_Scope_(16-500)').GetValue()) if Product.Attr('MSASE_Analyser_System_Part_of_Metering_Package').GetValue() == "No" else 0
Product.Attr('MS Project Meetings (Internal)').AssignValue(str(Deliverable_16))
import math
QF=(1*int(Product.Attr('PRMS Number of Metering Packages').GetValue()))+(0.2*int(Product.Attr('PRMS Number of Filtration Packages').GetValue()))+(0.8*int(Product.Attr('PRMS Number of Regulating Packages').GetValue()))+(0.8*int(Product.Attr('PRMS Number of Heating Packages').GetValue()))
QFU=(1*int(Product.Attr('PRMS Number of Unique Metering Package Designs').GetValue()))+(0.2*int(Product.Attr('PRMS Number of Unique Filtering Packages').GetValue()))+(0.8*int(Product.Attr('PRMS Number of Unique Regulation Package Designs').GetValue()))+(0.8*int(Product.Attr('PRMS Number of Unique Heating Package Designs').GetValue()))+(0.30*int(Product.Attr('PRMS Number of Dedicated Master or Check Meters').GetValue()))
QD=QF-QFU
QM=int(Product.Attr('PRMS Number of Pay Meters (1-999)').GetValue())+int(Product.Attr('PRMS Number of Dedicated Master or Check Meters').GetValue())

#Deliverable1
SalesHandOverMeeting=2*(1+(QF*0.5)+(int(Product.Attr('PRMS Number of Project Specifications Supplied by Client (1-999)').GetValue())*0.25))
Product.Attr('PRMS Sales Handover Meeting').AssignValue(str(SalesHandOverMeeting))

#Deliverable2
SpecificationReview=(int(Product.Attr('PRMS Number of Project Specifications Supplied by Client (1-999)').GetValue())*2)
Product.Attr('PRMS Project Specification Review').AssignValue(str(SpecificationReview))

#Deliverable3
DefineDocument=2+(QFU*3)+(QD*1)+(int(Product.Attr('PRMS Number of Specifications for Product Purchases (1-999)').GetValue())*0.25)
Product.Attr('PRMS Define Document Requirements').AssignValue(str(DefineDocument))

#Deliverable4
KickOffMeeting=2*(16+8*math.floor(1.2+(QFU*0.2)))
Product.Attr('PRMS Kick-Off Meeting with Client (at Client Location)').AssignValue(str(KickOffMeeting))

#Deliverable5
ProgressMeeting=(int(Product.Attr('PRMS Number of Client Meetings at Client Site').GetValue())-1)*48
Product.Attr('PRMS Progress Meeting with Client (at Client Location)').AssignValue(str(ProgressMeeting))

#Deliverable6
HomeMeeting=(int(Product.Attr('PRMS Number of Client Meetings at Home Site or On-line (4-99)').GetValue()))*2
Product.Attr('PRMS Progress Meeting with Client (at Home Location)').AssignValue(str(HomeMeeting))

#Deliverable7
RegularCommunication=(int(Product.Attr('PRMS Estimated Project Duration (16-500)').GetValue()))*2
Product.Attr('PRMS Regular Communications with Client').AssignValue(str(RegularCommunication))

#Deliverable8
TechnicalRequirement=8+(QFU*0.2)+(int(Product.Attr('PRMS Number of Specifications for Product Purchases (1-999)').GetValue())*8)
Product.Attr('PRMS Technical Requirement Specifications').AssignValue(str(TechnicalRequirement))

#Deliverable9
SubContractorKOM=2*(16+8*math.floor(1.6+(QFU*0.3)))
Product.Attr('PRMS Kick-Off Meeting with Subcontractor').AssignValue(str(SubContractorKOM))

#Deliverable10
SubContractor=2*8*math.floor(math.floor(1+QFU)*3.5+0.5)
Product.Attr('PRMS Progress Meeting with Subcontractor').AssignValue(str(SubContractor))

#Deliverable11
SubContractorLoc=2*(16*math.floor(1+(3+(QFU*2)+(QD*1))/12) + 8*math.ceil(3+(QFU*2)+QD*1))
Product.Attr('PRMS Pre-FAT at Subcontractor Location').AssignValue(str(SubContractorLoc))

#Deliverable12
SubContractorLoc2=2*(16*math.floor(1+(2+(QFU*1.5)+(QD*0.5))/12)+8*math.ceil(2+(QFU*1.5)+QD*0.5))
Product.Attr('PRMS FAT at Subcontractor Location').AssignValue(str(SubContractorLoc2))

#Deliverable13
SubContractorDoc=2*math.ceil(30+(QFU*10) + (QD*2))
Product.Attr('PRMS Document Review (Subcontractor)').AssignValue(str(SubContractorDoc))

#Deliverable14
SupplierKOM=2*4*int(Product.Attr('PRMS Number of Specifications for Product Purchases (1-999)').GetValue())
Product.Attr('PRMS Kick-Off and Progress Meeting with Supplier').AssignValue(str(SupplierKOM))

#Deliverable15
FAT_Meter=(16*int(Product.Attr('PRMS Number of Meter Calibration Events').GetValue()))+8*math.ceil((QM*(int(Product.Attr('PRMS Percentage of Meter Calibrations to be Witnessed (0%-100%)').GetValue())*0.01)/3))
Product.Attr('PRMS FAT of Meter at Supplier Location').AssignValue(str(FAT_Meter))

#Deliverable16
DocReviewSup=8*2*int(Product.Attr('PRMS Number of Specifications for Product Purchases (1-999)').GetValue())
Product.Attr('PRMS Document Review (Supplier)').AssignValue(str(DocReviewSup))

#Deliverable17
DesignDoc=(32+(29*QFU)+(QD*8))
Product.Attr('PRMS Project Design Documents').AssignValue(str(DesignDoc))

#Deliverable18
ProjectProc=54+(26*QFU)+(QD*6.5)
Product.Attr('PRMS Project Procedures (PEP_FAT_IOM)').AssignValue(str(ProjectProc))

#Deliverable19
ProjectMeet=2*int(Product.Attr('PRMS Estimated Project Duration (16-500)').GetValue())
Product.Attr('PRMS Project Meetings (Internal)').AssignValue(str(ProjectMeet))
C300=0
CN100=0
HIVE300=0
Virtual=0
Physical=0
universal=0
fam1=0
fam=0
family=0
Foundation=0
Profibus=0
Ethernet=0
PMIO=0
cont = Product.GetContainerByName("CE_System_Cont")
for row in cont.Rows:
    C300attr =row["C300_controlerrequred300_for_proposal"] if row["C300_controlerrequred300_for_proposal"] !='' else 0
    if int(C300attr) >0:
        Trace.Write("C300 "+str(row["C300_controlerrequred300_for_proposal"]))
        C300 +=1
    CN100ATR =row["C300_controler_100_for_proposal"] if row["C300_controler_100_for_proposal"] !='' else 0
    if int(CN100ATR) >0:
        Trace.Write("CN100 "+str(row["C300_controler_100_for_proposal"]))
        CN100 +=1
    HIVE300ATR =row["C300_100controlerrequred300_for_proposal"] if row["C300_100controlerrequred300_for_proposal"] !='' else 0
    if int(HIVE300ATR) >0:
        Trace.Write("HIVE300 "+str(row["C300_100controlerrequred300_for_proposal"]))
        HIVE300 +=1
    CN100attr =row["C300_Contro_vertual_for_proposal"] if row["C300_Contro_vertual_for_proposal"] !='' else 0
    if int(CN100attr) >0:
        Trace.Write("Virtual "+str(row["C300_Contro_vertual_for_proposal"]))
        Virtual +=1
    PhysicalATR =row["C300_contro_physical_for_proposal"] if row["C300_contro_physical_for_proposal"] !='' else 0
    if int(PhysicalATR) >0:
        Trace.Write("Physical "+str(row["C300_contro_physical_for_proposal"]))
        Physical +=1
    universalATR =row["C300_universal_marshling_for_proposal"] if row["C300_universal_marshling_for_proposal"] !='' else 0
    if int(universalATR) >0:
        Trace.Write("universal "+str(row["C300_universal_marshling_for_proposal"]))
        universal +=1
    famATR =row["C300_IO_FamilY1_for_proposal"] if row["C300_IO_FamilY1_for_proposal"] !='' else 0
    if int(famATR) >0:
        Trace.Write("CN100 "+str(row["C300_IO_FamilY1_for_proposal"]))
        fam +=1
    fam1ATR =row["C300_IO_FamilY2_for_proposal"] if row["C300_IO_FamilY2_for_proposal"] !='' else 0
    if int(fam1ATR) >0:
        Trace.Write("fam1 "+str(row["C300_IO_FamilY2_for_proposal"]))
        fam1 +=1
    familyATR =row["IO_Family_document"] if row["IO_Family_document"] !='' else 0
    if int(familyATR) >0:
        Trace.Write("family "+str(row["IO_Family_document"]))
        family +=1
    FoundationATR =row["Foundation_Fieldbus_document"] if row["Foundation_Fieldbus_document"] !='' else 0
    if int(FoundationATR) >0:
        Trace.Write("Foundation "+str(row["Foundation_Fieldbus_document"]))
        Foundation +=1
    ProfibusATR =row["Profibus_Gateway_Interface_document"] if row["Profibus_Gateway_Interface_document"] !='' else 0
    if int(ProfibusATR) >0:
        Trace.Write("Profibus "+str(row["Profibus_Gateway_Interface_document"]))
        Profibus +=1
    EthernetATR =row["Ethernet_Interface_document"] if row["Ethernet_Interface_document"] !='' else 0
    if int(EthernetATR) >0:
        Trace.Write("Ethernet "+str(row["Ethernet_Interface_document"]))
        Ethernet +=1
    PMIOATR =row["PM_IO_Solution_required_document"] if row["PM_IO_Solution_required_document"] !='' else 0
    if int(PMIOATR) >0:
        Trace.Write("PMIO "+str(row["PM_IO_Solution_required_document"]))
        PMIO +=1
Product.Attr("IO_Family_document").AssignValue(str(family))
Product.Attr("Foundation_Fieldbus_document").AssignValue(str(Foundation))
Product.Attr("Profibus_Gateway_Interface_document").AssignValue(str(Profibus))
Product.Attr("Ethernet_Interface_document").AssignValue(str(Ethernet))
Product.Attr("PM_IO_Solution_required_document").AssignValue(str(PMIO))
Product.Attr("C300_IO_FamilY1_for_proposal").AssignValue(str(fam))
Product.Attr("C300_IO_FamilY2_for_proposal").AssignValue(str(fam1))
Product.Attr("C300_controlerrequred300_for_proposal").AssignValue(str(C300))
Product.Attr("C300_controler_100_for_proposal").AssignValue(str(CN100))
Product.Attr("C300_100controlerrequred300_for_proposal").AssignValue(str(HIVE300))
Product.Attr("C300_Contro_vertual_for_proposal").AssignValue(str(Virtual))
Product.Attr("C300_contro_physical_for_proposal").AssignValue(str(Physical))
Product.Attr("C300_universal_marshling_for_proposal").AssignValue(str(universal))
Trace.Write("family ={} Foundation ={} Profibus ={} Ethernet ={} PMIO ={} fam ={} fam1 ={} C300 ={} CN100 ={} HIVE300 ={} Virtual ={} Physical ={} universal ={}".format(family,Foundation,Profibus,Ethernet,PMIO,fam,fam1,C300,CN100,HIVE300,Virtual,Physical,universal))
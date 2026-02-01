import System.Decimal as D
import GS_C300_BOM_Rail_IO_Part_calcs #only for remote group 
import GS_C300_BOM_UIO
import GS_C300_IO_Calc
import GS_C300_Cal_Parts
import GS_SerC_parts
import GS_C300_IO_Calc2
#CXCPQ-39275
def AMP_A(Product):
    A,B,C,D4=GS_C300_Cal_Parts.getpartsseriesc(Product)
    params = GS_C300_IO_Calc.getIOCount(Product, 'SerC_IO_Params', ['Z51', 'Z52', 'Z53'])
    UIO = GS_C300_BOM_UIO.IOComponents(Product)
    PUIO31,TUIO41,TUIO31,Amp_A=UIO.C300_Rail()
    rail=GS_C300_BOM_Rail_IO_Part_calcs.IOComponents(Product)
    MDUR18,MDUN12,TUIO11,TUIO01,Amp_A1=rail.C300_Rail()
    Sum1=Sum17A=Sum2=Sum3=Sum4=Sum5=Sum6=Sum7=Sum8=Sum9=pcntqnt=Sum10=Sum11=Sum12=Sum13=Sum14=Sum5N=Sum15=Sum16=Sum17=Sum18=Sum19=Sum20=Sum479N=AMP_A=Sum39N=Sum12N=Sum157N=Sum38N=Sum17Aa=Sum1A=Sum1B=parts5sum=tamtqnt1=tamtqnt2=SCMB02=SCMB05=tamtqnt3=0
    cg_part=Product.GetContainerByName('Series_C_CG_Part_Summary_Cont')
    rg_part=Product.GetContainerByName('Series_C_RG_Part_Summary_Cont')
    #for High volt cals
    parts01=['CC-SCMB02']
    part6=['CC-SFPR01'] 
    part0002=['TC-CCN014'] #
    part0003=['CC-CEN021'] #
    parts02=['CC-GDIL01','CC-GDIL11','CC-GDIL21']
    parts03=['CC-GAOX11','CC-GAOX21']
    parts05=['CC-PDIH01']
    parts5N=['CC-TPIX11']
    parts076=['CC-PAIM01']
    parts479=['CC-PAOH01','CC-PAOX01']
    parts095=['CC-PDIL01']
    parts147=['CC-SDOR01']
    part07=['CC-SDRX01','CC-PDIL51','CC-SDRX01']
    parts15=['CC-PCF901','CC-IION01']
    parts18=['CC-PAIH51','CC-PAIH02','CC-PAIN01','CC-PAIL51','CC-PAIX02','CC-PAIH01','CC-PAIX01']
    parts19=['CC-TDIL11','CC-TDIL01']
    parts212=['CC-PFB402']
    parts271=['CC-SCMB05']
    parts32=['CC-TAIX61','CC-TAIX51','CC-GAIX11','CC-GAIX21','CC-TAIN11','CC-TAIN01','CC-TAID01','CC-TAID11','CC-TAIX01','CC-TAIX11']
    pcnt=['CC-PCNT02','CC-PCNT05']
    parts39N=['CC-IP0101','CC-TPOX01','CC-TPOX01']
    parts346=['CC-PDIS01']
    parts48=['CC-PAOH51','CC-PAON01']
    parts8=['CC-PDOB01']
    parts50=['CC-TDOB11','CC-TDOB01']
    parts12N= ['CC-PPIX01']
    parts38N= ['CC-PFB801']
    parts157N= ['CC-PEIM01']
    railP= ['CC-MDUR18','CC-MDUN12']
    uio=['CC-TUIO41','CC-TUIO31','CC-PUIO31']
    enhance=['CC-TDOB11','CC-TDOB01']
    TION11part=['CC-TION11']
    if Product.Name=="Series-C Control Group":
        HN,HN2=GS_SerC_parts.Get_CG_IOTA(Product)
        a,b,qntpcnt=GS_C300_Cal_Parts.getPartCCPCNTQty(Product)
        mounting_sol=Product.Attr('SerC_CG_IO_Mounting_Solution').GetValue()
        #below calculation only applicable for control group
        controllerType = Product.Attr("SerC_CG_Controller_Type").GetValue()
        if controllerType == "Redundant":
            qntpcnt = qntpcnt * 2
        if Product.Attr('SerC_CG_Controller_Memory_Backup').GetValue() =="Yes" and controllerType == "Redundant": 
            SCMB02= D.Ceiling(qntpcnt /8.0)
            SCMB05= D.Ceiling(qntpcnt /8.0)
        else:
            SCMB02= D.Ceiling(qntpcnt /4.0)
            SCMB05= D.Ceiling(qntpcnt /8.0)
        Controller=Product.Attr('SerC_CG_Type_of_Controller_Required').GetValue()
        currnt=Product.Attr('SerC_CG_Current_required_for_each_DO').GetValue() if Product.Attr('SerC_CG_Current_required_for_each_DO').GetValue() !='' else 0
        curr= D.Ceiling(int(currnt)/1000.0)
        Trace.Write(currnt)
        if mounting_sol=="Cabinet":
            Trace.Write('Controller '+str(Controller))
            if Controller=='CN100 CEE':
                pcnt=['pcnt']
                parts15=['CC-IION01']
                parts18=['CC-PAIH51','CC-PAIH02','CC-PAIN01','CC-PAIL51','CC-PAIX02']
                parts32=['CC-GAIX21','CC-GAIX11','CC-TAID01','CC-TAID11','CC-TAIX51','CC-TAIX61','CC-TAIN11','CC-TAIN01','CC-TAIX01','CC-TAIX11']
                parts479=['CC-PAOH01']
                parts8=['CC-PDOB01']
            #for High volt cals
            for row in cg_part.Rows:
                #Trace.Write(row.GetColumnByName("PartNumber").Value)
                if row.GetColumnByName("PartNumber").Value in ['MC-TAMR04']: #tamt
                    tamtqnt3 =int(A) if A !='' else 0
                if row.GetColumnByName("PartNumber").Value in ['MC-TAMT04']: #tamt
                    tamtqnt1 =int(B) if B !='' else 0
                if row.GetColumnByName("PartNumber").Value in ['MC-TAMT14']: #tamt
                    tamtqnt2 =int(C) if C !='' else 0
                if row.GetColumnByName("PartNumber").Value in pcnt: #pcnt
                    pcntqnt +=int(qntpcnt) if qntpcnt !='' else 0
                if row.GetColumnByName("PartNumber").Value in parts50: #1
                    parts5sum +=int(row.GetColumnByName("Part_Qty").Value)
                if row.GetColumnByName("PartNumber").Value in part0002: #1
                    Sum1A +=int(row.GetColumnByName("Part_Qty").Value)
                if row.GetColumnByName("PartNumber").Value in part0003: #1
                    Sum1B +=int(row.GetColumnByName("Part_Qty").Value)
                if row.GetColumnByName("PartNumber").Value in parts5N: #1
                    Sum5N +=int(row.GetColumnByName("Part_Qty").Value)
                if row.GetColumnByName("PartNumber").Value in parts479: #1
                    Sum479N +=int(row.GetColumnByName("Part_Qty").Value)
                if row.GetColumnByName("PartNumber").Value in parts157N: #1
                    Sum157N +=int(row.GetColumnByName("Part_Qty").Value)
                if row.GetColumnByName("PartNumber").Value in parts38N: #1
                    Sum38N +=int(row.GetColumnByName("Part_Qty").Value)
                if row.GetColumnByName("PartNumber").Value in parts39N: #1
                    Sum39N +=int(row.GetColumnByName("Part_Qty").Value)
                if row.GetColumnByName("PartNumber").Value in parts12N: #1
                    #Sum12N +=int(row.GetColumnByName("Part_Qty").Value)
                    Sum12N += GS_C300_IO_Calc2.getParams44490(Product)
                if row.GetColumnByName("PartNumber").Value in parts01: #1
                    Sum1 =int(SCMB02)
                if row.GetColumnByName("PartNumber").Value in parts02: #2
                    Sum2 +=int(row.GetColumnByName("Part_Qty").Value)
                if row.GetColumnByName("PartNumber").Value in parts03: #3
                    Sum3 +=int(row.GetColumnByName("Part_Qty").Value)
                if row.GetColumnByName("PartNumber").Value in parts05: #4
                    Sum4 +=int(row.GetColumnByName("Part_Qty").Value)
                if row.GetColumnByName("PartNumber").Value in parts076: #5
                    Sum5 +=int(row.GetColumnByName("Part_Qty").Value)
                if row.GetColumnByName("PartNumber").Value in parts095: #6
                    Sum6 +=int(row.GetColumnByName("Part_Qty").Value)
                if row.GetColumnByName("PartNumber").Value in parts147: #7
                    Sum7 +=int(row.GetColumnByName("Part_Qty").Value)
                if row.GetColumnByName("PartNumber").Value in parts15: #8
                    Sum8 +=int(row.GetColumnByName("Part_Qty").Value)
                if row.GetColumnByName("PartNumber").Value in parts18: #9
                    Sum9 +=int(row.GetColumnByName("Part_Qty").Value)
                if row.GetColumnByName("PartNumber").Value in parts19: #10
                    Sum10 +=int(row.GetColumnByName("Part_Qty").Value)
                if row.GetColumnByName("PartNumber").Value in parts212: #11
                    Sum11 +=int(row.GetColumnByName("Part_Qty").Value)
                if row.GetColumnByName("PartNumber").Value in parts271: #12
                    Sum12 +=int(SCMB05)
                if row.GetColumnByName("PartNumber").Value in parts32: #13
                    Sum13 +=int(row.GetColumnByName("Part_Qty").Value)
                if row.GetColumnByName("PartNumber").Value in parts346: #14
                    Sum14 +=int(row.GetColumnByName("Part_Qty").Value)
                if row.GetColumnByName("PartNumber").Value in parts48: #15
                    Sum15 +=int(row.GetColumnByName("Part_Qty").Value)
                if row.GetColumnByName("PartNumber").Value in parts8: #16
                    Sum16 +=int(row.GetColumnByName("Part_Qty").Value)
                if row.GetColumnByName("PartNumber").Value in ['8937-HN2']: #16
                    Sum16 +=int(HN2) if HN2 != '' else 0
                if row.GetColumnByName("PartNumber").Value in TION11part: #17A
                    Sum17A +=int(row.GetColumnByName("Part_Qty").Value)
                if row.GetColumnByName("PartNumber").Value in part07: #17Aa
                    Sum17Aa +=int(row.GetColumnByName("Part_Qty").Value)
                if row.GetColumnByName("PartNumber").Value in part6: #17
                    Sum17 +=int(row.GetColumnByName("Part_Qty").Value)
                if row.GetColumnByName("PartNumber").Value in parts50: #17
                    Sum20 = D.Ceiling((params['Z51'])+(params['Z52'])+(params['Z53']))
                    Trace.Write("Sum20 "+str(Sum20))
                if row.GetColumnByName("PartNumber").Value in railP: #for Rail
                    Sum18 =Amp_A1
                    Trace.Write("Sum18 "+str(Sum18))
                if row.GetColumnByName("PartNumber").Value in uio: #for UIO
                    Sum19 =Amp_A
                    Trace.Write("Sum19AAAA "+str(Sum19))
            if Controller=='CN100 CEE':
                AMP_A= D.Ceiling((Sum17A*0.0028)+(Sum2*0.02)+Sum19+(Sum3*0.03)+(Sum4*0.05)+(Sum5*0.076)+(Sum6*0.095)+(Sum7*0.147)+(Sum10*0.19)+(Sum14*0.095)+((Sum8+tamtqnt1+tamtqnt2+tamtqnt3)*0.15)+(Sum9*0.18)+(Sum13*0.32)+(Sum479N*0.479)+(Sum15*0.48)+(Sum5N*0.5)+(Sum16*0.8)+(Sum12N)+(parts5sum*0))
            else:
                SumAB= D.Ceiling((Sum1A*0.002)+(Sum1B*0.003)+(parts5sum*0)+(pcntqnt*0.32)+((Sum8+tamtqnt1+tamtqnt2+tamtqnt3)*0.15))
                AMP_A=D.Ceiling((Sum5N*0.5)+(Sum157N*0.157)+(Sum479N*0.479)+(Sum38N*0.38)+(Sum39N*0.39)+(Sum1*0.271)+(Sum2*0.02)+(Sum3*0.03)+(Sum4*0.05)+(Sum5*0.076)+(Sum6*0.095)+(Sum7*0.147)+(Sum9*0.18)+(Sum10*0.19)+(Sum11*0.212)+(Sum12*0.271)+(Sum13*0.32)+(Sum14*0.095)+(Sum15*0.48)+(Sum16*0.8)+(Sum17*0.6)+(Sum12N)+(Sum17A*0.0028)+(Sum17Aa*0.07))
                AMP_A=AMP_A+(Sum18)+(Sum19)+(Sum20*5)+SumAB
    elif Product.Name=="Series-C Remote Group":
        Hn,HN2,X,Y=GS_SerC_parts.Get_RG_IOTA(Product)
        Controller=Product.Attr('SerC_CG_Type_of_Controller_Required').GetValue()
        mounting_sol=Product.Attr('SerC_IO_Mounting_Solution').GetValue()
        currnt=Product.Attr('SerC_CG_Current_required_for_each_DO1').GetValue() if Product.Attr('SerC_CG_Current_required_for_each_DO1').GetValue() !='' else 0
        curr=D.Ceiling(int(currnt)/1000)
        Trace.Write(currnt)
        #for High volt cals
        if mounting_sol=="Cabinet":
            Trace.Write('Controller '+str(Controller))
            if Controller=='CN100 CEE':
                pcnt=['pcnt']
                parts15=['CC-IION01']
                parts18=['CC-PAIH51','CC-PAIH02','CC-PAIN01','CC-PAIL51','CC-PAIX02']
                parts32=['CC-GAIX21','CC-GAIX11','CC-TAID01','CC-TAID11','CC-TAIX51','CC-TAIX61','CC-TAIN11','CC-TAIN01','CC-TAIX01','CC-TAIX11']
                parts479=['CC-PAOH01']
                parts8=['CC-PDOB01']
            #for High volt cals
            for row in rg_part.Rows:
                #Trace.Write(row.GetColumnByName("PartNumber").Value)
                if row.GetColumnByName("PartNumber").Value in ['MC-TAMR04']: #tamt
                    tamtqnt3 =int(A) if A !='' else 0
                if row.GetColumnByName("PartNumber").Value in ['MC-TAMT04']: #tamt
                    tamtqnt1 =int(B) if B !='' else 0
                if row.GetColumnByName("PartNumber").Value in ['MC-TAMT14']: #tamt
                    tamtqnt2 =int(C) if C !='' else 0
                if row.GetColumnByName("PartNumber").Value in pcnt: #pcnt
                    pcntqnt +=int(qntpcnt) if qntpcnt !='' else 0
                if row.GetColumnByName("PartNumber").Value in parts50: #1
                    parts5sum +=int(row.GetColumnByName("Part_Qty").Value)
                if row.GetColumnByName("PartNumber").Value in part0002: #1
                    Sum1A +=int(row.GetColumnByName("Part_Qty").Value)
                if row.GetColumnByName("PartNumber").Value in part0003: #1
                    Sum1B +=int(row.GetColumnByName("Part_Qty").Value)
                if row.GetColumnByName("PartNumber").Value in parts5N: #1
                    Sum5N +=int(row.GetColumnByName("Part_Qty").Value)
                if row.GetColumnByName("PartNumber").Value in parts479: #1
                    Sum479N +=int(row.GetColumnByName("Part_Qty").Value)
                if row.GetColumnByName("PartNumber").Value in parts157N: #1
                    Sum157N +=int(row.GetColumnByName("Part_Qty").Value)
                if row.GetColumnByName("PartNumber").Value in parts38N: #1
                    Sum38N +=int(row.GetColumnByName("Part_Qty").Value)
                if row.GetColumnByName("PartNumber").Value in parts39N: #1
                    Sum39N +=int(row.GetColumnByName("Part_Qty").Value)
                if row.GetColumnByName("PartNumber").Value in parts12N: #1
                    #Sum12N +=int(row.GetColumnByName("Part_Qty").Value)
                    Sum12N += GS_C300_IO_Calc2.getParams44490(Product)
                if row.GetColumnByName("PartNumber").Value in parts01: #1
                    Sum1 +=int(row.GetColumnByName("Part_Qty").Value)
                if row.GetColumnByName("PartNumber").Value in parts02: #2
                    Sum2 +=int(row.GetColumnByName("Part_Qty").Value)
                if row.GetColumnByName("PartNumber").Value in parts03: #3
                    Sum3 +=int(row.GetColumnByName("Part_Qty").Value)
                if row.GetColumnByName("PartNumber").Value in parts05: #4
                    Sum4 +=int(row.GetColumnByName("Part_Qty").Value)
                if row.GetColumnByName("PartNumber").Value in parts076: #5
                    Sum5 +=int(row.GetColumnByName("Part_Qty").Value)
                if row.GetColumnByName("PartNumber").Value in parts095: #6
                    Sum6 +=int(row.GetColumnByName("Part_Qty").Value)
                if row.GetColumnByName("PartNumber").Value in parts147: #7
                    Sum7 +=int(row.GetColumnByName("Part_Qty").Value)
                if row.GetColumnByName("PartNumber").Value in parts15: #8
                    Sum8 +=int(row.GetColumnByName("Part_Qty").Value)
                if row.GetColumnByName("PartNumber").Value in parts18: #9
                    Sum9 +=int(row.GetColumnByName("Part_Qty").Value)
                if row.GetColumnByName("PartNumber").Value in parts19: #10
                    Sum10 +=int(row.GetColumnByName("Part_Qty").Value)
                if row.GetColumnByName("PartNumber").Value in parts212: #11
                    Sum11 +=int(row.GetColumnByName("Part_Qty").Value)
                if row.GetColumnByName("PartNumber").Value in parts271: #12
                    Sum12 +=int(row.GetColumnByName("Part_Qty").Value)
                if row.GetColumnByName("PartNumber").Value in parts32: #13
                    Sum13 +=int(row.GetColumnByName("Part_Qty").Value)
                if row.GetColumnByName("PartNumber").Value in parts346: #14
                    Sum14 +=int(row.GetColumnByName("Part_Qty").Value)
                if row.GetColumnByName("PartNumber").Value in parts48: #15
                    Sum15 +=int(row.GetColumnByName("Part_Qty").Value)
                if row.GetColumnByName("PartNumber").Value in parts8: #16
                    Sum16 +=int(row.GetColumnByName("Part_Qty").Value)
                if row.GetColumnByName("PartNumber").Value in ['8937-HN2']: #16
                    Sum16 +=int(HN2) if HN2 != '' else 0
                if row.GetColumnByName("PartNumber").Value in TION11part: #17A
                    Sum17A +=int(row.GetColumnByName("Part_Qty").Value)
                if row.GetColumnByName("PartNumber").Value in part07: #17Aa
                    Sum17Aa +=int(row.GetColumnByName("Part_Qty").Value)
                if row.GetColumnByName("PartNumber").Value in part6: #17
                    Sum17 +=int(row.GetColumnByName("Part_Qty").Value)
                if row.GetColumnByName("PartNumber").Value in parts50: #17
                    Sum20 = D.Ceiling((params['Z51'])+(params['Z52'])+(params['Z53']))
                    Trace.Write("Sum20 "+str(Sum20))
                if row.GetColumnByName("PartNumber").Value in railP: #for Rail
                    Sum18 =Amp_A1
                    Trace.Write("Sum18 "+str(Sum18))
                if row.GetColumnByName("PartNumber").Value in uio: #for UIO
                    Sum19 =Amp_A
                    Trace.Write("Sum19AAAA "+str(Sum19))
            if Controller=='CN100 CEE':
                AMP_A= D.Ceiling((Sum17A*0.0028)+(Sum2*0.02)+Sum19+(Sum3*0.03)+(Sum4*0.05)+(Sum5*0.076)+(Sum6*0.095)+(Sum7*0.147)+(Sum10*0.19)+(Sum14*0.095)+((Sum8+tamtqnt1+tamtqnt2+tamtqnt3)*0.15)+(Sum9*0.18)+(Sum13*0.32)+(Sum479N*0.479)+(Sum15*0.48)+(Sum5N*0.5)+(Sum16*0.8)+(Sum12N)+(parts5sum*0))
            else:
                SumAB= D.Ceiling((Sum1A*0.002)+(Sum1B*0.003)+(parts5sum*0)+(pcntqnt*0.32)+((Sum8+tamtqnt1+tamtqnt2+tamtqnt3)*0.15))
                AMP_A=D.Ceiling((Sum5N*0.5)+(Sum157N*0.157)+(Sum479N*0.479)+(Sum38N*0.38)+(Sum39N*0.39)+(Sum1*0.271)+(Sum2*0.02)+(Sum3*0.03)+(Sum4*0.05)+(Sum5*0.076)+(Sum6*0.095)+(Sum7*0.147)+(Sum9*0.18)+(Sum10*0.19)+(Sum11*0.212)+(Sum12*0.271)+(Sum13*0.32)+(Sum14*0.095)+(Sum15*0.48)+(Sum16*0.8)+(Sum17*0.6)+(Sum12N)+(Sum17A*0.0028)+(Sum17Aa*0.07))
                AMP_A=AMP_A+(Sum18)+(Sum19)+(Sum20*5)+SumAB
    return AMP_A
#a=AMP_A(Product)
#Trace.Write(a)
#Trace.Write(b)
#Calculation For Display count 
import math
import System.Decimal as D
market_seg=TagParserProduct.ParseString('<*CTX( Quote.CustomField(Market Segment))*>')
if Product.Attr('Is HMI Engineering in Scope?').GetValue()=="Yes":
    display_s=display_m=display_c=Faceplate_s=Faceplate_m=Faceplate_C=0
    display=Product.GetContainerByName('Experion_Ent_Displays_Shapes_Faceplates').Rows[0].GetColumnByName('Customer Data').Value
    if display=='':
        display=0
    Trace.Write(display)
    display = int(float(display)) if isinstance(display, str) and display.strip() else int(float(display) if display else 0)
    if market_seg=="1000 - Refining":
        display_s=round(0.1*int(display))
        display_m=round(0.7*int(display))
        display_c=round(0.2*int(display))
    elif market_seg=="1400 - Chemicals and Petrochem":
        display_s=round(0.3*int(display))
        display_m=round(0.3*int(display))
        display_c=round(0.4*int(display))
    elif market_seg=="1100 - Oil and Gas":
        display_s=round(0.15*int(display))
        display_m=round(0.6*int(display))
        display_c=round(0.25*int(display))
    elif market_seg=="1600 - Life Sciences":
        display_s=round(0.1*int(display))
        display_m=round(0.2*int(display))
        display_c=round(0.7*int(display))
    elif market_seg=="1200 - Pulp, Paper, Printing & CWS":
        display_s=round(0.25*int(display))
        display_m=round(0.4*int(display))
        display_c=round(0.35*int(display))
    elif market_seg=="1300 - Power Generation":
        display_s=round(0.2*int(display))
        display_m=round(0.5*int(display))
        display_c=round(0.3*int(display))
    elif market_seg!='':
        display_s=round(0.4*int(display))
        display_m=round(0.1*int(display))
        display_c=round(0.5*int(display))
    Product.GetContainerByName('Experion_Ent_Displays_Shapes_Faceplates').Rows[1].SetColumnValue('Calculated Value', str(int(display_s)))
    Product.GetContainerByName('Experion_Ent_Displays_Shapes_Faceplates').Rows[2].SetColumnValue('Calculated Value', str(int(display_m)))
    Product.GetContainerByName('Experion_Ent_Displays_Shapes_Faceplates').Rows[3].SetColumnValue('Calculated Value', str(int(display_c)))
    #for Faceplate calcs
    Faceplate=round((math.sqrt(int(display)))*0.4)
    Methodology=Product.Attr('Implementation Methodology').GetValue()
    Faceplate_s=Faceplate_m=Faceplate_C=0
    if Methodology=="Non-Standard Build Estimate":
        if Faceplate >25:
            Faceplate=25
        Faceplate_s=round(0.1*int(Faceplate))
        Faceplate_m=round(0.7*int(Faceplate))
        Faceplate_C=round(0.2*int(Faceplate))
    Product.GetContainerByName('Experion_Ent_Displays_Shapes_Faceplates').Rows[11].SetColumnValue('Calculated Value', str(int(Faceplate_s)))
    Product.GetContainerByName('Experion_Ent_Displays_Shapes_Faceplates').Rows[12].SetColumnValue('Calculated Value', str(int(Faceplate_m)))
    Product.GetContainerByName('Experion_Ent_Displays_Shapes_Faceplates').Rows[13].SetColumnValue('Calculated Value', str(int(Faceplate_C)))
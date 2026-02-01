# this action helps to populats Proposal
import GS_PopulatePASPLCDocumentTable
import GS_PopulatePASUOCDocumentTable
import GS_PopulatePASRTUDocumentTable
import GS_PopulatePASSMDocumentTable
import GS_PopulatePAS_EXPENT__DocumentTable
import GS_PAS_C300Documnet_Generater

Cond = TagParserQuote.ParseString("[AND]([OR](([EQ](<*CTX( Quote.CustomField(Booking LOB) )*>,PAS)),([EQ](<*CTX( Quote.CustomField(Booking LOB) )*>,LSS)),([EQ](<*CTX( Quote.CustomField(Booking LOB) )*>,PMC))),[EQ](<*CTX( Quote.CustomField(Quote Type) )*>,Projects), [GT](<*Table(select COUNT(*) from cart_item i where i.CATALOGCODE = 'PRJT' and i.cart_id=<*CTX(Quote.CartId)*> and i.USERID=<*CTX(Quote.OwnerId)*>)*>,0))")

if Cond == '1':
    PLCFlag = GS_PopulatePASPLCDocumentTable.populatePASData(Quote)
    UOCFlag = GS_PopulatePASUOCDocumentTable.populateUOCData(Quote)
    RTUFlag = GS_PopulatePASRTUDocumentTable.populateRTUData(Quote)
    SMFlag = GS_PopulatePASSMDocumentTable.populateSMData(Quote)
    ExpEntFlag = GS_PopulatePAS_EXPENT__DocumentTable.populateEXP_ENTData(Quote)
    C300 = GS_PAS_C300Documnet_Generater.populateC300DataPoP(Quote)

    if not PLCFlag and not UOCFlag and not RTUFlag and not SMFlag and not ExpEntFlag and not C300:
        QT_Table = Quote.QuoteTables["PAS_Document_Data"]
        QT_Table.Rows.Clear()
[IF]([GT](<*VALUE(Additional Stations)*>,0)){<*ALLOWATTRIBUTES(Station Type)*><*SELECTVALUE(Station Type:STN_STD_DELL_Tower_NonRAID)*>
}{<*DISALLOWATTRIBUTES(Station Type)*>
}[ENDIF]
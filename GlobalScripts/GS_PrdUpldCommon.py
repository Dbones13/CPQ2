def fnEscpUniode(data, totalRows, colCont):
	Trace.Write("colCont==="+str(colCont))
	for i in range(1,totalRows):
		for j in range(0,colCont):
			data[i,j] = data[i,j].strip().encode('unicode_escape')
	return data
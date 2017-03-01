class ProgramList:

    programs = {'farmaco.exe':'Торговый отдел', \
                'doc_dlvr.exe':'Маршрутный лист', \
                'SalesRep.exe':'Отчеты по продажам', \
                'TaxBillReestr.exe':'test',\
                'cstmrsdt.exe':'Информация по клиентам'}

    
    def getProgramName(self,programName):
        if programName in self.programs:
            return self.programs[programName]
        else:
            return programName

class ProgramList:

    #program names dictionary
    programs = {'farmaco.exe':'Торговый отдел', \
                'doc_dlvr.exe':'Маршрутный лист', \
                'SalesRep.exe':'Отчеты по продажам', \
                'TaxBillReestr.exe':'TaxBillReestr.exe',\
                'cstmrsdt.exe':'Информация по клиентам', \
                'DOCWATCH.exe':'Документы на складе', \
                'boxcheck2.exe':'Выходной контроль ящиков', \
                'resupply.exe':'WMS Control Panel', \
                'SPTData2.exe':'Прием товара на склад', \
                'boxlnchr2.exe':'Box Launcher (A4)', \
                'boxlnchr.exe':'Box Launcher (A5)', \
                'gdsmvmnt.exe':'Движение товара', \
                'Inventor.exe':'Инвентор', \
                'DaysOut.exe':'DaysOut.exe', \
                'amplitud.exe':'amplitud.exe', \
                'SERTISCN.exe':'Хранилище сертификатов', \
                'scanfirst.exe':'Модуль сканирования штрихкодов', \
                'goodaddr.exe':'goodaddr.exe', \
                'monitor51.exe':'Монитор 51', \
                #Бухгалтеры
                'bartrep.exe':'БАРТЕР', \
                'f2mnpltr.exe':'Склеивание накладных', \
                'CHECK_GR.EXE':'Проверка', \
                'salesrst.exe':'salesrst.exe', \
                'cmanager2.exe':'Бонусы', \
                'exptrnfs.exe':'Хоз. операции', \
                'cust_bl.exe':'Блокировка', \
                'DOCCHECK.EXE':'DOCCHECK.EXE', \
                'paysaldo.exe':'paysaldo.exe', \
                'BUHG_ARM.exe':'БУХГАЛТЕРИЯ', \
                'PASSPORT.EXE':'ПАСПОРТ', \
                'debetmon.exe':'Акт сверки', \
                'Salary.exe':'Зарплата', \
                'refprices.exe':'Цены референтные'}

    #returns program name from dictionary or file
    #name if there is no such program    
    def getProgramName(self,programName):
        if programName in self.programs:
            return self.programs[programName]
        else:
            return programName

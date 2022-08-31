import numpy,http.client
import pandas as pd
import datetime
from io import StringIO



    
abbrevDict={'Oklahoma':'OK', 'Arkansas':'AR',
 'New York':'NY', 
 'Oregon':'OR',
 'West Virginia':'WV', 
 'New Mexico':'NM',
 'Maryland':'MD',
 'Utah':'UT',
 'Georgia':'GA', 
 'South Carolina':'SC', 
 'Minnesota':"MN",
 'Virginia':'VA', 
 'Michigan':"MI", 
 'Hawaii':'HI', 
 'Maine':"ME", 
 'Puerto Rico':"PR",
 'Tennessee':'TN', 
 'Montana':'MT',
 'Idaho':'ID', 
 'Mississippi':"MS",
 'California':"CA", 
 'South Dakota':'SD',
 'Missouri':'MO',
 'Colorado':'CO',
 'Illinois':'IL',
 'Delaware':'DE', 
 'Louisiana':'LA', 
 'New York City':'NYC',
 'Kentucky':'KY',
 'Connecticut':'CT', 
 'Nebraska':'NE',
 'Ohio':'OH',
 'Washington':'WA', 
 'United States':"US", 
 'Massachusetts':"MA",
 'North Dakota':'ND', 
 'District of Columbia':'DC', 
 'the District of Columbia':'DC',           
 'Vermont':'VT',
 'New Hampshire':'NH',
 'Iowa':'IA',
 'Nevada':'NV',
 'Alabama':'AL',
 'Arizona':"AZ",
 'North Carolina':'NC', 
 'Wisconsin':'WI',
 'New Jersey':"NJ",
 'Rhode Island':'RI',
 'Texas':"TX", 
 'Alaska':'AK', 
 'Pennsylvania':"PA",
 'Wyoming':"WY",
 'Indiana':"IN",
 'Kansas':"KS",
 'Florida':"FL"}

abbrevStates=list(abbrevDict.keys())

abbrevStates.remove('the District of Columbia')

reverseAbbrevDict=dict(zip([abbrevDict[st] for st in abbrevStates],abbrevStates))
  
def recreateStringency(minDateInt=20200301,maxDateInt=20220301,oxf=pd.DataFrame({'a':[1]}),metric='StringencyIndex'):
    #columns of csv:
    #CountryName,CountryCode,RegionName,RegionCode,Jurisdiction,Date,C1_School closing,C1_Flag,C2_Workplace closing,C2_Flag,C3_Cancel public events,C3_Flag,C4_Restrictions on gatherings,C4_Flag,C5_Close public transport,C5_Flag,C6_Stay at home requirements,C6_Flag,C7_Restrictions on internal movement,C7_Flag,C8_International travel controls,E1_Income support,E1_Flag,E2_Debt/contract relief,E3_Fiscal measures,E4_International support,H1_Public information campaigns,H1_Flag,H2_Testing policy,H3_Contact tracing,H4_Emergency investment in healthcare,H5_Investment in vaccines,H6_Facial Coverings,H6_Flag,H7_Vaccination policy,H7_Flag,H8_Protection of elderly people,H8_Flag,M1_Wildcard,ConfirmedCases,ConfirmedDeaths,StringencyIndex,StringencyIndexForDisplay,StringencyLegacyIndex,StringencyLegacyIndexForDisplay,GovernmentResponseIndex,GovernmentResponseIndexForDisplay,ContainmentHealthIndex,ContainmentHealthIndexForDisplay,EconomicSupportIndex,EconomicSupportIndexForDisplay
    if (oxf.columns[0] == 'a'):
        print('READING oxf')
        oxf=pd.read_csv('https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/OxCGRT_latest.csv')  
    #print(list(set(oxf['RegionName'].values)))
    means=oxf[numpy.logical_and(oxf.Date >= minDateInt,oxf.Date <= maxDateInt)].groupby('RegionName')[metric].mean()
    stateDct=dict()
    #print('means::::')
    #print(means)
    for state in abbrevDict:
        if (not (state in ['Puerto Rico','New York City','United States','the District of Columbia'])):
            if (state=='District of Columbia'):
                stateDct[state]=means['Washington DC']
            else:
                stateDct[state]=means[state]
    return stateDct


    
def getStringencyByMonth(startYearAndMonth,endYearAndMonth,day=1,metric='StringencyIndex'):
    #oxf=pd.read_csv('https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/OxCGRT_latest.csv') 
    print('stringency new way')
    oxf=pd.read_csv('C:\\Users\\joe_s\\OneDrive\\CovidGiniPaper\\OfficialData_downloadedJuly25_2022\\OxCGRT_latest.csv')
    startYear,startMonth=startYearAndMonth
    endYear,endMonth=endYearAndMonth
    def getInt(year,month):
        #return year*10000 + month*100 + 1
        return year*10000 + month*100 + day
    
    startInt=getInt(startYear,startMonth)
    endInt=getInt(endYear,endMonth)
    def getNext(year,month):
        if (month==12):
            return year+1,1
        else:
            return year, month +1
    nextYear,nextMonth=getNext(startYear,startMonth)
    nextInt=getInt(nextYear,nextMonth)
    currYear=startYear
    currMonth=startMonth
    currInt=startInt
    stateDct=dict()
    while (nextInt <= endInt):
        print((currYear,currMonth))
        stateDct[(currYear,currMonth)]=recreateStringency(currInt,nextInt,oxf=oxf,metric=metric)
        currInt=nextInt
        currYear=nextYear
        currMonth=nextMonth
        nextYear,nextMonth=getNext(currYear,currMonth)
        nextInt=getInt(nextYear,nextMonth)               
    return stateDct


def getRaifmanDataByMonth(startEndFieldPairs,startYearAndMonth,endYearAndMonth):
    print('Raifman new way')
    
    df=pd.read_csv('C:\\Users\\joe_s\\OneDrive\\CovidGiniPaper\\OfficialData_downloadedJuly25_2022\\COVID-19 US state policy database 3_30_2022.csv')
    
    #    RaifmanStatePolicy.csv')
    valStart=4
    states=df['STATE'].values[valStart:]
    def toDateObj(aStrIn):
        #print(aStrIn)
        if (type(aStrIn) != str):
            if (numpy.isnan(aStrIn)):
                return None
        aStr=aStrIn.strip()
        if (aStr=='0'):
            return None
        #print('aStr',aStr)
        splts=aStr.split('/')
        month=int(splts[0])
        day=int(splts[1])
        year=int(splts[2])
        return datetime.date(year,month,day)
    
    def getDctForPair(pair):
        startField,endField=pair
        states=df['STATE'].values[valStart:]
        startDates=[toDateObj(v) for v in df[startField].values[valStart:]]
        if (endField=='FMSCHOOL_END_2022'):
            endDates=[datetime.date(2022,6,15) for v in df[startField].values[valStart:]]
        else:
            endDates=[toDateObj(v) for v in df[endField].values[valStart:]]
        startAndEndDates=zip(startDates,endDates)
        return dict(zip(states,startAndEndDates))
    dctList=[]
    for pair in startEndFieldPairs:
        dctList.append(getDctForPair(pair)) 
        
    month=startYearAndMonth
    
    dctByMonth=dict()
    while (month <= endYearAndMonth):
        #print('dctByMonth')
        dctByMonth[(month.year,month.month)]=dict()
        #print(dctByMonth)
        for state in abbrevDict.keys():
            if (state in ['Puerto Rico','New York City','Guam','United States','the District of Columbia']):
                continue
            if (month.month==12):
                nextMonth=datetime.date(month.year+1,1,1)
            else:
                nextMonth=datetime.date(month.year,month.month +1,1)
           
            totalDaysInside=0
            for dct in dctList:
                #print(dct.keys())
                windowStartDate,windowEndDate=dct[state]
                if (windowStartDate==None):
                    continue
                if (windowEndDate==None):
                    windowEndDate=datetime.date(2100,1,1)
                if (month >= windowStartDate):
                    #month entirely contained
                    if (nextMonth <= windowEndDate):
                        daysInside=(nextMonth-month).days
                    else:
                        #month starts inside window, ends outside
                        daysInside=numpy.max([(windowEndDate-month).days,0])
                elif (nextMonth <= windowEndDate):
                    daysInside=numpy.max([( (nextMonth - windowStartDate).days,0)])
                else:
                    daysInside=(windowEndDate-windowStartDate).days
                totalDaysInside=totalDaysInside + daysInside
            daysInMonth=(nextMonth-month).days
            if (totalDaysInside > daysInMonth):
                raise Exception('days inside should not be > days in month')
                
            #print('month here',month)
            dctByMonth[(month.year,month.month)][state]=float(totalDaysInside)/daysInMonth
        month=nextMonth
    return dctByMonth

           
    
def getMobilityByMonth(startYearAndMonth,endYearAndMonth,day=1,fields=['retail_and_recreation',
                                                                       'grocery_and_pharmacy',
                                                                       'parks',
                                                                       'transit_stations',
                                                                       'workplaces']):
    print('mobility new way')
    baseDir="C:\\Users\\joe_s\\OneDrive\\CovidGiniPaper\\OfficialData_downloadedJuly25_2022\\GoogleMobilityData"
    
    df2020=pd.read_csv(baseDir + "\\Region_Mobility_Report_CSVs\\2020_US_Region_Mobility_Report.csv")
    df2021=pd.read_csv(baseDir + "\\Region_Mobility_Report_CSVs\\2021_US_Region_Mobility_Report.csv")
    df2022=pd.read_csv(baseDir + "\\Region_Mobility_Report_CSVs\\2022_US_Region_Mobility_Report.csv")
                       
    #print(df2020['date'])
    addDateObjMobility(df2020,dateStr='date')
    addDateObjMobility(df2021,dateStr='date')
    addDateObjMobility(df2022,dateStr='date')
    month=startYearAndMonth
    if (month.month==12):
        nextMonth=datetime.date(month.year+1,1,1)
    else:
        nextMonth=datetime.date(month.year,month.month +1,1)
    dctByMonth=dict()
    suffix="_percent_change_from_baseline"
    while (month <= endYearAndMonth):
        print(month)
        if (month.year==2020):
            df=df2020
        elif (month.year==2021):
            df=df2021
        elif (month.year==2022):
            df=df2022
        else:
            raise Exception('no mobility data for year %d'%year)
         
        dctByMonth[(month.year,month.month)]=dict()
        #print('month here', dctByMonth[month])
        for abbrev in abbrevDict.keys():
            state=abbrev
            stateDF=df[df['sub_region_1']==state]
            meanMetric=numpy.mean([stateDF[numpy.logical_and(stateDF['DateObj'] >= month,
                                             stateDF['DateObj'] < nextMonth)][metric + suffix].mean() for metric in fields])
            dctByMonth[(month.year,month.month)][state]=-meanMetric
        month=nextMonth
        if (month.month==12):
            nextMonth=datetime.date(month.year+1,1,1)
        else:
            nextMonth=datetime.date(month.year,month.month +1,1)
    return dctByMonth

def getVaxRateByMonth(startYearAndMonth,endYearAndMonth,day=1,boosted=False):
    vaxDF=pd.read_csv('C:\\Users\\joe_s\\OneDrive\\CovidGiniPaper\\OfficialData_downloadedJuly25_2022\\COVID-19_Vaccinations_in_the_United_States_Jurisdiction.csv')
    addDateObjAlt(vaxDF)
    month=startYearAndMonth
    if (month.month==12):
        nextMonth=datetime.date(month.year+1,1,1)
    else:
        nextMonth=datetime.date(month.year,month.month +1,1)
    dctByMonth=dict()
    while (month < endYearAndMonth):
        dctByMonth[month]=dict()
        #print('month here', dctByMonth[month])
        for abbrev in abbrevDict.keys():
            state=abbrevDict[abbrev]
            #print('state',state)
            stateDF=vaxDF[vaxDF.Location==state] 
            
            #metric='Series_Complete_65PlusPop_Pct'
            if (boosted):
                metric='Additional_Doses_Vax_Pct'
                #metric='Additional_Doses_50Plus_Vax_Pct'
            else:
                metric='Series_Complete_Pop_Pct'
                #metric='Administered_Dose1_Pop_Pct'
            meanVaxRate=stateDF[numpy.logical_and(stateDF['DateObj'] >= month,
                                                  stateDF['DateObj'] < nextMonth)][metric].mean()
            #print('month here again', dctByMonth[month])
            #print('meanVax',meanVaxRate)
            dctByMonth[month][reverseAbbrevDict[state]]=meanVaxRate
        month=nextMonth
        if (month.month==12):
            nextMonth=datetime.date(month.year+1,1,1)
        else:
            nextMonth=datetime.date(month.year,month.month +1,1)
    return dctByMonth
 
def readCDC_CSV(fName):
        inF=open(fName,'r')
        line=inF.readline()
        line=inF.readline()
        line=inF.readline()
        content=''
        while (line.strip() != ''):
            content=content + line + '\n'
            line=inF.readline()
        return content
    
def addCovidCasesByMonth(startMonth=datetime.date(2020,3,1),endMonth=datetime.date(2021,5,1)):
    import os
    #from io import StringIO
    #files downloaded from https://covid.cdc.gov/covid-data-tracker/#trends_dailytrendsdeaths
    #files=os.listdir('cdcCovidDeathsCleaned')
    #files=os.listdir('cdcCovidCases_May25_2022_cleaned')
    theDir='OfficialData_downloadedJuly25_2022\\cdcCovidCases_July25_2022'
    files=os.listdir(theDir)
    #files=os.listdir('cdcCovidDeaths_Dec9_Cleaned')
    stateDct=dict()
    
    
    
    for fle in files:
        print(fle)
        #df=addDateObj(pd.read_csv('cdcCovidCases_May25_2022_cleaned/' + fle))
        df=addDateObj(pd.read_csv(StringIO(readCDC_CSV(theDir + '\\' + fle))))
        #state=fle.replace('data_table_for_daily_case_trends__','').replace('_',' ')
        #state=state.replace('.csv','').replace('_',' ')
        
        state=fle.replace('data_table_for_daily_case_trends__','').replace('.csv','')
        state=state.replace('(1)','').replace('(2)','').replace('(3)','').strip()
        state=state.replace('_(excludes_nyc)_','')
        state=state.replace('_',' ').strip()
        #state=fle.split('__')[0].strip().replace('_',' ')
        capitalized=[]
        print(state)
        for word in state.split(' '):
            if (word != 'of'):
                capitalized.append(word[0].upper() + word[1:])
            else:
                capitalized.append(word)
        state=' '.join(capitalized)
        stateDct[state]=df
    month=startMonth
    if (month.month==12):
        nextMonth=datetime.date(month.year+1,1,1)
    else:
        nextMonth=datetime.date(month.year,month.month +1,1)
    dctByMonth=dict()
    while (month < endMonth):
        dctByMonth[month]=dict()
        for state in stateDct:
            df=stateDct[state] 
            cases=df[numpy.logical_and(df['DateObj'] >= month,df['DateObj'] < nextMonth)]['New Cases'].sum()
            dctByMonth[month][state]=cases
        #print(dctByMonth[month].keys())
        dctByMonth[month]['New York']=dctByMonth[month]['New York'] + dctByMonth[month]['New York City']
        month=nextMonth
        if (month.month==12):
            nextMonth=datetime.date(month.year+1,1,1)
        else:
            nextMonth=datetime.date(month.year,month.month +1,1)
    return dctByMonth

def addCovidDeathsByMonth(startMonth=datetime.date(2020,3,1),endMonth=datetime.date(2021,5,1)):
    import os
    #files downloaded from https://covid.cdc.gov/covid-data-tracker/#trends_dailytrendsdeaths
    #files=os.listdir('cdcCovidDeathsCleaned')
    #files=os.listdir('cdcCovidDeaths_May12_2022_cleaned')
    theDir='OfficialData_downloadedJuly25_2022\\cdcCovidDeaths_July25_2022'
    files=os.listdir(theDir)
    #files=os.listdir('cdcCovidDeaths_Dec9_Cleaned')
    stateDct=dict()
    for fle in files:
        print(fle)
        df1=pd.read_csv(StringIO(readCDC_CSV(theDir + '/' + fle)))
        #print('cols',df1.columns)
        df=addDateObj(pd.read_csv(StringIO(readCDC_CSV(theDir + '/' + fle))))
        #state=fle.replace('_deaths.csv','').replace('_',' ')
        #state=fle.replace('.csv','').replace('_',' ')
        state=fle.replace('data_table_for_daily_death_trends__','').replace('.csv','').replace('(2)','').replace('(3)','').strip()
        state=state.replace('_(excludes_nyc)_','')
        state=state.replace('_',' ').strip()
        #state=fle.split('__')[0].strip().replace('_',' ')
        capitalized=[]
        for word in state.split(' '):
            print('STATE:',state)
            if (word != 'of'):
                capitalized.append(word[0].upper() + word[1:])
            else:
                capitalized.append(word)
        state=' '.join(capitalized)
        #print('state here',state)
        stateDct[state]=df
    month=startMonth
    if (month.month==12):
        nextMonth=datetime.date(month.year+1,1,1)
    else:
        nextMonth=datetime.date(month.year,month.month +1,1)
    dctByMonth=dict()
    while (month < endMonth):
        dctByMonth[month]=dict()
        for state in stateDct:
            df=stateDct[state] 
            deaths=df[numpy.logical_and(df['DateObj'] >= month,df['DateObj'] < nextMonth)]['New Deaths'].sum()
            dctByMonth[month][state]=deaths
        #print(dctByMonth[month].keys())
        dctByMonth[month]['New York']=dctByMonth[month]['New York'] + dctByMonth[month]['New York City']
        month=nextMonth
        if (month.month==12):
            nextMonth=datetime.date(month.year+1,1,1)
        else:
            nextMonth=datetime.date(month.year,month.month +1,1)
    return dctByMonth
    
def specificStringencyMeasures(minDateInt=20210601,maxDateInt=20220301):
    #columns of csv:
    #CountryName,CountryCode,RegionName,RegionCode,Jurisdiction,Date,C1_School closing,C1_Flag,C2_Workplace closing,C2_Flag,C3_Cancel public events,C3_Flag,C4_Restrictions on gatherings,C4_Flag,C5_Close public transport,C5_Flag,C6_Stay at home requirements,C6_Flag,C7_Restrictions on internal movement,C7_Flag,C8_International travel controls,E1_Income support,E1_Flag,E2_Debt/contract relief,E3_Fiscal measures,E4_International support,H1_Public information campaigns,H1_Flag,H2_Testing policy,H3_Contact tracing,H4_Emergency investment in healthcare,H5_Investment in vaccines,H6_Facial Coverings,H6_Flag,H7_Vaccination policy,H7_Flag,H8_Protection of elderly people,H8_Flag,M1_Wildcard,ConfirmedCases,ConfirmedDeaths,StringencyIndex,StringencyIndexForDisplay,StringencyLegacyIndex,StringencyLegacyIndexForDisplay,GovernmentResponseIndex,GovernmentResponseIndexForDisplay,ContainmentHealthIndex,ContainmentHealthIndexForDisplay,EconomicSupportIndex,EconomicSupportIndexForDisplay
    oxf=pd.read_csv('https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/OxCGRT_latest.csv')  
    #print(list(set(oxf['RegionName'].values)))
    stateDct=dict()
    for measure in ['GovernmentResponseIndex','C1_School closing','C2_Workplace closing','C3_Cancel public events','C4_Restrictions on gatherings','C5_Close public transport','C6_Stay at home requirements','C7_Restrictions on internal movement','E1_Income support','E2_Debt/contract relief','E3_Fiscal measures','H1_Public information campaigns','H2_Testing policy','H6_Facial Coverings']:
        means=oxf[numpy.logical_and(oxf.Date >= minDateInt,oxf.Date < maxDateInt)].groupby('RegionName')[measure].mean()
        for state in abbrevDict:
            if (not (state in stateDct)):
                stateDct[state]=dict()
            if (not (state in ['Puerto Rico','New York City','United States','the District of Columbia'])):
                if (state=='District of Columbia'):
                    stateDct[state][measure.strip().replace(' ','_')]=means['Washington DC']
                else:
                    stateDct[state][measure.strip().replace(' ','_')]=means[state]
    return stateDct

        
def getExcessPctByMonth(sloppyWay=False,typ='Predicted (weighted)',metric='ExcessPct',negativesAllowed=False):
    df=pd.read_csv('C:\\Users\joe_s\\OneDrive\\CovidGiniPaper\\OfficialData_downloadedJuly25_2022\\Excess_Deaths_Associated_with_COVID-19.csv')
    df=df[df['Type']==typ]
    df=df[df['Outcome']=='All causes']
    
    def excessPct(obsNum,avgExpectedCount):
        if (numpy.isnan(obsNum)):
            return 0
        if (avgExpectedCount ==0):
            return 0
        return 100*(obsNum-avgExpectedCount)/avgExpectedCount
    
    df['ExcessPct']=df.apply(lambda dFrame: excessPct(dFrame['Observed Number'],dFrame['Average Expected Count']),axis=1)
    #print(df['Week Ending Date'])
    def monthFromDateString(date):
        splts=date.strip().split('-')
        year=int(splts[0])
        month=int(splts[1])
        return datetime.date(year,month,1)
    def dayFromDateString(date):
        splts=date.strip().split('-')
        year=int(splts[0])
        month=int(splts[1])
        day=int(splts[2])
        return datetime.date(year,month,day)
    df['MonthStartObj']=df['Week Ending Date'].apply(monthFromDateString)
    df=df[df['MonthStartObj'] >=datetime.date(2019,11,1)] 
    if (sloppyWay):
         return df.groupby(['State','MonthStartObj'])['Percent Excess Estimate'].mean()
    df['WeekEndingDayObj']=df['Week Ending Date'].apply(dayFromDateString)
    def weightForWeek(weekEndingDayObj,monthStartObj):
        if (weekEndingDayObj < monthStartObj):
            return 0
        if (weekEndingDayObj - monthStartObj > datetime.timedelta(38)):
            return 0
        count=0
        for dayDelta in range(0,7):
            day=weekEndingDayObj - datetime.timedelta(dayDelta)
            if (day.month==monthStartObj.month):
                count=count +1
        return count
    dct=dict()
    for month in list(set(df['MonthStartObj'].values)):
        if (month > datetime.date(2022,4,1)):
            continue
        print('month',str(month))
        totalWeight=dict()
        totalWeightedSum=dict()
        totalSum=dict()
        for week in list(set(df['WeekEndingDayObj'].values)):
            weekWeight=weightForWeek(week,month)
            if (weekWeight > 0):
                #print('weekWeight',weekWeight)
                for state in list(set(df['State'].values)):
                    #print('state',state)
                    #print(df[numpy.logical_and(df.State==state,df.WeekEndingDayObj==week)]['Percent Excess Estimate'].values[0])
                    if (metric=='ExcessPct'):
                        if (negativesAllowed):
                            col='ExcessPct'
                        else:
                            col='Percent Excess Estimate'
                    else:
                        col=metric
                    totalWeightedSum[state]=totalWeightedSum.get(state,0) + weekWeight*df[numpy.logical_and(df.State==state,df.WeekEndingDayObj==week)][col].values[0]
                    totalSum[state]=totalSum.get(state,0) + weekWeight*df[numpy.logical_and(df.State==state,df.WeekEndingDayObj==week)][col].values[0]/7.
                    totalWeight[state]=totalWeight.get(state,0) + weekWeight
        for state in list(set(df['State'].values)):
            if (metric=='ExcessPct'):
                dct[(state,month)]=totalWeightedSum[state]/totalWeight[state]
            elif (metric in ['Excess Estimate','Average Expected Count']):
                dct[(state,month)]=int(numpy.round(totalSum[state]))
            else:
                dct[(state,month)]=int(numpy.round(totalWeightedSum[state]/totalWeight[state]))
    return dct
                                 
           

def dateStrToDate(dStr):
    #print('dStr',dStr)
    monthMap={'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}
    splts=dStr.strip().split(' ')
    #print('splts',splts)
    if (len(splts)==4):
        year=int(splts[3].strip())
        day=int(splts[2].strip())
        month=monthMap[splts[0].strip()]
    else:
        year=int(splts[2].strip())
        day=int(splts[1].strip())
        month=monthMap[splts[0].strip()]
    return datetime.date(year,month,day)
                   
def addDateObj(cdcDF):
    cdcDF['DateObj']=cdcDF['Date'].apply(dateStrToDate)
    return cdcDF

def dateStrExcessToDate(dStr):
    splts=dStr.strip().split('-')
    return datetime.date(int(splts[0]),int(splts[1]),int(splts[2]))

def nursingDateStrToDate(dStr):
    splts=dStr.split('/')
    #print(splts)
    return datetime.date(2000+int(splts[2]),int(splts[0]),int(splts[1]))

def addWeekEndDateObjNursing(exDF):
    exDF['WeekEndingObj']=exDF['Week Ending'].apply(nursingDateStrToDate)

def addWeekEndDateObj(exDF):
    exDF['WeekEndingObj']=exDF['Week Ending Date'].apply(dateStrExcessToDate)
                   
def dateStrExcessToDateAlt(dStr):
    print(dStr)
    splts=dStr.strip().split('/')
    return datetime.date(int(splts[2]),int(splts[0]),int(splts[1]))

def dateStrExcessToDateMobility(dStr):
    #print(dStr)
    splts=dStr.strip().split('-')
    return datetime.date(int(splts[0]),int(splts[1]),int(splts[2]))

def addDateObjMobility(exDF,dateStr='date'):
    exDF['DateObj']=exDF[dateStr].apply(dateStrExcessToDateMobility) 

def addDateObjAlt(exDF,dateStr='Date'):
    exDF['DateObj']=exDF[dateStr].apply(dateStrExcessToDateAlt)  
    
def addWeekEndDateObjAlt(exDF):
    exDF['WeekEndingObj']=exDF['Week Ending Date'].apply(dateStrExcessToDateAlt)  
  
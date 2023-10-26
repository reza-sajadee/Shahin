from datetime import datetime as dt

def gregorian_to_jalali(gy, gm, gd):
 g_d_m = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
 if (gm > 2):
  gy2 = gy + 1
 else:
  gy2 = gy
 days = 355666 + (365 * gy) + ((gy2 + 3) // 4) - ((gy2 + 99) // 100) + ((gy2 + 399) // 400) + gd + g_d_m[gm - 1]
 jy = -1595 + (33 * (days // 12053))
 days %= 12053
 jy += 4 * (days // 1461)
 days %= 1461
 if (days > 365):
  jy += (days - 1) // 365
  days = (days - 1) % 365
 if (days < 186):
  jm = 1 + (days // 31)
  jd = 1 + (days % 31)
 else:
  jm = 7 + ((days - 186) // 30)
  jd = 1 + ((days - 186) % 30)
 return [jy, jm, jd]

def jalali_to_gregorian(jy, jm, jd):
 jy += 1595
 days = -355668 + (365 * jy) + ((jy // 33) * 8) + (((jy % 33) + 3) // 4) + jd
 if (jm < 7):
  days += (jm - 1) * 31
 else:
  days += ((jm - 7) * 30) + 186
 gy = 400 * (days // 146097)
 days %= 146097
 if (days > 36524):
  days -= 1
  gy += 100 * (days // 36524)
  days %= 36524
  if (days >= 365):
   days += 1
 gy += 4 * (days // 1461)
 days %= 1461
 if (days > 365):
  gy += ((days - 1) // 365)
  days = (days - 1) % 365
 gd = days + 1
 if ((gy % 4 == 0 and gy % 100 != 0) or (gy % 400 == 0)):
  kab = 29
 else:
  kab = 28
 sal_a = [0, 31, kab, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
 gm = 0
 while (gm < 13 and gd > sal_a[gm]):
  gd -= sal_a[gm]
  gm += 1
 return [gy, gm, gd]

def get_jalali_year_of_month(datetime):
    jalaliToday = gregorian_to_jalali(datetime.today().year , datetime.today().month , datetime.today().day )
    return (jalaliToday[0] , jalaliToday[1])
def create_activity( performance_formula , PerformanceIndexActivityManager , performance_settings , Event):
    crJalali = gregorian_to_jalali(dt.today().year , dt.today().month , dt.today().day)

    
    cycle = performance_formula.cycle
 
    for i in range(1,13):
        if(i < crJalali[1]+1):
            pass
        else:
            #if(cycle == 'monthly'):
            if(cycle == 'seasonal'):
              if i%3 != 0:
                continue
            if(cycle == 'semiAnnualy'):
              if i%6 != 0:
                continue
            if(cycle == 'annualy'):
               if i%12 != 0:
                continue
            for variable in performance_formula.variablesRelated.all():
                startJalali = jalali_to_gregorian(crJalali[0] , i +1 , performance_settings.startPeriod)
                endJalali = jalali_to_gregorian(crJalali[0] , i +1 , performance_settings.endPeriod)
                startDate = dt(year = startJalali[0], month =startJalali[1] , day =startJalali[2] )
                endDate = dt(year = endJalali[0], month =endJalali[1] , day =endJalali[2] )
                if(PerformanceIndexActivityManager.objects.all().filter(variableRelated = variable).filter(startTime = startDate)):
                  continue
                PerformanceIndexActivityManager.objects.create( reciver =variable.responsible.profile ,variableRelated = variable  , startTime = startDate , deadLine = endDate)
                Event.objects.create(user = variable.responsible.profile ,title =  variable.title,description = variable.description ,start = startDate ,end = endDate ,color = 'red' )
            # if(cycle == 'seasonal'):
            #    if i%3 == 0:
            #       for variable in performance_formula.variablesRelated.all():
            #            startJalali = jalali_to_gregorian(crJalali[0] , i +1 , performance_settings.startPeriod)
            #            endJalali = jalali_to_gregorian(crJalali[0] , i +1 , performance_settings.endPeriod)
            #            startDate = dt(year = startJalali[0], month =startJalali[1] , day =startJalali[2] )
            #            endDate = dt(year = endJalali[0], month =endJalali[1] , day =endJalali[2] )
            #            PerformanceIndexActivityManager.objects.create( reciver =variable.responsible.profile ,variableRelated = variable  , startTime = startDate , deadLine = endDate)
            # if(cycle == 'semiAnnualy'):
            #    if i%6 == 0:
            #       for variable in performance_formula.variablesRelated.all():
            #            startJalali = jalali_to_gregorian(crJalali[0] , i +1 , performance_settings.startPeriod)
            #            endJalali = jalali_to_gregorian(crJalali[0] , i +1 , performance_settings.endPeriod)
            #            startDate = dt(year = startJalali[0], month =startJalali[1] , day =startJalali[2] )
            #            endDate = dt(year = endJalali[0], month =endJalali[1] , day =endJalali[2] )
            #            PerformanceIndexActivityManager.objects.create( reciver =variable.responsible.profile ,variableRelated = variable  , startTime = startDate , deadLine = endDate)
            # if(cycle == 'annualy'):
            #    if i%12 == 0:
            #       for variable in performance_formula.variablesRelated.all():
            #            startJalali = jalali_to_gregorian(crJalali[0] , i +1 , performance_settings.startPeriod)
            #            endJalali = jalali_to_gregorian(crJalali[0] , i +1 , performance_settings.endPeriod)
            #            startDate = dt(year = startJalali[0], month =startJalali[1] , day =startJalali[2] )
            #            endDate = dt(year = endJalali[0], month =endJalali[1] , day =endJalali[2] )
            #            PerformanceIndexActivityManager.objects.create( reciver =variable.responsible.profile ,variableRelated = variable  , startTime = startDate , deadLine = endDate)

def get_activity_done( performance_formula , PerformanceIndexActivityManager , variable):
    crJalali = gregorian_to_jalali(dt.today().year , dt.today().month , dt.today().day)
    dayName = {1 : 'فروردین', 2 :'اردیبهشت' ,3 :'خرداد' , 4 :'تیر' ,5 :'مرداد' , 6 :'شهریور' ,7 :'مهر' , 8 :'آبان' ,9 :'آذر' , 10 : 'دی',11 :'بهمن' , 12 :'اسفند' ,}
    
    cycle = performance_formula.cycle
    dataDict ={}
    for i in range(1,13):
        print(crJalali[1])
        if(i > crJalali[1]):
            print(i, 'step=2')
            break
        else:
            
            if(cycle == 'seasonal'):
              if i%3 != 0:
                continue
            if(cycle == 'semiAnnualy'):
              if i%6 != 0:
                continue
            if(cycle == 'annualy'):
               if i%12 != 0:
                continue
            crGregorian = jalali_to_gregorian(crJalali[0] , i , 1)
            
            dataDict[dayName[i] + variable.code] = PerformanceIndexActivityManager.objects.all().filter(startTime__month = crGregorian[1]).filter(variableRelated = variable)
    return dataDict
            # if(cycle == 'seasonal'):
            #    if i%3 == 0:
            #       for variable in performance_formula.variablesRelated.all():
            #            startJalali = jalali_to_gregorian(crJalali[0] , i +1 , performance_settings.startPeriod)
            #            endJalali = jalali_to_gregorian(crJalali[0] , i +1 , performance_settings.endPeriod)
            #            startDate = dt(year = startJalali[0], month =startJalali[1] , day =startJalali[2] )
            #            endDate = dt(year = endJalali[0], month =endJalali[1] , day =endJalali[2] )
            #            PerformanceIndexActivityManager.objects.create( reciver =variable.responsible.profile ,variableRelated = variable  , startTime = startDate , deadLine = endDate)
            # if(cycle == 'semiAnnualy'):
            #    if i%6 == 0:
            #       for variable in performance_formula.variablesRelated.all():
            #            startJalali = jalali_to_gregorian(crJalali[0] , i +1 , performance_settings.startPeriod)
            #            endJalali = jalali_to_gregorian(crJalali[0] , i +1 , performance_settings.endPeriod)
            #            startDate = dt(year = startJalali[0], month =startJalali[1] , day =startJalali[2] )
            #            endDate = dt(year = endJalali[0], month =endJalali[1] , day =endJalali[2] )
            #            PerformanceIndexActivityManager.objects.create( reciver =variable.responsible.profile ,variableRelated = variable  , startTime = startDate , deadLine = endDate)
            # if(cycle == 'annualy'):
            #    if i%12 == 0:
            #       for variable in performance_formula.variablesRelated.all():
            #            startJalali = jalali_to_gregorian(crJalali[0] , i +1 , performance_settings.startPeriod)
            #            endJalali = jalali_to_gregorian(crJalali[0] , i +1 , performance_settings.endPeriod)
            #            startDate = dt(year = startJalali[0], month =startJalali[1] , day =startJalali[2] )
            #            endDate = dt(year = endJalali[0], month =endJalali[1] , day =endJalali[2] )
            #            PerformanceIndexActivityManager.objects.create( reciver =variable.responsible.profile ,variableRelated = variable  , startTime = startDate , deadLine = endDate)


colorPalette = ["#55efc4", "#81ecec", "#a29bfe", "#ffeaa7", "#fab1a0", "#ff7675", "#fd79a8"]
colorPrimary, colorSuccess, colorDanger = "#79aec8", colorPalette[0], colorPalette[5]

def generate_color_palette(amount):
    palette = []

    i = 0
    while i < len(colorPalette) and len(palette) < amount:
        palette.append(colorPalette[i])
        i += 1
        if i == len(colorPalette) and len(palette) < amount:
            i = 0

    return palette
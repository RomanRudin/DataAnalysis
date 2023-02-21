#Импортирование библиотек
import pandas as pd
import matplotlib.pyplot as pl

#   Функция очистки и превращения значений строковых в значения целочисленные
def toint(a):
    if isinstance(a, str):
        b = a.find(',')
        if b == -1:
            b = a.find('.')
        return int(a[:b])
    if isinstance(a, float):
        return(int(a))
    return 1

#   Функция удаления лишних пробелов
def spacing(string):
    if isinstance(string, str):
        return string.lstrip(' ').rstrip(' ')
    return string

#   Функция "обрезки" колонок
def status_deleting(status):
    return status[6:]
 


#!  Начало подготовки
df = pd.read_csv('Space_Corrected.csv')

#   Удаление двух ненужных столбцов
df = df.drop(['Unnamed: 0', 'Unnamed: 0.1'], axis='columns')

#   Переименовывание столбцов
df.rename(columns = {' Rocket' : 'Rocket'}, inplace = True)
df.rename(columns = {'Status Rocket' : 'Rocket status'}, inplace = True)
df.rename(columns = {'Status Mission' : 'Mission status'}, inplace = True)
df.rename(columns = {'Datum' : 'Date'}, inplace = True)
df.rename(columns = {'Company Name' : 'Company name'}, inplace = True)

#   Удаление пробелов среди данных всех столбцов
df['Company name'] = df['Company name'].apply(spacing)
df['Location'] = df['Location'].apply(spacing)
df['Date'] = df['Date'].apply(spacing)
df['Detail'] = df['Detail'].apply(spacing)
df['Rocket Status'] = df['Rocket status'].apply(spacing)
df['Rocket'] = df['Rocket'].apply(spacing)
df['Mission Status'] = df['Mission status'].apply(spacing)

#   Редактирование столбцов типа "Статус"
df['Rocket status'] = df['Rocket status'].apply(status_deleting)

#   Очистка данных в столбце "Рокеты"
df['Rocket'].fillna(1, inplace = True)
df['Rocket'] = df['Rocket'].apply(toint)



#! Первый этап
#   Функция-определитель типа компании
def company_type(company):
    a1 = (company.find('US Navy') == -1) #США
    a2 = (company.find('Roscosmos') == -1) #Россия
    a3 = (company.find('USSR') == -1) #СССР
    a4 = (company.find('JAXA') == -1) #Япония
    a5 = (company.find('ExPace') == -1) #Китай
    a6 = (company.find('ISA') == -1) #Израиль
    a7 = (company.find('ISRO') == -1) #Индия
    a8 = (company.find('CASIC') == -1) #Китай
    a9 = (company.find('KCST') == -1) #Северная Корея
    a10 = (company.find('Sandia') == -1) #США
    a11 = (company.find('KARI') == -1) #Южная Корея
    a12 = (company.find('ESA') == -1) #Европейское космическое агенство
    a13 = (company.find('NASA') == -1) #США
    a14 = (company.find('ISAS') == -1) #Израиль
    a15 = (company.find('AEB') == -1) #Бразилия
    a16 = (company.find('Yuzhmash') == -1) #Россия
    a17 = (company.find('ASI') == -1) #Италия
    a18 = (company.find('CNES') == -1) #Франция
    a19 = (company.find('US Air Force') == -1) #США
    a20 = (company.find('OKB-586') == -1) #Россия
    a21 = (company.find("Arm??e de l'Air") == -1) #Франция
    if a1 and a2 and a3 and a4 and a5 and a6 and a7  and a8 and a9 and a10 and a11 and a12 and a13 and a14 and a15 and a16 and a17 and a18 and a19 and a20:
        return 'Private'
    else:
        return 'State'

#   Создание столбца "Тип компании" основного DataFrame и его заполнение
df.insert(1, 'Company type', '')
df['Company type'] = df['Company name'].apply(company_type)
Rockets = (df.groupby(by = 'Company type')['Rocket'].agg('sum'))
Rockets_Success = (df[df['Mission status'] == 'Success'].groupby(by = 'Company type')['Rocket'].agg('sum'))

#   Сощдвние итогового DataFrame и его заполнение
result1_list = {'Type': ['Private', 'State']}
Result1 = pd.DataFrame(result1_list)
Result1.insert(1, 'Persentage', '')
for i in range(len(result1_list)+1):
    Result1['Persentage'][i] = Rockets_Success[i] / Rockets[i] * 100

#   Показ первого графика
Result1.plot.bar(x='Type', y='Persentage', grid=True)
pl.show()



#! Второй этап
#   Вспомогательный список
most_countries_list = ['Russia', 'Kazakhstan', 'USA', 'Japan', 'China', 'France', 'India', 'Pacific Ocean']

#   Функция очистки
def countries(location):
    a = location.rfind(',')
    if most_countries_list.count(location[a+2:]) != 0:
        return location[a+2:]
    return 'Others'

#   Создание итоговой колонки основного DataFrame
df.insert(4, 'Location country', '')
df['Location country'] = df['Location'].apply(countries)

#   Показ второго графика
df['Location country'].value_counts().plot(kind='pie')
pl.show()


#! Третий этап
#   Вспомогательный словарь
months_dict = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}

#   Функции очистки и сортировки столбцов из основного DataFrame
def baikonur(location):
    if location.find('Baikonur') != -1:
        return 1
def month(date):
    return date[4:7]

#   Создание вспомогательного и итогового DataFrame
data3 = pd.DataFrame({'Mission status': [], 'Month': []})
Result3 = pd.DataFrame({'Months': [], 'Month order': []})

#   Заполнение вспомогательного DataFrame
data3['Month'] = df[df['Location'].apply(baikonur) == 1]['Date'].apply(month)
data3['Mission status'] = df[df['Location'].apply(baikonur) == 1]['Mission status']

#   Заполнение итогового Data Frame
Result3['Months'] = data3['Month'].value_counts()

#   Заполнение и сортировка по столбцу "Месяцы"
for i in range(12):
    a = Result3.index[i]
    Result3['Month order'][a] = str(Result3.index[i])
Result3 = Result3.replace({'Month order': months_dict})
Result3 = Result3.sort_values(by='Month order')
Result3['Rcokets per month'] = data3['Month'].value_counts()

#   Показ третьего графика
Result3.plot(x='Month order', y='Rcokets per month', kind='scatter')
pl.show()
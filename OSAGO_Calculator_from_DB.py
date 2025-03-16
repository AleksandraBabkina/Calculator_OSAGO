#TAR - Vehicle Type - SELECT * FROM al_babkina_TAR
#KBM - Driver’s Accident Record - SELECT * FROM al_babkina_KBM
#KVS - Driver’s Age and Driving Experience - SELECT * FROM al_babkina_KVS
#KM - Engine Power - SELECT * FROM al_babkina_KM
#KO - Number of Drivers - SELECT * FROM al_babkina_KO
#KP - Insurance Term - SELECT * FROM al_babkina_KP
#KS - Period of Vehicle Use During the Insurance Term - SELECT * FROM al_babkina_KS
#KT - Registration Address - SELECT * FROM al_babkina_KT

from sqlalchemy import create_engine, Column, String, Float, select, or_, and_
from sqlalchemy.orm import sessionmaker, declarative_base
from functools import reduce
from operator import mul
import re
import pandas as pd
from IPython.display import display, clear_output 
import time

#Header with connection DO NOT TOUCH”
username = 'username'
password = 'password'
dsn = 'dsn'

conection_string = f'oracle+oracledb://{username}:{password}@{dsn}' # Open sql

# Creating the connection engine
engine = create_engine(conection_string)
Base = declarative_base()

# Defining the table model
class AlBabkinaTar(Base):
    __tablename__ = 'al_babkina_tar'
    TYPE_TS_TAR = Column(String, primary_key=True)
    COEFF_TS_TAR_MIN = Column(Float)
    COEFF_TS_TAR_MAX = Column(Float)

class AlBabkinaKbm(Base):
    __tablename__ = 'al_babkina_kbm'
    CLASS_KBM = Column(String, primary_key=True)
    COEFF_KBM = Column(Float)

class AlBabkinaKm(Base):
    __tablename__ = 'al_babkina_km'
    TYPE_KM_TS = Column(String, primary_key=True)
    COEFF_KM = Column(Float)

class AlBabkinaKo(Base):
    __tablename__ = 'al_babkina_ko'
    TYPE_KO = Column(String, primary_key=True)
    COEFF_KO = Column(Float)

class AlBabkinaKp(Base):
    __tablename__ = 'al_babkina_kp'
    DAY_STRAH_KP = Column(String, primary_key=True)
    COEFF_KP = Column(Float)

class AlBabkinaKs(Base):
    __tablename__ = 'al_babkina_ks'
    DAY_STRAH_KS = Column(String, primary_key=True)
    COEFF_KS = Column(Float)

class AlBabkinaKvs(Base):
    __tablename__ = 'al_babkina_kvs'
    AGE_KVS = Column(String, primary_key=True)
    STAG_KVS_0 = Column(Float)
    STAG_KVS_1 = Column(Float)
    STAG_KVS_2 = Column(Float)
    STAG_KVS_3_4 = Column(Float)
    STAG_KVS_5_6 = Column(Float)
    STAG_KVS_7_9 = Column(Float)
    STAG_KVS_10_14 = Column(Float)
    STAG_KVS_MORE_14 = Column(Float)

class AlBabkinaKt(Base):
    __tablename__ = 'AL_BABKINA_KТ'
    TER_KT = Column(String, primary_key=True)
    TYPE_TS_KT = Column(String, primary_key=True)
    COEFF_KT = Column(Float)

# Creating the session
Session = sessionmaker(bind=engine)
session = Session()

print("Калькулятор ОСАГО\n")

coefficients = []

time.sleep(1)

##################################################################### TARIF ######################################################################
type_ts_tar_values = session.execute(select(AlBabkinaTar.TYPE_TS_TAR).distinct()).all()

replace_dict = {
    "А": "A",
    "М": "M",
    "В": "B",
    "Б": "B",
    "ВЕ": "BE",
    "БЕ": "BE",
    "С": "C",
    "СЕ": "CE",
    "Д": "D",
    "ДЕ": "DE",
    "ТМ": "Tm",
    "ТБ": "Tb",
    "TM": "Tm",
    "TB": "Tb"
}

while True:
    try:
        clear_output()
        user_tar = str(input("Введите категорию транспортного средства (A, M, B, BE, C, CE, D, DE, Tm, Tb, Другое):\n"))
        user_tar = user_tar.upper()
        user_tar = ''.join(replace_dict.get(char, char) for char in user_tar)
        user_tar = ''.join(char for char in user_tar if char.isalnum())
        if 1 <= len(user_tar) <= 6 and user_tar in ["A", "M", "B", "BE", "C", "CE", "D", "DE", "Tm", "Tb", "DРУГОЕ"]:
            break
        else:
            print("\nДопустимые значения: A, M, B, BE, C, CE, D, DE, Tm, Tb, Другое")
            time.sleep(1)
            continue
    except (ValueError,IndexError):    
        print("Неверно введенное значение")
        time.sleep(1)
        clear_output()
        
while True:
    try:
        if user_tar in ["B", "BE"]:
            while True:
                try:
                    clear_output()
                    taxi_or_not = int(input("\nЕсли ваша цель использования ТС ТАКСИ - ВВЕДИТЕ 1, если НЕТ - 0: "))
                    if taxi_or_not == 1:
                        mass = "Такси"
                        clear_output()
                        break
                    elif taxi_or_not == 0:
                        while True:
                            try:
                                user_tar_type = ["Физ. лица", "Юр. лица"] 
                                print("Выберите вашу категорию лиц:") 
                                for idx, option in enumerate(user_tar_type, 1):
                                    print(f"{idx}. {option}")
                                tar_type_choice = int(input("Введите номер вашего выбора: ")) 
                                mass = user_tar_type[tar_type_choice - 1]
                                print()
                                time.sleep(1)
                                break
                            except (ValueError,IndexError):
                                print("\nОшибка. Введите только число 1 или 2\n")
                                time.sleep(1)
                                clear_output()
                        clear_output()
                        break
                    else:
                        print("Введите цифру 1 или 2")
                        time.sleep(1)
                        continue
                except (ValueError,IndexError):
                    print("\nОшибка. Введите только число 1 или 2\n")
                    time.sleep(1)
                    clear_output()
        elif user_tar in ["C", "CE"]:
            while True:
                try:
                    mass = input("\nВведите массу транспортного средства в тоннах:  ")
                    if int(mass)>=0:
                        mass = mass.replace(" ", "").replace(",", ".")
                        mass = int(round(float(mass)))
                        break
                    else:
                        print("Масса быть только положительным числом.")
                        time.sleep(1)
                        clear_output()
                except (ValueError,IndexError):
                    print("Введите только число")
                    time.sleep(1)
                    clear_output()
        elif user_tar in ["D", "DE"]:
            while True:
                try:
                    reg_per = int(input("\nЕсли транспорт используется на регулярных перевозках с посадкой и высадкой пассажиров - ВВЕДИТЕ 1, если НЕТ - 0: "))
                    if reg_per == 1:
                        clear_output()
                        break
                    elif reg_per == 0:
                        for_d()
                        break
                    else:
                        print("Введите цифру 1 или 2")
                        time.sleep(1)
                        continue
                except (ValueError,IndexError):
                    print("Введите цифру 1 или 2")
                    time.sleep(1)
                    clear_output()
        else:
            break
        break
    except (ValueError,IndexError):    
        print("Неверно введенное значение")
        time.sleep(1)
        clear_output()

def for_d():
    while True:
        try:
            mass = input("\nВведите число пассажирских мест:  ")
            if int(mass)>=0:
                mass = mass.replace(" ", "").replace(",", ".")
                mass = int(round(float(mass)))
                break
            else:
                print("Число пассажирских мест может быть только положительным числом.")
                time.sleep(1)
                clear_output()
        except (ValueError,IndexError):
            print("Введите только число")
            time.sleep(1)
            clear_output()

time.sleep(1)
clear_output()

if user_tar in ["B", "BE"] and mass == "Физ. лица":
    user_input_tar_cleaned = "«B», «BE» Физ. лица"
elif user_tar in ["B", "BE"] and mass == "Юр. лица":
    user_input_tar_cleaned = "«B», «BE»: Юр. лица"
elif user_tar in ["B", "BE"] and mass == "Такси":
    user_input_tar_cleaned = "«В», «ВЕ»: Такси"
elif user_tar in ["C", "CE"] and mass > 16:
    user_input_tar_cleaned = "«C» и «CE» с массой более 16 тонн"
elif user_tar in ["C", "CE"] and mass <= 16:
    user_input_tar_cleaned = "«C» и «CE» с массой 16 тонн и менее"
elif user_tar in ["D", "DE"] and reg_per == 1:
    user_input_tar_cleaned = "«D» и «DE», используемые на регулярных перевозках с посадкой и высадкой пассажиров"
elif user_tar in ["D", "DE"] and mass <= 16:
    user_input_tar_cleaned = "«D» и «DE» с числом пассажирских мест до 16 включительно"
elif user_tar in ["D", "DE"] and mass > 16:
    user_input_tar_cleaned = "«D» и «DE» с числом пассажирских мест более 16"
elif user_tar in ["A", "M"]:
    user_input_tar_cleaned = "«A», «M»: мотоциклы, мопеды и легкие квадрициклы"
elif user_tar == "Tm":
    user_input_tar_cleaned = "«Tm»: трамваи"
elif user_tar == "Tb":
    user_input_tar_cleaned = "«Tb»: троллейбусы"
elif user_tar == "DРУГОЕ":
    user_input_tar_cleaned = "Тракторы, самоходные дорожно-строительные и иные машины, кроме не имеющих колесных движителей"

matching_values_tar = session.execute(select(AlBabkinaTar).filter(AlBabkinaTar.TYPE_TS_TAR.like(f"%{user_input_tar_cleaned}%"))).scalars().all()

while True:
    try:
        for match in matching_values_tar:
            user_input_tar = str(input(f"\n Введите ваш тариф в пределах от {match.COEFF_TS_TAR_MIN} и до {match.COEFF_TS_TAR_MAX}\n"))
        user_input_tar = user_input_tar.replace(" ", "").replace(",", ".")
        user_input_tar = int(round(float(user_input_tar)))
        if match.COEFF_TS_TAR_MIN <= user_input_tar <= match.COEFF_TS_TAR_MAX:
            coefficients.append(user_input_tar)
            break
        else:
            print("Ваш коэффициент не находится в указанном диапозоне")
            time.sleep(1)
            clear_output()
    except (ValueError,IndexError):
        print("Неверно введенное значение")
        time.sleep(1)
        clear_output()

time.sleep(1)
clear_output()

##################################################################### KO ######################################################################\
if user_tar in ["B", "BE"] and mass in ["Физ. лица", "Юр. лица"]:
    type_ko1 = mass
else:
    while True:
        try:
            clear_output()
            ko_kat_options = ["Физ. лица", "Юр. лица"] 
            print("Выберите вашу категорию лиц:") 
            for idx, option in enumerate(ko_kat_options, 1):
                print(f"{idx}. {option}")
            ko_kat_choice = int(input("Введите номер вашего выбора: ")) 
            type_ko1 = ko_kat_options[ko_kat_choice - 1]
            time.sleep(1)
            break
        except (ValueError,IndexError):
            print("\nОшибка. Введите только число 1 или 2\n")
            time.sleep(1.3)
clear_output()

while True:
    try:
        clear_output()
        ko_ogr_options = ["Ограниченное", "Не ограниченное"] 
        print("Количество водителей ограничено?") 
        for idx, option in enumerate(ko_ogr_options, 1):
            print(f"{idx}. {option}")
        ko_ogr_choice = int(input("Введите номер вашего выбора: ")) 
        type_ko2 = ko_ogr_options[ko_ogr_choice - 1]
        time.sleep(1)
        break
    except (ValueError,IndexError):
        print("\nОшибка. Введите только число 1 или 2\n")
        time.sleep(1.3)
clear_output()

type_ko_values = session.execute(select(AlBabkinaKo.TYPE_KO).distinct()).all()

if type_ko1 == "Физ. лица" and type_ko2 == "Ограниченное":
    user_input_ko = "Физ. лица: Ограниченное"
elif type_ko1 == "Юр. лица" and type_ko2 == "Ограниченное":
    user_input_ko = "Юр. лица: Ограниченное"
elif type_ko1 == "Физ. лица" and type_ko2 == "Не ограниченное":
    user_input_ko = "Физ. лица: Не ограниченное"
elif type_ko1 == "Юр. лица" and type_ko2 == "Не ограниченное":
    user_input_ko = "Юр. лица: Не ограниченное"

# Find suitable options in the column
matching_values_ko = session.execute(select(AlBabkinaKo).filter(AlBabkinaKo.TYPE_KO.like(f"%{user_input_ko}%"))).scalars().all()

selected_value_ko = matching_values_ko[0].COEFF_KO
coefficients.append(selected_value_ko)

time.sleep(1)
clear_output()

####################################################################### KVS #######################################################################
def kvs():
    type_kvs_values = session.execute(select(AlBabkinaKvs.AGE_KVS).distinct()).all()
    while True:
        try:
            user_experience = input("\nВведите стаж (в годах):  ")
            if int(user_experience)>=0:
                user_experience = user_experience.replace(" ", "").replace(",", ".")
                user_experience = int(round(float(user_experience)))
                break
            else:
                print("Стаж может быть только положительным числом.")
                time.sleep(1)
                clear_output()
        except (ValueError,IndexError):
            print("Введите только число")
            time.sleep(1)
            clear_output()
            
    while True:
        try:
            user_input_kvs = input("\nВведите ваш возраст:  ")
            if int(user_input_kvs)>=16 and int(user_input_kvs)-int(user_experience) >=16:
                user_input_kvs = user_input_kvs.replace(" ", "").replace(",", ".")
                user_input_kvs = int(round(float(user_input_kvs)))
                break
            else:
                print("\nВозраст может быть только больше или равно 16.\nСтаж не может быть больше допустимого возраста вождения.")
                time.sleep(2.5)
                clear_output()
        except (ValueError,IndexError):
            print("Введите только число")
            time.sleep(1)
            clear_output()
            
    matching_value_kvs = None
    matching_desc = None

    # Define the corresponding column STAG_KVS based on the experience
    if user_experience <= 1:
        column_name = 'STAG_KVS_0'
    elif user_experience <= 2:
        column_name = 'STAG_KVS_1'
    elif user_experience <= 4:
        column_name = 'STAG_KVS_3_4'
    elif user_experience <= 6:
        column_name = 'STAG_KVS_5_6'
    elif user_experience <= 9:
        column_name = 'STAG_KVS_7_9'
    elif user_experience <= 14:
        column_name = 'STAG_KVS_10_14'
    else:
        column_name = 'STAG_KVS_MORE_14'

    age_ranges = {
        (16, 21): "От 16 до 21 лет",
        (22, 24): "От 22 до 24 лет", 
        (25, 29): "От 25 до 29 лет", 
        (30, 34): "От 30 до 34 лет", 
        (35, 39): "От 35 до 39 лет", 
        (40, 49): "От 40 до 49 лет", 
        (50, 59): "От 50 до 59 лет", 
        (60, float('inf')): "От 60 лет и старше"
    }
    
    for range_, description in age_ranges.items():
        start, end = range_
        if start <= user_input_kvs <= end:
            matching_desc = description
            break

    matching_row = session.execute(select(AlBabkinaKvs).filter(AlBabkinaKvs.AGE_KVS == matching_desc)).scalars().first()
    selected_value_kvs = getattr(matching_row, column_name, 0.0)
    if selected_value_kvs != 0.0:
        coef_kvs.append(selected_value_kvs)


####################################################################### KBM #######################################################################
def kbm():
    while True:
        try:
            user_input_kbm = str(input("\nВведите КБМ (3.92, 2.94, 2.25, 1.76, 1.17, 1, 0.91, 0.83, 0.78, 0.74, 0.68, 0.63, 0.57, 0.52, 0.46):\n"))
            if user_input_kbm == 1:
                user_input_kbm = int(user_input_kbm.replace(" ", ""))
            else:
                user_input_kbm = float(user_input_kbm.replace(" ", "").replace(",", "."))
                
            if user_input_kbm in [3.92, 2.94, 2.25, 1.76, 1.17, 1, 0.91, 0.83, 0.78, 0.74, 0.68, 0.63, 0.57, 0.52, 0.46]:
                matching_values_kbm = session.execute(select(AlBabkinaKbm).filter(AlBabkinaKbm.COEFF_KBM.like(f"%{user_input_kbm}%"))).scalars().all()
                selected_value_kbm = matching_values_kbm[0].COEFF_KBM
                coef_kbm.append(selected_value_kbm)
                break
            else:
                print("Нет такого значения КБМ. Введите один из представленных значений.")
                time.sleep(1)
                clear_output()
                continue
        except (ValueError, IndexError):
            print("Нет такого значения КБМ. Введите один из представленных значений.")
            time.sleep(1)
            clear_output()
##############################################################################################################################################

coef_kvs = []
coef_kbm = []

if type_ko2 == "Ограниченное":
    while True:
        try:
            vod = int(input("\nВведите количество водителей: \n"))
            break
        except ValueError:
            print("Введите только целое число")
            time.sleep(1)
            clear_output()
    
    for i in range(vod):
        print(f"\nВодитель {i+1}:")
        kvs()
        kbm()
        max_kvs = max(coef_kvs)
        max_kbm = max(coef_kbm)
        coefficients.append(max_kvs)
        coefficients.append(max_kbm)
        time.sleep(1)
        clear_output()

##################################################################### KM ######################################################################
type_km_ts_values = session.execute(select(AlBabkinaKm.TYPE_KM_TS).distinct()).all()

while True:
    try:
        user_input_km = input("\nВведите мощность двигателя:\n")
        user_input_km = user_input_km.replace(" ", "").replace(",", ".")
        user_input_km = int(round(float(user_input_km)))
        break
    except (ValueError,IndexError):
        print("Введите только число")
        time.sleep(1)
        clear_output()

ranges_and_descriptions = {
    (50, 70): "от 50 до 70 включительно",
    (70, 100): "от 70 до 100 включительно",
    (100, 120): "от 100 до 120 включительно",
    (120, 150): "от 120 до 150 включительно",
    (0, 50): "до 50 включительно",
    (150, float('inf')): "от 150"
}

# Search for the corresponding range and value in the TYPE_KM_TS column
matching_description = None
for range_, description in ranges_and_descriptions.items():
    start, end = range_
    if start <= user_input_km <= end:
        matching_description = description
        break

# Search for the corresponding value in the TYPE_KM_TS column and display the coefficient
matching_row = session.execute(select(AlBabkinaKm).filter(AlBabkinaKm.TYPE_KM_TS == matching_description)).scalars().first()
selected_value_km = matching_row.COEFF_KM
coefficients.append(selected_value_km)

time.sleep(1)
clear_output()


############################################################# КS ######################################################################
while True:
    try:
        user_input_ks = int(input("\nЕсли транспорт используется сезонно (снегоуборочные, газонокосильные, сельскохозяйственные, поливочные и другие спец машины) - ВВЕДИТЕ 1, если НЕТ - 0: "))
        if user_input_ks == 1:
            while True:
                try:
                    choice2 = int(input("\nСколько месяцев будет использоваться транспортное средство?"))
                    if choice2>0:
                        if 0 < choice2 <= 3:
                            user_input_ks = "от 0 до 3"
                            break
                        elif 3 < choice2 <= 4:
                            user_input_ks = "от 3 до 4"
                            break
                        elif 4 < choice2 <= 5:
                            user_input_ks = "от 4 до 5"
                            break
                        elif 5 < choice2 <= 6:
                            user_input_ks = "от 5 до 6"
                            break
                        elif 6 < choice2 <= 7:
                            user_input_ks = "от 5 до 6"
                            break
                        elif 7 < choice2 <= 8:
                            user_input_ks = "от 7 до 8"
                            break
                        elif 8 < choice2 <= 9:
                            user_input_ks = "от 8 до 9"
                            break
                        elif choice2 > 9:
                            user_input_ks = "больше 9"
                            break
                    else:
                        print("Количество застрахованных месяцев может быть только целым положительным числом")
                        time.sleep(1)
                        clear_output()
                        continue
                except (ValueError,IndexError):
                    print("Введите только целое число")
                    time.sleep(1)
                    clear_output()
            day_strah_ks_values = session.execute(select(AlBabkinaKs.DAY_STRAH_KS.distinct())).all()      
            matching_values_ks = session.execute(select(AlBabkinaKs).filter(AlBabkinaKs.DAY_STRAH_KS.like(f"%{user_input_ks}%"))).scalars().all()
            selected_value_ks = float(matching_values_ks[0].COEFF_KS)
            coefficients.append(selected_value_ks)
            time.sleep(1)
            clear_output()
            break
        elif user_input_ks == 0:
            break
        else:
            print("Введите цифру 1 или 2")
            time.sleep(1)
            continue
    except (ValueError,IndexError):    
        print("Неверно введенное значение")
        time.sleep(1)
        clear_output()


##################################################################### КP ######################################################################
while True:
    try:
        user_choice_kp = int(input("\nЕсли транспорт был зарегестрирован на территории иностранного государства и ВРЕМЕННО используется на территории РФ - ВВЕДИТЕ 1, если НЕТ - 0: "))
        if user_choice_kp == 1:
            while True:
                try:
                    choice1 = int(input("\nЕсли вы хотите застраховать машину на срок БОЛЬШЕ 1 месяца - ВВЕДИТЕ 1, если НЕТ - 0: "))
                    if choice1 == 0:
                        choice2 = int(input("\nНа сколько дней вы хотите застрохавать машину?"))
                        if 5 <= choice2 <= 15:
                            user_input_kp = "от 5 до 15 дней"
                            break
                        elif 16 <= choice2 <= 31:
                            user_input_kp = "от 16 дней до 1 мес"
                            break
                        else:
                            print("Минимальный срок страховки 5 дней. Если вы хотите застроховать машину на срок БОЛЬШЕ 1 месяца - ВВЕДИТЕ 1")
                            continue
                    elif choice1 == 1:
                        choice2 = int(input("\nНа сколько месяцев вы хотите застрохавать машину?"))
                        if 1 <= choice2 <= 2:
                            user_input_kp = "2 мес"
                            break
                        elif 2 < choice2 <= 3:
                            user_input_kp = "3 мес"
                            break
                        elif 3 < choice2 <= 4:
                            user_input_kp = "4 мес"
                            break
                        elif 4 < choice2 <= 5:
                            user_input_kp = "5 мес"
                            break
                        elif 5 < choice2 <= 8:
                            user_input_kp = "8 мес"
                            break
                        elif choice2 > 8:
                            user_input_kp = "8 мес"
                            break
                        else:
                            print("Минимальный срок страховки 1 месяц. Если вы хотите застроховать машину на срок МЕНЬШЕ 1 месяца - ВВЕДИТЕ 0")
                            continue
                    else:
                        print("Введите цифру 1 или 0")
                        time.sleep(1)
                except (ValueError,IndexError):
                    print("Введите только число")
                    time.sleep(1)
                    clear_output()
            day_strah_ks_values = session.execute(select(AlBabkinaKp.DAY_STRAH_KP.distinct())).all()
            matching_values = session.execute(select(AlBabkinaKp).filter(AlBabkinaKp.DAY_STRAH_KP.like(f"%{user_input_kp}%"))).scalars().all()
            selected_value_km = matching_values[0].COEFF_KP
            coefficients.append(selected_value_km)
            time.sleep(1)
            clear_output()
            break
        elif user_choice_kp == 0:
            break
        else:
            print("Введите цифру 1 или 2")
            time.sleep(1)
            continue
    except (ValueError,IndexError):    
        print("Неверно введенное значение")
        time.sleep(1)
        clear_output()

####################################################################### КТ #######################################################################
while True:
    try:
        clear_output()
        type_ts_options = ["ТС", "Спецтехника"] 
        print("Выберите тип транспортного средства:") 
        for idx, option in enumerate(type_ts_options, 1):
            print(f"{idx}. {option}")
        type_ts_choice = int(input("Введите номер вашего выбора: ")) 
        type_ts = type_ts_options[type_ts_choice - 1]
        time.sleep(1)
        break
    except (ValueError,IndexError):
        print("\nОшибка. Введите только число 1 или 2\n")
        time.sleep(1.3)
clear_output()

ter_kt = 0
while ter_kt == 0:
    while True:
        try:
            clear_output()
            # Prompt the user to enter keywords for searching in the TER_KT
            keywords = input("Введите территорию на которой зарегестрированно ваше транспортное средство: ").split()
            # Search for all unique values in the TER_KT column that match the keywords
            conditions = [AlBabkinaKt.TER_KT.ilike(f"%{keyword}%") for keyword in keywords] 
            ter_kt_values = session.execute(select(AlBabkinaKt.TER_KT).filter(or_(*conditions)).distinct()).all()
            if not ter_kt_values:
                print("Не найдено значений, соответствующих заданным ключевым словам.")
                time.sleep(1)
                clear_output()
                continue
            else: # Display the list of found values
                print("\nСписок найденных значений из столбца TER_KT: \n")
                for idx, value_kt in enumerate(ter_kt_values, 1):
                    print(f"{idx}. {value_kt[0]}")
                break
        except (ValueError,IndexError):
            print("\nНе найдено значений, соответствующих заданным ключевым словам. \n")
            time.sleep(1.3)
            clear_output()

    while True:
        print("\nЕСЛИ НЕТ НУЖНОГО ВАРИАНТА - ВВЕДИТЕ 0\n")
        try:
            # Ask the user to select a value from the list
            ter_kt_choice = int(input("Введите номер вашего выбора: "))
            if ter_kt_choice == 0:
                ter_kt = 0
                break
            else:
                ter_kt = ter_kt_values[ter_kt_choice - 1][0]
                break
        except (ValueError,IndexError):
            print("Введите только число")
            time.sleep(1)
            clear_output()

# Search for the coefficient based on the selected values and display the result
matching_row = session.execute(select(AlBabkinaKt).filter(and_(AlBabkinaKt.TYPE_TS_KT == type_ts, AlBabkinaKt.TER_KT == ter_kt))).scalars().first()
selected_value_kt = matching_row.COEFF_KT
coefficients.append(selected_value_kt)

time.sleep(1)
clear_output()
# Close the session
session.close()

#################################################################### OSAGO price #######################################################################
result = round(reduce(mul, coefficients))
print("\nСТОИМОСТЬ ПОЛИСА ОСАГО", result) 

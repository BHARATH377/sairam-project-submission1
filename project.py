import pyrebase
import warnings
import sklearn


from numpy import double

warnings.filterwarnings('ignore')
import pandas as pd
import serial
import time
import schedule
import pandas as pd
def main_func():
    firebase = pyrebase.initialize_app(firebaseconfig)
    db = firebase.database()
    loc = db.child("User").get()
    for location in loc.each():
        current_loc = location.val()
        print(location.val())
    city_name = (current_loc['location'])
    arduino = serial.Serial('com3', 4800)
    print('Established serial connection to esp2866')
    arduino_data = arduino.readline()
    f_ard = float(arduino_data)
    # D_rate=int(input("Enter infrastructure rating"))

    if(f_ard < 0):
        f_ard=0.00

    decoded_values = str(arduino_data[0:len(arduino_data)].decode('ISO-8859-1'))
    d = decoded_values
    #if (d[0] == '-'):
    #    d = '0.00'
    print(f_ard)
    dam_df=pd.read_csv("C:/Users/barat/Documents/reservoirs_live.csv")
    lvl=dam_df.iloc[1,3]
    strg=dam_df.iloc[1,5]

    # python_test.py
    import requests

    api_key = "AAAAPPPPIIII___KKKKEEEEYYYY"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    #city_name = #input("Enter city name : ")
    complete_url = base_url + "appid=" + 'd850f7f52bf19300a9eb4b0aa6b80f0d' + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()

    if x["cod"] != "404":
        y = x["main"]

        #current_temperature = y["temp"]
        c_temp=y["temp"]
        c_temp = c_temp-273.15
        current_temperature = "{:.2f}".format(c_temp)

        z = x["weather"]
        a = y["humidity"]

        weather_description = z[0]["description"]
        hum=a

        print(" Temperature (in kelvin unit) = " +
              str(current_temperature) +
              "\n description = " +
              str(weather_description)+"\n Humidity : "+str(hum))

    else:
        print(" City Not Found ")
    weather = str(weather_description)
    lr = "light rain"
    hi = "heavy intensity rain"
    h = "heavy rain"
    mr= "moderate rain"
    oc="overcast clouds"
    hz="haze"
    sc="scattered clouds"
    fc="few clouds"
    bc="broken clouds"

    found = weather.find(lr)
    found1 = weather.find(h)
    found2 = weather.find(hi)
    found3 = weather.find(mr)
    dff = pd.read_csv("C:/Users/barat/Documents/test2.csv")
    data = {'DRAIN_LEVEL(INCH)': [f_ard],'infrastructure':[D_rate],'DAM_LEVEL(FT)':[lvl],'STORAGE(P)':[strg],'Temperature':[current_temperature],'Humidity':[hum]}
    df6 = pd.DataFrame(data)
    dff = dff.append(df6)
    print(dff)
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import MinMaxScaler  # normalization  (0...1)
    minmax = MinMaxScaler()
    from sklearn.neighbors import KNeighborsClassifier
    if (found != -1):
        # light rainfall
        # data = {'Cumulative rainfall (inch)': [0.5, 0.6, 0.4, 0.3, 0.2], 'Drain_Level (m)': []}
        df1=pd.read_csv('C:/Users/barat/Downloads/l.csv')
        x = df1.loc[:, ['DRAIN_LEVEL(INCH)','infrastructure','DAM LEVEL(FT)','STORAGE(P)','Temperature','Humidity']]
        y = df1.iloc[:, 8:9]
        #from sklearn.model_selection import train_test_split
        x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.9, test_size=0.1, random_state=0)
        x_train_std = minmax.fit_transform(x_train)
        x_test_std = minmax.transform(x_test)
        #from sklearn.neighbors import KNeighborsClassifier
        model1 = KNeighborsClassifier()
        Kfit = model1.fit(x_train_std, y_train)
        #now giving our dynamically generated dataset

        x_test_std_i = minmax.transform(dff)
        y_predt=Kfit.predict(x_test_std_i)
        out1=""
        for j in y_predt:
            if(j.isalpha()or ' '):
                out1=out1+j
        print(out1)
        out1=out1.upper()
        #print(y_predt)
        #arduino_data2=str(arduino_data1)
        weather1=str(weather)
        weather1=weather1.upper()
        #prediction=str(y_predt)
        city_name1=str(city_name)
        #print(arduino_data2)
        print("current_temperature"+current_temperature)
        #print(d)
        data={
            "FLOOD PREDICTION":out1
        }
        data1={
            "PLACE ": city_name
        }
        data2 = {
            "DRAIN LEVEL":f_ard
        }
        data3 = {
            "WEATHER DESCRIPTION": weather1
        }
        data4 = {
            "CURRENT TEMPERATURE": current_temperature
        }
        data5 = {
            "Humidity(%)": hum
        }
        #db.push(data)
        db.child("Data").set(data)
        db.child("location").set(data1)
        db.child("drain_level").set(data2)
        db.child("weather").set(data3)
        db.child("current_temperature").set(data4)
        db.child("Humidity(%)").set(data5)



    elif (found1 != -1):
        df2=pd.read_csv('C:/Users/barat/Downloads/h.csv') #heavy rain
        x = df2.loc[:, ['DRAIN_LEVEL(INCH)','infrastructure','DAM LEVEL(FT)','STORAGE(P)','Temperature','Humidity']]
        y = df2.iloc[:, 8:9]
        x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.9, test_size=0.1, random_state=0)
        x_train_std = minmax.fit_transform(x_train)
        x_test_std = minmax.transform(x_test)
        model1 = KNeighborsClassifier()
        Kfit = model1.fit(x_train_std, y_train)
        x_test_std_i = minmax.transform(dff)
        y_predt = Kfit.predict(x_test_std_i)
        out1 = ""
        for j in y_predt:
            if (j.isalpha() or ' '):
                out1 = out1 + j
        print(out1)
        out1 = out1.upper()
        #print(y_predt)
        #arduino_data2 = str(arduino_data1)
        weather1 = str(weather)
        weather1 = weather1.upper()
        #prediction = str(y_predt)
        city_name1 = str(city_name)
        print("current_temperature" + current_temperature)
        data = {
            "FLOOD PREDICTION": out1
        }
        data1 = {
            "PLACE ": city_name
        }
        data2 = {
            "DRAIN LEVEL": f_ard
        }
        data3 = {
            "WEATHER DESCRIPTION": weather1
        }
        data4 = {
            "CURRENT TEMPERATURE": current_temperature
        }
        data5 = {
            "Humidity(%)": hum
        }
        #db.push(data)
        db.child("Data").set(data)
        db.child("location").set(data1)
        db.child("drain_level").set(data2)
        db.child("weather").set(data3)
        db.child("current_temperature").set(data4)
        db.child("Humidity(%)").set(data5)

    elif(found3 !=-1):
        df4 = pd.read_csv('C:/Users/barat/Downloads/moderate rain222.csv')# moderate rain
        x = df4.loc[:, ['DRAIN_LEVEL(INCH)','infrastructure','DAM LEVEL(FT)','STORAGE(P)','Temperature','Humidity']]
        y = df4.iloc[:, 8:9]
        x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.9, test_size=0.1, random_state=0)
        x_train_std = minmax.fit_transform(x_train)
        x_test_std = minmax.transform(x_test)
        model1 = KNeighborsClassifier()
        Kfit = model1.fit(x_train_std, y_train)
        x_test_std_i = minmax.transform(dff)
        y_predt = Kfit.predict(x_test_std_i)
        out1 = ""
        for j in y_predt:
            if (j.isalpha() or ' '):
                out1 = out1 + j
        print(out1)
        out1 = out1.upper()
        #print(y_predt)
        #arduino_data2 = str(arduino_data1)
        weather1 = str(weather)
        weather1 = weather1.upper()
        #prediction = str(y_predt)
        print("current_temperature" + current_temperature)
        print("city_name"+city_name)
        city_name1 = str(city_name)
        data = {
            "FLOOD PREDICTION": out1
        }
        data1 = {
            "PLACE ": city_name
        }
        data2 = {
            "DRAIN LEVEL": f_ard
        }
        data3 = {
            "WEATHER DESCRIPTION": weather1
        }
        data4 = {
            "CURRENT TEMPERATURE": current_temperature
        }
        data5 = {
            "Humidity(%)": hum
        }
        #db.push(data)
        db.child("Data").set(data)
        db.child("location").set(data1)
        db.child("drain_level").set(data2)
        db.child("weather").set(data3)
        db.child("current_temperature").set(data4)
        db.child("Humidity(%)").set(data5)

    else:
        if (found2 != -1):   # heavy intensity
            df3=pd.read_csv('C:/Users/barat/Downloads/vh.csv')
            x = df3.loc[:, ['DRAIN_LEVEL(INCH)','infrastructure','DAM LEVEL(FT)','STORAGE(P)','Temperature','Humidity']]
            y = df3.iloc[:, 8:9]
            x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.9, test_size=0.1, random_state=0)
            x_train_std = minmax.fit_transform(x_train)
            x_test_std = minmax.transform(x_test)
            model1 = KNeighborsClassifier()
            Kfit = model1.fit(x_train_std, y_train)
            x_test_std_i = minmax.transform(dff)
            y_predt = Kfit.predict(x_test_std_i)
            out1 = ""
            for j in y_predt:
                if (j.isalpha() or ' '):
                    out1 = out1 + j
            print(out1)
            out1 = out1.upper()
            #print(y_predt)
            #arduino_data2 = str(arduino_data1)
            weather1 = str(weather)
            weather1 = weather1.upper()
            #prediction = str(y_predt)
            print("current_temperature" + current_temperature)
            city_name1 = str(city_name)
            data = {
                "FLOOD PREDICTION": out1
            }
            data1 = {
                "PLACE ": city_name
            }
            data2 = {
                "DRAIN LEVEL": f_ard
            }
            data3 = {
                "WEATHER DESCRIPTION": weather1
            }
            data4 = {
                "CURRENT TEMPERATURE": current_temperature
            }
            data5 = {
                "Humidity(%)": hum
            }
            #db.push(data)
            db.child("Data").set(data)
            db.child("location").set(data1)
            db.child("drain_level").set(data2)
            db.child("weather").set(data3)
            db.child("current_temperature").set(data4)
            db.child("Humidity(%)").set(data5)

            # blocked
        elif(oc!=-1 or hz!=-1 or sc!=-1 or fc!=-1 or bc!=-1):
            df5=pd.read_csv('C:/Users/barat/Downloads/no.csv')
            x = df5.loc[:, ['DRAIN_LEVEL(INCH)','infrastructure','DAM LEVEL(FT)','STORAGE(P)','Temperature','Humidity']]
            y = df5.iloc[:, 8:9]
            x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.9, test_size=0.1, random_state=0)
            x_train_std = minmax.fit_transform(x_train)
            x_test_std = minmax.transform(x_test)
            model1 = KNeighborsClassifier()
            Kfit = model1.fit(x_train_std, y_train)
            x_test_std_i = minmax.transform(dff)
            y_predt = Kfit.predict(x_test_std_i)
            out1 = ""
            for j in y_predt:
                if (j.isalpha() or ' '):
                    out1 = out1 + j
            print(out1)
            out1 = out1.upper()
            # print(y_predt)
            # arduino_data2 = str(arduino_data1)
            weather1 = str(weather)
            weather1 = weather1.upper()
            # prediction = str(y_predt)
            city_name1 = str(city_name)
            print("current_temperature" + current_temperature)
            data = {
                "FLOOD PREDICTION": out1
            }
            data1 = {
                "PLACE ": city_name
            }
            data2 = {
                "DRAIN LEVEL": f_ard
            }
            data3 = {
                "WEATHER DESCRIPTION": weather1
            }
            data4 = {
                "CURRENT TEMPERATURE": current_temperature
            }
            data5 = {
                "Humidity(%)": hum
            }
            # db.push(data)
            db.child("Data").set(data)
            db.child("location").set(data1)
            db.child("drain_level").set(data2)
            db.child("weather").set(data3)
            db.child("current_temperature").set(data4)
            db.child("Humidity(%)").set(data5)

        #else:
        #    print("weather : ",weather)  # no rain
        #    print("NO CHANCES FOR FLOOD")
        #    #arduino_data2 = str(arduino_data1)
        #    weather1 = str(weather)
        #    weather1 = weather1.upper()
        #    print(weather1)
        #    city_name1 = str(city_name)
        #    data = {
        #        "FLOOD PREDICTION": "NO CHANCES FOR FLOOD"
        #    }
        #    data1 = {
        #        "PLACE ": city_name1,
        #    }
        #   data2 = {
        #        "DRAIN LEVEL": f_ard
        #   }
        #    data3 = {
        #        "WEATHER DESCRIPTION": weather1
        #   }
        #    #db.push(data)
        #    db.child("Data").set(data)
        #    db.child("location").set(data1)
        #    db.child("drain_level").set(data2)
        #    db.child("weather").set(data3)


print('Program started')

firebaseconfig = {
  "apiKey": "AIzaSyDq9hcHVdYVQeCG8Q-2GqnhWhONEbjRW9U",
  "authDomain": "esp32-2d8de.firebaseapp.com",
  "databaseURL": "https://esp32-2d8de-default-rtdb.firebaseio.com",
  "projectId": "esp32-2d8de",
  "storageBucket": "esp32-2d8de.appspot.com",
  "messagingSenderId": "255090196089",
  "appId": "1:255090196089:web:ff8e420511928b56429ea8",
  "measurementId": "G-7BHT2MLDQ6"
}

#city_name = input("Enter city name : ")
D_rate=2#int(input("Enter infrastructure rating : "))
# Setting up the Arduino
schedule.every(1).seconds.do(main_func)

while True:
    schedule.run_pending()
    time.sleep(1)
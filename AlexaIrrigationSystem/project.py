import config    #this file contains the SSID API Key and Bolt device ID
import json,time   
from boltiot import Sms,Bolt     #used to call methods to sen SMS and use Bolt WiFi Module

     

mybolt = Bolt(config.API_KEY, config.DEVICE_ID)        #To configure the Bolt WiFi Module
sms = Sms(config.SSID, config.AUTH_TOKEN, config.TO_NUMBER, config.FROM_NUMBER)       #To configure the Twilio SMS Service

while True:
    response = mybolt.analogRead('A0')     #Read the values
    data = json.loads(response)     #store the response given recieved in JSON format
    if data['success'] != 1:            # To detect if the value recieved contains keyword success and corresponding value should be 1 denoting STATUS OK
        print("There was an error and error is " + data['value'] )
        time.sleep(10)
        continue

    print ("This is the value "+data['value'])  #To print the Analog Value received form the Bolt WiFi Module

    try:
        moist=(int(data['value'])/1024)*100   #To convert the vales in Percentage
        moist = 100 - moist     #To find the moisture content left in soil out of total 100%
        print ("The Moisture content is ",moist," % mg/L")
    except e:
        print("There was an error while parsing the response: ",e)
        continue
    try:     #To find the moisture content of the land
        if moist < 30:
            print ("The Moisture level is  highly decreased.  SMS is sent.")
            response = sms.send_sms("THE MOISTURE CONTENT IN LAND IS LESS THAN 30%, SO PLEASE WATER YOUR PLANTS")
            print("This is the response ")
        elif moist < 30 and moist < 50:
            print ("The Moisture level is decreased.  SMS is sent.")
            response = sms.send_sms("THE MOISTURE CONTENT  IN LAND IS LESS THAN 50%, SO PLEASE WATER YOUR PLANTS.")
            print("This is the response ")
        else:
            print("The Moisture level is GOOD. SMS is sent")
            response = sms.send_sms("MOISTURE IS MODERATE AND GOOD DONT WATER YOUR PLANTS MORE NOW")
            print("This is the response")     
    except Exception as e:
        print ("Error occred : Below are details",e)
    time.sleep(10)

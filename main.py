import time

import requests
from datetime import datetime
import smtplib

MY_LAT = 49.595379 # Your latitude
MY_LONG = 18.010139 # Your longitude

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

#Your position is within +5 or -5 degrees of the ISS position.
able_to_see = False
if int(MY_LAT-5) <= int(iss_latitude) <= int(MY_LAT+5) and int(MY_LONG-5) <= int(iss_longitude) <= int(MY_LONG+5):
    able_to_see = True


parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

time_now = datetime.now()
is_dark = False
if sunrise <= time_now.hour <= sunset:
    is_dark = True

while able_to_see and is_dark:
    time.sleep(60)
    email = "lukaspokus7@gmail.com"
    password = "asdf12345."
    connection = smtplib.SMTP("smtp.gmail.com")
    connection.starttls()
    connection.login(user=email, password=password)
    connection.sendmail(
        from_addr=email,
        to_addrs="lukaspokus7@yahoo.com",
        msg=f"Subject: Look over head\n\n ISS on position{iss_latitude, iss_longitude}"
    )
    connection.close()

#If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.




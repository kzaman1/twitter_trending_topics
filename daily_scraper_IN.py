from credentials import *
import time
import csv
from datetime import date
import tweepy
from tweepy.auth import OAuthHandler
from tweepy import API
import pandas as pd
from email.message import EmailMessage
import ssl
import smtplib

# Twitter API Authentication
auth = tweepy.OAuthHandler(api_key,api_key_secret)
auth.set_access_token(access_token,access_token_secret)
api = tweepy.API(auth)

# Create Filename
country = "India"
filename = "files_trending_topics/_" + "trending_topics_" + country + "_" + str(date.today().strftime("%m-%d-%y")) + ".csv"
print("Filename Generated: ", filename)

woeid_country = 23424848 #India

# Making sure authentication works
try:
    api.verify_credentials()
    print('Successful Authentication \n \n')
except:
    print('Failed authentication')

# Scrape the trending topics from a specific country and print the type of the data
trending_topics = api.get_place_trends(id=woeid_country)
print(type(trending_topics))

# Print the number of elements in the list
print(len(trending_topics))

# Access the dictionary from the list
dict_access1 = trending_topics[0]
print(dict_access1)
print(type(dict_access1))

# Access the dictionary nested inside of the dictionary
dict_access2 = dict_access1['trends']
print(dict_access2)
print(type(dict_access2))

# Convert the child list into a pandas DataFrame
df = pd.DataFrame(dict_access2)
print(df)
# The issue here is that it explodes each list item into a separate column when I need it to be a row.

df.to_csv(filename)

# Send email
subject = "Trending Topics: " + country + " " + str(date.today().strftime("%m-%d-%y"))
print(subject)
body = """
Hello,

Attached you'll find the trending topics from today.

"""
print(body)

em = EmailMessage()
em['From'] = email_sender
em['To'] = email_receiver
em['Subject'] = subject
em.set_content(body)

context = ssl.create_default_context()


with open(filename, "rb") as f:
    file_data = f.read()
    print(file_data)
    em.add_attachment(file_data, maintype = "application", subtype = "csv", filename = filename)

# Set the email server and port
with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
    smtp.login(email_sender, email_password)
    smtp.sendmail(email_sender, email_receiver, em.as_string())

print("Email Sent!")

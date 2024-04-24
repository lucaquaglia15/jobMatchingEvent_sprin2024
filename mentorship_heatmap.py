import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import csv
import os
import copy
import requests
from bs4 import BeautifulSoup

# Function to retrieve Zoom meeting info from CERN INDICO website
def retrieve_zoom_info(username, password, page_url):
    session = requests.Session()

    # Login
    login_data = {"username": username, "password": password}
    session.post(login_url, data=login_data)

    # Request the page after login
    response = session.get(page_url)

    # Parse HTML
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all elements containing Zoom links
    zoom_meetings = soup.find_all("div", class_="event-service-row")

    # Prepare data
    zoom_info = {}
    zoom_links = []
    zoom_meetingid = []
    zoom_passcode = []
    for meeting in zoom_meetings:
        event_name = meeting.find("span", class_="event-service-title").text.strip()
        meeting_id = meeting.find("dt", text="Zoom Meeting ID").find_next_sibling("dd").text.strip()
        passcode = meeting.find("dt", text="Passcode").find_next_sibling("dd").text.strip()
        zoom_url = meeting.find("input", type="text")["value"]
        zoom_info[event_name] = {"Meeting ID": meeting_id, "Passcode": passcode, "Zoom URL": zoom_url}
        zoom_links.append(zoom_url)
        zoom_meetingid.append(meeting_id)
        zoom_passcode.append(passcode)

    return zoom_meetingid, zoom_links, zoom_passcode

# Credentials
username = ""
password = ""

# URLs
login_url = "https://auth.cern.ch/auth/realms/cern/login-actions/authenticate?execution=133f73d5-6454-4197-b529-b109a5d9432c&client_id=indico-cern&tab_id=tgmlNdWhv-o"
page_url = "https://indico.cern.ch/event/1391268/videoconference/"

# Retrieve Zoom meeting info and links
zoom_meetingid, zoom_links, zoom_passcode = retrieve_zoom_info(username, password, page_url)

#Download file from Indico filtering only with name, e-mail address and job offer session (relevant info only)

#If true, debug printouts are enabled
debug = False

#list of recruiters and time of their session
recruiters = ["Manjarres","Roloff","Kortner","Williams","Balli","Corpe","Roloff","Williams","Evans","Manjarres","Kortner","Mijovic","Sofonov","Stupak","Haas","Mijovic","Sofonov","Haas","Whiteson","Evans","Corpe","Balli","Orimoto","Stupak","Orimoto"]
times = ["09:00-10:00","09:00-10:00","10:00-11:00","10:00-11:00","11:00-12:00","11:00-12:00","12:00-13:00","12:00-13:00","14:00-15:00","14:00-15:00","14:00-15:00","15:00-15:55","15:00-16:00","15:00-16:00","15:30-16:30","16:00-17:00","16:05-17:05","16:35-17:35","17:00-18:00","17:00-18:00","17:00-18:00","18:00-19:00","18:00-18:55","19:00-20:00","19:00-20:00"]

#list to keep track of total participants to a given session, to be modified according to the actual number of sessions
totParticipants = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

#open the list of people as pandas df
jobMatching = pd.read_csv("registrations_jobMatching_2023.csv")

jobOfferSessionParticipation = []

#Participant names and sessions as a list, extracted from the df 
participants = jobMatching.loc[:,"Name"].tolist()
sessions = jobMatching.loc[:,"Job Offer Sessions"].tolist()

#Some participants had not indicated their sessions and it said this phrase: To be updated by Oct 17th once recruiter list is finalized, please check back then to update your registration. :)
#So I remove it and I also remove the name of the participants associated with it
for i,j in enumerate(participants):
    if sessions[i] == "To be updated by Oct 17th once recruiter list is finalized, please check back then to update your registration. :)":
        participants.remove(participants[i])
        sessions.remove(sessions[i])

#There is also the case that for some people one of the session is indicated as To be updated [...]
#I also remove these ones
for i in sessions:
    if debug:
        print("analyzing")
    participantSessions = i.split(";")
    for x in participantSessions:
        if x == ' To be updated by Oct 17th once recruiter list is finalized, please check back then to update your registration. :)' or x == ' A session I want to attend is full.':
            participantSessions.remove(x)
                
    jobOfferSessionParticipation.append(participantSessions)

#merge names of recruiters and time of the session to use a title of the columns
mergedTimeRecruiters = [m + " " + str(n) for m,n in zip(recruiters,times)]
mergedTimeRecruiters.insert(0,"Name")

#list of 0s and 1s for all sessions, one list per participant (if == 1 student is participating to the session, if 0 no)
participating = []

if debug:
    print (len(jobOfferSessionParticipation),len(participants))

#remove .csv output file if it exists already
if os.path.exists('participantView.csv'):
    print("Removing old file")
    os.remove('participantView.csv')
else:
    print("File does not exist, moving on")

#Here we write the actual output file
with open('participantView.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    
    #This writes the first line (surname of job recruiter and time slot)
    writer.writerow(mergedTimeRecruiters)

    #This checkes for each job seeker if they have applied for a specific session
    for i,studentSession in enumerate(sessions):
        for j,recruiter in enumerate(recruiters):              
            if studentSession.find(recruiters[j]) != -1 and studentSession.find(times[j]) != -1:
                #if yes -> put a 1 in the participating list  
                participating.append(1)
                #increase by 1 the number of participants to the session
                totParticipants[j] += 1
            else:
                #if no append a 0
                participating.append(0)
       
        #Once the loop is over add the name of the student as the frist element of the participating list
        participating.insert(0,participants[i])
        #write to the .csv file
        writer.writerow(participating)
        #clear list for next iteration       
        participating.clear()

    #Add name of tot participants list
    totParticipants.insert(0,"Tot participants to session")
    #write total number of participants to each session
    writer.writerow(totParticipants)

    #Add name of the zoom sessions list
    zoom_meetingid.insert(0,"Zoom Meeting ID")
    #write zoom links for each session
    writer.writerow(zoom_meetingid)
    
    #Add name of the zoom sessions list
    zoom_passcode.insert(0,"Zoom Passcode")
    #write zoom links for each session
    writer.writerow(zoom_passcode)
    
    #Add name of the zoom sessions list
    zoom_links.insert(0,"Zoom Links")
    #write zoom links for each session
    writer.writerow(zoom_links)
    
    



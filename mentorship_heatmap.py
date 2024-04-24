import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import csv
import os
import copy

#Download file from Indico filtering only with name, e-mail address and job offer session (relevant info only)

#If true, debug printouts are enabled
debug = False

#list of recruiters and time of their session
recruiters = ["Manjarres","Roloff","Kortner","Williams","Balli","Corpe","Roloff","Williams","Evans","Manjarres","Kortner","Mijovic","Sofonov","Stupak","Haas","Mijovic","Sofonov","Haas","Whiteson","Evans","Corpe","Balli","Orimoto","Stupak","Orimoto"]
times = ["09:00-10:00","09:00-10:00","10:00-11:00","10:00-11:00","11:00-12:00","11:00-12:00","12:00-13:00","12:00-13:00","14:00-15:00","14:00-15:00","14:00-15:00","15:00-15:55","15:00-16:00","15:00-16:00","15:30-16:30","16:00-17:00","16:05-17:05","16:35-17:35","17:00-18:00","17:00-18:00","17:00-18:00","18:00-19:00","18:00-18:55","19:00-20:00","19:00-20:00"]

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
            else:
                #if no append a 0
                participating.append(0)
       
        #Once the loop is over add the name of the student as the frist element of the participating list
        participating.insert(0,participants[i])
        #write to the .csv file
        writer.writerow(participating)
        #clear list for next iteration       
        participating.clear()
    




Python script to produce a csv file "participantsView" starting from registrations on Indico

#### How to get the input .csv file

1) Go to Indico (for the moment it's the 2023 [Job Matching Event](https://indico.cern.ch/event/1322376/))

2) Switch to the management area of the event

3) Go to "Registrations"

4) Job seeker's Registration Forms >> Manage >> List of registrations >> Manage >> Customise list

5) Select the following voices: "Has tags", "Does not have tags", "Email Address", "Job Offer Session" and "The sessions are full?" >> Apply

6) [This](https://indico.cern.ch/event/1322376/manage/registration/97732/registrations/?config=d672b2bc-f208-473f-b04c-a1d7496a1551) should be a direct link to the list with the proper filters already applied

7) Select all names >> Export >> CSV

#### How to launch the script

1) Download the input csv file and place it in the same folder as the python script

2) Execute: python3 mentorship_heatmap.py



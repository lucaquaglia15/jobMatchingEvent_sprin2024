Python script to produce a csv file "participantsView.csv" starting from registrations on Indico

#### How to get the input .csv file

0) [This](https://indico.cern.ch/event/1322376/manage/registration/97732/registrations/?config=d672b2bc-f208-473f-b04c-a1d7496a1551) is a direct link to ge the list with the proper filters already applied but in case you would like to customize the list you can follow these steps:

1) Go to Indico (for the moment it's the 2023 [Job Matching Event](https://indico.cern.ch/event/1322376/))

2) Switch to the management area of the event

3) Go to "Registrations"

4) Job seeker's Registration Forms >> Manage >> List of registrations >> Manage >> Customise list

5) Select the filters you want and click "Apply"

6) Select all names >> Export >> CSV

#### How to launch the script

1) Download the input csv file and place it in the same folder as the python script

2) Execute: python3 mentorship_heatmap.py



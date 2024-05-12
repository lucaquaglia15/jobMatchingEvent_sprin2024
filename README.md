Python script to produce a csv file "participantsView.csv" starting from registrations on Indico

The script will now also produced a .xlsx file with a bit nicer format (i.e. bold text, background colors, fixed rows and columns for easy scrolling). To use the code you need to install the **openpyxl Python library** with the following command:

```
pip install openpyxl
```

which will install all the required dependencies

#### How to get the input .csv file

0) [This](https://indico.cern.ch/event/1391268/manage/registration/103748/registrations/?config=b82f9f8a-5093-46c1-badd-c92020a8873c) is a direct link to ge the list with the proper filters already applied (you just have to select all names to be included, then export and select csv format) but in case you would like to customize the list you can follow these steps:

1) Go to the Indico page of the 2024 [Job Matching Event - spring edition](https://indico.cern.ch/event/1391268/overview))

2) Switch to the management area of the event

3) Go to "Registrations"

4) Job seeker's Registration Forms >> Manage >> List of registrations >> Manage >> Customise list

5) Select the filters you want and click "Apply"

6) Select all names >> Export >> CSV

#### How to launch the script

1) Download the input csv file and place it in the same folder as the python script

2) Execute: python3 mentorship_heatmap.py

3) The script will create the participantsView2024.xlsx file in the same folder and you can use that to mark the people as present or absent during your sessions (please note that the code also produces a temporary .csv file, which is deleted at the end of the exectuion, leaving only the .xlsx file)

#### Logic of the script

- The code takes as input a list with the names of recruiters and their timetables. It fetches the .csv input file gathered in point 1) and then it loads it into a pandas dataframe.

- The columns with the names of the job seekers and the sessions they are interested in are saved.

- In a loop the code checks whether the name of any recruiter is included in the sessions in which a job seeker is interested in. If yes then a 1 is added, otherwise a 0 is added. A sum of all participants in a given session is also carried out and added at the bottom.

- Moreover the script gets the zoom links/ID/passcode and adds them to the last lines of the output file.



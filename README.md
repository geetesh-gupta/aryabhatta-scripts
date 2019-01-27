# aryabhatta-scripts
Scripts to scrap Attendance and mail data from IITJ Aryabhatta portal

## How to use

1. Replace the sample credentials in the `.env` file with your own credentials.
1. [Optional]Create a virtual environment `virtualenv script-venv`
1. Activate the virtualenv `source script-venv/bin/activate`
1. Install the requirements 'pip3 install -r requirements.txt` 
1. To check the attendance 
    1. Run the script using `python3 attendance.py`
1. To check new mails
    1. Run the script using `python3 mail.py`

> Currently the output is on the console, working on the script to make it automated and send emails automatically every day!

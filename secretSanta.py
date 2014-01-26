# Simple Secret Santa program, using Gmail
import smtplib
import random
import getpass
from email.mime.text import MIMEText

# Gmail credentials
user = input('Gmail username: ')
pw = getpass.getpass('Gmail password: ')

# Add your participants here, where the key is the participant's name and the value is their email address
participants = { 'John' : 'john@example.com', \
                 'Jane' : 'jane@example.com', \
                 'Jack' : 'jack@example.com', \
                 'Alex' : 'alex@example.com' }

# Add all possible recipients for each Secret Santa participant. This is useful if you don't want couples/spouses to be Secret Santas for each other.
# In the following example, John and Jane are married.
# (Use the same keys as 'participants')
possible_combos = { 'John' : ['Jack', 'Alex'], \
                    'Jane' : ['Jack', 'Alex'], \
                    'Jack' : ['John', 'Jane', 'Alex'], \
                    'Alex' : ['John', 'Jane', 'Jack'] }

random_selection = {}
while random_selection == {}:
    temp = {}
    # Create a temporary copy of 'possible_combos'
    for key,val in possible_combos.items():
        temp[key] = list(val)

    for participant in participants.keys():
        # Make sure we still have possible recipients
        if len(temp[participant]) > 0:
            # Choose a random recipient
            random_selection[participant] = random.choice(temp[participant])
            # Once we've selected a recipient, remove that recipient from everyone else's lists
            for person in temp.keys():
                if random_selection[participant] in temp[person]:
                    temp[person].remove(random_selection[participant])
        else:
            # No one to choose from, start over
            random_selection = {}
            break

# Send out emails with their Secret Santa info
smtp_session = smtplib.SMTP('smtp.gmail.com', 587)
print(smtp_session.ehlo())
print(smtp_session.starttls())
print(smtp_session.ehlo())
print(smtp_session.login(user, pw))

for participant in random_selection.keys():
    msg = MIMEText('Ho ho ho!\n\nYour Secret Santa recipient is: %s' % random_selection[participant])
    msg['Subject'] = 'Your Secret Santa info'
    msg['From'] = 'secretsanta@no-reply.com' # Never have gotten this to work, Gmail doesn't like spoofing email addresses for some reason... :)
    msg['To'] = participants[participant]

    smtp_session.sendmail(msg['From'], [msg['To']], msg.as_string())

smtp_session.quit()
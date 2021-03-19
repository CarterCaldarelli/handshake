from autohandshake import HandshakeSession, InsightsPage, FileType
import json 
import pandas as pd
from pandas.io.json import json_normalize
import os
import shutil

#Declare variables needed to access website, define dictionary for iterating through web pages.
school_url = 'https://nl.joinhandshake.com'
email = 'ccaldarelli@nl.edu'
password = 'cesareIV4'
insights_url = 'https://app.joinhandshake.com/analytics/explore_embed?insights_page='
dim_dict = {'hs_applications':'ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuZHNoYWtlX3Byb2R1Y3Rpb24vYXBwbGljYXRpb25zP3FpZD1MNXZJeDlsSGZvQXFPb2xPZHdtbjdUJmVtYmVkX2RvbWFpbj1odHRwczolMkYlMkZhcHAuam9pbmhhbmRzaGFrZS5jb20=',
            'hs_appointments':'ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuZHNoYWtlX3Byb2R1Y3Rpb24vYXBwb2ludG1lbnRzP3FpZD1heGM4UG9jb1MyMHdkbG1ZUldwRUMwJmVtYmVkX2RvbWFpbj1odHRwczolMkYlMkZhcHAuam9pbmhhbmRzaGFrZS5jb20mdG9nZ2xlPWZpbA==',
            'hs_appointment_notes':'ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuZHNoYWtlX3Byb2R1Y3Rpb24vYXBwb2ludG1lbnRzP3FpZD1YN3JXVkw4bzNpc2I1c09WdjlUQ3l4JmVtYmVkX2RvbWFpbj1odHRwczolMkYlMkZhcHAuam9pbmhhbmRzaGFrZS5jb20mdG9nZ2xlPWZpbA==',
            'hs_career_fair_attendees':'ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuZHNoYWtlX3Byb2R1Y3Rpb24vY2FyZWVyX2ZhaXJfc2Vzc2lvbl9hdHRlbmRlZXM_cWlkPU9OQ1NSUktVRllDR05EN3k1U1VCY3AmZW1iZWRfZG9tYWluPWh0dHBzOiUyRiUyRmFwcC5qb2luaGFuZHNoYWtlLmNvbSZ0b2dnbGU9Zmls',
            'hs_documents':'ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuZHNoYWtlX3Byb2R1Y3Rpb24vc3R1ZGVudHM_cWlkPVI3MDRTMzRjSzZCaFlMTEVMTkdKTjcmZW1iZWRfZG9tYWluPWh0dHBzOiUyRiUyRmFwcC5qb2luaGFuZHNoYWtlLmNvbSZ0b2dnbGU9Zmls',
            'hs_event_attendees':'ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuZHNoYWtlX3Byb2R1Y3Rpb24vZXZlbnRzP3FpZD1HMmU4dzlMb2NGUjdKaWZNVHZkdFJEJmVtYmVkX2RvbWFpbj1odHRwczolMkYlMkZhcHAuam9pbmhhbmRzaGFrZS5jb20=',
            'hs_events':'ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuZHNoYWtlX3Byb2R1Y3Rpb24vZXZlbnRzP3FpZD1lOVpRWkNRRXZRSHVKZUc1dGJ1UDljJmVtYmVkX2RvbWFpbj1odHRwczolMkYlMkZhcHAuam9pbmhhbmRzaGFrZS5jb20=',
            'hs_experiences':'ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuZHNoYWtlX3Byb2R1Y3Rpb24vZXhwZXJpZW5jZXM_cWlkPU9TUlcyZE04RVVHMmNibld6a1pWem0mZW1iZWRfZG9tYWluPWh0dHBzOiUyRiUyRmFwcC5qb2luaGFuZHNoYWtlLmNvbQ==',
            'hs_student_usage':'ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuZHNoYWtlX3Byb2R1Y3Rpb24vc3R1ZGVudHM_cWlkPVdremp2bkhxT2tuUktuaEtrcnQ0UTImZW1iZWRfZG9tYWluPWh0dHBzOiUyRiUyRmFwcC5qb2luaGFuZHNoYWtlLmNvbSZ0b2dnbGU9Zmls',
            'hs_applications_plt':'ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuZHNoYWtlX3Byb2R1Y3Rpb24vYXBwbGljYXRpb25zP3FpZD1FQzNFTnZLaHFMbXFCRXBxYlpWTk5qJmVtYmVkX2RvbWFpbj1odHRwczolMkYlMkZhcHAuam9pbmhhbmRzaGFrZS5jb20mdG9nZ2xlPWZpbA==',
            'hs_experiences_plt':'ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuZHNoYWtlX3Byb2R1Y3Rpb24vZXhwZXJpZW5jZXM_cWlkPVRHTzFKdWZaSFlKb3B6UkxxWHYwZnAmZW1iZWRfZG9tYWluPWh0dHBzOiUyRiUyRmFwcC5qb2luaGFuZHNoYWtlLmNvbQ==',
            'hs_profile_notes':'ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuZHNoYWtlX3Byb2R1Y3Rpb24vc3R1ZGVudHM_cWlkPWFwTFc2RkhhOEVadzJ1aVFRZEYxdnYmZW1iZWRfZG9tYWluPWh0dHBzOiUyRiUyRmFwcC5qb2luaGFuZHNoYWtlLmNvbSZ0b2dnbGU9Zmls',
            'hs_experience_page': 'ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuZHNoYWtlX3Byb2R1Y3Rpb24vZXhwZXJpZW5jZXM_cWlkPW1kMHJJWUNuUGVOU01XUGd4RUxPRlEmZW1iZWRfZG9tYWluPWh0dHBzOiUyRiUyRmFwcC5qb2luaGFuZHNoYWtlLmNvbSZ0b2dnbGU9Zmls',
            'hs_requested_experience_label':'ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuZHNoYWtlX3Byb2R1Y3Rpb24vc3R1ZGVudHM_cWlkPVN2RUd0dHZ3Vk5nVUZweHRYN1Fad2wmZW1iZWRfZG9tYWluPWh0dHBzOiUyRiUyRmFwcC5qb2luaGFuZHNoYWtlLmNvbSZ0b2dnbGU9Zmls',
            'hs_jobs':'ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuZHNoYWtlX3Byb2R1Y3Rpb24vam9icz9xaWQ9cTF5UlFkNXhjS3ByOVB5RmVma0dSZyZlbWJlZF9kb21haW49aHR0cHM6JTJGJTJGYXBwLmpvaW5oYW5kc2hha2UuY29tJnRvZ2dsZT1maWw=',
            'hs_milestone_events':'ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuZHNoYWtlX3Byb2R1Y3Rpb24vZXZlbnRzP3FpZD1XTU1rWG9kbFhndWoxRzZHR0RQYWZaJmVtYmVkX2RvbWFpbj1odHRwczolMkYlMkZhcHAuam9pbmhhbmRzaGFrZS5jb20mdG9nZ2xlPWZpbA=='}

dir_pairs = {
            'hs_applications':'Applications',
            'hs_appointments':'Appointments',
            'hs_appointment_notes':'Appointment Notes',
            'hs_career_fair_attendees':'Career Fair Attendees',
            'hs_documents':'Documents',
            'hs_events':'Events',
            'hs_event_attendees':'Events Attendance',
            'hs_experiences':'Experiences',
            'hs_student_usage':'Students Usage',
            'hs_milestone_events':'Events',
            'hs_applications_plt':'Pipeline Exports\\Applications',
            'hs_experiences_plt':'Pipeline Exports\\Experiences',
            'hs_profile_notes':'Pipeline Exports\\Profile Notes',
            'hs_experience_page':'Pipeline Exports\\Experiences',
            'hs_requested_experience_label':'Pipeline Exports\\Experiences'       
}

#Iterate through web pages and download datasets
with HandshakeSession(school_url, email, password, max_wait_time = 120, chromedriver_path = "C:\\Users\\ccaldarelli\\chromedriver.exe") as browser:
    for fname, url in dim_dict.items():
        cur_insight_page = InsightsPage(insights_url+url, browser)
        report_data = cur_insight_page.download_file(download_dir = "C:\\Users\\ccaldarelli\\downloads", file_name = fname, file_type = FileType.CSV)

#Move files from downloads to network drives
for key,value in dir_pairs.items():
    source = "C:\\Users\\ccaldarelli\\Downloads\\"+key+".csv" 
    destination ="L:\\UGC Data Analysis & Reports\\Raw Data\\HandShake\\"+value
    dest = shutil.copy(source, destination)
    print("Destination path:", dest)

jobs_src = "C:\\Users\\ccaldarelli\\Downloads\\hs_jobs.csv"
erm_dest = "H:\\Power BI Reports\\ERM Reports"
shutil.copy(jobs_src,erm_dest)

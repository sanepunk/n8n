import streamlit as st
import requests
import json
from datetime import datetime
import os
from dotenv import load_dotenv
import psycopg2
import time
from datetime import timezone

load_dotenv()

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("host"),
        database=os.getenv("dbname"),
        user=os.getenv("user"),
        password=os.getenv("SUPABASE_PASS"),
        port=os.getenv("port")
    )

def get_all_records():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM valve ORDER BY created_at DESC')
    records = cur.fetchall()
    cur.close()
    conn.close()
    return records

def get_analysis_result(student_id, max_retries=10, delay_seconds=2):
    for attempt in range(max_retries):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT * FROM valve 
                WHERE "StudentID" = %s 
                ORDER BY created_at DESC 
                LIMIT 1
            """, (student_id,))
            result = cur.fetchone()
            cur.close()
            conn.close()

            if result:
                return result
            
            remaining = max_retries - attempt - 1
            st.info(f"Waiting for analysis... (Attempts remaining: {remaining})")
            time.sleep(delay_seconds)
            
        except Exception as e:
            st.error(f"Database error during retry: {str(e)}")
            return None
    
    return None

st.title('Student Performance Analysis')

webhook_url = os.getenv("N8N_WEBHOOK_TEST")
if not webhook_url:
    st.error("⚠️ N8N_WEBHOOK_TEST environment variable is not set!")
else:
    st.success(f"✓ Webhook URL is configured")

with st.form("student_form"):
    student_id = st.text_input("Student ID")
    name = st.text_input("Name")
    subject = st.text_input("Subject")
    percentage = st.number_input("Percentage Marks", min_value=0.0, max_value=100.0)
    weak_topics = st.text_area("Topics with Less Marks (comma-separated)")
    
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        if not webhook_url:
            st.error("Cannot submit: Webhook URL is not configured!")
        else:
            data = {
                "StudentID": student_id,
                "StudentName": name,
                "QuizTopic": subject,
                "ScorePercentage": float(percentage),
                "IncorrectTopics": weak_topics
            }
            
            try:
                st.write("Sending request to n8n webhook...")
                st.json(data)
                
                response = requests.post(webhook_url, json=data)
                st.write(f"Response status code: {response.status_code}")
                
                if response.status_code == 200:
                    response_data = response.json()
                    st.write("Response data:", response_data)
                    
                    initial_message = response_data.get('message', '')
                    if initial_message == 'Workflow was started':
                        st.info("Analysis in progress...")
                        
                        result = get_analysis_result(student_id)
                        
                        if result:
                            st.success("Analysis completed!")
                            
                            with st.expander("Latest Analysis Result", expanded=True):
                                id, created_at, student_id, name, subject, percentage, topics, conclusion = result
                                st.markdown("### Analysis Conclusion")
                                st.markdown(conclusion)
                        else:
                            st.warning("Analysis result not found after multiple retries. The process might take longer than expected.")
                    else:
                        st.error(f"Unexpected response from n8n webhook: {initial_message}")
                else:
                    st.error(f"Error {response.status_code}: {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Request error: {str(e)}")
            except Exception as e:
                st.error(f"Error: {str(e)}")

st.subheader("Previous Analysis Records")

try:
    records = get_all_records()
    if records:
        for record in records:
            id, created_at, student_id, name, subject, percentage, topics, conclusion = record
            
            with st.expander(f"Student: {name} - ID: {student_id} - Subject: {subject}"):
                st.write(f"Percentage: {percentage}%")
                st.write(f"Topics Needing Improvement: {topics}")
                st.markdown("### Analysis Conclusion")
                st.markdown(conclusion)
                st.write(f"Generated at: {created_at}")
    else:
        st.info("No previous analysis records found.")
except Exception as e:
    st.error(f"Error fetching records: {str(e)}")
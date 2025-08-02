# Report Generator Bot for Scoreazy

An AI-powered agent designed to automatically generate personalized, one-page performance reports for students based on their quiz results. Built with Streamlit, N8N automation, and Google's Gemini AI.

## Overview

The Report Generator Bot analyzes student quiz data and generates constructive, encouraging summaries that:
- Highlight student strengths
- Identify specific areas for improvement
- Suggest actionable next steps
- Maintain a supportive, education-first tone

## Features

- **User-Friendly Interface**: Built with Streamlit for easy data input and report viewing
- **Automated Workflow**: Processes data through N8N webhooks for reliable automation
- **Personalized Reports**: Creates individualized feedback based on student performance data
- **Structured Output**: Generates reports with consistent sections:
  - What You Did Well 🌟
  - Areas to Focus On Next 🌱
  - Tips to Get Started 💡
- **Data Persistence**: Stores all reports in PostgreSQL for easy access and history tracking

## Input Data Structure

The bot expects the following data structure through the Streamlit interface:

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| StudentID | String | Unique identifier for the student | "1234567890" |
| StudentName | String | First name of the student | "Rohan" |
| QuizTopic | String | Subject/topic of assessment | "Chemical Reactions" |
| ScorePercentage | Number | Final score as percentage | 65 |
| IncorrectTopics | String | Comma-separated list of mistake areas | "Balancing Equations, Redox Reactions" |

## Technical Architecture

### Components

- **Frontend**: Streamlit web application
- **Automation Platform**: N8N with webhook triggers
- **AI Model**: Google Gemini Pro
- **Database**: PostgreSQL
- **Backend**: Python integration layer

### Workflow

1. **Data Input**:
   - Users enter student data through Streamlit interface
   - Data validation and preprocessing

2. **Automation Flow**:
   - Streamlit sends data to N8N webhook endpoint
   - N8N processes and formats the data

3. **Report Generation**:
   - N8N triggers Gemini API call
   - AI generates personalized report
   - Report is stored in PostgreSQL

4. **Data Access**:
   - Reports are fetched from PostgreSQL
   - Displayed in Streamlit interface
   - Historical reports available for review

## Project Structure

```
n8n-agent/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── agent_description.md  # Agent workflow documentation
└── .gitignore           # Git ignore rules
```

## Setup

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables:
```bash
GEMINI_API_KEY=your_gemini_api_key
N8N_WEBHOOK_URL=your_webhook_url
POSTGRES_CONNECTION_STRING=your_postgres_connection_string
```

3. Run the Streamlit application:
```bash
streamlit run app.py
```

## Sample Output

Here's an example of a generated report:

```markdown
### 🌟 What You Did Well
Great job tackling the Chemical Reactions quiz, Rohan! A score of 65% shows you have a good foundational knowledge of the topic. It's clear you've been putting in the work to understand how different substances interact, and that's a fantastic starting point!

### 🌱 Areas to Focus On Next
This quiz showed us a couple of great opportunities to strengthen your chemistry skills even more. Let's spend a little extra time on:

Balancing Equations: This is a crucial skill because it's the foundation for understanding all chemical reactions.

Redox Reactions: Mastering this will help you predict how and why reactions happen.

### 💡 A Few Tips to Get Started
Try the "Equation Balancing" practice set in the app. Just doing 5-10 problems will make the process feel much more natural.

Watch the short 7-minute video on "Intro to Redox Reactions." Sometimes, seeing it explained visually makes all the difference.

You're building a great skill set, Rohan. Keep up the curiosity and effort!
```

## Requirements

- Python 3.8+
- Streamlit
- N8N automation platform
- Google Gemini API access
- PostgreSQL database
- Required Python packages (see requirements.txt)

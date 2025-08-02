# Student Performance Analysis Agent

## 1. Agent Objective
The agent is designed to analyze student performance data and provide personalized feedback and recommendations. It processes quiz/test results, identifies weak areas, and generates detailed performance insights using AI-powered analysis through Gemini 2.0.

## 2. Input
The agent requires the following inputs through a Streamlit form:
- Student ID (text)
- Student Name (text)
- Subject/Quiz Topic (text)
- Percentage Marks (number: 0-100)
- Topics with Less Marks (comma-separated text)

## 3. Workflow

### Trigger
The workflow is triggered when a user submits the Streamlit form with student performance data.

### Step-by-step Process
1. **Data Collection**
   - User fills out the Streamlit form with student performance data
   - Form validation ensures all required fields are completed

2. **Data Processing**
   - Streamlit application sends data to N8N webhook
   - N8N workflow is triggered with the following data structure:
     ```json
     {
       "StudentID": "string",
       "StudentName": "string",
       "QuizTopic": "string",
       "ScorePercentage": float,
       "IncorrectTopics": "string"
     }
     ```

3. **AI Analysis**
   - N8N forwards the data to Gemini 2.0
   - Gemini processes the data and generates personalized analysis
   - Analysis includes:
     - Performance evaluation
     - Weak area identification
     - Improvement recommendations
     - Study strategies

4. **Data Storage**
   - Analysis results are stored in PostgreSQL via Supabase
   - Database schema includes:
     - Student information
     - Performance metrics
     - AI-generated analysis
     - Timestamp

5. **Result Display**
   - Streamlit application polls the database for results
   - Results are displayed in markdown format
   - Historical analyses are available for review

### Tools/Services Used
- Frontend: Streamlit
- Workflow Automation: N8N
- AI Analysis: Gemini 2.0
- Database: PostgreSQL (via Supabase)
- API Integration: Webhooks

## 4. Prompt Sample

### Analysis Generation Prompt
```
Analyze the following student performance data and provide detailed feedback:

Student: {StudentName}
Subject: {QuizTopic}
Score: {ScorePercentage}%
Weak Topics: {IncorrectTopics}

Please provide:
1. Overall performance assessment
2. Detailed analysis of weak areas
3. Specific improvement strategies for each weak topic
4. Study plan recommendations
5. Positive reinforcement and encouragement

Format the response in markdown with clear sections and bullet points.
```

## 5. Output Example
```
### Performance Analysis for John Doe
**Subject**: Mathematics
**Score**: 75%

#### Overall Assessment
Your performance shows good understanding of basic concepts but indicates room for improvement in specific areas.

#### Areas Needing Attention
- Trigonometry (35% accuracy)
- Complex Numbers (42% accuracy)

#### Improvement Strategies
1. **Trigonometry**
- Focus on understanding fundamental relationships between angles
- Practice solving right triangle problems
- Review unit circle concepts

2. **Complex Numbers**
- Start with basic operations review
- Use visualization techniques for better understanding
- Practice with real-world applications

#### Recommended Study Plan
1. Dedicate 2 hours/week to each weak topic
2. Use interactive tools for visualization
3. Complete practice problems daily
4. Review progress weekly

#### Positive Notes
- Strong performance in Algebra sections
- Good problem-solving approach in word problems
- Consistent improvement pattern from previous assessments

Keep up the great work! With focused practice on the identified areas, you're well-positioned to improve your understanding and scores.


📌 **Note**: This agent can be extended with additional features such as:
- Progress tracking over time
- Comparative analysis with peer performance
- Custom study resource recommendations
- Parent/teacher notification system
- Integration with learning management systems
```
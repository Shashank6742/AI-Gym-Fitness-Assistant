# VITALIQ AI — Intelligent Fitness Platform

VITALIQ AI is an AI-powered fitness platform designed to provide personalized workout assistance, nutrition guidance, fitness habit tracking, performance analytics, AI-powered fitness conversations, and nearby gym recommendations.

The platform combines computer vision, artificial intelligence, data analytics, and location-based services into a single fitness assistant.

---

## 🚀 Features

### 🏋️ AI Gym Trainer
- Real-time exercise detection using webcam
- MediaPipe-based human pose estimation
- Automatic repetition counting
- Exercise form analysis
- Form score and feedback
- Supports multiple exercises including:
  - Squats
  - Bicep Curls
  - Push-ups
  - Lunges
  - Shoulder Press
  - Jumping Jacks
  - Sit-ups
  - High Knees
  - Lateral Raises
  - Front Raises
  - Calf Raises
  - Plank
- Plank hold-time tracking

### 🥗 Nutrition Coach
- BMI calculation
- BMR calculation
- Personalized calorie target
- Protein target calculation
- Goal-based nutrition guidance
- Supports:
  - Weight Loss
  - Weight Maintenance
  - Muscle Building
- Meal planning
- Grocery list generation
- Daily calorie tracking

### 🤖 AI Fitness Buddy
- AI-powered fitness assistant
- Natural-language fitness conversations
- Workout and nutrition context
- Personalized fitness guidance
- Powered by Groq AI

### 📈 Habit Intelligence
- Daily workout tracking
- Water intake tracking
- Sleep tracking
- Weekly fitness goals
- Consistency tracking
- Streak calculation
- Fitness consistency score
- Progress insights

### 📊 Performance Analytics
- Workout session history
- Exercise-wise performance tracking
- Repetition and hold tracking
- Form-score analysis
- Session duration
- Joint-angle information
- AI-generated performance insights

### 📍 Gym Finder
- Find nearby gyms and fitness centers
- OpenStreetMap-based location search
- Adjustable search radius
- Distance-based sorting
- Gym address information
- Available phone and website information
- Map-based results
- Directions support

### 🔐 Authentication & User Management
- Secure user authentication using Supabase
- Individual user sessions
- User-specific fitness data
- Admin role support
- Separate admin dashboard
- User data isolation

### 👨‍💼 Admin Dashboard
- Admin-only access
- User information
- Workout session information
- Fitness activity overview
- Administrative monitoring

---

## 🛠️ Technologies Used

### Frontend / Application
- Python
- Streamlit

### AI & Computer Vision
- MediaPipe
- OpenCV
- Groq AI

### Data & Database
- Supabase
- PostgreSQL
- Pandas
- NumPy

### Other Technologies
- Streamlit WebRTC
- OpenStreetMap
- Nominatim / Overpass APIs
- Python-dotenv

---

## 🧠 AI & Computer Vision

The AI Gym Trainer uses MediaPipe Pose to identify human body landmarks from the webcam.

The detected landmarks are used to calculate joint angles and determine exercise movement.

The general workflow is:

```text
Webcam
   ↓
Video Frames
   ↓
MediaPipe Pose Detection
   ↓
Body Landmark Detection
   ↓
Joint Angle Calculation
   ↓
Exercise Movement Analysis
   ↓
Rep / Hold Detection
   ↓
Form Score
   ↓
Real-Time Feedback
🏗️ System Architecture
                    VITALIQ AI
                         │
        ┌────────────────┼────────────────┐
        │                │                │
   AI Gym Trainer   Nutrition Coach   AI Fitness Buddy
        │                │                │
   MediaPipe         Calculations       Groq AI
   OpenCV            Meal Planning      Chat
        │                │                │
        └────────────────┼────────────────┘
                         │
                Fitness Data Layer
                         │
        ┌────────────────┼────────────────┐
        │                │                │
   Habit Tracking   Performance      Gym Finder
                    Analytics
                         │
                         ↓
                  Supabase Database
                         │
                         ↓
                  User / Admin Data
📁 Project Structure
AI-Gym-Fitness-Assistant/
│
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── assets/
│
├── data/
│
├── modules/
│
├── reports/
│
└── utils/
⚙️ Installation
1. Clone the repository
git clone https://github.com/Shashank6742/AI-Gym-Fitness-Assistant.git
2. Navigate to the project
cd AI-Gym-Fitness-Assistant
3. Create a virtual environment
python -m venv venv
4. Activate the virtual environment

For Windows Command Prompt:

venv\Scripts\activate
5. Install dependencies
pip install -r requirements.txt
🔑 Environment Variables

Create a .env file in the project root.

GROQ_API_KEY=your_groq_api_key
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_publishable_key

Do not publish API keys or other private credentials to GitHub.

▶️ Run the Application

Start the Streamlit application using:

streamlit run app.py

Or, when using the project virtual environment:

venv\Scripts\python.exe -m streamlit run app.py

The application will open in the browser.

🔐 Database

VITALIQ AI uses Supabase for authentication and persistent fitness data.

The database stores information related to:

User profiles
Workout sessions
Nutrition profiles
Habit logs
User roles

Row Level Security (RLS) is used to restrict user data access.

📊 Main Modules
Module	Purpose
AI Gym Trainer	Real-time workout and posture analysis
Nutrition Coach	Personalized nutrition and calorie guidance
AI Fitness Buddy	AI-powered fitness conversations
Habit Intelligence	Fitness habit and consistency tracking
Performance Analytics	Workout history and performance insights
Gym Finder	Nearby gym and fitness-center discovery
Admin Dashboard	Administrative monitoring
🌐 Deployment

The application is designed for deployment using Streamlit Community Cloud.

The deployed application requires the following secrets:

GROQ_API_KEY
SUPABASE_URL
SUPABASE_KEY

These values should be configured through the deployment platform's secrets management rather than committed to the repository.

🔒 Security
API keys are stored using environment variables.
.env is excluded from Git.
User authentication is handled through Supabase.
User fitness data is associated with individual authenticated accounts.
Admin functionality is restricted using role-based access.
Database Row Level Security is enabled.
🎯 Project Objective

The objective of VITALIQ AI is to provide a unified AI-powered fitness ecosystem that helps users:

Perform exercises with real-time assistance
Monitor workout performance
Receive nutrition guidance
Maintain healthy fitness habits
Interact with an AI fitness assistant
Discover nearby gyms
👨‍💻 Author

Shashank BH

B.E. Computer Science and Engineering (AI & ML)
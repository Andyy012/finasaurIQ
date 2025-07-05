import streamlit as st
import json
import datetime
import random
from typing import Dict, List, Optional
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="FinIq - Learn Finance the Fun Way",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- THEME CSS ---
def inject_theme_css(night_mode=False):
    if not night_mode:
        # White & light green theme
        st.markdown("""
        <style>
        .stApp, .block-container {
            background-color: #fff !important;
        }
        body {
            background-color: #fff !important;
            color: #222 !important;
        }
        .main-header {
            font-size: 2.5rem;
            font-weight: bold;
            color: #43b77a;
            text-align: center;
            margin-bottom: 1.5rem;
            letter-spacing: 1px;
        }
        .duo-mascot {
            font-size: 2.5rem;
            margin-right: 0.5rem;
            vertical-align: middle;
        }
        .lesson-card {
            background: #f6fcf7 !important;
            padding: 1.5rem;
            border-radius: 18px;
            margin: 1.2rem 0;
            border-left: 8px solid #43b77a;
            box-shadow: 0 2px 8px rgba(67,183,122,0.08);
            transition: box-shadow 0.2s;
        }
        .lesson-card:hover {
            box-shadow: 0 4px 16px rgba(67,183,122,0.18);
        }
        .question-card {
            background: #fff !important;
            padding: 2rem;
            border-radius: 18px;
            margin: 1.5rem 0;
            box-shadow: 0 2px 8px rgba(67,183,122,0.08);
            border: 2px solid #43b77a;
        }
        .badge {
            display: inline-block;
            background-color: #e6f9ed;
            color: #43b77a;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            margin: 0.25rem;
            font-weight: bold;
        }
        .streak-counter {
            background: linear-gradient(45deg, #ffb36b, #ffe066);
            color: #fff;
            padding: 1rem;
            border-radius: 10px;
            text-align: center;
            margin: 1rem 0;
        }
        .duo-btn {
            background-color: #43b77a !important;
            color: #fff !important;
            border-radius: 12px !important;
            font-size: 1.1rem !important;
            font-weight: bold !important;
            padding: 0.7rem 2.2rem !important;
            margin: 0.5rem 0 !important;
            border: none !important;
            box-shadow: 0 2px 8px rgba(67,183,122,0.08);
            transition: background 0.2s;
        }
        .duo-btn:hover {
            background-color: #2e8c5e !important;
        }
        .duo-progress {
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 1.5rem 0 0.5rem 0;
        }
        .duo-dot {
            width: 18px;
            height: 18px;
            border-radius: 50%;
            background: #e0e0e0;
            margin: 0 6px;
            display: inline-block;
            border: 2px solid #43b77a;
            transition: background 0.2s, border 0.2s;
        }
        .duo-dot.active {
            background: #43b77a;
            border: 2px solid #ffd740;
        }
        .duo-dot.completed {
            background: #ffd740;
            border: 2px solid #43b77a;
        }
        .sidebar-profile {
            background: #e3e5e8 !important;
            border-radius: 18px;
            padding: 1.2rem;
            margin-bottom: 1.5rem;
            text-align: center;
            box-shadow: 0 2px 8px rgba(67,183,122,0.08);
            position: relative;
        }
        .sidebar-profile .duo-mascot {
            font-size: 3rem;
            margin-bottom: 0.5rem;
        }
        .sidebar-profile .username {
            font-size: 1.3rem;
            font-weight: bold;
            color: #43b77a;
            margin-bottom: 0.2rem;
        }
        .sidebar-profile .level {
            font-size: 1.1rem;
            color: #ffd740;
            font-weight: bold;
        }
        .sidebar-profile button#edit_profile_btn {
            position: absolute;
            top: 10px;
            right: 10px;
            padding: 2px 10px;
            border-radius: 8px;
            background: #43b77a !important;
            color: #fff !important;
            border: none;
            font-weight: bold;
            cursor: pointer;
            font-size: 0.9rem;
            transition: background 0.2s;
        }
        .sidebar-profile button#edit_profile_btn:hover {
            background: #2e8c5e !important;
        }
        .stButton > button {
            background-color: #43b77a !important;
            color: #fff !important;
            border-radius: 12px !important;
            font-size: 1.1rem !important;
            font-weight: bold !important;
            padding: 0.7rem 2.2rem !important;
            margin: 0.5rem 0 !important;
            border: none !important;
            box-shadow: 0 2px 8px rgba(67,183,122,0.08);
            transition: background 0.2s;
        }
        .stButton > button:hover {
            background-color: #2e8c5e !important;
        }
        /* Sidebar background and text */
        section[data-testid="stSidebar"], .css-6qob1r, .stSidebar {
            background-color: #f6fcf7 !important;
            color: #222 !important;
        }
        /* Sidebar profile card text */
        .sidebar-profile, .sidebar-profile * {
            color: #222 !important;
        }
        .sidebar-profile .username {
            color: #43b77a !important;
        }
        .sidebar-profile .level {
            color: #ffd740 !important;
        }
        /* Sidebar headings and stats */
        .stSidebar h1, .stSidebar h2, .stSidebar h3, .stSidebar h4, .stSidebar h5, .stSidebar h6, .stSidebar p, .stSidebar span, .stSidebar label, .stSidebar div {
            color: #222 !important;
        }
        /* Input and select boxes */
        .stTextInput input, .stSelectbox div[data-baseweb="select"], .stSelectbox, .stSelectbox input {
            background-color: #fff !important;
            color: #111 !important;
            border: 1px solid #d0d4d7 !important;
        }
        .stTextInput input::placeholder {
            color: #888 !important;
        }
        .stSelectbox span, .stSelectbox label, .stSelectbox div {
            color: #111 !important;
        }
        /* General text color for main content and cards */
        .main-header, .lesson-card, .question-card, .badge, .streak-counter, .duo-btn, .duo-dot, .sidebar-profile, .stApp, .block-container, .stMarkdown, .stDataFrame, .stTable, .stMetric, .stAlert, .stInfo, .stSuccess, .stWarning, .stError {
            color: #111 !important;
        }
        /* Quiz answer choices (radio/checkbox labels) */
        .stRadio label, .stCheckbox label {
            color: #111 !important;
        }
        /* Back to lessons arrow */
        .stApp svg, .stApp [data-testid="stAppViewContainer"] svg {
            color: #43b77a !important;
            fill: #43b77a !important;
        }
        /* Make selectbox (choose a page) match username input */
        .stSelectbox__control, .stSelectbox__single-value, .stSelectbox__value-container, .stSelectbox__dropdown, .stSelectbox [data-baseweb="select"] {
            background-color: #fff !important;
            color: #111 !important;
            border: 1px solid #d0d4d7 !important;
        }
        .stSelectbox__option, .stSelectbox__option span {
            background-color: #fff !important;
            color: #111 !important;
        }
        /* General text color for all light backgrounds */
        .main-header, .lesson-card, .question-card, .badge, .streak-counter, .duo-btn, .duo-dot, .sidebar-profile, .stApp, .block-container, .stMarkdown, .stDataFrame, .stTable, .stMetric, .stAlert, .stInfo, .stSuccess, .stWarning, .stError, .stSidebar, .stSidebar *, .stTextInput input, .stSelectbox__single-value, .stSelectbox__option, .stSelectbox__option span, .stSelectbox label, .stSelectbox span, .stSelectbox__value-container, .stSelectbox__dropdown, .stRadio label, .stCheckbox label, .stButton > button, .stSelectbox__control {
            color: #111 !important;
        }
        /* Force all main content text under the FinIQ dashboard to black */
        .block-container, .block-container * {
            color: #111 !important;
        }
        /* Lesson navigation selectbox (top left in lesson) */
        .stSelectbox__control, .stSelectbox__single-value, .stSelectbox__value-container, .stSelectbox__dropdown, .stSelectbox [data-baseweb="select"] {
            background-color: #fff !important;
            color: #111 !important;
            border: 1px solid #d0d4d7 !important;
        }
        .stSelectbox__option, .stSelectbox__option span {
            background-color: #fff !important;
            color: #111 !important;
        }
        /* Sidebar navigation selectbox (force app theme color) */
        .stSelectbox__control, .stSelectbox__single-value, .stSelectbox__value-container {
            background-color: #43b77a !important;
            color: #fff !important;
            border: 1px solid #43b77a !important;
        }
        .stSelectbox__dropdown {
            background-color: #fff !important;
        }
        .stSelectbox__option, .stSelectbox__option span {
            background-color: #fff !important;
            color: #111 !important;
        }
        .stSelectbox__single-value {
            color: #fff !important;
        }
        /* Force selectbox input to app green and white */
        .stSelectbox__control, .stSelectbox__single-value, .stSelectbox__value-container {
            background-color: #43b77a !important;
            color: #fff !important;
            border: 1px solid #43b77a !important;
        }
        .stSelectbox__single-value, .stSelectbox__placeholder {
            color: #fff !important;
        }
        /* Force dropdown menu to white background and dark text */
        .stSelectbox__menu, .stSelectbox__menu-list, .stSelectbox__option, .stSelectbox__option span {
            background-color: #fff !important;
            color: #111 !important;
        }
        .stSelectbox__option--is-selected, .stSelectbox__option--is-focused {
            background-color: #e6f9ed !important;
            color: #222 !important;
        }
        /* Target Streamlit's internal react-select classes for extra force */
        [data-baseweb="select"] .css-1wa3eu0-placeholder,
        [data-baseweb="select"] .css-1uccc91-singleValue {
            color: #fff !important;
        }
        [data-baseweb="select"] .css-1okebmr-indicatorSeparator {
            background-color: #43b77a !important;
        }
        [data-baseweb="select"] .css-1pahdxg-control {
            background-color: #43b77a !important;
            color: #fff !important;
            border: 1px solid #43b77a !important;
        }
        [data-baseweb="select"] .css-1dimb5e-menu {
            background-color: #fff !important;
            color: #111 !important;
        }
        [data-baseweb="select"] .css-1n7v3ny-option {
            background-color: #fff !important;
            color: #111 !important;
        }
        [data-baseweb="select"] .css-1n7v3ny-option[aria-selected="true"],
        [data-baseweb="select"] .css-1n7v3ny-option:hover {
            background-color: #e6f9ed !important;
            color: #222 !important;
        }
        /* Profile edit selectboxes (avatar/account type) - main box light green */
        .stSelectbox__control, .stSelectbox__value-container, .stSelectbox__single-value {
            background-color: #e6f9ed !important;
            color: #111 !important;
            border: 1.5px solid #43b77a !important;
        }
        .stSelectbox__dropdown {
            background-color: #fff !important;
        }
        .stSelectbox__option, .stSelectbox__option span {
            background-color: #fff !important;
            color: #111 !important;
        }
        .stSelectbox__single-value, .stSelectbox__placeholder {
            color: #111 !important;
        }
        /* Extra force for Streamlit/react-select classes in profile edit */
        [data-baseweb="select"] .css-1pahdxg-control {
            background-color: #e6f9ed !important;
            color: #111 !important;
            border: 1.5px solid #43b77a !important;
        }
        [data-baseweb="select"] .css-1uccc91-singleValue,
        [data-baseweb="select"] .css-1wa3eu0-placeholder {
            color: #111 !important;
        }
        /* Username input box - thinner black outline */
        .stTextInput input {
            border: 1.5px solid #222 !important;
            box-shadow: none !important;
        }
        /* Remove the white line (indicator separator) in the navigation selectbox */
        .css-1okebmr-indicatorSeparator {
            background-color: transparent !important;
            width: 0 !important;
        }
        </style>
        """, unsafe_allow_html=True)
    else:
        # Night mode: the old greenish 'light' theme
        st.markdown("""
        <style>
        .stApp, .block-container {
            background-color: #f6f9f6;
        }
        body {
            background-color: #f6f9f6;
        }
        .main-header {
            font-size: 2.5rem;
            font-weight: bold;
            color: #43b77a;
            text-align: center;
            margin-bottom: 1.5rem;
            letter-spacing: 1px;
        }
        .duo-mascot {
            font-size: 2.5rem;
            margin-right: 0.5rem;
            vertical-align: middle;
        }
        .lesson-card {
            background: linear-gradient(90deg, #e6f9ed 60%, #f6f9f6 100%);
            padding: 1.5rem;
            border-radius: 18px;
            margin: 1.2rem 0;
            border-left: 8px solid #43b77a;
            box-shadow: 0 2px 8px rgba(67,183,122,0.08);
            transition: box-shadow 0.2s;
        }
        .lesson-card:hover {
            box-shadow: 0 4px 16px rgba(67,183,122,0.18);
        }
        .question-card {
            background: linear-gradient(90deg, #fffbe6 60%, #f6f9f6 100%);
            padding: 2rem;
            border-radius: 18px;
            margin: 1.5rem 0;
            box-shadow: 0 2px 8px rgba(255,215,64,0.08);
            border: 2px solid #ffd740;
        }
        .badge {
            display: inline-block;
            background-color: #ffd700;
            color: #000;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            margin: 0.25rem;
            font-weight: bold;
        }
        .streak-counter {
            background: linear-gradient(45deg, #ff6b6b, #ffa500);
            color: white;
            padding: 1rem;
            border-radius: 10px;
            text-align: center;
            margin: 1rem 0;
        }
        .duo-btn {
            background-color: #43b77a !important;
            color: #fff !important;
            border-radius: 12px !important;
            font-size: 1.1rem !important;
            font-weight: bold !important;
            padding: 0.7rem 2.2rem !important;
            margin: 0.5rem 0 !important;
            border: none !important;
            box-shadow: 0 2px 8px rgba(67,183,122,0.08);
            transition: background 0.2s;
        }
        .duo-btn:hover {
            background-color: #2e8c5e !important;
        }
        .duo-progress {
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 1.5rem 0 0.5rem 0;
        }
        .duo-dot {
            width: 18px;
            height: 18px;
            border-radius: 50%;
            background: #e0e0e0;
            margin: 0 6px;
            display: inline-block;
            border: 2px solid #43b77a;
            transition: background 0.2s, border 0.2s;
        }
        .duo-dot.active {
            background: #43b77a;
            border: 2px solid #ffd740;
        }
        .duo-dot.completed {
            background: #ffd740;
            border: 2px solid #43b77a;
        }
        .sidebar-profile {
            background: linear-gradient(90deg, #e6f9ed 60%, #f6f9f6 100%);
            border-radius: 18px;
            padding: 1.2rem;
            margin-bottom: 1.5rem;
            text-align: center;
            box-shadow: 0 2px 8px rgba(67,183,122,0.08);
        }
        .sidebar-profile .duo-mascot {
            font-size: 3rem;
            margin-bottom: 0.5rem;
        }
        .sidebar-profile .username {
            font-size: 1.3rem;
            font-weight: bold;
            color: #43b77a;
            margin-bottom: 0.2rem;
        }
        .sidebar-profile .level {
            font-size: 1.1rem;
            color: #ffd740;
            font-weight: bold;
        }
        .stButton > button {
            background-color: #43b77a !important;
            color: #fff !important;
            border-radius: 12px !important;
            font-size: 1.1rem !important;
            font-weight: bold !important;
            padding: 0.7rem 2.2rem !important;
            margin: 0.5rem 0 !important;
            border: none !important;
            box-shadow: 0 2px 8px rgba(67,183,122,0.08);
            transition: background 0.2s;
        }
        .stButton > button:hover {
            background-color: #2e8c5e !important;
        }
        </style>
        """, unsafe_allow_html=True)

# --- END THEME CSS ---

# Add night_mode to session state
if 'night_mode' not in st.session_state:
    st.session_state.night_mode = False

# Inject theme CSS at the top of the app
inject_theme_css(st.session_state.night_mode)

# Initialize session state
if 'user_data' not in st.session_state:
    st.session_state.user_data = {
        'username': '',
        'level': 1,
        'xp': 0,
        'coins': 100,
        'streak': 0,
        'last_login': None,
        'completed_lessons': [],
        'badges': [],
        'correct_answers': 0,
        'total_questions': 0
    }

if 'current_lesson' not in st.session_state:
    st.session_state.current_lesson = None

if 'question_index' not in st.session_state:
    st.session_state.question_index = 0

if 'lesson_completed' not in st.session_state:
    st.session_state.lesson_completed = False

if 'show_answer' not in st.session_state:
    st.session_state.show_answer = False

if 'last_answer_correct' not in st.session_state:
    st.session_state.last_answer_correct = False

if 'perfect_lessons' not in st.session_state:
    st.session_state.perfect_lessons = []

# Add to session state initialization
if 'avatar' not in st.session_state:
    st.session_state.avatar = '🦖'
if 'account_type' not in st.session_state:
    st.session_state.account_type = 'Home'
if 'show_profile_edit' not in st.session_state:
    st.session_state.show_profile_edit = False
# In session state initialization, add avatar unlock tracking
if 'avatar_unlocked' not in st.session_state:
    st.session_state.avatar_unlocked = False

# Sample data for lessons and questions
LESSONS_DATA = {
    "Budgeting Basics": {
        "level": 1,
        "description": "Learn the fundamentals of creating and sticking to a budget",
        "content": """
        # Budgeting Basics 📊
        
        **What is a Budget?**
        A budget is a financial plan that helps you track your income and expenses. Think of it as a roadmap for your money that shows where your money comes from and where it goes.
        
        **Why Budget?**
        - ✅ **Control your spending** - Know exactly where your money goes
        - ✅ **Save for goals** - Build an emergency fund or save for big purchases
        - ✅ **Avoid debt** - Prevent overspending and credit card debt
        - ✅ **Plan for the future** - Save for retirement, education, or other long-term goals
        
        **The 50/30/20 Rule**
        This is a simple budgeting method that divides your after-tax income into three categories:
        
        🏠 **50% - Needs (Essential Expenses)**
        - Rent or mortgage payments
        - Food and groceries
        - Utilities (electricity, water, gas)
        - Basic transportation
        - Health insurance
        - Minimum debt payments
        
        🎮 **30% - Wants (Lifestyle Choices)**
        - Entertainment and dining out
        - Shopping for clothes and electronics
        - Hobbies and recreation
        - Travel and vacations
        - Streaming services and subscriptions
        
        💰 **20% - Savings & Debt Repayment**
        - Emergency fund contributions
        - Retirement savings
        - Extra debt payments
        - Investment contributions
        
        **Creating Your First Budget**
        1. **Track your income** - List all sources of money (salary, side jobs, etc.)
        2. **List all expenses** - Write down everything you spend money on
        3. **Categorize expenses** - Sort into needs, wants, and savings
        4. **Set spending limits** - Use the 50/30/20 rule as a guide
        5. **Monitor and adjust** - Review your budget regularly and make changes as needed
        
        **Pro Tips:**
        - Start small and be realistic about your spending habits
        - Use budgeting apps or spreadsheets to track your progress
        - Review your budget monthly and adjust as your situation changes
        - Don't forget to include irregular expenses like car repairs or medical bills
        """,
        "questions": [
            {
                "question": "What is the main purpose of creating a budget?",
                "options": ["To spend all your money", "To track income and expenses", "To avoid saving money", "To increase debt"],
                "correct": 1,
                "explanation": "A budget helps you track your income and expenses so you can make informed financial decisions and control your spending."
            },
            {
                "question": "According to the 50/30/20 rule, what percentage should go to needs?",
                "options": ["30%", "50%", "20%", "70%"],
                "correct": 1,
                "explanation": "The 50/30/20 rule allocates 50% of your after-tax income to essential needs like housing, food, and utilities."
            },
            {
                "question": "Which of the following is considered a 'need' in budgeting?",
                "options": ["Movie tickets", "Rent payment", "New video game", "Restaurant dinner"],
                "correct": 1,
                "explanation": "Rent payment is a need because shelter is essential for survival. Entertainment items like movies, games, and dining out are wants."
            },
            {
                "question": "What should you do first when creating a budget?",
                "options": ["Set spending limits", "Track your income", "Buy a budgeting app", "Cut all expenses"],
                "correct": 1,
                "explanation": "You must first know how much money you have coming in (your income) before you can plan how to spend it."
            },
            {
                "question": "Which category would a Netflix subscription fall into?",
                "options": ["Needs (50%)", "Wants (30%)", "Savings (20%)", "None of the above"],
                "correct": 1,
                "explanation": "Streaming services like Netflix are entertainment and fall into the wants category (30%) since they're not essential for survival."
            },
            {
                "question": "How often should you review and adjust your budget?",
                "options": ["Never", "Once a year", "Monthly", "Only when you run out of money"],
                "correct": 2,
                "explanation": "Reviewing your budget monthly helps you stay on track and make adjustments as your income or expenses change."
            }
        ]
    },
    "Saving Strategies": {
        "level": 2,
        "description": "Master different saving techniques and build your emergency fund",
        "content": """
        # Saving Strategies 🏦
        
        Saving money is crucial for financial security. Here are key strategies:
        
        ## Emergency Fund
        - Save 3-6 months of expenses
        - Keep in a separate savings account
        - Only use for true emergencies
        
        ## Pay Yourself First
        - Set aside money for savings before spending
        - Automate transfers to make it easier
        - Start with 10% of your income
        """,
        "questions": [
            {
                "question": "How much should you have in your emergency fund?",
                "options": ["1 month of expenses", "3-6 months of expenses", "1 year of expenses", "Whatever you can save"],
                "correct": 1,
                "explanation": "Financial experts recommend 3-6 months of expenses in your emergency fund."
            },
            {
                "question": "What does 'pay yourself first' mean?",
                "options": ["Spend money on yourself", "Save money before spending", "Take out a loan", "Invest in stocks"],
                "correct": 1,
                "explanation": "Pay yourself first means setting aside money for savings before spending on other things."
            },
            {
                "question": "Where is the best place to keep your emergency fund?",
                "options": ["In cash at home", "In a separate savings account", "In stocks", "In a checking account"],
                "correct": 1,
                "explanation": "Your emergency fund should be kept in a separate savings account so it's safe and easily accessible."
            },
            {
                "question": "What is a good first step to start saving?",
                "options": ["Wait until you have more money", "Set up automatic transfers to savings", "Spend less on groceries", "Open a credit card"],
                "correct": 1,
                "explanation": "Setting up automatic transfers to savings helps you save consistently and makes saving a habit."
            },
            {
                "question": "Which of the following is NOT a good reason to use your emergency fund?",
                "options": ["Car repair after an accident", "Buying a new TV", "Unexpected medical bill", "Job loss"],
                "correct": 1,
                "explanation": "Buying a new TV is not an emergency. Emergency funds are for true emergencies like job loss or medical bills."
            },
            {
                "question": "If you save 10% of your income each month, what is this strategy called?",
                "options": ["Pay yourself first", "Impulse saving", "Budgeting", "Windfall saving"],
                "correct": 0,
                "explanation": "Saving 10% of your income each month before spending is called 'pay yourself first.'"
            }
        ]
    },
    "Understanding Taxes": {
        "level": 3,
        "description": "Learn about different types of taxes and how they work",
        "content": """
        # Understanding Taxes 💰
        
        Taxes are mandatory payments to the government. Common types include:
        
        ## Income Tax
        - Based on your earnings
        - Progressive system (higher income = higher rate)
        - Withheld from paycheck
        
        ## Sales Tax
        - Added to purchases
        - Varies by state/city
        - Not included in listed prices
        """,
        "questions": [
            {
                "question": "What type of tax is based on your earnings?",
                "options": ["Sales tax", "Income tax", "Property tax", "Gas tax"],
                "correct": 1,
                "explanation": "Income tax is based on how much money you earn from work or investments."
            },
            {
                "question": "Which tax is added to purchases at stores?",
                "options": ["Income tax", "Property tax", "Sales tax", "Gas tax"],
                "correct": 2,
                "explanation": "Sales tax is added to most purchases and varies by location."
            },
            {
                "question": "What is a W-2 form used for?",
                "options": ["Reporting wages and taxes to employees", "Paying property taxes", "Filing for unemployment", "Applying for a loan"],
                "correct": 0,
                "explanation": "A W-2 form is used by employers to report wages and taxes to employees and the IRS."
            },
            {
                "question": "Which of the following is NOT a type of tax?",
                "options": ["Income tax", "Sales tax", "Vacation tax", "Property tax"],
                "correct": 2,
                "explanation": "There is no such thing as a 'vacation tax.' The others are real types of taxes."
            },
            {
                "question": "What does 'withholding' mean on your paycheck?",
                "options": ["Money taken out for taxes before you get paid", "A bonus payment", "A loan repayment", "A retirement contribution"],
                "correct": 0,
                "explanation": "Withholding is money taken out of your paycheck for taxes before you receive it."
            },
            {
                "question": "Why is it important to file your taxes on time?",
                "options": ["To avoid penalties and interest", "To get a bigger paycheck", "To increase your credit score", "To avoid jury duty"],
                "correct": 0,
                "explanation": "Filing your taxes on time helps you avoid penalties and interest charges from the government."
            }
        ]
    },
    "Credit & Debt Management": {
        "level": 4,
        "description": "Learn how to use credit wisely and manage debt effectively",
        "content": """
        # Credit & Debt Management 💳
        
        Understanding credit and debt is essential for financial health:
        
        ## Credit Score
        - Ranges from 300-850
        - Higher scores = better loan terms
        - Based on payment history, credit utilization, length of credit
        
        ## Types of Debt
        - **Good Debt**: Student loans, mortgages (builds wealth)
        - **Bad Debt**: Credit cards, payday loans (high interest)
        
        ## Debt Management
        - Pay more than minimum payments
        - Focus on high-interest debt first
        - Consider debt consolidation
        """,
        "questions": [
            {
                "question": "What is considered a good credit score range?",
                "options": ["300-500", "500-700", "700-850", "850-1000"],
                "correct": 2,
                "explanation": "A credit score of 700-850 is considered good to excellent."
            },
            {
                "question": "Which type of debt is generally considered 'good debt'?",
                "options": ["Credit card debt", "Student loans", "Payday loans", "Car title loans"],
                "correct": 1,
                "explanation": "Student loans are considered good debt because they invest in your future earning potential."
            },
            {
                "question": "What should you prioritize when paying off multiple debts?",
                "options": ["The largest debt", "The debt with highest interest rate", "The newest debt", "The smallest debt"],
                "correct": 1,
                "explanation": "Pay off high-interest debt first to minimize total interest paid."
            },
            {
                "question": "What is the main benefit of diversification?",
                "options": ["Higher returns", "Lower risk", "Faster growth", "Tax benefits"],
                "correct": 1,
                "explanation": "Diversification spreads risk across different investments, reducing overall risk."
            },
            {
                "question": "What is dollar-cost averaging?",
                "options": ["Investing a fixed amount regularly", "Buying only when prices are low", "Selling when prices are high", "Investing all money at once"],
                "correct": 0,
                "explanation": "Dollar-cost averaging means investing the same amount regularly, regardless of market conditions."
            },
            {
                "question": "What is a good credit utilization ratio?",
                "options": ["Under 30%", "Under 50%", "Under 70%", "Under 100%"],
                "correct": 0,
                "explanation": "Keep your credit utilization under 30% to maintain a good credit score."
            }
        ]
    },
    "Investing Fundamentals": {
        "level": 5,
        "description": "Start your investment journey with basic concepts and strategies",
        "content": """
        # Investing Fundamentals 📈
        
        Investing helps your money grow over time:
        
        ## Investment Basics
        - **Stocks**: Ownership in a company
        - **Bonds**: Lending money to companies/governments
        - **Mutual Funds**: Pooled investments managed by professionals
        - **ETFs**: Exchange-traded funds, similar to mutual funds
        
        ## Risk vs. Return
        - Higher potential returns = higher risk
        - Diversification reduces risk
        - Time horizon affects investment choices
        
        ## Investment Strategies
        - **Dollar-cost averaging**: Invest regularly regardless of market
        - **Buy and hold**: Long-term investment approach
        - **Diversification**: Don't put all eggs in one basket
        """,
        "questions": [
            {
                "question": "What does buying a stock mean?",
                "options": ["Lending money to a company", "Owning a piece of a company", "Borrowing from a company", "Selling to a company"],
                "correct": 1,
                "explanation": "Buying a stock means you own a small piece (share) of that company."
            },
            {
                "question": "What is the main benefit of diversification?",
                "options": ["Higher returns", "Lower risk", "Faster growth", "Tax benefits"],
                "correct": 1,
                "explanation": "Diversification spreads risk across different investments, reducing overall risk."
            },
            {
                "question": "What is dollar-cost averaging?",
                "options": ["Investing a fixed amount regularly", "Buying only when prices are low", "Selling when prices are high", "Investing all money at once"],
                "correct": 0,
                "explanation": "Dollar-cost averaging means investing the same amount regularly, regardless of market conditions."
            },
            {
                "question": "What is a good credit utilization ratio?",
                "options": ["Under 30%", "Under 50%", "Under 70%", "Under 100%"],
                "correct": 0,
                "explanation": "Keep your credit utilization under 30% to maintain a good credit score."
            },
            {
                "question": "What is a good credit utilization ratio?",
                "options": ["Under 30%", "Under 50%", "Under 70%", "Under 100%"],
                "correct": 0,
                "explanation": "Keep your credit utilization under 30% to maintain a good credit score."
            },
            {
                "question": "What is a good credit utilization ratio?",
                "options": ["Under 30%", "Under 50%", "Under 70%", "Under 100%"],
                "correct": 0,
                "explanation": "Keep your credit utilization under 30% to maintain a good credit score."
            }
        ]
    },
    "Insurance Basics": {
        "level": 6,
        "description": "Understand different types of insurance and why you need them",
        "content": """
        # Insurance Basics 🛡️
        
        Insurance protects you from financial losses:
        
        ## Types of Insurance
        - **Health Insurance**: Covers medical expenses
        - **Auto Insurance**: Protects against car accidents
        - **Renters/Homeowners**: Protects your belongings and property
        - **Life Insurance**: Provides for family if you pass away
        
        ## Insurance Terms
        - **Premium**: Amount you pay for coverage
        - **Deductible**: Amount you pay before insurance kicks in
        - **Coverage**: What the insurance pays for
        - **Policy**: Your insurance contract
        
        ## Choosing Insurance
        - Compare multiple quotes
        - Understand what's covered
        - Consider your specific needs
        - Don't just choose the cheapest option
        """,
        "questions": [
            {
                "question": "What is a deductible in insurance?",
                "options": ["The monthly payment", "Amount you pay before insurance covers", "The total coverage amount", "The insurance company's profit"],
                "correct": 1,
                "explanation": "A deductible is the amount you must pay out of pocket before your insurance starts covering costs."
            },
            {
                "question": "Which type of insurance is most important for young adults?",
                "options": ["Life insurance", "Health insurance", "Pet insurance", "Travel insurance"],
                "correct": 1,
                "explanation": "Health insurance is crucial for young adults to protect against high medical costs."
            },
            {
                "question": "What should you do when choosing insurance?",
                "options": ["Always choose the cheapest option", "Compare multiple quotes", "Only buy what your friends have", "Skip insurance to save money"],
                "correct": 1,
                "explanation": "Always compare multiple quotes to find the best coverage for your needs and budget."
            },
            {
                "question": "What is a deductible in insurance?",
                "options": ["The monthly payment", "Amount you pay before insurance covers", "The total coverage amount", "The insurance company's profit"],
                "correct": 1,
                "explanation": "A deductible is the amount you must pay out of pocket before your insurance starts covering costs."
            },
            {
                "question": "Which type of insurance is most important for young adults?",
                "options": ["Life insurance", "Health insurance", "Pet insurance", "Travel insurance"],
                "correct": 1,
                "explanation": "Health insurance is crucial for young adults to protect against high medical costs."
            },
            {
                "question": "What should you do when choosing insurance?",
                "options": ["Always choose the cheapest option", "Compare multiple quotes", "Only buy what your friends have", "Skip insurance to save money"],
                "correct": 1,
                "explanation": "Always compare multiple quotes to find the best coverage for your needs and budget."
            }
        ]
    },
    "Financial Goal Setting": {
        "level": 7,
        "description": "Learn how to set and achieve your financial goals",
        "content": """
        # Financial Goal Setting 🎯
        
        Setting clear financial goals helps you stay motivated:
        
        ## SMART Goals
        - **Specific**: Clear and well-defined
        - **Measurable**: Can track progress
        - **Achievable**: Realistic for your situation
        - **Relevant**: Important to you
        - **Time-bound**: Has a deadline
        
        ## Types of Goals
        - **Short-term**: Emergency fund, vacation (1-2 years)
        - **Medium-term**: Down payment, car (3-5 years)
        - **Long-term**: Retirement, college fund (10+ years)
        
        ## Goal Achievement
        - Break big goals into smaller steps
        - Automate savings for goals
        - Review and adjust regularly
        - Celebrate milestones
        """,
        "questions": [
            {
                "question": "What does the 'M' in SMART goals stand for?",
                "options": ["Money", "Measurable", "Monthly", "Maximum"],
                "correct": 1,
                "explanation": "The 'M' in SMART goals stands for Measurable - you should be able to track your progress."
            },
            {
                "question": "How long are short-term financial goals typically?",
                "options": ["1-2 years", "3-5 years", "5-10 years", "10+ years"],
                "correct": 0,
                "explanation": "Short-term financial goals are typically 1-2 years, like building an emergency fund."
            },
            {
                "question": "What should you do to achieve financial goals?",
                "options": ["Set them and forget them", "Break them into smaller steps", "Only focus on one goal", "Wait until you have more money"],
                "correct": 1,
                "explanation": "Breaking big goals into smaller, manageable steps makes them easier to achieve."
            },
            {
                "question": "What does the 'M' in SMART goals stand for?",
                "options": ["Money", "Measurable", "Monthly", "Maximum"],
                "correct": 1,
                "explanation": "The 'M' in SMART goals stands for Measurable - you should be able to track your progress."
            },
            {
                "question": "How long are short-term financial goals typically?",
                "options": ["1-2 years", "3-5 years", "5-10 years", "10+ years"],
                "correct": 0,
                "explanation": "Short-term financial goals are typically 1-2 years, like building an emergency fund."
            },
            {
                "question": "What should you do to achieve financial goals?",
                "options": ["Set them and forget them", "Break them into smaller steps", "Only focus on one goal", "Wait until you have more money"],
                "correct": 1,
                "explanation": "Breaking big goals into smaller, manageable steps makes them easier to achieve."
            }
        ]
    },
    "Banking & Checking Accounts": {
        "level": 8,
        "description": "Understand different types of bank accounts and banking services",
        "content": """
        # Banking & Checking Accounts 🏦
        
        Banking is the foundation of personal finance:
        
        ## Types of Bank Accounts
        - **Checking Account**: For daily transactions, debit cards
        - **Savings Account**: For saving money, earns interest
        - **Money Market Account**: Higher interest, limited transactions
        - **Certificate of Deposit (CD)**: Fixed term, higher interest
        
        ## Banking Services
        - **Online Banking**: 24/7 access to your accounts
        - **Mobile Banking**: Banking on your phone
        - **Direct Deposit**: Automatic paycheck deposits
        - **Bill Pay**: Automatic bill payments
        
        ## Choosing a Bank
        - Compare fees and interest rates
        - Check ATM network and locations
        - Read reviews and ask friends
        - Consider online-only banks
        """,
        "questions": [
            {
                "question": "Which type of account is best for daily spending?",
                "options": ["Savings account", "Checking account", "CD", "Money market account"],
                "correct": 1,
                "explanation": "Checking accounts are designed for daily transactions and come with debit cards."
            },
            {
                "question": "What is direct deposit?",
                "options": ["Automatic paycheck deposits", "Automatic bill payments", "ATM withdrawals", "Online transfers"],
                "correct": 0,
                "explanation": "Direct deposit automatically puts your paycheck into your bank account."
            },
            {
                "question": "What should you consider when choosing a bank?",
                "options": ["Only the interest rate", "Fees, locations, and services", "Just the bank name", "Only ATM locations"],
                "correct": 1,
                "explanation": "Consider fees, ATM network, locations, and services when choosing a bank."
            },
            {
                "question": "Which type of account is best for daily spending?",
                "options": ["Savings account", "Checking account", "CD", "Money market account"],
                "correct": 1,
                "explanation": "Checking accounts are designed for daily transactions and come with debit cards."
            },
            {
                "question": "What is direct deposit?",
                "options": ["Automatic paycheck deposits", "Automatic bill payments", "ATM withdrawals", "Online transfers"],
                "correct": 0,
                "explanation": "Direct deposit automatically puts your paycheck into your bank account."
            },
            {
                "question": "What should you consider when choosing a bank?",
                "options": ["Only the interest rate", "Fees, locations, and services", "Just the bank name", "Only ATM locations"],
                "correct": 1,
                "explanation": "Consider fees, ATM network, locations, and services when choosing a bank."
            }
        ]
    },
    "Credit Cards & Interest": {
        "level": 9,
        "description": "Learn how credit cards work and how to use them responsibly",
        "content": """
        # Credit Cards & Interest 💳
        
        Credit cards can be useful tools when used responsibly:
        
        ## How Credit Cards Work
        - **Credit Limit**: Maximum amount you can borrow
        - **Statement**: Monthly summary of charges
        - **Due Date**: When payment is due
        - **Minimum Payment**: Smallest amount you can pay
        
        ## Interest & Fees
        - **APR**: Annual Percentage Rate (interest rate)
        - **Grace Period**: Time to pay without interest
        - **Late Fees**: Penalties for missing payments
        - **Annual Fees**: Yearly cost to have the card
        
        ## Responsible Credit Card Use
        - Pay full balance each month
        - Never spend more than you can afford
        - Monitor your spending regularly
        - Keep credit utilization under 30%
        """,
        "questions": [
            {
                "question": "What is APR on a credit card?",
                "options": ["Annual Percentage Rate", "Average Payment Rate", "Account Payment Record", "Annual Purchase Rate"],
                "correct": 0,
                "explanation": "APR stands for Annual Percentage Rate, which is the interest rate on your credit card."
            },
            {
                "question": "What should you do to avoid credit card interest?",
                "options": ["Pay the minimum payment", "Pay the full balance each month", "Only use the card for emergencies", "Never use the card"],
                "correct": 1,
                "explanation": "Pay the full balance each month to avoid paying interest on your purchases."
            },
            {
                "question": "What is a good credit utilization ratio?",
                "options": ["Under 30%", "Under 50%", "Under 70%", "Under 100%"],
                "correct": 0,
                "explanation": "Keep your credit utilization under 30% to maintain a good credit score."
            },
            {
                "question": "What is APR on a credit card?",
                "options": ["Annual Percentage Rate", "Average Payment Rate", "Account Payment Record", "Annual Purchase Rate"],
                "correct": 0,
                "explanation": "APR stands for Annual Percentage Rate, which is the interest rate on your credit card."
            },
            {
                "question": "What should you do to avoid credit card interest?",
                "options": ["Pay the minimum payment", "Pay the full balance each month", "Only use the card for emergencies", "Never use the card"],
                "correct": 1,
                "explanation": "Pay the full balance each month to avoid paying interest on your purchases."
            },
            {
                "question": "What is a good credit utilization ratio?",
                "options": ["Under 30%", "Under 50%", "Under 70%", "Under 100%"],
                "correct": 0,
                "explanation": "Keep your credit utilization under 30% to maintain a good credit score."
            }
        ]
    },
    "Student Loans & Education Financing": {
        "level": 10,
        "description": "Understand student loans and how to finance education wisely",
        "content": """
        # Student Loans & Education Financing 🎓
        
        Education is an investment in your future:
        
        ## Types of Student Loans
        - **Federal Loans**: Government loans with lower interest rates
        - **Private Loans**: Bank loans with higher interest rates
        - **Subsidized**: Government pays interest while in school
        - **Unsubsidized**: You pay all interest
        
        ## Loan Terms
        - **Principal**: Original amount borrowed
        - **Interest**: Cost of borrowing money
        - **Grace Period**: Time after graduation before payments start
        - **Deferment**: Temporary pause in payments
        
        ## Smart Education Financing
        - Apply for scholarships and grants first
        - Use federal loans before private loans
        - Only borrow what you need
        - Understand your repayment options
        """,
        "questions": [
            {
                "question": "Which type of student loan typically has lower interest rates?",
                "options": ["Private loans", "Federal loans", "Credit card loans", "Personal loans"],
                "correct": 1,
                "explanation": "Federal student loans typically have lower interest rates than private loans."
            },
            {
                "question": "What is the grace period for student loans?",
                "options": ["Time to apply for loans", "Time after graduation before payments start", "Time to consolidate loans", "Time to refinance loans"],
                "correct": 1,
                "explanation": "The grace period is the time after graduation before you must start making payments."
            },
            {
                "question": "What should you do first when financing education?",
                "options": ["Apply for private loans", "Apply for scholarships and grants", "Use credit cards", "Take out personal loans"],
                "correct": 1,
                "explanation": "Apply for scholarships and grants first, as they don't need to be repaid."
            },
            {
                "question": "Which type of student loan typically has lower interest rates?",
                "options": ["Private loans", "Federal loans", "Credit card loans", "Personal loans"],
                "correct": 1,
                "explanation": "Federal student loans typically have lower interest rates than private loans."
            },
            {
                "question": "What is the grace period for student loans?",
                "options": ["Time to apply for loans", "Time after graduation before payments start", "Time to consolidate loans", "Time to refinance loans"],
                "correct": 1,
                "explanation": "The grace period is the time after graduation before you must start making payments."
            },
            {
                "question": "What should you do first when financing education?",
                "options": ["Apply for private loans", "Apply for scholarships and grants", "Use credit cards", "Take out personal loans"],
                "correct": 1,
                "explanation": "Apply for scholarships and grants first, as they don't need to be repaid."
            }
        ]
    },
    "Retirement Planning": {
        "level": 11,
        "description": "Start planning for retirement early with basic concepts",
        "content": """
        # Retirement Planning 🌅
        
        It's never too early to start planning for retirement:
        
        ## Retirement Accounts
        - **401(k)**: Employer-sponsored retirement plan
        - **IRA**: Individual Retirement Account
        - **Roth IRA**: Tax-free withdrawals in retirement
        - **Traditional IRA**: Tax-deductible contributions
        
        ## Compound Interest
        - Money grows exponentially over time
        - Start early to maximize growth
        - Small amounts add up over decades
        - Time is your biggest advantage
        
        ## Retirement Planning Steps
        - Start saving early, even small amounts
        - Take advantage of employer matches
        - Increase contributions over time
        - Diversify your investments
        """,
        "questions": [
            {
                "question": "What is a 401(k)?",
                "options": ["A type of savings account", "An employer-sponsored retirement plan", "A type of insurance", "A credit card"],
                "correct": 1,
                "explanation": "A 401(k) is an employer-sponsored retirement plan that allows you to save for retirement."
            },
            {
                "question": "What is the biggest advantage of starting retirement savings early?",
                "options": ["Compound interest", "Higher interest rates", "Lower taxes", "More investment options"],
                "correct": 0,
                "explanation": "Compound interest allows your money to grow exponentially over time, making early saving crucial."
            },
            {
                "question": "What should you do if your employer offers a 401(k) match?",
                "options": ["Ignore it", "Contribute at least enough to get the full match", "Only contribute the minimum", "Wait until you're older"],
                "correct": 1,
                "explanation": "Always contribute at least enough to get the full employer match - it's free money!"
            },
            {
                "question": "What is a 401(k)?",
                "options": ["A type of savings account", "An employer-sponsored retirement plan", "A type of insurance", "A credit card"],
                "correct": 1,
                "explanation": "A 401(k) is an employer-sponsored retirement plan that allows you to save for retirement."
            },
            {
                "question": "What is the biggest advantage of starting retirement savings early?",
                "options": ["Compound interest", "Higher interest rates", "Lower taxes", "More investment options"],
                "correct": 0,
                "explanation": "Compound interest allows your money to grow exponentially over time, making early saving crucial."
            },
            {
                "question": "What should you do if your employer offers a 401(k) match?",
                "options": ["Ignore it", "Contribute at least enough to get the full match", "Only contribute the minimum", "Wait until you're older"],
                "correct": 1,
                "explanation": "Always contribute at least enough to get the full employer match - it's free money!"
            }
        ]
    },
    "Real Estate & Mortgages": {
        "level": 12,
        "description": "Learn about buying property and understanding mortgages",
        "content": """
        # Real Estate & Mortgages 🏠
        
        Buying a home is often the biggest financial decision:
        
        ## Types of Mortgages
        - **Fixed-Rate**: Interest rate stays the same
        - **Adjustable-Rate**: Interest rate can change
        - **FHA**: Government-backed, lower down payment
        - **Conventional**: Traditional mortgage requirements
        
        ## Home Buying Costs
        - **Down Payment**: Initial payment (usually 3-20%)
        - **Closing Costs**: Fees for processing the loan
        - **Property Taxes**: Annual taxes on the property
        - **Homeowners Insurance**: Protects your property
        
        ## Smart Home Buying
        - Save for a substantial down payment
        - Get pre-approved for a mortgage
        - Don't buy more house than you can afford
        - Consider all ongoing costs
        """,
        "questions": [
            {
                "question": "What is a down payment?",
                "options": ["Monthly mortgage payment", "Initial payment when buying a home", "Property taxes", "Homeowners insurance"],
                "correct": 1,
                "explanation": "A down payment is the initial payment you make when buying a home, typically 3-20% of the purchase price."
            },
            {
                "question": "Which type of mortgage has a fixed interest rate?",
                "options": ["Adjustable-rate mortgage", "Fixed-rate mortgage", "FHA loan", "Conventional loan"],
                "correct": 1,
                "explanation": "A fixed-rate mortgage has an interest rate that stays the same throughout the loan term."
            },
            {
                "question": "What should you do before buying a home?",
                "options": ["Get pre-approved for a mortgage", "Skip the inspection", "Buy the most expensive house", "Ignore your budget"],
                "correct": 0,
                "explanation": "Get pre-approved for a mortgage to know how much you can afford and show sellers you're serious."
            },
            {
                "question": "What is a down payment?",
                "options": ["Monthly mortgage payment", "Initial payment when buying a home", "Property taxes", "Homeowners insurance"],
                "correct": 1,
                "explanation": "A down payment is the initial payment you make when buying a home, typically 3-20% of the purchase price."
            },
            {
                "question": "Which type of mortgage has a fixed interest rate?",
                "options": ["Adjustable-rate mortgage", "Fixed-rate mortgage", "FHA loan", "Conventional loan"],
                "correct": 1,
                "explanation": "A fixed-rate mortgage has an interest rate that stays the same throughout the loan term."
            },
            {
                "question": "What should you do before buying a home?",
                "options": ["Get pre-approved for a mortgage", "Skip the inspection", "Buy the most expensive house", "Ignore your budget"],
                "correct": 0,
                "explanation": "Get pre-approved for a mortgage to know how much you can afford and show sellers you're serious."
            }
        ]
    }
}

# Badges system
BADGES = {
    "First Steps": {"requirement": "Complete your first lesson", "icon": "🎯"},
    "Question Master": {"requirement": "Answer 10 questions correctly", "icon": "🧠"},
    "Streak Champion": {"requirement": "Maintain a 7-day streak", "icon": "🔥"},
    "Saver": {"requirement": "Earn 500 coins", "icon": "💰"},
    "Dedicated Learner": {"requirement": "Complete 5 lessons", "icon": "📚"},
    "Perfect Score": {"requirement": "Get 100% on a lesson", "icon": "⭐"},
    "Century Club": {"requirement": "Answer 100 questions correctly", "icon": "🏆"}
}

# Leaderboard data (simulated)
LEADERBOARD_DATA = [
    {"username": "FinanceWizard", "xp": 2500, "level": 5, "streak": 15},
    {"username": "MoneyMaster", "xp": 2100, "level": 4, "streak": 12},
    {"username": "BudgetPro", "xp": 1800, "level": 4, "streak": 8},
    {"username": "SavingsKing", "xp": 1500, "level": 3, "streak": 10},
    {"username": "TaxGuru", "xp": 1200, "level": 3, "streak": 6}
]

def check_streak():
    """Check and update user's daily streak"""
    today = datetime.date.today()
    if st.session_state.user_data['last_login'] is None:
        st.session_state.user_data['last_login'] = today.strftime('%Y-%m-%d')
        st.session_state.user_data['streak'] = 1
    else:
        last_login = datetime.datetime.strptime(st.session_state.user_data['last_login'], '%Y-%m-%d').date()
        if today == last_login:
            return  # Already logged in today
        elif today - last_login == datetime.timedelta(days=1):
            st.session_state.user_data['streak'] += 1
        else:
            st.session_state.user_data['streak'] = 1
        st.session_state.user_data['last_login'] = today.strftime('%Y-%m-%d')

def check_badges():
    """Check if user has earned new badges"""
    new_badges = []
    
    # First Steps
    if len(st.session_state.user_data['completed_lessons']) >= 1 and "First Steps" not in st.session_state.user_data['badges']:
        new_badges.append("First Steps")
    
    # Question Master
    if st.session_state.user_data['correct_answers'] >= 10 and "Question Master" not in st.session_state.user_data['badges']:
        new_badges.append("Question Master")
    
    # Streak Champion
    if st.session_state.user_data['streak'] >= 7 and "Streak Champion" not in st.session_state.user_data['badges']:
        new_badges.append("Streak Champion")
    
    # Saver
    if st.session_state.user_data['coins'] >= 500 and "Saver" not in st.session_state.user_data['badges']:
        new_badges.append("Saver")
    
    # Dedicated Learner
    if len(st.session_state.user_data['completed_lessons']) >= 5 and "Dedicated Learner" not in st.session_state.user_data['badges']:
        new_badges.append("Dedicated Learner")
    
    # Century Club
    if st.session_state.user_data['correct_answers'] >= 100 and "Century Club" not in st.session_state.user_data['badges']:
        new_badges.append("Century Club")
    
    for badge in new_badges:
        st.session_state.user_data['badges'].append(badge)
    
    return new_badges

# Utility function to recalculate level based on XP
def recalculate_level():
    st.session_state.user_data['level'] = 1 + (st.session_state.user_data['xp'] // 400)

def main():
    # Check streak on app load
    check_streak()
    
    # Sidebar for navigation and user info
    with st.sidebar:
        if not st.session_state.show_profile_edit:
            # Profile box with Streamlit 'Edit' button in top right, not bold
            st.markdown('''
            <style>
            .edit-profile-btn {
                position: absolute;
                top: 10px;
                right: 10px;
                z-index: 10;
            }
            .sidebar-profile { position: relative; }
            /* Make the Edit button match the Start Learning button */
            .stButton > button#profile-edit-btn {
                background-color: #43b77a !important;
                color: #fff !important;
                border-radius: 12px !important;
                font-size: 1.1rem !important;
                font-weight: bold !important;
                padding: 0.7rem 2.2rem !important;
                margin: 0.5rem 0 !important;
                border: none !important;
                box-shadow: 0 2px 8px rgba(67,183,122,0.08);
                transition: background 0.2s;
            }
            .stButton > button#profile-edit-btn:hover {
                background-color: #2e8c5e !important;
            }
            /* Make only the Edit button green */
            .stButton > button[data-testid="baseButton-secondary-profile-edit-btn"] {
                background-color: #43b77a !important;
                color: #fff !important;
                border-radius: 8px !important;
                border: none !important;
                font-size: 0.9rem !important;
                font-weight: normal !important;
                padding: 2px 14px !important;
                position: absolute !important;
                top: 10px !important;
                right: 10px !important;
                z-index: 10 !important;
            }
            .stButton > button[data-testid="baseButton-secondary-profile-edit-btn"]:hover {
                background-color: #2e8c5e !important;
            }
            </style>
            ''', unsafe_allow_html=True)
            st.markdown(f'''<div class="sidebar-profile" style="position:relative;">
                <span class="duo-mascot">{st.session_state.avatar}</span><br>
                <span class="username">{st.session_state.user_data['username'] if st.session_state.user_data['username'] else 'Guest'}</span><br>
                <span class="level">Level: {st.session_state.user_data['level']}</span><br>
                <span style="color:#888;font-size:0.95rem;">{st.session_state.account_type} Account</span>
            </div>''', unsafe_allow_html=True)
            # Absolutely position the Streamlit button for the edit action
            btn_placeholder = st.empty()
            btn_html = '<div class="edit-profile-btn" style="position:absolute;top:10px;right:10px;z-index:10;width:60px;"></div>'
            st.markdown(btn_html, unsafe_allow_html=True)
            if btn_placeholder.button("Edit", key="profile-edit-btn", help="Edit Profile"):
                st.session_state.show_profile_edit = True
        else:
            st.markdown('<div class="sidebar-profile">', unsafe_allow_html=True)
            st.markdown(f'<span class="duo-mascot">{st.session_state.avatar}</span>', unsafe_allow_html=True)
            new_name = st.text_input("Username", value=st.session_state.user_data['username'], key="profile_name_input")
            avatar_options = ['🦖', '🦁', '🐼', '🐧', '🐸', '🐻', '🐨', '🐰', '🦊', '🐶', '🐱']
            # Avatar select: only enabled if avatar_unlocked
            if st.session_state.avatar_unlocked:
                new_avatar = st.selectbox("Avatar", avatar_options, index=avatar_options.index(st.session_state.avatar) if st.session_state.avatar in avatar_options else 0, key="profile_avatar_select")
            else:
                st.selectbox("Avatar (buy 'Custom Avatar' in Rewards to unlock)", avatar_options, index=avatar_options.index(st.session_state.avatar) if st.session_state.avatar in avatar_options else 0, key="profile_avatar_select", disabled=True)
                new_avatar = st.session_state.avatar
                st.info("Buy 'Custom Avatar' in the Rewards shop to unlock more avatars!")
            new_type = st.selectbox("Account Type", ["Home", "Student", "Teacher"], index=["Home", "Student", "Teacher"].index(st.session_state.account_type), key="profile_type_select")
            night_mode_toggle = st.checkbox("Night Mode", value=st.session_state.night_mode, key="night_mode_toggle")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Save", key="profile_save_btn"):
                    st.session_state.user_data['username'] = new_name
                    st.session_state.avatar = new_avatar
                    st.session_state.account_type = new_type
                    st.session_state.night_mode = night_mode_toggle
                    st.session_state.show_profile_edit = False
                    st.rerun()
            with col2:
                if st.button("Cancel", key="profile_cancel_btn"):
                    st.session_state.show_profile_edit = False
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        
        # User profile section
        if st.session_state.user_data['username'] == '':
            username = st.text_input("Enter your username:")
            if st.button("Start Learning"):
                if username.strip():
                    st.session_state.user_data['username'] = username.strip()
                    st.rerun()
        else:
            st.success(f"Welcome, {st.session_state.user_data['username']}!")
            
            # User stats
            st.subheader("Your Stats")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Level", st.session_state.user_data['level'])
                st.metric("XP", st.session_state.user_data['xp'])
            with col2:
                st.metric("Coins", st.session_state.user_data['coins'])
                st.metric("Streak", st.session_state.user_data['streak'])
            
            # Streak counter
            st.markdown(f"""
            <div class="streak-counter">
                🔥 {st.session_state.user_data['streak']} Day Streak!
            </div>
            """, unsafe_allow_html=True)
            
            # Badges
            if st.session_state.user_data['badges']:
                st.subheader("Your Badges")
                for badge in st.session_state.user_data['badges']:
                    st.markdown(f'<span class="badge">{BADGES[badge]["icon"]} {badge}</span>', unsafe_allow_html=True)
        
        # Navigation
        st.subheader("Navigation")
        st.markdown("**Choose a page:**")
        page = st.selectbox("", ["🏠 Dashboard", "📚 Lessons", "🏆 Leaderboard", "🎁 Rewards", "👥 Friends"], label_visibility="collapsed")
        st.session_state.page = page
    
    # Main content area
    if page == "🏠 Dashboard":
        show_dashboard()
    elif page == "📚 Lessons":
        show_lessons()
    elif page == "🏆 Leaderboard":
        show_leaderboard()
    elif page == "🎁 Rewards":
        show_rewards()
    elif page == "👥 Friends":
        show_friends()

def show_dashboard():
    """Display the main dashboard"""
    st.markdown('<h1 class="main-header"><span class="duo-mascot">🦖</span> Finasaur - Learn Finance the Fun Way</h1>', unsafe_allow_html=True)
    
    if st.session_state.user_data['username'] == '':
        st.info("Please enter your username in the sidebar to start learning!")
        return
    
    # Welcome message
    st.success(f"Welcome back, {st.session_state.user_data['username']}! Ready to learn about finance?")
    
    # Progress overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Lessons Completed", len(st.session_state.user_data['completed_lessons']))
    
    with col2:
        accuracy = (st.session_state.user_data['correct_answers'] / max(st.session_state.user_data['total_questions'], 1)) * 100
        st.metric("Accuracy", f"{accuracy:.1f}%")
    
    with col3:
        st.metric("Questions Answered", st.session_state.user_data['total_questions'])
    
    # Recent activity
    st.subheader("Recent Activity")
    if st.session_state.user_data['completed_lessons']:
        for lesson in st.session_state.user_data['completed_lessons'][-3:]:
            st.info(f"✅ Completed: {lesson}")
    else:
        st.info("No lessons completed yet. Start your first lesson!")
    
    # Daily challenge
    st.subheader("Daily Challenge")
    st.info("Complete a lesson today to maintain your streak and earn bonus XP!")

def show_lessons():
    """Display available lessons"""
    # Check if a lesson is currently active
    if st.session_state.current_lesson:
        show_current_lesson()
        return
    
    st.title("📚 Available Lessons")
    
    if st.session_state.user_data['username'] == '':
        st.warning("Please enter your username first!")
        return
    
    # Show all lessons but indicate which ones are locked
    lesson_names = list(LESSONS_DATA.keys())
    for idx, (lesson_name, lesson_data) in enumerate(LESSONS_DATA.items()):
        with st.container():
            # Unlock logic: first lesson always available, others only if previous is in perfect_lessons
            is_available = False
            if idx == 0:
                is_available = True
            else:
                prev_lesson = lesson_names[idx-1]
                if prev_lesson in st.session_state.perfect_lessons:
                    is_available = True
            # Allow replay if completed
            can_replay = lesson_name in st.session_state.user_data['completed_lessons']
            if is_available or can_replay:
                st.markdown(f"""
                <div class="lesson-card">
                    <h3 style="color: #000000;">{lesson_name}</h3>
                    <p style="color: #000000;"><strong>Level {lesson_data['level']}</strong> - {lesson_data['description']}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="lesson-card" style="opacity: 0.6; background-color: #e0e0e0;">
                    <h3 style="color: #666666;">{lesson_name} 🔒</h3>
                    <p style="color: #666666;"><strong>Level {lesson_data['level']}</strong> - {lesson_data['description']}</p>
                    <p style="color: #666666;"><em>Complete the previous lesson with 100% accuracy to unlock</em></p>
                </div>
                """, unsafe_allow_html=True)
            
            col1, col2 = st.columns([3, 1])
            with col1:
                if lesson_name in st.session_state.user_data['completed_lessons']:
                    st.success("✅ Completed!")
                    # Allow replay
                    if st.button(f"Replay {lesson_name}", key=f"replay_{lesson_name}"):
                        st.session_state.current_lesson = lesson_name
                        st.session_state.question_index = 0
                        st.session_state.lesson_completed = False
                        st.session_state.show_answer = False
                        st.session_state.selected_answer = None
                        st.rerun()
                elif is_available:
                    if st.button(f"Start {lesson_name}", key=f"start_{lesson_name}"):
                        st.session_state.current_lesson = lesson_name
                        st.session_state.question_index = 0
                        st.session_state.lesson_completed = False
                        st.session_state.show_answer = False
                        st.session_state.selected_answer = None
                        st.rerun()
                else:
                    st.info(f"🔒 Requires perfect completion of previous lesson")
            with col2:
                st.write(f"Questions: {len(lesson_data['questions'])}")

def show_current_lesson():
    """Display the current lesson content and questions"""
    lesson_name = st.session_state.current_lesson
    lesson_data = LESSONS_DATA[lesson_name]
    # Add a green, functional back button
    back_btn_style = "background:#43b77a;color:#fff;font-weight:bold;font-size:1.1rem;padding:0.5rem 1.5rem;border-radius:10px;border:none;cursor:pointer;"
    back_btn_html = f'<style>div[data-testid="stButton"] button{{{back_btn_style}}}</style>'
    st.markdown(back_btn_html, unsafe_allow_html=True)
    if st.button("\u2190 Back to Lessons", key="back_to_lessons", help="Return to lesson list"):
        st.session_state.current_lesson = None
        st.session_state.question_index = 0
        st.session_state.lesson_completed = False
        st.session_state.show_answer = False
        st.session_state.selected_answer = None
        st.session_state.last_answer_correct = False
        st.rerun()
    st.title(f"📚 {lesson_name}")
    st.markdown(f"**Level {lesson_data['level']}** - {lesson_data['description']}")
    # Progress dots for quiz
    if st.session_state.question_index > 0:
        total_q = len(lesson_data['questions'])
        st.markdown('<div class="duo-progress">' + ''.join([
            f'<span class="duo-dot {"active" if i+1==st.session_state.question_index else ("completed" if i+1<st.session_state.question_index else "")}"></span>'
            for i in range(total_q)
        ]) + '</div>', unsafe_allow_html=True)
    # Show lesson content
    if st.session_state.question_index == 0:
        st.markdown("---")
        st.subheader("📖 Lesson Content")
        st.markdown(lesson_data['content'])
        st.markdown("---")
        st.subheader("🎯 Ready to Test Your Knowledge?")
        st.info("Take your time to read through the lesson content above. When you're ready, click the button below to start the quiz!")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Start Quiz", key="start_quiz_btn"):
                st.session_state.question_index = 1
                st.session_state.show_answer = False
                st.session_state.selected_answer = None
                st.rerun()
    elif st.session_state.question_index <= len(lesson_data['questions']):
        question_data = lesson_data['questions'][st.session_state.question_index - 1]
        st.markdown("---")
        st.subheader(f"Question {st.session_state.question_index} of {len(lesson_data['questions'])}")
        st.markdown(f"""
        <div class="question-card">
            <h3 style="color: #000000; margin-bottom: 15px;">{question_data['question']}</h3>
        </div>
        """, unsafe_allow_html=True)
        st.subheader("Select your answer:")
        radio_key = f"q{st.session_state.question_index}_radio"
        selected_answer = st.radio("Choose your answer:", question_data['options'], key=radio_key)
        if 'selected_answer' not in st.session_state or st.session_state.selected_answer is None:
            st.session_state.selected_answer = None
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Submit Answer", key=f"submit_{st.session_state.question_index}") and not st.session_state.show_answer:
                st.session_state.selected_answer = selected_answer
                correct_answer = question_data['options'][question_data['correct']]
                st.session_state.last_answer_correct = (selected_answer == correct_answer)
                st.session_state.show_answer = True
                st.session_state.user_data['total_questions'] += 1
                if st.session_state.last_answer_correct:
                    st.session_state.user_data['correct_answers'] += 1
                    st.session_state.user_data['xp'] += 20
                    st.session_state.user_data['coins'] += 10
                    recalculate_level()
                new_badges = check_badges()
                if new_badges:
                    st.balloons()
                    st.success(f"🎉 New badge earned: {', '.join(new_badges)}")
                st.rerun()
        if st.session_state.show_answer:
            correct_answer = question_data['options'][question_data['correct']]
            if st.session_state.last_answer_correct:
                st.success("✅ Correct!")
                st.markdown(f"""
                <div style="background-color: #d4edda; border: 1px solid #c3e6cb; border-radius: 8px; padding: 15px; margin: 15px 0;">
                    <h4 style="color: #155724; margin: 0;">Explanation:</h4>
                    <p style="color: #155724; margin: 10px 0 0 0;">{question_data['explanation']}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error(f"❌ Incorrect. The correct answer is: {correct_answer}")
                st.markdown(f"""
                <div style="background-color: #f8d7da; border: 1px solid #f5c6cb; border-radius: 8px; padding: 15px; margin: 15px 0;">
                    <h4 style="color: #721c24; margin: 0;">Explanation:</h4>
                    <p style="color: #721c24; margin: 10px 0 0 0;">{question_data['explanation']}</p>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("---")
            if st.session_state.question_index < len(lesson_data['questions']):
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if st.button("Next Question", key=f"next_{st.session_state.question_index}"):
                        st.session_state.question_index += 1
                        st.session_state.show_answer = False
                        st.session_state.selected_answer = None
                        st.rerun()
            else:
                st.session_state.lesson_completed = True
                st.session_state.user_data['completed_lessons'].append(lesson_name)
                st.session_state.user_data['xp'] += 100  # Bonus for completing lesson
                st.session_state.user_data['coins'] += 50
                recalculate_level()
                num_questions = len(lesson_data['questions'])
                correct_in_lesson = 0
                if st.session_state.user_data['correct_answers'] >= num_questions and st.session_state.user_data['total_questions'] >= num_questions:
                    if lesson_name not in st.session_state.perfect_lessons:
                        st.session_state.perfect_lessons.append(lesson_name)
                if st.session_state.user_data['correct_answers'] == len(lesson_data['questions']):
                    if "Perfect Score" not in st.session_state.user_data['badges']:
                        st.session_state.user_data['badges'].append("Perfect Score")
                        st.success("🎉 Perfect Score! You earned the Perfect Score badge!")
                st.success("🎉 Lesson completed! Great job!")
                st.metric("XP Earned", "+100")
                st.metric("Coins Earned", "+50")
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if st.button("Continue to Next Lesson", key="continue_next_lesson"):
                        st.session_state.current_lesson = None
                        st.session_state.question_index = 0
                        st.session_state.lesson_completed = False
                        st.session_state.show_answer = False
                        st.session_state.selected_answer = None
                        st.rerun()

def show_leaderboard():
    """Display the leaderboard"""
    st.title("🏆 Leaderboard")

    leaderboard_type = st.radio("Leaderboard Type", ["Worldwide Leaderboard", "Friends Leaderboard"], horizontal=True)

    if leaderboard_type == "Worldwide Leaderboard":
        # Add current user to leaderboard
        leaderboard = LEADERBOARD_DATA.copy()
        if st.session_state.user_data['username']:
            leaderboard.append({
                "username": st.session_state.user_data['username'],
                "xp": st.session_state.user_data['xp'],
                "level": st.session_state.user_data['level'],
                "streak": st.session_state.user_data['streak']
            })
        # Sort by XP
        leaderboard.sort(key=lambda x: x['xp'], reverse=True)
        # Create DataFrame for display
        df = pd.DataFrame(leaderboard)
        # Highlight current user
        def highlight_user(row):
            if row['username'] == st.session_state.user_data['username']:
                return ['background-color: yellow'] * len(row)
            return [''] * len(row)
        st.dataframe(df.style.apply(highlight_user, axis=1), use_container_width=True)
    else:
        # Friends leaderboard (user + Andy, Brian, Kaan, Elisa)
        friends = [
            {"username": "Andy", "xp": 1200, "level": 3, "streak": 5},
            {"username": "Brian", "xp": 950, "level": 2, "streak": 3},
            {"username": "Kaan", "xp": 800, "level": 2, "streak": 2},
            {"username": "Elisa", "xp": 700, "level": 1, "streak": 1}
        ]
        if st.session_state.user_data['username']:
            friends.append({
                "username": st.session_state.user_data['username'],
                "xp": st.session_state.user_data['xp'],
                "level": st.session_state.user_data['level'],
                "streak": st.session_state.user_data['streak']
            })
        # Sort by XP
        friends.sort(key=lambda x: x['xp'], reverse=True)
        df = pd.DataFrame(friends)
        def highlight_user(row):
            if row['username'] == st.session_state.user_data['username']:
                return ['background-color: yellow'] * len(row)
            return [''] * len(row)
        st.dataframe(df.style.apply(highlight_user, axis=1), use_container_width=True)

def show_rewards():
    """Display rewards and shop"""
    st.title("🎁 Rewards & Shop")
    
    if st.session_state.user_data['username'] == '':
        st.warning("Please enter your username first!")
        return
    
    # Available badges
    st.subheader("🏆 Available Badges")
    st.markdown("Complete challenges to earn these badges:")
    
    # Create a grid layout for badges
    badge_cols = st.columns(2)
    for i, (badge_name, badge_info) in enumerate(BADGES.items()):
        earned = badge_name in st.session_state.user_data['badges']
        with badge_cols[i % 2]:
            if earned:
                st.markdown(f"""
                <div style="background-color: #d4edda; border: 2px solid #28a745; border-radius: 10px; padding: 15px; margin: 10px 0;">
                    <h4 style="color: #000000; margin: 0;">{badge_info['icon']} {badge_name}</h4>
                    <p style="color: #000000; margin: 5px 0;">{badge_info['requirement']}</p>
                    <p style="color: #28a745; font-weight: bold; margin: 0;">✅ EARNED!</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background-color: #f8f9fa; border: 2px solid #6c757d; border-radius: 10px; padding: 15px; margin: 10px 0;">
                    <h4 style="color: #6c757d; margin: 0;">{badge_info['icon']} {badge_name}</h4>
                    <p style="color: #6c757d; margin: 5px 0;">{badge_info['requirement']}</p>
                    <p style="color: #6c757d; font-weight: bold; margin: 0;">🔒 LOCKED</p>
                </div>
                """, unsafe_allow_html=True)
    
    # Shop items (cosmetic)
    st.subheader("🎨 Shop")
    st.info(f"💰 You have **{st.session_state.user_data['coins']} coins** to spend!")
    
    shop_items = {
        "Custom Avatar": {"price": 200, "description": "Unlock a custom avatar for your profile", "icon": "👤"},
        "Profile Theme": {"price": 150, "description": "Change your profile theme and colors", "icon": "🎨"},
        "Special Effects": {"price": 300, "description": "Add special effects to your profile", "icon": "✨"},
        "Exclusive Badge Frame": {"price": 500, "description": "Get an exclusive badge frame", "icon": "🏅"},
        "XP Booster": {"price": 400, "description": "Get 2x XP for 24 hours", "icon": "⚡"},
        "Streak Protector": {"price": 250, "description": "Protect your streak for one day", "icon": "🛡️"}
    }
    
    st.markdown("### Available Items:")
    
    for item_name, item_info in shop_items.items():
        st.markdown(f"""
        <div style="background-color: #ffffff; border: 1px solid #dee2e6; border-radius: 8px; padding: 15px; margin: 10px 0;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="flex: 1;">
                    <h4 style="color: #000000; margin: 0;">{item_info['icon']} {item_name}</h4>
                    <p style="color: #666666; margin: 5px 0;">{item_info['description']}</p>
                </div>
                <div style="text-align: right;">
                    <p style="color: #000000; font-weight: bold; margin: 0;">{item_info['price']} coins</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        with col1:
            pass  # Space for layout
        with col2:
            if item_name == "Custom Avatar" and st.session_state.avatar_unlocked:
                st.success("Unlocked!")
            elif st.session_state.user_data['coins'] >= item_info['price']:
                if st.button(f"Buy {item_name}", key=f"buy_{item_name}"):
                    st.session_state.user_data['coins'] -= item_info['price']
                    st.success(f"🎉 Purchased {item_name}!")
                    if item_name == "Custom Avatar":
                        st.session_state.avatar_unlocked = True
                    st.rerun()
            else:
                                 st.info(f"Need {item_info['price'] - st.session_state.user_data['coins']} more coins")

def show_friends():
    st.title("👥 Friends")
    # Friends system state
    if 'friends' not in st.session_state:
        st.session_state.friends = []
    if 'friend_requests_sent' not in st.session_state:
        st.session_state.friend_requests_sent = []
    if 'friend_requests_received' not in st.session_state:
        st.session_state.friend_requests_received = []

    with st.expander("Add a Friend", expanded=True):
        friend_username = st.text_input("Enter username to add as friend:", key="add_friend_input_main")
        if st.button("Send Friend Request", key="send_friend_request_btn_main"):
            if friend_username and friend_username != st.session_state.user_data['username']:
                if friend_username not in st.session_state.friend_requests_sent and friend_username not in st.session_state.friends:
                    st.session_state.friend_requests_sent.append(friend_username)
                    st.success(f"Friend request sent to {friend_username}!")
                else:
                    st.info("Already sent or already friends.")
            else:
                st.warning("Enter a valid username (not your own).")

    # Display current friends
    if st.session_state.friends:
        st.markdown("**Your Friends:**")
        for f in st.session_state.friends:
            st.markdown(f"- {f}")
    else:
        st.info("No friends yet. Add some!")

    # Display sent requests
    if st.session_state.friend_requests_sent:
        st.markdown("**Sent Friend Requests:**")
        for f in st.session_state.friend_requests_sent:
            st.markdown(f"- {f} (pending)")

    # Display received requests (simulate for demo)
    if st.session_state.friend_requests_received:
        st.markdown("**Received Friend Requests:**")
        for f in st.session_state.friend_requests_received:
            col1, col2 = st.columns([2,1])
            with col1:
                st.markdown(f"- {f}")
            with col2:
                if st.button(f"Accept {f}", key=f"accept_{f}_main"):
                    st.session_state.friends.append(f)
                    st.session_state.friend_requests_received.remove(f)
                    st.success(f"You are now friends with {f}!")
                if st.button(f"Decline {f}", key=f"decline_{f}_main"):
                    st.session_state.friend_requests_received.remove(f)
                    st.info(f"Declined friend request from {f}.")

if __name__ == "__main__":
    main()

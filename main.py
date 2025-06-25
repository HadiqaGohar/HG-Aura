import os
import asyncio
import requests
import streamlit as st
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool
from agents.run import RunConfig
from agents.extensions.models.litellm_model import LitellmModel

# 🔐 Load API Key
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    st.error("🔑 GEMINI_API_KEY environment variable is not set ❗")
    st.stop()

# 🌐 Setup Gemini
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    openai_client=external_client,
    model="gemini-2.0-flash",
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True,
)

@function_tool
def getWeather(city: str) -> str:
    """
    🌦️ Get the weather for a given city.
    """
    weather_api_key = "8e3aca2b91dc4342a1162608252604"
    try:
        result = requests.get(
            f"http://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={city}"
        )
        result.raise_for_status()
        data = result.json()
        return f"📍 Weather in {city}: {data['current']['temp_c']}°C 🌡️ with {data['current']['condition']['text']} ☁️"
    except requests.exceptions.RequestException as e:
        return f"❌ Sorry, I couldn't fetch the weather data due to a network error: {e}. Please try again later."
    except Exception as e:
        return f"❌ An unexpected error occurred while processing weather data: {e}. Please try again later."

# 🛠️ Tool setup
tools = [getWeather]

# 🎯 Streamlit UI Configuration
st.set_page_config(
    page_title=" HG Aura Weather Agent ☁️",
    page_icon="🌤️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- Custom CSS for the New Theme ---
st.markdown("""
    <style>
    /* Import Inter font for consistency */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    /* Overall App Styling */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); /* Dark blue gradient */
        color: #e0e0e0; /* Light gray text for readability */
        font-family: 'Inter', sans-serif;
        padding: 2rem;
    }

    /* Title Styling */
    h1 {
        color: #ffffff;
        font-weight: 700;
        text-align: center;
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }

    /* Markdown Text Styling */
    .stMarkdown p {
        color: #d1d5db; /* Light gray for better readability */
        text-align: center;
        font-size: 1.1rem;
        line-height: 1.6;
        margin-bottom: 2rem;
    }

    /* Text Input Styling */
    .stTextInput > label {
        color: #ffffff;
        font-weight: 600;
        font-size: 1rem;
        text-align: center;
        display: block;
    }
    .stTextInput > div > div > input {
        background-color: #2d3748; /* Darker input background */
        border: 1px solid #4b5563; /* Subtle border */
        border-radius: 8px;
        padding: 0.75rem 1.25rem;
        color: #ffffff;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    .stTextInput > div > div > input::placeholder {
        color: #9ca3af; /* Light gray placeholder */
    }
    .stTextInput > div > div > input:focus {
        border-color: #3b82f6; /* Blue accent on focus */
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.3);
    }

    /* Button Styling */
    .stButton > button {
        background: linear-gradient(90deg, #3b82f6 0%, #60a5fa 100%); /* Blue gradient */
        color: #ffffff;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1rem;
        border: none;
        transition: all 0.3s ease;
      
        margin-top: 1rem;
        width: 100%; /* Full-width button */
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.6);
    }

    /* Alert Styling */
    .stAlert {
        border-radius: 8px;
        padding: 1rem;
        margin-top: 1.5rem;
    }
    .stAlert.success {
        background-color: rgba(34, 197, 94, 0.15); /* Green tint */
        border-left: 5px solid #22c55e;
        color: #d1fae5; /* Light green text */
    }
    .stAlert.warning {
        background-color: rgba(234, 179, 8, 0.15); /* Yellow tint */
        border-left: 5px solid #e9b308;
        color: #fef9c3; /* Light yellow text */
    }
    .stAlert.error {
        background-color: rgba(239, 68, 68, 0.15); /* Red tint */
        border-left: 5px solid #ef4444;
        color: #fee2e2; /* Light red text */
    }

    /* Center Input and Button */
    .stTextInput, .stButton {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
        max-width: 500px; /* Limit width for better appearance */
        margin: 0 auto;
    }

    /* Spinner Styling */
    .stSpinner > div > div {
        border-color: #3b82f6 transparent transparent transparent !important;
    }

    /* Main Content Area Padding */
    .block-container {
        padding: 2rem 1rem;
    }

    /* Footer Styling */
    footer {
        visibility: hidden; /* Hide default Streamlit footer */
    }

    #custom-footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: rgba(0, 0, 0, 0.2); /* Slightly transparent dark background */
        backdrop-filter: blur(5px); /* Subtle frosted glass effect for footer */
        color: rgba(255, 255, 255, 0.7);
        text-align: center;
        padding: 1rem 0;
        font-size: 0.9rem;
        z-index: 1000; /* Ensure it stays on top */
        font-family: 'Inter', sans-serif;
    }

    #custom-footer a {
        color: #4FC3F7; /* Accent blue for links */
        text-decoration: none;
        transition: color 0.3s ease;
    }

    #custom-footer a:hover {
        color: #2196F3;
    }           

    /* AI-Powered Badge Styling */
    .ai-powered-badge {
        display: inline-flex; /* Use inline-flex to center content and allow width to shrink */
        align-items: center;
        justify-content: center; /* Center content horizontally */
        background-color: rgba(255, 255, 255, 0.15); /* Semi-transparent background */
        border: 1px solid rgba(255, 255, 255, 0.3); /* Subtle border */
        border-radius: 20px; /* Highly rounded corners */
        padding: 0.5rem 1.25rem; /* Padding */
        color: #FFFFFF; /* White text */
        font-size: 0.9rem;
        font-weight: 600;
        margin-bottom: 2rem; /* Space below the badge */
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2); /* Soft shadow */
    }

    .ai-powered-badge .sparkle-icon {
        font-size: 1.2em; /* Slightly larger icon */
        margin-right: 0.5rem; /* Space between icon and text */
        color: #FFD700; /* Gold color for sparkle */
    }

    /* Centering the badge within Streamlit's layout */
    .stMarkdown.st-emotion-cache-1r6c0d8.e1nzilvr0 p { /* Specific Streamlit paragraph class, may change */
        text-align: center;
    }
    .ai-powered-container {
        display: flex;
        justify-content: center;
        width: 100%;
        margin-bottom: 20px; /* Space between badge and title */
    }            
    </style>
    """, unsafe_allow_html=True)

# --- AI-Powered Badge Section ---
st.markdown(
    """
    <div class="ai-powered-container">
        <div class="ai-powered-badge">
            <span class="sparkle-icon">✨</span> AI-Powered Weather Agent
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# --- Streamlit Application Content ---
st.title("🌤️ HG Aura Weather Agent ")
st.markdown("Ask me about the current weather in any city, and I'll fetch the latest data for you! 🌦️")

user_input = st.text_input("Enter a city name:", placeholder="e.g., London, New York")
if st.button("Get Weather"):
    if not user_input.strip():
        st.warning("Please enter a valid city name.")
    else:
        async def run_agent():
            agent = Agent(
                name="🌤️ WeatherAgentsBot",
                instructions="I am Hadiqa Gohar's agent 🤖. You are a helpful weather bot that provides weather information 🌦️",
                tools=tools
            )
            result = await Runner.run(agent, input=f"What is the weather in {user_input}?", run_config=config)
            return result.final_output

        with st.spinner('Fetching weather data...'):
            response = asyncio.run(run_agent())

        if "❌" in response:
            st.error(response)
        elif "📍" in response:
            st.success(response)
        else:
            st.info(response)

# --- Custom Footer HTML ---
st.markdown(
    """
    <div id="custom-footer">
        Made with ❤️ by Hadiqa Gohar | Powered by Gemini
    </div>
    """,
    unsafe_allow_html=True
)            
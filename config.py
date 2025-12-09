import os
from dotenv import load_dotenv
import pandas as pd

# Load environment variables
load_dotenv()

# Try to get from Streamlit secrets first, then fall back to environment variables
try:
    import streamlit as st
    SUPABASE_URL = st.secrets.get("EXPO_PUBLIC_SUPABASE_URL", os.getenv("EXPO_PUBLIC_SUPABASE_URL"))
    SUPABASE_KEY = st.secrets.get("EXPO_PUBLIC_SUPABASE_ANON_KEY", os.getenv("EXPO_PUBLIC_SUPABASE_ANON_KEY"))
    DATABASE_URL = st.secrets.get("DATABASE_URL", os.getenv("DATABASE_URL"))
except:
    SUPABASE_URL = os.getenv("EXPO_PUBLIC_SUPABASE_URL")
    SUPABASE_KEY = os.getenv("EXPO_PUBLIC_SUPABASE_ANON_KEY")
    DATABASE_URL = os.getenv("DATABASE_URL")

# Lazy import supabase to avoid errors if not installed
supabase_client = None

def get_supabase_client():
    """
    Create and return a Supabase client instance
    """
    global supabase_client
    if supabase_client is not None:
        return supabase_client
        
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("Supabase URL and Key must be set in secrets or .env file")
    
    try:
        from supabase import create_client, Client
        supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
        return supabase_client
    except ImportError:
        raise ImportError("supabase package not installed")


def load_data_from_supabase(table_name: str = "mental_health_data"):
    """
    Load data from Supabase table using the Supabase client.
    Returns a list of dictionaries (or None on error).
    """
    try:
        supabase = get_supabase_client()
        response = supabase.table(table_name).select("*").execute()
        return response.data
    except Exception as e:
        print(f"Error loading data from Supabase REST client: {e}")
        return None


def load_data_from_postgres(table_name: str = "mental_health_data"):
    """
    Load data from a Postgres database given by `DATABASE_URL`.
    """
    db_url = DATABASE_URL
    if not db_url:
        print("DATABASE_URL not set in environment. Cannot load from Postgres.")
        return None

    try:
        from sqlalchemy import create_engine, text
        engine = create_engine(db_url)
        query = text("""
            SELECT 
                wa.stress_level,
                wa.anxiety_score,
                wa.happiness_score,
                wa.sleep_duration,
                wa.focus_score,
                u.gender,
                u.education_level,
                u.income_level,
                r.region_name as region,
                dls.digital_dependence_score,
                dls.productivity_score,
                al.hours_used as device_hours_per_day,
                al.phone_unlocks,
                d.device_type
            FROM users u
            JOIN wellness_assessments wa ON u.user_id = wa.user_id
            JOIN digital_lifestyle_scores dls ON wa.assessment_id = dls.assessment_id
            JOIN activity_logs al ON u.user_id = al.user_id AND wa.date = al.date
            JOIN devices d ON al.device_id = d.device_id
            JOIN regions r ON u.region_id = r.region_id
        """)
        with engine.connect() as conn:
            df = pd.read_sql_query(query, conn)
        return df.to_dict(orient="records")
    except Exception as e:
        print(f"Error loading data from Postgres: {e}")
        return None


def load_data(table_name: str = "mental_health_data", prefer_postgres: bool = True):
    """
    Unified loader: try Postgres first, otherwise fall back to Supabase REST client.
    """
    if prefer_postgres and DATABASE_URL:
        data = load_data_from_postgres(table_name)
        if data is not None:
            return data

    # fallback to Supabase REST
    return load_data_from_supabase(table_name)

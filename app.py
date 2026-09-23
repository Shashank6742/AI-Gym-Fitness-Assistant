import streamlit as st
from textwrap import dedent
import math
import threading
import time
import os
import re
from datetime import date, timedelta

import requests
import pandas as pd

from dotenv import load_dotenv
from groq import Groq
from supabase import create_client, Client

import cv2
import mediapipe as mp
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import av

# ============================================================
# VITALIQ AI — AI GYM & FITNESS ASSISTANT
# ============================================================

load_dotenv()

st.set_page_config(
    page_title="VitalIQ AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# HTML HELPER
# ============================================================

def html(content):
    content = dedent(content)
    content = "\n".join(
        line.strip()
        for line in content.splitlines()
        if line.strip()
    )
    st.markdown(content, unsafe_allow_html=True)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at 85% 5%, rgba(46,196,182,0.10), transparent 25%),
        radial-gradient(circle at 20% 90%, rgba(124,92,255,0.08), transparent 30%),
        #07111F;
    color: #F4F7FB;
}

.main .block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}

/* ================= SIDEBAR ================= */

[data-testid="stSidebar"] {
    background: #091523;
    border-right: 1px solid #17283B;
}

[data-testid="stSidebar"] * {
    color: #E7EEF7;
}

.brand-container {
    padding: 5px 8px 28px 8px;
}

.brand-name {
    font-size: 28px;
    font-weight: 850;
    letter-spacing: -1.5px;
    color: #F5F8FC;
}

.brand-name span {
    color: #2ED4C2;
}

.brand-subtitle {
    font-size: 9px;
    letter-spacing: 1.7px;
    color: #71859A;
    margin-top: 4px;
}

.side-section {
    color: #60758B;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin: 8px 8px 10px 8px;
}

.side-status {
    margin-top: 25px;
    padding: 16px;
    border-radius: 15px;
    background: linear-gradient(145deg, #102236, #0C1928);
    border: 1px solid #1B344D;
}

.side-status-title {
    font-size: 9px;
    color: #6F8297;
    letter-spacing: 1.2px;
    font-weight: 700;
}

.side-status-main {
    font-size: 19px;
    font-weight: 800;
    margin-top: 6px;
}

.side-status-text {
    font-size: 11px;
    color: #8294A8;
    margin-top: 5px;
}

/* ================= HEADER ================= */

.header-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 25px;
}

.eyebrow {
    color: #2ED4C2;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1.8px;
    text-transform: uppercase;
    margin-bottom: 7px;
}

.page-title {
    font-size: 38px;
    font-weight: 850;
    letter-spacing: -1.8px;
    line-height: 1.1;
}

.page-title span {
    color: #2ED4C2;
}

.page-description {
    color: #8496AA;
    font-size: 13px;
    margin-top: 9px;
}

.profile {
    display: flex;
    align-items: center;
    gap: 11px;
    background: #0D1B2B;
    border: 1px solid #1B3147;
    border-radius: 15px;
    padding: 9px 14px;
}

.profile-avatar {
    width: 37px;
    height: 37px;
    border-radius: 11px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #2ED4C2, #7C5CFF);
    font-weight: 800;
    color: white;
}

.profile-name {
    font-size: 13px;
    font-weight: 700;
}

.profile-role {
    color: #71859A;
    font-size: 10px;
    margin-top: 2px;
}

/* ================= HERO ================= */

.hero {
    position: relative;
    overflow: hidden;
    padding: 30px;
    border-radius: 23px;
    background: linear-gradient(
        115deg,
        #102A38 0%,
        #0D1F31 48%,
        #171936 100%
    );
    border: 1px solid #23475A;
    margin-bottom: 22px;
}

.hero:after {
    content: "";
    position: absolute;
    width: 250px;
    height: 250px;
    right: -80px;
    top: -110px;
    border-radius: 50%;
    background: rgba(46,212,194,0.09);
}

.hero-label {
    color: #2ED4C2;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1.7px;
}

.hero-title {
    font-size: 28px;
    font-weight: 850;
    margin-top: 8px;
}

.hero-text {
    color: #91A4B8;
    font-size: 13px;
    max-width: 700px;
    line-height: 1.6;
    margin-top: 8px;
}

.hero-chip {
    display: inline-block;
    margin-top: 17px;
    padding: 8px 13px;
    border-radius: 20px;
    background: rgba(46,212,194,0.10);
    border: 1px solid rgba(46,212,194,0.25);
    color: #7CE9DD;
    font-size: 10px;
    font-weight: 700;
}

/* ================= STAT CARDS ================= */

.stat-card {
    min-height: 145px;
    padding: 20px;
    border-radius: 19px;
    background: #0D1A29;
    border: 1px solid #1A2E43;
}

.stat-icon {
    font-size: 23px;
    margin-bottom: 12px;
}

.stat-label {
    color: #6F8297;
    font-size: 9px;
    font-weight: 750;
    letter-spacing: 1.1px;
}

.stat-value {
    font-size: 27px;
    font-weight: 850;
    margin-top: 6px;
}

.stat-note {
    color: #2ED4C2;
    font-size: 10px;
    font-weight: 650;
    margin-top: 6px;
}

/* ================= SECTION ================= */

.section-heading {
    display: flex;
    justify-content: space-between;
    align-items: end;
    margin: 30px 0 14px 0;
}

.section-title {
    font-size: 20px;
    font-weight: 800;
}

.section-subtitle {
    color: #687C91;
    font-size: 11px;
}

/* ================= FEATURE CARDS ================= */

.feature-card {
    min-height: 182px;
    padding: 21px;
    border-radius: 19px;
    background: #0D1A29;
    border: 1px solid #1A2E43;
    margin-bottom: 15px;
}

.feature-icon {
    width: 45px;
    height: 45px;
    border-radius: 13px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    background: #12283A;
    border: 1px solid #20465B;
    margin-bottom: 15px;
}

.feature-title {
    font-size: 16px;
    font-weight: 800;
    margin-bottom: 7px;
}

.feature-description {
    color: #7E91A5;
    font-size: 11px;
    line-height: 1.6;
}

/* ================= QUICK ACTIONS ================= */

.action-card {
    padding: 18px;
    border-radius: 16px;
    background: #0B1725;
    border: 1px solid #1A2D41;
    text-align: center;
}

.action-icon {
    font-size: 25px;
}

.action-title {
    font-size: 12px;
    font-weight: 750;
    margin-top: 7px;
}

.action-text {
    color: #687C91;
    font-size: 10px;
    margin-top: 3px;
}

/* ================= MOTIVATION ================= */

.motivation {
    margin-top: 12px;
    padding: 24px;
    border-radius: 20px;
    background: linear-gradient(135deg, #171A37, #101A2B);
    border: 1px solid #31355F;
}

.motivation-label {
    color: #A99BFF;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1.4px;
}

.motivation-text {
    font-size: 20px;
    font-weight: 800;
    margin-top: 7px;
}

.motivation-sub {
    color: #7C8EA2;
    font-size: 11px;
    margin-top: 6px;
}

/* ================= BUTTONS ================= */

.stButton > button {
    border-radius: 11px !important;
    border: 1px solid #24435A !important;
    background: #102235 !important;
    color: #EAF5F5 !important;
    font-weight: 700 !important;
}

.stButton > button:hover {
    border-color: #2ED4C2 !important;
    color: #7CE9DD !important;
}

/* ================= CHAT INPUT ================= */

/* Keep the AI Fitness Buddy input readable on the dark VITALIQ theme. */
[data-testid="stChatInput"] {
    background: #0B1928 !important;
    border: 1px solid #24435A !important;
    border-radius: 12px !important;
}

[data-testid="stChatInput"] textarea {
    color: #F4F7FB !important;
    -webkit-text-fill-color: #F4F7FB !important;
    background: #0B1928 !important;
    caret-color: #2ED4C2 !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #7E91A5 !important;
    -webkit-text-fill-color: #7E91A5 !important;
    opacity: 1 !important;
}

[data-testid="stChatInput"] button {
    color: #07111F !important;
    background: #2ED4C2 !important;
}

/* ================= RADIO ================= */

[data-testid="stSidebar"] .stRadio label {
    font-size: 12px;
}

/* ================= MOBILE ================= */

@media (max-width: 900px) {

    .page-title {
        font-size: 29px;
    }

    .profile {
        display: none;
    }

}


/* ============================================================
   VITALIQ AI — FINAL PROFESSIONAL UI POLISH
   ============================================================ */

:root {
    --vq-bg: #060D18;
    --vq-panel: #0B1524;
    --vq-panel-2: #0E1B2C;
    --vq-border: #1C3046;
    --vq-text: #F3F7FB;
    --vq-muted: #A8B7C8;
    --vq-soft: #71859B;
    --vq-cyan: #35E0CC;
    --vq-cyan-soft: rgba(53,224,204,.12);
    --vq-purple: #8B7CFF;
}

html, body, .stApp {
    font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif !important;
}

.stApp {
    background:
        radial-gradient(900px 500px at 88% -5%, rgba(53,224,204,.085), transparent 62%),
        radial-gradient(800px 500px at 5% 100%, rgba(139,124,255,.075), transparent 62%),
        linear-gradient(180deg, #060D18 0%, #07111E 100%) !important;
}

/* cleaner content width */
.main .block-container {
    max-width: 1500px !important;
    padding: 2.2rem 3rem 4rem !important;
}

/* ---------- sidebar ---------- */
[data-testid="stSidebar"] {
    background:
        linear-gradient(180deg, #091321 0%, #07101C 100%) !important;
    border-right: 1px solid #17283B !important;
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.2rem;
}

.brand-container {
    padding: 8px 10px 25px !important;
}

.brand-name {
    font-size: 30px !important;
    letter-spacing: -1.8px !important;
}

.brand-subtitle {
    color: #8EA1B5 !important;
}

.side-section {
    color: #73889D !important;
    margin: 6px 10px 9px !important;
}

/* Make navigation look like a real application menu. */
[data-testid="stSidebar"] .stRadio > div {
    gap: 6px !important;
}

[data-testid="stSidebar"] .stRadio label {
    position: relative !important;
    display: flex !important;
    align-items: center !important;
    min-height: 43px !important;
    padding: 0 12px !important;
    border-radius: 12px !important;
    border: 1px solid transparent !important;
    color: #AEBCCD !important;
    font-size: 12px !important;
    font-weight: 650 !important;
    transition: all .18s ease !important;
}

[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(53,224,204,.055) !important;
    border-color: #1A3448 !important;
    color: #EAF7F6 !important;
}

/* Hide native radio circles while retaining Streamlit accessibility. */
[data-testid="stSidebar"] .stRadio label > div:first-child {
    display: none !important;
}

[data-testid="stSidebar"] .stRadio label:has(input:checked) {
    background: linear-gradient(90deg, rgba(53,224,204,.13), rgba(53,224,204,.035)) !important;
    border-color: rgba(53,224,204,.25) !important;
    color: #E9FFFC !important;
    box-shadow: inset 3px 0 0 #35E0CC !important;
}

[data-testid="stSidebar"] .stRadio label:has(input:checked)::after {
    content: "›";
    margin-left: auto;
    color: #35E0CC;
    font-size: 18px;
    font-weight: 500;
}

/* ---------- headings ---------- */
.eyebrow {
    color: #35E0CC !important;
    letter-spacing: 2px !important;
    font-size: 10px !important;
}

.page-title {
    color: #F7FAFD !important;
    font-size: 42px !important;
    letter-spacing: -2px !important;
}

.page-title span {
    color: #35E0CC !important;
}

.page-description {
    color: #A8B7C8 !important;
    font-size: 13px !important;
    line-height: 1.65 !important;
}

/* ---------- cards ---------- */
.hero,
.stat-card,
.feature-card,
.action-card,
.motivation,
.profile,
.side-status {
    box-shadow: 0 12px 35px rgba(0,0,0,.14) !important;
}

.hero {
    background:
        radial-gradient(420px 220px at 92% 0%, rgba(53,224,204,.13), transparent 70%),
        linear-gradient(135deg, #102A3A 0%, #0C1D2E 55%, #151733 100%) !important;
    border: 1px solid #244A5D !important;
}

.hero-title {
    color: #F7FAFD !important;
}

.hero-text {
    color: #B5C2D0 !important;
}

.stat-card,
.feature-card {
    background: linear-gradient(145deg, #0D1A2A, #0A1523) !important;
    border-color: #1D3147 !important;
    transition: transform .18s ease, border-color .18s ease, box-shadow .18s ease !important;
}

.stat-card:hover,
.feature-card:hover,
.action-card:hover {
    transform: translateY(-2px);
    border-color: #2A5063 !important;
    box-shadow: 0 16px 40px rgba(0,0,0,.20) !important;
}

.stat-label,
.section-subtitle,
.feature-description,
.action-text,
.motivation-sub,
.profile-role,
.side-status-text {
    color: #9EAFBF !important;
}

.stat-value {
    color: #F5F9FC !important;
    font-size: 29px !important;
}

.section-title {
    color: #F2F6FA !important;
}

.action-card {
    background: #0A1726 !important;
    border-color: #1B3045 !important;
}

/* ---------- Streamlit metrics ---------- */
[data-testid="stMetric"] {
    background: linear-gradient(145deg, #0D1A2A, #0A1523) !important;
    border: 1px solid #1C3046 !important;
    border-radius: 16px !important;
    padding: 16px 18px !important;
    min-height: 105px !important;
    box-shadow: 0 10px 28px rgba(0,0,0,.12) !important;
}

[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] p {
    color: #A9B8C8 !important;
    font-size: 11px !important;
    font-weight: 650 !important;
}

[data-testid="stMetricValue"],
[data-testid="stMetricValue"] div {
    color: #F7FAFD !important;
    font-weight: 800 !important;
}

[data-testid="stMetricDelta"] {
    color: #35E0CC !important;
}

/* ---------- all normal Streamlit text ---------- */
.stMarkdown, .stMarkdown p, .stMarkdown li,
[data-testid="stCaptionContainer"] {
    color: #D5DEE8;
}

[data-testid="stCaptionContainer"] p {
    color: #9EAFBF !important;
}

/* ---------- inputs/selects ---------- */
div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div,
div[data-baseweb="textarea"] > div {
    background: #0B1726 !important;
    border-color: #254057 !important;
    color: #F4F8FB !important;
}

div[data-baseweb="input"] input,
div[data-baseweb="textarea"] textarea,
div[data-baseweb="select"] input {
    color: #F4F8FB !important;
    -webkit-text-fill-color: #F4F8FB !important;
    caret-color: #35E0CC !important;
}

div[data-baseweb="input"] input::placeholder,
div[data-baseweb="textarea"] textarea::placeholder {
    color: #8296AA !important;
    -webkit-text-fill-color: #8296AA !important;
    opacity: 1 !important;
}

label[data-testid="stWidgetLabel"] p {
    color: #C8D4DF !important;
    font-weight: 650 !important;
}

/* ---------- buttons ---------- */
.stButton > button {
    min-height: 42px !important;
    padding: 0 18px !important;
    border-radius: 11px !important;
    border: 1px solid #29465B !important;
    background: linear-gradient(180deg, #12263A, #0D1D2D) !important;
    color: #F2F8FA !important;
    font-weight: 750 !important;
    transition: all .18s ease !important;
}

.stButton > button:hover {
    border-color: #35E0CC !important;
    color: #9AFFF3 !important;
    box-shadow: 0 0 0 3px rgba(53,224,204,.08) !important;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #1D8F87, #2469A0) !important;
    border-color: #35E0CC !important;
    color: #FFFFFF !important;
}

/* ---------- alerts ---------- */
[data-testid="stAlert"] {
    background: #0C1A2A !important;
    border: 1px solid #254057 !important;
    color: #DDE7EF !important;
    border-radius: 13px !important;
}

/* ---------- dataframe ---------- */
[data-testid="stDataFrame"] {
    border: 1px solid #1C3046 !important;
    border-radius: 14px !important;
    overflow: hidden !important;
}

/* ---------- chat ---------- */
[data-testid="stChatMessage"] {
    background: #0B1726 !important;
    border: 1px solid #1B3045 !important;
    border-radius: 15px !important;
    margin-bottom: 10px !important;
}

[data-testid="stChatInput"] {
    background: #0B1726 !important;
    border: 1px solid #2A465D !important;
    border-radius: 14px !important;
    box-shadow: 0 10px 28px rgba(0,0,0,.18) !important;
}

[data-testid="stChatInput"] textarea {
    color: #F7FAFD !important;
    -webkit-text-fill-color: #F7FAFD !important;
}

/* ---------- remove accidental HTML-looking line breaks ---------- */
br {
    line-height: 1.2;
}

/* ---------- responsive ---------- */
@media (max-width: 900px) {
    .main .block-container {
        padding: 1.2rem 1rem 2.5rem !important;
    }
    .page-title {
        font-size: 30px !important;
        letter-spacing: -1.2px !important;
    }
    .hero {
        padding: 22px !important;
    }
}


/* ============================================================
   VITALIQ AI — FINAL CLEANUP PASS
   Focus: remove remaining Streamlit visual artifacts only.
   Functionality/layout structure intentionally unchanged.
   ============================================================ */

/* ---------- sidebar navigation: remove native radio markers ---------- */
[data-testid="stSidebar"] [role="radiogroup"] {
    gap: 5px !important;
}

[data-testid="stSidebar"] [role="radiogroup"] label {
    min-height: 40px !important;
    margin: 0 !important;
    padding: 0 11px !important;
}

[data-testid="stSidebar"] [role="radiogroup"] label > div:first-child,
[data-testid="stSidebar"] [role="radiogroup"] label > div:first-child > div:first-child,
[data-testid="stSidebar"] [role="radiogroup"] label input[type="radio"] {
    display: none !important;
    visibility: hidden !important;
    width: 0 !important;
    height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
}

[data-testid="stSidebar"] [role="radiogroup"] label > div:last-child {
    margin-left: 0 !important;
    width: 100% !important;
}

/* ---------- fixed chat area: remove the white Streamlit footer ---------- */
[data-testid="stBottom"],
[data-testid="stBottomBlockContainer"],
div[class*="stBottomBlockContainer"],
section[class*="stChatFloatingInputContainer"] {
    background: rgba(6, 13, 24, .96) !important;
    background-color: #060D18 !important;
    border-top: 1px solid #172B40 !important;
    box-shadow: 0 -10px 30px rgba(0,0,0,.18) !important;
}

section[class*="stChatFloatingInputContainer"] {
    padding: 10px 0 14px !important;
}

[data-testid="stChatInput"] {
    background: #0B1726 !important;
    background-color: #0B1726 !important;
    border: 1px solid #2A465D !important;
    border-radius: 14px !important;
    box-shadow: 0 8px 25px rgba(0,0,0,.24) !important;
}

[data-testid="stChatInput"] > div {
    background: #0B1726 !important;
    background-color: #0B1726 !important;
    border-radius: 14px !important;
}

[data-testid="stChatInput"] textarea {
    background: #0B1726 !important;
    background-color: #0B1726 !important;
    color: #F7FAFD !important;
    -webkit-text-fill-color: #F7FAFD !important;
}

[data-testid="stChatInput"] textarea:focus {
    outline: none !important;
    box-shadow: none !important;
}

[data-testid="stChatInput"] button {
    background: #35E0CC !important;
    color: #06131D !important;
    border-radius: 9px !important;
    border: 0 !important;
}

/* ---------- cleaner tables ---------- */
[data-testid="stDataFrame"] div[role="columnheader"] {
    background: #0D1B2B !important;
    color: #DCE8F1 !important;
}

[data-testid="stDataFrame"] div[role="gridcell"] {
    color: #CBD7E2 !important;
}

/* ---------- cleaner number/select controls ---------- */
div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div {
    min-height: 42px !important;
    border-radius: 9px !important;
}

/* ---------- keep headings visually consistent ---------- */
h1, h2, h3, h4 {
    color: #F3F7FB !important;
}

/* ---------- remove accidental excessive white space from Streamlit containers ---------- */
[data-testid="stVerticalBlockBorderWrapper"] {
    border-color: #1C3046 !important;
}

/* ---------- mobile footer ---------- */
@media (max-width: 900px) {
    section[class*="stChatFloatingInputContainer"] {
        padding-left: 8px !important;
        padding-right: 8px !important;
    }
}

</style>
""", unsafe_allow_html=True)



# ============================================================
# SUPABASE AUTHENTICATION & USER ACCOUNTS
# ============================================================

SUPABASE_URL = os.getenv("SUPABASE_URL", "").strip()
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "").strip()


@st.cache_resource
def get_supabase_client():
    if not SUPABASE_URL or not SUPABASE_KEY:
        return None
    return create_client(SUPABASE_URL, SUPABASE_KEY)


supabase = get_supabase_client()


def valid_email(email):
    return bool(re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email.strip()))


def _response_data(response):
    return getattr(response, "data", None) or []


def get_profile(user_id=None, email=None):
    if supabase is None or (not user_id and not email):
        return None
    try:
        query = supabase.table("profiles").select(
            "id, full_name, email, role, created_at, updated_at"
        )
        if user_id:
            query = query.eq("id", str(user_id))
        else:
            query = query.eq("email", str(email).strip().lower())
        response = query.limit(1).execute()
        rows = _response_data(response)
        return rows[0] if rows else None
    except Exception:
        return None


def ensure_profile(user):
    if supabase is None or not user:
        return None
    user_id = str(getattr(user, "id", "") or (user.get("id", "") if isinstance(user, dict) else ""))
    email = str(getattr(user, "email", "") or (user.get("email", "") if isinstance(user, dict) else "")).strip().lower()
    if not user_id or not email:
        return None
    profile = get_profile(user_id=user_id)
    if not profile:
        profile = get_profile(email=email)
    if profile:
        return profile
    metadata = getattr(user, "user_metadata", None)
    if metadata is None and isinstance(user, dict):
        metadata = user.get("user_metadata", {})
    metadata = metadata or {}
    full_name = (metadata.get("full_name") or metadata.get("name") or email.split("@")[0]).strip()
    try:
        response = supabase.table("profiles").insert({
            "id": user_id, "full_name": full_name[:120], "email": email, "role": "user"
        }).execute()
        rows = _response_data(response)
        return rows[0] if rows else (get_profile(user_id=user_id) or get_profile(email=email))
    except Exception:
        return get_profile(user_id=user_id) or get_profile(email=email)


def set_authenticated_user(user, profile=None):
    user_id = str(getattr(user, "id", "") or (user.get("id", "") if isinstance(user, dict) else ""))
    email = str(getattr(user, "email", "") or (user.get("email", "") if isinstance(user, dict) else "")).strip().lower()
    profile = profile or ensure_profile(user) or {}
    st.session_state.authenticated = True
    st.session_state.auth_user = user
    st.session_state.user_id = user_id
    st.session_state.user_name = profile.get("full_name") or email.split("@")[0] or "User"
    st.session_state.user_email = email
    st.session_state.user_role = profile.get("role") or "user"


def clear_auth_state():
    # Clear authentication AND all user-specific cached/session data.
    # This prevents data from a previous account appearing after sign-out.
    user_session_keys = [
        "authenticated", "auth_user", "user_id", "user_name", "user_email",
        "user_role", "auth_mode", "performance_history", "nutrition_profile",
        "habit_log", "habit_settings", "buddy_messages", "gym_location",
        "gym_location_label", "gym_results", "trainer_state"
    ]
    for key in user_session_keys:
        st.session_state.pop(key, None)


def sign_in_user(email, password):
    if supabase is None:
        return False, "Supabase is not configured. Check SUPABASE_URL and SUPABASE_KEY in your .env file."
    try:
        response = supabase.auth.sign_in_with_password({"email": email.strip().lower(), "password": password})
        user = getattr(response, "user", None)
        session = getattr(response, "session", None)
        if not user:
            return False, "Sign in failed. Please check your email and password."
        if not session:
            clear_auth_state()
            return False, "Please confirm your email address first, then sign in again."

        # Fetch the profile only after Supabase has established the auth session.
        # This ensures the user's RLS-protected role (including admin) is read
        # from public.profiles instead of falling back to the default "user".
        profile = get_profile(user_id=str(getattr(user, "id", "") or ""))
        if not profile:
            profile = get_profile(email=email.strip().lower())
        if not profile:
            profile = ensure_profile(user)

        # Final authoritative admin check. This avoids relying only on the
        # profile row returned by the client and uses the Supabase security
        # function that checks auth.uid() against the profiles table.
        is_admin = False
        try:
            admin_response = supabase.rpc("is_admin").execute()
            is_admin = bool(getattr(admin_response, "data", False))
        except Exception:
            is_admin = False

        if profile is None:
            profile = {}
        profile = dict(profile)
        if is_admin:
            profile["role"] = "admin"

        set_authenticated_user(user, profile)
        return True, "Signed in successfully."
    except Exception as exc:
        msg = str(exc).lower()
        if "email not confirmed" in msg:
            return False, "Please confirm your email address first, then sign in again."
        if "invalid login credentials" in msg:
            return False, "Incorrect email or password."
        return False, "Sign in failed. Please check your details and try again."


def register_user(full_name, email, password):
    if supabase is None:
        return False, "Supabase is not configured. Check SUPABASE_URL and SUPABASE_KEY in your .env file."
    try:
        response = supabase.auth.sign_up({
            "email": email.strip().lower(),
            "password": password,
            "options": {"data": {"full_name": full_name.strip()}}
        })
        user = getattr(response, "user", None)
        session = getattr(response, "session", None)
        if not user:
            return False, "Account could not be created. Please try again."
        if session:
            profile = ensure_profile(user)
            set_authenticated_user(user, profile)
            return True, "Account created successfully."
        return True, "Account created. Check your email to confirm the account, then sign in."
    except Exception as exc:
        msg = str(exc).lower()
        if "already registered" in msg or "already exists" in msg:
            return False, "An account with this email already exists."
        return False, "Registration failed. Please check your details and try again."


def logout_user():
    if supabase is not None:
        try:
            supabase.auth.sign_out()
        except Exception:
            pass
    clear_auth_state()


def render_auth_page():
    html("""
    <style>
    .auth-shell { max-width: 560px; margin: 5vh auto 0; }
    .auth-brand { text-align:center; margin-bottom:22px; }
    .auth-brand-name { font-size:42px; font-weight:900; letter-spacing:-2px; color:#F5F9FC; }
    .auth-brand-name span { color:#35E0CC; }
    .auth-tagline { color:#8FA3B7; font-size:11px; letter-spacing:2px; margin-top:4px; }
    .auth-card { background:linear-gradient(145deg,#0E1D2D,#091522); border:1px solid #24445A; border-radius:24px; padding:30px; box-shadow:0 20px 60px rgba(0,0,0,.25); }
    .auth-title { color:#F5F9FC; font-size:27px; font-weight:850; }
    .auth-text { color:#9EB0C1; font-size:12px; margin:7px 0 20px; line-height:1.6; }
    .auth-note { text-align:center; color:#70859A; font-size:10px; margin-top:14px; }
    </style>
    <div class="auth-shell"><div class="auth-brand"><div class="auth-brand-name">VITAL<span>IQ</span></div><div class="auth-tagline">INTELLIGENT FITNESS PLATFORM</div></div></div>
    """)
    _, left, right, _ = st.columns([0.25, 1, 1, 0.25])
    with left: sign_in = st.button("Sign In", use_container_width=True, type="primary")
    with right: sign_up = st.button("Create Account", use_container_width=True)
    if "auth_mode" not in st.session_state: st.session_state.auth_mode = "login"
    if sign_in: st.session_state.auth_mode = "login"; st.rerun()
    if sign_up: st.session_state.auth_mode = "register"; st.rerun()
    if st.session_state.auth_mode == "login":
        st.markdown("<div class='auth-card'>", unsafe_allow_html=True)
        st.markdown("<div class='auth-title'>Welcome back</div><div class='auth-text'>Sign in to continue to your personalized VITALIQ fitness workspace.</div>", unsafe_allow_html=True)
        email = st.text_input("Email", placeholder="you@example.com", key="login_email")
        password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password")
        if st.button("Sign In to VITALIQ", type="primary", use_container_width=True):
            if not valid_email(email): st.error("Enter a valid email address.")
            elif not password: st.error("Enter your password.")
            else:
                ok, message = sign_in_user(email, password)
                if ok: st.success(message); st.rerun()
                else: st.error(message)
        st.markdown("<div class='auth-note'>Authentication is securely handled by Supabase Auth.</div></div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='auth-card'>", unsafe_allow_html=True)
        st.markdown("<div class='auth-title'>Create your VITALIQ account</div><div class='auth-text'>Register once to keep your fitness workspace separate from other users.</div>", unsafe_allow_html=True)
        name = st.text_input("Full Name", placeholder="Your name", key="register_name")
        email = st.text_input("Email", placeholder="you@example.com", key="register_email")
        password = st.text_input("Password", type="password", placeholder="At least 8 characters", key="register_password")
        confirm = st.text_input("Confirm Password", type="password", placeholder="Re-enter your password", key="register_confirm")
        if st.button("Create VITALIQ Account", type="primary", use_container_width=True):
            if len(name.strip()) < 2: st.error("Enter your full name.")
            elif not valid_email(email): st.error("Enter a valid email address.")
            elif len(password) < 8: st.error("Password must be at least 8 characters.")
            elif password != confirm: st.error("Passwords do not match.")
            else:
                ok, message = register_user(name, email, password)
                if ok:
                    st.success(message)
                    if st.session_state.get("authenticated"): st.rerun()
                    st.session_state.auth_mode = "login"; st.rerun()
                else: st.error(message)
        st.markdown("<div class='auth-note'>Your fitness data is separated by your Supabase user account.</div></div>", unsafe_allow_html=True)


if supabase is None:
    st.error("VITALIQ Supabase connection is not configured. Add SUPABASE_URL and SUPABASE_KEY to your .env file, then restart Streamlit.")
    st.stop()
if "authenticated" not in st.session_state: st.session_state.authenticated = False
if not st.session_state.authenticated:
    render_auth_page()
    st.stop()


def save_workout_session(exercise, reps, form_score, joint_angle, duration_seconds, feedback):
    try:
        supabase.table("workout_sessions").insert({
            "user_id": st.session_state.user_id, "exercise": exercise, "reps": int(reps),
            "hold_seconds": int(reps) if exercise == "Plank" else 0, "form_score": float(form_score),
            "joint_angle": float(joint_angle) if joint_angle is not None else None,
            "duration_seconds": int(duration_seconds), "feedback": feedback
        }).execute()
        return True, "Workout session saved successfully."
    except Exception as exc:
        return False, f"Workout could not be saved: {type(exc).__name__}."


def load_user_workouts(limit=100):
    try:
        response = (supabase.table("workout_sessions").select("*").eq("user_id", st.session_state.user_id)
                    .order("created_at", desc=True).limit(limit).execute())
        return _response_data(response)
    except Exception:
        return []


def load_user_nutrition():
    try:
        response = (supabase.table("nutrition_profiles").select("*").eq("user_id", st.session_state.user_id)
                    .limit(1).execute())
        rows = _response_data(response)
        return rows[0] if rows else None
    except Exception:
        return None


def save_user_nutrition(profile):
    try:
        supabase.table("nutrition_profiles").upsert({
            "user_id": st.session_state.user_id, "age": int(profile["age"]), "sex": profile["sex"],
            "height_cm": float(profile["height"]), "weight_kg": float(profile["weight"]),
            "activity_level": profile["activity"], "goal": profile["goal"], "diet": profile["preference"],
            "bmi": float(profile["bmi"]), "bmr": float(profile["bmr"]),
            "calorie_target": float(profile["target"]), "protein_target": float(profile["protein"])
        }, on_conflict="user_id").execute()
        return True
    except Exception:
        return False


def load_user_habits():
    try:
        response = (supabase.table("habit_logs").select("*").eq("user_id", st.session_state.user_id)
                    .order("log_date", desc=False).limit(60).execute())
        result = {}
        for row in _response_data(response):
            result[str(row["log_date"])] = {"workout": bool(row.get("workout_completed", False)),
                                             "water": int(row.get("water_glasses", 0) or 0),
                                             "sleep": float(row.get("sleep_hours", 0) or 0),
                                             "notes": row.get("notes") or ""}
        return result
    except Exception:
        return {}


def save_habit_log(log_date, item):
    try:
        supabase.table("habit_logs").upsert({
            "user_id": st.session_state.user_id, "log_date": log_date,
            "workout_completed": bool(item["workout"]), "water_glasses": int(item["water"]),
            "sleep_hours": float(item["sleep"]), "notes": item.get("notes", "")
        }, on_conflict="user_id,log_date").execute()
        return True
    except Exception:
        return False


# ============================================================
# OPENSTREETMAP — GYM FINDER / RECOMMENDER
# ============================================================

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
OVERPASS_URL = "https://overpass-api.de/api/interpreter"
OSM_USER_AGENT = "VitalIQ-AI-Gym-Fitness-Assistant/1.0 (student project)"


def geocode_location(query):
    """Convert a typed place/address into latitude and longitude using OSM Nominatim."""
    response = requests.get(
        NOMINATIM_URL,
        params={
            "q": query,
            "format": "jsonv2",
            "limit": 1,
        },
        headers={"User-Agent": OSM_USER_AGENT},
        timeout=15,
    )
    response.raise_for_status()
    results = response.json()
    if not results:
        return None
    return {
        "lat": float(results[0]["lat"]),
        "lon": float(results[0]["lon"]),
        "display_name": results[0].get("display_name", query),
    }


def haversine_km(lat1, lon1, lat2, lon2):
    """Return great-circle distance in kilometres."""
    earth_radius = 6371.0
    p1 = math.radians(lat1)
    p2 = math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return earth_radius * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def search_osm_gyms(lat, lon, radius_m):
    """Find nearby gym/fitness-related places from OpenStreetMap via Overpass."""
    query = f"""
    [out:json][timeout:30];
    (
      nwr(around:{int(radius_m)},{lat},{lon})["leisure"="fitness_centre"];
      nwr(around:{int(radius_m)},{lat},{lon})["leisure"="sports_centre"];
      nwr(around:{int(radius_m)},{lat},{lon})["amenity"="gym"];
      nwr(around:{int(radius_m)},{lat},{lon})["sport"~"fitness|gym",i];
    );
    out center tags;
    """

    response = requests.post(
        OVERPASS_URL,
        data=query,
        headers={"User-Agent": OSM_USER_AGENT},
        timeout=40,
    )
    response.raise_for_status()
    data = response.json()

    gyms = []
    seen = set()

    for element in data.get("elements", []):
        tags = element.get("tags", {}) or {}
        name = tags.get("name") or tags.get("official_name") or "Unnamed fitness location"

        if "lat" in element and "lon" in element:
            item_lat = float(element["lat"])
            item_lon = float(element["lon"])
        elif element.get("center"):
            item_lat = float(element["center"]["lat"])
            item_lon = float(element["center"]["lon"])
        else:
            continue

        key = (round(item_lat, 6), round(item_lon, 6), name.lower().strip())
        if key in seen:
            continue
        seen.add(key)

        if tags.get("leisure") == "fitness_centre" or tags.get("amenity") == "gym":
            category = "Gym / Fitness Centre"
        elif tags.get("leisure") == "sports_centre":
            category = "Sports Centre"
        else:
            category = "Fitness / Sports"

        distance = haversine_km(lat, lon, item_lat, item_lon)
        address_parts = [
            tags.get("addr:housenumber", ""),
            tags.get("addr:street", ""),
            tags.get("addr:suburb", ""),
            tags.get("addr:city", ""),
        ]
        address = ", ".join(x for x in address_parts if x).strip()

        gyms.append({
            "name": name,
            "category": category,
            "lat": item_lat,
            "lon": item_lon,
            "distance_km": distance,
            "address": address,
            "phone": tags.get("phone") or tags.get("contact:phone", ""),
            "website": tags.get("website") or tags.get("contact:website", ""),
            "opening_hours": tags.get("opening_hours", ""),
            "osm_type": element.get("type", ""),
            "osm_id": element.get("id", ""),
        })

    gyms.sort(key=lambda x: x["distance_km"])
    return gyms


# ============================================================
# AI GYM TRAINER — POSE / REP / FORM ENGINE
# ============================================================

def calculate_angle(a, b, c):
    """Return the angle ABC in degrees."""
    ax, ay = a
    bx, by = b
    cx, cy = c

    radians = math.atan2(cy - by, cx - bx) - math.atan2(ay - by, ax - bx)
    angle = abs(math.degrees(radians))
    if angle > 180:
        angle = 360 - angle
    return angle


class GymTrainer:
    """MediaPipe-based exercise detector for the VitalIQ AI Gym Trainer.

    The engine intentionally keeps all exercises inside one class so the UI can
    switch exercises without changing the camera pipeline.
    """

    def __init__(self, exercise):
        self.exercise = exercise
        self.counter = 0
        self.stage = "UP"
        self.feedback = "Position yourself in front of the camera."
        self.score = 0
        self.frames = 0
        self.good_frames = 0
        self.last_angle = 0
        self.hold_start = None

    def reset(self, exercise=None):
        if exercise:
            self.exercise = exercise
        self.counter = 0
        self.stage = "UP"
        self.feedback = "Position yourself in front of the camera."
        self.score = 0
        self.frames = 0
        self.good_frames = 0
        self.last_angle = 0
        self.hold_start = None

    def process(self, landmarks, width, height):
        def visible(*indices, threshold=0.65):
            return all(
                getattr(landmarks[idx], "visibility", 0.0) >= threshold
                for idx in indices
            )

        def p(idx):
            lm = landmarks[idx]
            return (lm.x * width, lm.y * height)

        def angle(a, b, c):
            return calculate_angle(p(a), p(b), p(c))

        def both_side_angle(a1, b1, c1, a2, b2, c2):
            return (angle(a1, b1, c1) + angle(a2, b2, c2)) / 2

        # ------------------------------------------------------------
        # 1. SQUATS
        # ------------------------------------------------------------
        if self.exercise == "Squats":
            if not visible(11, 12, 23, 24, 25, 26, 27, 28):
                self.feedback = "Full body not clearly visible — step back slightly."
                self.last_angle = 0
                return self.counter, self.feedback, self.score, self.last_angle

            self.frames += 1
            a = both_side_angle(23, 25, 27, 24, 26, 28)
            self.last_angle = a

            if a > 160:
                self.stage = "UP"
                self.feedback = "Good starting position"
            elif 95 <= a <= 140:
                if self.stage == "UP":
                    self.counter += 1
                    self.stage = "DOWN"
                self.feedback = "Good depth — drive upward"
                self.good_frames += 1
            elif a < 95:
                self.feedback = "Too deep — maintain control"
            else:
                self.feedback = "Lower with controlled movement"

        # ------------------------------------------------------------
        # 2. BICEP CURLS
        # ------------------------------------------------------------
        elif self.exercise == "Bicep Curls":
            if not visible(11, 12, 13, 14, 15, 16):
                self.feedback = "Keep both arms clearly visible to the camera."
                self.last_angle = 0
                return self.counter, self.feedback, self.score, self.last_angle

            self.frames += 1
            a = both_side_angle(11, 13, 15, 12, 14, 16)
            self.last_angle = a

            if a > 155:
                self.stage = "DOWN"
                self.feedback = "Extend the arms"
            elif a < 55:
                if self.stage == "DOWN":
                    self.counter += 1
                    self.stage = "UP"
                self.feedback = "Great curl — squeeze at the top"
                self.good_frames += 1
            else:
                self.feedback = "Control the movement"

        # ------------------------------------------------------------
        # 3. PUSH-UPS
        # ------------------------------------------------------------
        elif self.exercise == "Push-ups":
            if not visible(11, 12, 13, 14, 15, 16):
                self.feedback = "Keep shoulders, elbows and wrists visible."
                self.last_angle = 0
                return self.counter, self.feedback, self.score, self.last_angle

            self.frames += 1
            a = both_side_angle(11, 13, 15, 12, 14, 16)
            self.last_angle = a

            if a > 155:
                self.stage = "UP"
                self.feedback = "Good top position"
                self.good_frames += 1
            elif a < 95:
                if self.stage == "UP":
                    self.counter += 1
                    self.stage = "DOWN"
                self.feedback = "Good depth — push back up"
                self.good_frames += 1
            else:
                self.feedback = "Lower with controlled movement"

        # ------------------------------------------------------------
        # 4. LUNGES
        # ------------------------------------------------------------
        elif self.exercise == "Lunges":
            if not visible(11, 12, 23, 24, 25, 26, 27, 28):
                self.feedback = "Show your full body for lunge detection."
                self.last_angle = 0
                return self.counter, self.feedback, self.score, self.last_angle

            self.frames += 1
            a = min(angle(23, 25, 27), angle(24, 26, 28))
            self.last_angle = a

            if a > 155:
                self.stage = "UP"
                self.feedback = "Good starting stance"
            elif 75 <= a <= 120:
                if self.stage == "UP":
                    self.counter += 1
                    self.stage = "DOWN"
                self.feedback = "Good lunge depth — drive upward"
                self.good_frames += 1
            else:
                self.feedback = "Control your knee position"

        # ------------------------------------------------------------
        # 5. SHOULDER PRESS
        # ------------------------------------------------------------
        elif self.exercise == "Shoulder Press":
            if not visible(11, 12, 13, 14, 15, 16):
                self.feedback = "Keep both arms and shoulders visible."
                self.last_angle = 0
                return self.counter, self.feedback, self.score, self.last_angle

            self.frames += 1
            a = both_side_angle(11, 13, 15, 12, 14, 16)
            self.last_angle = a

            if a < 100:
                self.stage = "DOWN"
                self.feedback = "Press upward with control"
            elif a > 150:
                if self.stage == "DOWN":
                    self.counter += 1
                    self.stage = "UP"
                self.feedback = "Good overhead position"
                self.good_frames += 1
            else:
                self.feedback = "Continue the press"

        # ------------------------------------------------------------
        # 6. JUMPING JACKS
        # ------------------------------------------------------------
        elif self.exercise == "Jumping Jacks":
            if not visible(11, 12, 23, 24, 27, 28):
                self.feedback = "Show your full body, including hands and feet."
                self.last_angle = 0
                return self.counter, self.feedback, self.score, self.last_angle

            self.frames += 1
            ls, rs = p(11), p(12)
            lw, rw = p(15), p(16)
            la, ra = p(27), p(28)

            shoulder_width = max(abs(rs[0] - ls[0]), 1)
            ankle_width = abs(ra[0] - la[0])
            hands_up = lw[1] < ls[1] and rw[1] < rs[1]
            legs_open = ankle_width > shoulder_width * 1.35
            open_position = hands_up and legs_open
            closed_position = (not hands_up) and ankle_width < shoulder_width * 1.20
            self.last_angle = 180 if open_position else 90

            if open_position:
                self.stage = "OPEN"
                self.feedback = "Great — bring arms and legs together"
                self.good_frames += 1
            elif closed_position:
                if self.stage == "OPEN":
                    self.counter += 1
                    self.stage = "CLOSED"
                self.feedback = "Ready for the next jump"
                self.good_frames += 1
            else:
                self.feedback = "Open arms and legs fully"

        # ------------------------------------------------------------
        # 7. SIT-UPS
        # ------------------------------------------------------------
        elif self.exercise == "Sit-ups":
            if not visible(11, 12, 23, 24, 25, 26):
                self.feedback = "Keep shoulders, hips and knees visible."
                self.last_angle = 0
                return self.counter, self.feedback, self.score, self.last_angle

            self.frames += 1
            a = (angle(11, 23, 25) + angle(12, 24, 26)) / 2
            self.last_angle = a

            if a > 150:
                self.stage = "DOWN"
                self.feedback = "Lower under control"
            elif a < 105:
                if self.stage == "DOWN":
                    self.counter += 1
                    self.stage = "UP"
                self.feedback = "Good sit-up — keep your core engaged"
                self.good_frames += 1
            else:
                self.feedback = "Continue through the full movement"

        # ------------------------------------------------------------
        # 8. HIGH KNEES
        # ------------------------------------------------------------
        elif self.exercise == "High Knees":
            if not visible(11, 12, 23, 24, 25, 26):
                self.feedback = "Show your upper body and both legs."
                self.last_angle = 0
                return self.counter, self.feedback, self.score, self.last_angle

            self.frames += 1
            left_knee = angle(23, 25, 27)
            right_knee = angle(24, 26, 28)
            hip_level_left = p(23)[1]
            hip_level_right = p(24)[1]
            left_knee_high = p(25)[1] < hip_level_left + height * 0.02
            right_knee_high = p(26)[1] < hip_level_right + height * 0.02
            self.last_angle = min(left_knee, right_knee)

            if left_knee < 120 and left_knee_high:
                active = "LEFT"
            elif right_knee < 120 and right_knee_high:
                active = "RIGHT"
            else:
                active = "NONE"

            if active != "NONE":
                if self.stage != active:
                    self.counter += 1
                    self.stage = active
                self.feedback = "Drive the knee higher"
                self.good_frames += 1
            else:
                self.feedback = "Lift each knee toward hip height"

        # ------------------------------------------------------------
        # 9. LATERAL RAISES
        # ------------------------------------------------------------
        elif self.exercise == "Lateral Raises":
            if not visible(11, 12, 13, 14, 15, 16):
                self.feedback = "Keep shoulders, elbows and wrists visible."
                self.last_angle = 0
                return self.counter, self.feedback, self.score, self.last_angle

            self.frames += 1
            left_elbow = angle(11, 13, 15)
            right_elbow = angle(12, 14, 16)
            left_up = p(15)[1] < p(11)[1] + height * 0.05
            right_up = p(16)[1] < p(12)[1] + height * 0.05
            raised = left_up and right_up and left_elbow > 130 and right_elbow > 130
            lowered = p(15)[1] > p(11)[1] + height * 0.18 and p(16)[1] > p(12)[1] + height * 0.18
            self.last_angle = (left_elbow + right_elbow) / 2

            if lowered:
                self.stage = "DOWN"
                self.feedback = "Raise both arms smoothly"
            elif raised:
                if self.stage == "DOWN":
                    self.counter += 1
                    self.stage = "UP"
                self.feedback = "Good lateral raise"
                self.good_frames += 1
            else:
                self.feedback = "Keep elbows slightly soft and raise to shoulder level"

        # ------------------------------------------------------------
        # 10. FRONT RAISES
        # ------------------------------------------------------------
        elif self.exercise == "Front Raises":
            if not visible(11, 12, 13, 14, 15, 16):
                self.feedback = "Keep shoulders, elbows and wrists visible."
                self.last_angle = 0
                return self.counter, self.feedback, self.score, self.last_angle

            self.frames += 1
            a = both_side_angle(11, 13, 15, 12, 14, 16)
            left_up = p(15)[1] < p(11)[1] - height * 0.12
            right_up = p(16)[1] < p(12)[1] - height * 0.12
            raised = left_up and right_up and a > 135
            lowered = p(15)[1] > p(11)[1] + height * 0.12 and p(16)[1] > p(12)[1] + height * 0.12
            self.last_angle = a

            if lowered:
                self.stage = "DOWN"
                self.feedback = "Raise arms to shoulder height"
            elif raised:
                if self.stage == "DOWN":
                    self.counter += 1
                    self.stage = "UP"
                self.feedback = "Good front raise"
                self.good_frames += 1
            else:
                self.feedback = "Control the raise — avoid swinging"

        # ------------------------------------------------------------
        # 11. CALF RAISES
        # ------------------------------------------------------------
        elif self.exercise == "Calf Raises":
            # Calf raises are detected from the heel moving above the toe.
            # MediaPipe image Y increases downward, so during a raise:
            # heel_y becomes smaller than toe_y.
            if not visible(23, 24, 25, 26, 27, 28, 29, 30, 31, 32):
                self.feedback = "Keep both legs, ankles and feet visible."
                self.last_angle = 0
                return self.counter, self.feedback, self.score, self.last_angle

            self.frames += 1

            left_knee = angle(23, 25, 27)
            right_knee = angle(24, 26, 28)
            a = (left_knee + right_knee) / 2
            self.last_angle = a

            # The toes stay near the floor while the heels rise.
            left_heel_lift = p(31)[1] - p(29)[1]
            right_heel_lift = p(32)[1] - p(30)[1]

            # Scale the threshold with body size/camera distance.
            threshold = height * 0.018
            left_rise = left_heel_lift > threshold
            right_rise = right_heel_lift > threshold

            # Require both heels to rise for a strict two-leg calf raise.
            raised = left_rise and right_rise

            if raised:
                if self.stage == "DOWN":
                    self.counter += 1
                    self.stage = "UP"
                self.feedback = "Good calf raise — hold the top briefly"
                self.good_frames += 1
            else:
                self.stage = "DOWN"
                self.feedback = "Rise onto your toes — lift both heels"

        # ------------------------------------------------------------
        # 12. PLANK — hold timer mode
        # ------------------------------------------------------------
        elif self.exercise == "Plank":
            # A normal plank is best viewed from the side. Use either body
            # side if visible so one side does not have to be perfectly
            # exposed to the camera.
            left_visible = visible(11, 23, 27)
            right_visible = visible(12, 24, 28)

            if not left_visible and not right_visible:
                self.feedback = "Keep one shoulder, hip and ankle visible."
                self.last_angle = 0
                self.hold_start = None
                self.counter = 0
                return self.counter, self.feedback, self.score, self.last_angle

            self.frames += 1

            angles = []
            if left_visible:
                angles.append(angle(11, 23, 27))
            if right_visible:
                angles.append(angle(12, 24, 28))

            a = sum(angles) / len(angles)
            self.last_angle = a

            # Allow a small tolerance because pose landmarks naturally wobble.
            if 155 <= a <= 180:
                if self.hold_start is None:
                    self.hold_start = time.monotonic()

                self.counter = int(time.monotonic() - self.hold_start)
                self.feedback = f"Excellent plank alignment — hold {self.counter}s"
                self.good_frames += 1

            elif 145 <= a < 155:
                self.hold_start = None
                self.counter = 0
                self.feedback = "Keep your body straighter — align hips with shoulders"

            else:
                self.hold_start = None
                self.counter = 0
                self.feedback = "Adjust your hips — keep a straight body line"

        else:
            self.feedback = "Select a supported exercise."

        if self.frames:
            self.score = int(max(0, min(100, (self.good_frames / self.frames) * 100)))

        return self.counter, self.feedback, self.score, self.last_angle


# Shared state between the WebRTC callback and Streamlit UI.
# Keep these objects inside Streamlit session state so they survive page
# navigation/reruns. Otherwise Performance Analytics would fall back to
# the default exercise (Squats) every time the page changed.
if "trainer_lock" not in st.session_state:
    st.session_state.trainer_lock = threading.Lock()

if "trainer_state" not in st.session_state:
    st.session_state.trainer_state = {
        "exercise": "Squats",
        "reps": 0,
        "score": 0,
        "feedback": "Camera ready",
        "angle": 0,
        "session_start": None,
        "last_update": None,
    }

trainer_lock = st.session_state.trainer_lock
trainer_state = st.session_state.trainer_state


def create_video_callback():
    pose = mp.solutions.pose.Pose(
        static_image_mode=False,
        model_complexity=1,
        smooth_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    )
    drawing = mp.solutions.drawing_utils
    local_trainer = GymTrainer("Squats")

    def video_frame_callback(frame):
        nonlocal local_trainer

        image = frame.to_ndarray(format="bgr24")
        image = cv2.flip(image, 1)

        height, width = image.shape[:2]
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb)

        if results.pose_landmarks:
            # Keep the selected exercise in sync with the sidebar/page state.
            with trainer_lock:
                selected = trainer_state["exercise"]

            if local_trainer.exercise != selected:
                local_trainer.reset(selected)
                with trainer_lock:
                    trainer_state["session_start"] = time.time()

            with trainer_lock:
                if trainer_state["session_start"] is None:
                    trainer_state["session_start"] = time.time()

            reps, feedback, score, angle = local_trainer.process(
                results.pose_landmarks.landmark, width, height
            )

            drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp.solutions.pose.POSE_CONNECTIONS,
            )

            # Live overlay.
            cv2.rectangle(image, (15, 15), (350, 145), (7, 17, 31), -1)
            cv2.putText(
                image, f"{local_trainer.exercise}",
                (30, 48), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                (46, 212, 194), 2
            )
            overlay_label = "HOLD" if local_trainer.exercise == "Plank" else "REPS"
            overlay_value = f"{reps}s" if local_trainer.exercise == "Plank" else str(reps)
            cv2.putText(
                image, f"{overlay_label}  {overlay_value}",
                (30, 83), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                (255, 255, 255), 2
            )
            cv2.putText(
                image, f"SCORE  {score}/100",
                (30, 118), cv2.FONT_HERSHEY_SIMPLEX, 0.65,
                (169, 155, 255), 2
            )

            # Feedback bar.
            cv2.rectangle(
                image, (15, height - 65), (width - 15, height - 15),
                (7, 17, 31), -1
            )
            cv2.putText(
                image, feedback[:65],
                (30, height - 33), cv2.FONT_HERSHEY_SIMPLEX, 0.62,
                (124, 233, 221), 2
            )

            with trainer_lock:
                trainer_state["reps"] = reps
                trainer_state["score"] = score
                trainer_state["feedback"] = feedback
                trainer_state["angle"] = round(angle, 1)
                trainer_state["last_update"] = time.time()

        else:
            with trainer_lock:
                trainer_state["feedback"] = "No pose detected — step back and face the camera."

            cv2.putText(
                image,
                "NO PERSON DETECTED",
                (30, 55),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (255, 255, 255),
                2,
            )

        return av.VideoFrame.from_ndarray(image, format="bgr24")

    return video_frame_callback


# ============================================================
# SIDEBAR
# ============================================================


with st.sidebar:

    html("""
    <div class="brand-container">
        <div class="brand-name">
            VITAL<span>IQ</span>
        </div>

        <div class="brand-subtitle">
            INTELLIGENT FITNESS PLATFORM
        </div>
    </div>
    """)

    html("""
    <div class="side-section">
        Workspace
    </div>
    """)

    nav_items = [
        "🏠  Overview",
        "🏋️  AI Gym Trainer",
        "🥗  Nutrition Coach",
        "🤖  AI Fitness Buddy",
        "📅  Habit Intelligence",
        "📊  Performance Analytics",
        "📍  Gym Finder",
    ]
    if st.session_state.get("user_role") == "admin":
        nav_items.append("🛡️  Admin Dashboard")

    page = st.radio(
        "Navigation",
        nav_items,
        label_visibility="collapsed"
    )

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='profile' style='margin:0 2px 12px;'>"
        f"<div class='profile-avatar'>{st.session_state.get('user_name','User')[:2].upper()}</div>"
        f"<div><div class='profile-name'>{st.session_state.get('user_name','User')}</div>"
        f"<div class='profile-role'>{st.session_state.get('user_role','user').title()} • {st.session_state.get('user_email','')}</div></div></div>",
        unsafe_allow_html=True
    )
    if st.button("↪  Sign Out", use_container_width=True):
        logout_user()
        st.rerun()

    html("""
    <div class="side-status">
        <div class="side-status-title">
            FITNESS STATUS
        </div>

        <div class="side-status-main">
            ⚡ On Track
        </div>

        <div class="side-status-text">
            7 day consistency streak
        </div>
    </div>
    """)


# ============================================================
# ADMIN DASHBOARD
# ============================================================

if page == "🛡️  Admin Dashboard":
    if st.session_state.get("user_role") != "admin":
        st.error("Administrator access required.")
        st.stop()

    try:
        profiles = _response_data(supabase.table("profiles").select("id, full_name, email, role, created_at, updated_at").order("created_at", desc=True).limit(200).execute())
        workouts = _response_data(supabase.table("workout_sessions").select("id, user_id, exercise, reps, hold_seconds, form_score, joint_angle, duration_seconds, feedback, created_at").order("created_at", desc=True).limit(200).execute())
    except Exception as exc:
        st.error("Admin analytics could not be loaded. Check the Supabase admin RLS policies.")
        st.code(str(exc))
        st.stop()

    user_count = sum(1 for row in profiles if row.get("role") == "user")
    total_accounts = len(profiles)
    workout_count = len(workouts)
    scores = [float(row.get("form_score",0) or 0) for row in workouts]
    avg_score = round(sum(scores)/len(scores),1) if scores else 0
    names = {str(row["id"]): row.get("full_name","User") for row in profiles}

    html("""
    <div class="header-container"><div><div class="eyebrow">SYSTEM ADMINISTRATION • PLATFORM ANALYTICS</div><div class="page-title">Admin <span>Dashboard</span></div><div class="page-description">Monitor VITALIQ accounts and workout activity from one administrative workspace.</div></div></div>
    <div class="hero"><div class="hero-label">VITALIQ PLATFORM CONTROL</div><div class="hero-title">A clear view of your fitness platform.</div><div class="hero-text">Account management and usage analytics for the deployed VITALIQ system.</div><div class="hero-chip">● ADMIN ACCESS ACTIVE</div></div>
    """)
    a,b,c,d=st.columns(4)
    a.metric("Registered Users",user_count); b.metric("Total Accounts",total_accounts); c.metric("Workout Sessions",workout_count); d.metric("Average Form Score",f"{avg_score}/100")
    st.markdown("### 👥 User Management")
    if profiles:
        st.dataframe(pd.DataFrame([{
            "Full Name":r.get("full_name",""),"Email":r.get("email",""),"Role":r.get("role","user"),"Created":r.get("created_at","")
        } for r in profiles]),use_container_width=True,hide_index=True)
    else: st.info("No users have registered yet.")
    st.markdown("### 🏋️ Recent Workout Activity")
    if workouts:
        rows=[]
        for r in workouts[:20]:
            rows.append({"User":names.get(str(r.get("user_id")),"User"),"Exercise":r.get("exercise",""),"Reps / Hold":r.get("hold_seconds",0) if r.get("exercise")=="Plank" else r.get("reps",0),"Score":r.get("form_score",0),"Created":r.get("created_at","")})
        st.dataframe(pd.DataFrame(rows),use_container_width=True,hide_index=True)
    else: st.info("No workout sessions have been saved yet.")
    html("""<div class="motivation"><div class="motivation-label">✦ ADMIN INSIGHT</div><div class="motivation-text">VITALIQ is ready for multi-user fitness tracking.</div><div class="motivation-sub">The dashboard reports registered accounts and saved workout analytics.</div></div>""")


# ============================================================
# OVERVIEW PAGE
# ============================================================

if page == "🏠  Overview":

    html(f"""
    <div class="header-container">

        <div>

            <div class="eyebrow">
                PERSONAL FITNESS INTELLIGENCE
            </div>

            <div class="page-title">
                Your Fitness <span>Command Center</span>
            </div>

            <div class="page-description">
                Track your body, understand your performance,
                and let AI guide your fitness journey.
            </div>

        </div>

        <div class="profile">

            <div class="profile-avatar">
                {st.session_state.get("user_name", "User")[:2].upper()}
            </div>

            <div>
                <div class="profile-name">
                    {st.session_state.get("user_name", "User")}
                </div>

                <div class="profile-role">
                    {st.session_state.get("user_role", "user").title()} • Fitness Explorer
                </div>
            </div>

        </div>

    </div>
    """)

    # --------------------------------------------------------
    # HERO
    # --------------------------------------------------------

    html("""
    <div class="hero">

        <div class="hero-label">
            ⚡ AI FITNESS INTELLIGENCE
        </div>

        <div class="hero-title">
            Build strength. Build consistency.
        </div>

        <div class="hero-text">
            VitalIQ combines computer vision, intelligent
            recommendations, behavioral insights and
            conversational AI into one personalized
            fitness ecosystem.
        </div>

        <div class="hero-chip">
            ● SYSTEM READY
        </div>

    </div>
    """)

    # --------------------------------------------------------
    # STAT CARDS
    # --------------------------------------------------------

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        html("""
        <div class="stat-card">
            <div class="stat-icon">🔥</div>
            <div class="stat-label">CALORIES BURNED</div>
            <div class="stat-value">420 kcal</div>
            <div class="stat-note">↑ 12% this week</div>
        </div>
        """)

    with c2:
        html("""
        <div class="stat-card">
            <div class="stat-icon">💪</div>
            <div class="stat-label">TOTAL REPS</div>
            <div class="stat-value">128</div>
            <div class="stat-note">↑ 18 today</div>
        </div>
        """)

    with c3:
        html("""
        <div class="stat-card">
            <div class="stat-icon">◈</div>
            <div class="stat-label">PERFORMANCE</div>
            <div class="stat-value">87 / 100</div>
            <div class="stat-note">Strong performance</div>
        </div>
        """)

    with c4:
        html("""
        <div class="stat-card">
            <div class="stat-icon">⚡</div>
            <div class="stat-label">ACTIVE STREAK</div>
            <div class="stat-value">7 Days</div>
            <div class="stat-note">Keep it going</div>
        </div>
        """)

    # --------------------------------------------------------
    # AI MODULES
    # --------------------------------------------------------

    html("""
    <div class="section-heading">
        <div class="section-title">
            AI Fitness Intelligence
        </div>

        <div class="section-subtitle">
            Your connected fitness ecosystem
        </div>
    </div>
    """)

    c1, c2, c3 = st.columns(3)

    with c1:
        html("""
        <div class="feature-card">
            <div class="feature-icon">🏋️</div>

            <div class="feature-title">
                AI Gym Trainer
            </div>

            <div class="feature-description">
                Computer vision analyzes body movement,
                counts repetitions and provides real-time
                exercise form feedback.
            </div>
        </div>
        """)

    with c2:
        html("""
        <div class="feature-card">
            <div class="feature-icon">🥗</div>

            <div class="feature-title">
                Nutrition Coach
            </div>

            <div class="feature-description">
                Generate personalized nutrition guidance,
                calorie targets and meal recommendations
                based on your fitness goals.
            </div>
        </div>
        """)

    with c3:
        html("""
        <div class="feature-card">
            <div class="feature-icon">🤖</div>

            <div class="feature-title">
                AI Fitness Buddy
            </div>

            <div class="feature-description">
                Chat with an intelligent fitness companion
                for motivation, workout guidance and
                personalized recommendations.
            </div>
        </div>
        """)

    c1, c2, c3 = st.columns(3)

    with c1:
        html("""
        <div class="feature-card">
            <div class="feature-icon">📅</div>

            <div class="feature-title">
                Habit Intelligence
            </div>

            <div class="feature-description">
                Monitor workout consistency, streaks and
                engagement patterns to understand your
                fitness habits.
            </div>
        </div>
        """)

    with c2:
        html("""
        <div class="feature-card">
            <div class="feature-icon">📊</div>

            <div class="feature-title">
                Performance Analytics
            </div>

            <div class="feature-description">
                Transform workout history into meaningful
                performance scores, trends and progress
                insights.
            </div>
        </div>
        """)

    with c3:
        html("""
        <div class="feature-card">
            <div class="feature-icon">📍</div>

            <div class="feature-title">
                Gym Finder
            </div>

            <div class="feature-description">
                Discover gyms, fitness programs and
                challenges aligned with your goals and
                preferences.
            </div>
        </div>
        """)

    # --------------------------------------------------------
    # QUICK ACTIONS
    # --------------------------------------------------------

    html("""
    <div class="section-heading">
        <div class="section-title">
            Quick Actions
        </div>

        <div class="section-subtitle">
            Start your next activity
        </div>
    </div>
    """)

    q1, q2, q3, q4 = st.columns(4)

    with q1:
        html("""
        <div class="action-card">
            <div class="action-icon">🏋️</div>
            <div class="action-title">Start Workout</div>
            <div class="action-text">AI-powered training</div>
        </div>
        """)

    with q2:
        html("""
        <div class="action-card">
            <div class="action-icon">🥗</div>
            <div class="action-title">Plan Nutrition</div>
            <div class="action-text">Personalized diet</div>
        </div>
        """)

    with q3:
        html("""
        <div class="action-card">
            <div class="action-icon">🤖</div>
            <div class="action-title">Ask AI Buddy</div>
            <div class="action-text">Get fitness guidance</div>
        </div>
        """)

    with q4:
        html("""
        <div class="action-card">
            <div class="action-icon">📊</div>
            <div class="action-title">View Progress</div>
            <div class="action-text">Analyze performance</div>
        </div>
        """)

    # --------------------------------------------------------
    # MOTIVATION
    # --------------------------------------------------------

    html("""
    <div class="motivation">

        <div class="motivation-label">
            ✦ AI DAILY INSIGHT
        </div>

        <div class="motivation-text">
            Consistency compounds. Your next workout
            is another step toward your goal.
        </div>

        <div class="motivation-sub">
            VitalIQ is ready to help you train smarter.
        </div>

    </div>
    """)


# ============================================================
# OTHER MODULES / AI GYM TRAINER
# ============================================================

elif page == "🏋️  AI Gym Trainer":

    html("""
    <div class="header-container">
        <div>
            <div class="eyebrow">COMPUTER VISION • REAL-TIME COACH</div>
            <div class="page-title">AI <span>Gym Trainer</span></div>
            <div class="page-description">
                Use your webcam to analyze movement, count repetitions
                and receive live exercise-form feedback.
            </div>
        </div>
    </div>
    """)

    selected_exercise = st.selectbox(
        "Select Exercise",
        ["Squats", "Bicep Curls", "Push-ups", "Lunges", "Shoulder Press", "Jumping Jacks", "Sit-ups", "High Knees", "Lateral Raises", "Front Raises", "Calf Raises", "Plank"],
        key="trainer_exercise"
    )

    with trainer_lock:
        trainer_state["exercise"] = selected_exercise

    html("""
    <div class="hero">
        <div class="hero-label">LIVE POSE INTELLIGENCE</div>
        <div class="hero-title">Train with <span style="color:#2ED4C2;">AI-guided movement analysis.</span></div>
        <div class="hero-text">
            Position the camera so the body parts required for the selected
            exercise are clearly visible. VitalIQ checks landmark visibility
            before counting repetitions to improve accuracy.
        </div>
        <div class="hero-chip">● CAMERA ANALYSIS READY</div>
    </div>
    """)

    left, right = st.columns([2.4, 1])

    with left:
        st.markdown("### 📷 Live Training Camera")

        try:
            ctx = webrtc_streamer(
                key="vitaliq-gym-trainer",
                mode=WebRtcMode.SENDRECV,
                video_frame_callback=create_video_callback(),
                media_stream_constraints={
                    "video": True,
                    "audio": False,
                },
                async_processing=True,
                rtc_configuration={
                    "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
                },
            )

            if not ctx.state.playing:
                st.info("Click **START** above to activate your webcam and begin the AI trainer.")

        except Exception as exc:
            st.error("The live camera component could not start.")
            st.code(str(exc))

    with right:
        html("""
        <div class="stat-card">
            <div class="stat-icon">🔢</div>
            <div class="stat-label">LIVE REPETITIONS</div>
            <div class="stat-value" id="rep-value">Live</div>
            <div class="stat-note">Detected from movement</div>
        </div>
        """)

        with trainer_lock:
            reps = trainer_state["reps"]
            score = trainer_state["score"]
            feedback = trainer_state["feedback"]
            angle = trainer_state["angle"]

        if selected_exercise == "Plank":
            st.metric("Hold Time", f"{reps}s")
        else:
            st.metric("Repetitions", reps)
        st.metric("Performance", f"{score}/100")
        st.metric("Joint Angle", f"{angle}°")

        html(f"""
        <div class="motivation">
            <div class="motivation-label">✦ LIVE AI FEEDBACK</div>
            <div class="motivation-text">{feedback}</div>
            <div class="motivation-sub">
                Keep the movement controlled and maintain good posture.
            </div>
        </div>
        """)

    html("""
    <div class="section-heading">
        <div class="section-title">How VitalIQ analyzes your workout</div>
        <div class="section-subtitle">Computer vision pipeline</div>
    </div>
    """)

    c1, c2, c3, c4 = st.columns(4)

    steps = [
        ("📷", "Camera", "Captures your movement"),
        ("🧍", "Pose", "Extracts body landmarks"),
        ("📐", "Kinematics", "Measures joint angles"),
        ("📊", "Feedback", "Counts reps & scores form"),
    ]

    for col, (icon, title, desc) in zip([c1, c2, c3, c4], steps):
        with col:
            html(f"""
            <div class="action-card">
                <div class="action-icon">{icon}</div>
                <div class="action-title">{title}</div>
                <div class="action-text">{desc}</div>
            </div>
            """)

    st.caption(
        "Tip: Keep your whole body visible, use good lighting, and position the "
        "camera far enough away to capture the required joints."
    )

elif page == "🥗  Nutrition Coach":

    # --------------------------------------------------------
    # NUTRITION COACH
    # --------------------------------------------------------
    if "nutrition_profile" not in st.session_state:
        saved_nutrition = load_user_nutrition()
        if saved_nutrition:
            st.session_state.nutrition_profile = {
                "age": saved_nutrition.get("age", 21),
                "sex": saved_nutrition.get("sex", "Male"),
                "height": float(saved_nutrition.get("height_cm", 170) or 170),
                "weight": float(saved_nutrition.get("weight_kg", 65) or 65),
                "activity": saved_nutrition.get("activity_level", "Moderately Active"),
                "goal": saved_nutrition.get("goal", "Maintain Weight"),
                "preference": saved_nutrition.get("diet", "Balanced / Non-Vegetarian"),
                "bmi": float(saved_nutrition.get("bmi", 0) or 0),
                "bmr": float(saved_nutrition.get("bmr", 0) or 0),
                "tdee": float(saved_nutrition.get("calorie_target", 0) or 0),
                "target": float(saved_nutrition.get("calorie_target", 0) or 0),
                "protein": float(saved_nutrition.get("protein_target", 0) or 0),
            }
        else:
            st.session_state.nutrition_profile = None

    html("""
    <div class="header-container">
        <div>
            <div class="eyebrow">AI DIETICIAN • CALORIE COACH</div>
            <div class="page-title">Nutrition <span>Coach</span></div>
            <div class="page-description">
                Build a personalized calorie target, meal plan and grocery list
                using your body metrics, fitness goal and food preference.
            </div>
        </div>
    </div>
    """)

    st.markdown("### 👤 Personal Profile")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        age = st.number_input("Age", min_value=13, max_value=100, value=21, step=1)
    with c2:
        sex = st.selectbox("Sex", ["Male", "Female"])
    with c3:
        height = st.number_input("Height (cm)", min_value=120.0, max_value=230.0, value=170.0, step=1.0)
    with c4:
        weight = st.number_input("Weight (kg)", min_value=30.0, max_value=250.0, value=65.0, step=0.5)

    c1, c2, c3 = st.columns(3)
    with c1:
        activity = st.selectbox(
            "Activity Level",
            [
                "Sedentary",
                "Lightly Active",
                "Moderately Active",
                "Very Active",
                "Athlete / Extremely Active",
            ],
        )
    with c2:
        goal = st.selectbox("Fitness Goal", ["Lose Weight", "Maintain Weight", "Build Muscle"])
    with c3:
        preference = st.selectbox(
            "Diet Preference",
            ["Balanced / Non-Vegetarian", "Vegetarian", "Eggetarian", "Vegan"],
        )

    generate = st.button("Generate My Nutrition Plan", type="primary", use_container_width=True)

    activity_factors = {
        "Sedentary": 1.20,
        "Lightly Active": 1.375,
        "Moderately Active": 1.55,
        "Very Active": 1.725,
        "Athlete / Extremely Active": 1.90,
    }

    if generate:
        bmi = weight / ((height / 100) ** 2)
        if sex == "Male":
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
        else:
            bmr = 10 * weight + 6.25 * height - 5 * age - 161
        tdee = bmr * activity_factors[activity]

        if goal == "Lose Weight":
            target = max(1200, tdee - 400)
            protein = weight * 1.6
        elif goal == "Build Muscle":
            target = tdee + 250
            protein = weight * 1.8
        else:
            target = tdee
            protein = weight * 1.4

        st.session_state.nutrition_profile = {
            "age": age, "sex": sex, "height": height, "weight": weight,
            "activity": activity, "goal": goal, "preference": preference,
            "bmi": bmi, "bmr": bmr, "tdee": tdee,
            "target": target, "protein": protein,
        }
        if not save_user_nutrition(st.session_state.nutrition_profile):
            st.warning("Nutrition plan is available, but the profile could not be saved to the database.")

    profile = st.session_state.nutrition_profile

    if profile:
        bmi = profile["bmi"]
        bmi_status = "Underweight" if bmi < 18.5 else "Healthy range" if bmi < 25 else "Overweight range" if bmi < 30 else "Obesity range"

        html(f"""
        <div class="hero">
            <div class="hero-label">PERSONALIZED NUTRITION SNAPSHOT</div>
            <div class="hero-title">Your daily target: <span style="color:#2ED4C2;">{round(profile['target'])} kcal</span></div>
            <div class="hero-text">
                Goal: {profile['goal']} • {profile['preference']} • {profile['activity']}
            </div>
            <div class="hero-chip">● AI PLAN READY</div>
        </div>
        """)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("BMI", f"{bmi:.1f}")
        c2.metric("BMI Category", bmi_status)
        c3.metric("Daily Calories", f"{round(profile['target'])} kcal")
        c4.metric("Protein Target", f"{round(profile['protein'])} g")

        st.markdown("### 🍽️ Personalized Meal Plan")

        plans = {
            "Balanced / Non-Vegetarian": [
                ("Breakfast", "Oats + milk + banana + 2 eggs", "~450 kcal"),
                ("Lunch", "Rice/roti + chicken + dal + mixed vegetables", "~650 kcal"),
                ("Snack", "Greek yogurt + fruit + nuts", "~250 kcal"),
                ("Dinner", "Roti + grilled chicken/fish + vegetables", "~550 kcal"),
            ],
            "Vegetarian": [
                ("Breakfast", "Oats + milk/curd + banana + nuts", "~450 kcal"),
                ("Lunch", "Rice/roti + dal + paneer + vegetables", "~650 kcal"),
                ("Snack", "Curd/yogurt + fruit + roasted chana", "~250 kcal"),
                ("Dinner", "Roti + paneer/tofu + mixed vegetables", "~550 kcal"),
            ],
            "Eggetarian": [
                ("Breakfast", "Oats + milk + banana + 2 eggs", "~450 kcal"),
                ("Lunch", "Rice/roti + dal + egg curry + vegetables", "~650 kcal"),
                ("Snack", "Greek yogurt + fruit + nuts", "~250 kcal"),
                ("Dinner", "Roti + egg bhurji + vegetables + curd", "~550 kcal"),
            ],
            "Vegan": [
                ("Breakfast", "Oats + soy milk + banana + peanut butter", "~450 kcal"),
                ("Lunch", "Rice/roti + dal + tofu + vegetables", "~650 kcal"),
                ("Snack", "Fruit + roasted chickpeas + nuts", "~250 kcal"),
                ("Dinner", "Roti + tofu/chickpea curry + vegetables", "~550 kcal"),
            ],
        }

        for meal, food, kcal in plans[profile["preference"]]:
            a, b, c = st.columns([1, 3, 1])
            with a:
                st.markdown(f"**{meal}**")
            with b:
                st.write(food)
            with c:
                st.caption(kcal)

        st.markdown("### 🛒 Smart Grocery List")
        grocery = {
            "Balanced / Non-Vegetarian": ["Oats", "Milk/curd", "Eggs", "Chicken/fish", "Dal", "Rice/roti", "Mixed vegetables", "Bananas", "Greek yogurt", "Nuts"],
            "Vegetarian": ["Oats", "Milk/curd", "Paneer", "Tofu", "Dal", "Rice/roti", "Mixed vegetables", "Fruits", "Roasted chana", "Nuts"],
            "Eggetarian": ["Oats", "Milk/curd", "Eggs", "Dal", "Rice/roti", "Paneer", "Mixed vegetables", "Fruits", "Greek yogurt", "Nuts"],
            "Vegan": ["Oats", "Soy milk", "Tofu", "Chickpeas", "Dal", "Rice/roti", "Mixed vegetables", "Bananas", "Seasonal fruits", "Nuts"],
        }[profile["preference"]]
        cols = st.columns(5)
        for i, item in enumerate(grocery):
            cols[i % 5].markdown(f"• {item}")

        st.markdown("### 📈 Daily Nutrition Tracker")
        t1, t2, t3, t4 = st.columns(4)
        with t1:
            breakfast = st.number_input("Breakfast kcal", min_value=0, max_value=2000, value=0, step=50, key="nut_breakfast")
        with t2:
            lunch = st.number_input("Lunch kcal", min_value=0, max_value=2500, value=0, step=50, key="nut_lunch")
        with t3:
            snack = st.number_input("Snack kcal", min_value=0, max_value=1500, value=0, step=50, key="nut_snack")
        with t4:
            dinner = st.number_input("Dinner kcal", min_value=0, max_value=2500, value=0, step=50, key="nut_dinner")

        consumed = breakfast + lunch + snack + dinner
        remaining = round(profile["target"] - consumed)
        if remaining >= 0:
            st.success(f"Consumed: {consumed} kcal • Remaining: {remaining} kcal")
        else:
            st.warning(f"Consumed: {consumed} kcal • Over target by {abs(remaining)} kcal")

        st.caption("This is an educational estimate, not a medical diagnosis or prescription. Individual calorie and nutrition needs can vary.")
    else:
        st.info("Enter your profile details and click **Generate My Nutrition Plan** to create your personalized plan.")

elif page == "🤖  AI Fitness Buddy":

    # --------------------------------------------------------
    # AI FITNESS BUDDY
    # --------------------------------------------------------
    if "buddy_messages" not in st.session_state:
        st.session_state.buddy_messages = [
            {
                "role": "assistant",
                "content": "Hi! I'm your VITALIQ Fitness Buddy. Ask me about workouts, exercise form, nutrition, recovery, motivation, or your current training session."
            }
        ]

    def buddy_context():
        with trainer_lock:
            exercise = trainer_state.get("exercise", "Squats")
            reps = trainer_state.get("reps", 0)
            score = trainer_state.get("score", 0)
            feedback = trainer_state.get("feedback", "Camera ready")

        profile = st.session_state.get("nutrition_profile")
        return exercise, reps, score, feedback, profile

    def get_groq_api_key():
        # Works locally through .env/environment and on Streamlit Cloud through Secrets.
        try:
            secret_key = st.secrets.get("GROQ_API_KEY", "")
        except Exception:
            secret_key = ""
        return (secret_key or os.getenv("GROQ_API_KEY", "")).strip()

    def build_buddy_context():
        exercise, reps, score, feedback, profile = buddy_context()
        profile_context = "No nutrition profile has been generated yet."
        if profile:
            profile_context = (
                f"Goal: {profile['goal']}; Diet: {profile.get('preference', 'not specified')}; "
                f"BMI: {profile.get('bmi', 'not specified')}; "
                f"Daily calories: {round(profile['target'])} kcal; "
                f"Protein target: {round(profile['protein'])} g/day."
            )

        return (
            f"Current exercise: {exercise}.\n"
            f"Current reps/hold: {reps}.\n"
            f"Current form score: {score}/100.\n"
            f"Latest trainer feedback: {feedback}.\n"
            f"Nutrition profile: {profile_context}"
        )

    def fitness_buddy_reply(message):
        api_key = get_groq_api_key()
        if not api_key:
            return (
                "⚠️ AI Fitness Buddy is not connected yet. Add your GROQ_API_KEY to the "
                ".env file for local use or Streamlit Secrets for deployment, then restart the app."
            )

        exercise, reps, score, feedback, profile = buddy_context()
        context = build_buddy_context()

        system_prompt = """
You are VITALIQ AI Fitness Buddy, the conversational AI assistant inside a student-built fitness platform.

Your job is to give useful, concise, practical fitness guidance using the user's current VITALIQ context when relevant.

Rules:
1. Answer the user's actual question directly. Do not rely on predefined answers.
2. Use the supplied trainer data and nutrition profile when relevant, but never invent measurements, reps, scores, diagnoses, or user details.
3. You may explain exercise technique, workout planning, recovery, motivation, general nutrition, calories, protein, and fitness concepts.
4. For pain, injury, illness, eating disorders, medication, or other medical concerns, do not diagnose or prescribe. Recommend an appropriately qualified healthcare professional when needed.
5. Do not encourage dangerous overtraining, extreme dieting, dehydration, or unsafe exercise.
6. If the user asks something unrelated to fitness, politely say you are focused on fitness, nutrition, recovery, and workout guidance.
7. Keep responses friendly and reasonably concise. Use bullets when they improve clarity.
8. Do not claim that camera analysis is happening unless the supplied context contains trainer data.
"""

        messages = [{"role": "system", "content": system_prompt}]
        # Keep a useful amount of conversation history without sending an unlimited chat.
        history = st.session_state.buddy_messages[-10:]
        for item in history:
            messages.append({"role": item["role"], "content": item["content"]})

        messages.append({
            "role": "user",
            "content": (
                f"VITALIQ live context:\n{context}\n\n"
                f"User's current question: {message}"
            ),
        })

        try:
            client = Groq(api_key=api_key)
            completion = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=messages,
                temperature=0.35,
                max_tokens=500,
            )
            answer = completion.choices[0].message.content.strip()
            return answer or "I couldn't generate a response right now. Please try again."
        except Exception as exc:
            error_text = str(exc)
            if "401" in error_text or "authentication" in error_text.lower() or "api key" in error_text.lower():
                return "⚠️ Groq authentication failed. Check that your GROQ_API_KEY is correct and restart the app."
            if "429" in error_text or "rate limit" in error_text.lower():
                return "⚠️ The AI service rate limit was reached. Please wait a moment and try again."
            return f"⚠️ I couldn't reach the AI service right now. Please try again. ({type(exc).__name__})"

    html("""
    <div class="header-container">
        <div>
            <div class="eyebrow">PERSONAL AI • FITNESS COMPANION</div>
            <div class="page-title">AI Fitness <span>Buddy</span></div>
            <div class="page-description">
                Your conversational fitness companion for workout guidance, form tips,
                nutrition context, recovery and motivation.
            </div>
        </div>
    </div>
    """)

    # Quick context cards from the live trainer and Nutrition Coach.
    exercise, reps, score, feedback, profile = buddy_context()
    b1, b2, b3, b4 = st.columns(4)
    with b1:
        st.metric("Current Exercise", exercise)
    with b2:
        st.metric("Reps / Hold", f"{reps}s" if exercise == "Plank" else reps)
    with b3:
        st.metric("Form Score", f"{score}/100")
    with b4:
        st.metric("Nutrition Profile", "Ready" if profile else "Not set")

    html(f"""
    <div class="hero">
        <div class="hero-label">VITALIQ CONVERSATIONAL FITNESS</div>
        <div class="hero-title">Train smarter with your <span style="color:#2ED4C2;">AI companion</span>.</div>
        <div class="hero-text">
            Ask questions about your current exercise, form, workout planning,
            nutrition, recovery or motivation. The buddy can also use your live
            trainer state and generated nutrition profile for more relevant responses.
        </div>
        <div class="hero-chip">● BUDDY ONLINE</div>
    </div>
    """)

    st.markdown("### 💬 Chat with VITALIQ Buddy")

    # Display conversation history.
    for msg in st.session_state.buddy_messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Useful one-click prompts make the module immediately testable.
    q1, q2, q3, q4 = st.columns(4)
    quick_prompt = None
    with q1:
        if st.button("Check my workout", use_container_width=True):
            quick_prompt = "How is my current workout?"
    with q2:
        if st.button("Improve my form", use_container_width=True):
            quick_prompt = "How can I improve my current exercise form?"
    with q3:
        if st.button("Nutrition advice", use_container_width=True):
            quick_prompt = "Give me nutrition advice based on my profile."
    with q4:
        if st.button("Motivate me", use_container_width=True):
            quick_prompt = "I need motivation for my workout."

    typed_prompt = st.chat_input("Ask your Fitness Buddy anything about your workout...")
    user_prompt = typed_prompt or quick_prompt

    if user_prompt:
        st.session_state.buddy_messages.append({"role": "user", "content": user_prompt})
        reply = fitness_buddy_reply(user_prompt)
        st.session_state.buddy_messages.append({"role": "assistant", "content": reply})
        st.rerun()

    if st.button("Clear Chat"):
        st.session_state.buddy_messages = [
            {
                "role": "assistant",
                "content": "Chat cleared. I'm ready for your next fitness question."
            }
        ]
        st.rerun()

    html(f"""
    <div class="motivation">
        <div class="motivation-label">✦ LIVE TRAINER CONTEXT</div>
        <div class="motivation-text">{feedback}</div>
        <div class="motivation-sub">The buddy uses the current VITALIQ session state when answering workout-related questions.</div>
    </div>
    """)

elif page == "📅  Habit Intelligence":

    # Session-persistent habit data. The tracker is intentionally local to
    # this Streamlit session so the module works without a database.
    if "habit_log" not in st.session_state:
        st.session_state.habit_log = load_user_habits()
    if "habit_settings" not in st.session_state:
        st.session_state.habit_settings = {
            "workout_goal": 4,
            "water_goal": 8,
            "sleep_goal": 7,
        }

    today = date.today()
    today_key = today.isoformat()

    # Create the current-day record if needed.
    if today_key not in st.session_state.habit_log:
        st.session_state.habit_log[today_key] = {
            "workout": False,
            "water": 0,
            "sleep": 0.0,
            "notes": "",
        }

    settings = st.session_state.habit_settings
    today_data = st.session_state.habit_log[today_key]

    html("""
    <div class="header-container">
        <div>
            <div class="eyebrow">CONSISTENCY • DAILY FITNESS INTELLIGENCE</div>
            <div class="page-title">Habit <span>Intelligence</span></div>
            <div class="page-description">
                Track daily fitness habits, build consistency streaks and turn
                your routine into measurable progress.
            </div>
        </div>
    </div>
    """)

    # ---------------- TODAY'S HABITS ----------------
    html(f"""
    <div class="hero">
        <div class="hero-label">TODAY • {today.strftime('%d %b %Y').upper()}</div>
        <div class="hero-title">Build consistency, <span style="color:#2ED4C2;">not perfection.</span></div>
        <div class="hero-text">
            Complete your daily habits and use the 7-day view to understand
            how consistently you are following your fitness routine.
        </div>
        <div class="hero-chip">● HABIT TRACKER ACTIVE</div>
    </div>
    """)

    st.markdown("### 🎯 Today's Habits")

    h1, h2, h3 = st.columns(3)
    with h1:
        workout_done = st.checkbox("Workout completed", value=bool(today_data["workout"]))
    with h2:
        water_value = st.number_input(
            "Water (glasses)", min_value=0, max_value=30,
            value=int(today_data["water"]), step=1
        )
    with h3:
        sleep_value = st.number_input(
            "Sleep (hours)", min_value=0.0, max_value=16.0,
            value=float(today_data["sleep"]), step=0.5
        )

    notes = st.text_input(
        "Daily note",
        value=today_data.get("notes", ""),
        placeholder="Example: 30-minute strength workout"
    )

    if st.button("Save Today's Habits", type="primary"):
        st.session_state.habit_log[today_key] = {
            "workout": workout_done,
            "water": int(water_value),
            "sleep": float(sleep_value),
            "notes": notes,
        }
        today_data = st.session_state.habit_log[today_key]
        if save_habit_log(today_key, today_data):
            st.success("Today's habit progress saved.")
        else:
            st.error("Habit progress could not be saved to the database.")

    # ---------------- GOALS ----------------
    st.markdown("### ⚙️ Weekly Habit Goals")
    g1, g2, g3 = st.columns(3)
    with g1:
        new_workout_goal = st.number_input(
            "Workouts / week", 1, 7, int(settings["workout_goal"]), 1
        )
    with g2:
        new_water_goal = st.number_input(
            "Water / day", 1, 20, int(settings["water_goal"]), 1
        )
    with g3:
        new_sleep_goal = st.number_input(
            "Sleep / night", 1.0, 12.0, float(settings["sleep_goal"]), 0.5
        )

    if st.button("Update Habit Goals"):
        st.session_state.habit_settings = {
            "workout_goal": int(new_workout_goal),
            "water_goal": int(new_water_goal),
            "sleep_goal": float(new_sleep_goal),
        }
        settings = st.session_state.habit_settings
        st.success("Habit goals updated.")

    # ---------------- 7-DAY INTELLIGENCE ----------------
    st.markdown("### 📅 7-Day Consistency")
    days = []
    for offset in range(6, -1, -1):
        d = today - timedelta(days=offset)
        key = d.isoformat()
        item = st.session_state.habit_log.get(
            key, {"workout": False, "water": 0, "sleep": 0.0, "notes": ""}
        )
        days.append((d, item))

    completed_workouts = sum(1 for _, item in days if item["workout"])
    water_days = sum(1 for _, item in days if item["water"] >= settings["water_goal"])
    sleep_days = sum(1 for _, item in days if item["sleep"] >= settings["sleep_goal"])

    # Current streak ending today.
    streak = 0
    cursor = today
    while True:
        item = st.session_state.habit_log.get(cursor.isoformat())
        if item and item.get("workout"):
            streak += 1
            cursor -= timedelta(days=1)
        else:
            break

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Workout Streak", f"{streak} day{'s' if streak != 1 else ''}")
    c2.metric("7-Day Workouts", f"{completed_workouts}/7")
    c3.metric("Hydration Days", f"{water_days}/7")
    c4.metric("Sleep Goal Days", f"{sleep_days}/7")

    # Simple habit heatmap-like row using the existing HTML card style.
    cells = ""
    for d, item in days:
        workout = bool(item["workout"])
        water_ok = item["water"] >= settings["water_goal"]
        sleep_ok = item["sleep"] >= settings["sleep_goal"]
        status = "✓" if workout else "•"
        cells += f"""
        <div style="flex:1;min-width:80px;padding:14px 8px;text-align:center;
                    border:1px solid {'#2ED4C2' if workout else '#24384D'};
                    border-radius:12px;background:{'#0D2B2D' if workout else '#0A1726'};">
            <div style="font-size:12px;color:#9DB0C2;">{d.strftime('%a')}</div>
            <div style="font-size:20px;margin:6px 0;color:{'#2ED4C2' if workout else '#6D7E90'};">{status}</div>
            <div style="font-size:10px;color:#708397;">W {item['water']} • S {item['sleep']:.1f}h</div>
        </div>
        """

    html(f"""
    <div style="display:flex;gap:10px;flex-wrap:wrap;margin:10px 0 24px;">
        {cells}
    </div>
    """)

    # ---------------- INTELLIGENCE ----------------
    workout_progress = min(100, round((completed_workouts / settings["workout_goal"]) * 100))
    hydration_progress = min(100, round((water_days / 7) * 100))
    sleep_progress = min(100, round((sleep_days / 7) * 100))
    habit_score = round((workout_progress + hydration_progress + sleep_progress) / 3)

    if streak >= 5:
        insight = "Strong consistency is building momentum. Keep the routine sustainable."
    elif completed_workouts >= settings["workout_goal"]:
        insight = "You have reached your weekly workout target. Focus on recovery and consistency."
    elif water_days < 4:
        insight = "Hydration is the biggest gap in your current 7-day pattern."
    elif sleep_days < 4:
        insight = "Sleep consistency is the main habit to improve this week."
    else:
        insight = "You are building a routine. Small, repeatable actions will improve your consistency."

    left, right = st.columns([1.4, 1])
    with left:
        html(f"""
        <div class="section-heading">
            <div class="section-title">Habit Progress</div>
            <div class="section-subtitle">Calculated from your current 7-day activity</div>
        </div>
        <div class="action-card">
            <div class="action-icon">📈</div>
            <div class="action-title">Consistency Score: {habit_score}/100</div>
            <div class="action-text">Workout {workout_progress}% • Hydration {hydration_progress}% • Sleep {sleep_progress}%</div>
        </div>
        """)
    with right:
        html(f"""
        <div class="motivation">
            <div class="motivation-label">✦ HABIT INSIGHT</div>
            <div class="motivation-text">{insight}</div>
            <div class="motivation-sub">Your habit score is a consistency indicator, not a medical measurement.</div>
        </div>
        """)

elif page == "📊  Performance Analytics":

    # The database is the source of truth; session state keeps the table responsive.
    if "performance_history" not in st.session_state:
        st.session_state.performance_history = []
    persisted_workouts = load_user_workouts(limit=100)
    if persisted_workouts:
        st.session_state.performance_history = [{
            "Exercise": row.get("exercise", ""),
            "Reps / Hold": row.get("hold_seconds", 0) if row.get("exercise") == "Plank" else row.get("reps", 0),
            "Score": row.get("form_score", 0),
            "Angle": row.get("joint_angle") or 0,
            "Duration": f"{int(row.get('duration_seconds', 0) or 0)//60}m {int(row.get('duration_seconds', 0) or 0)%60}s",
        } for row in reversed(persisted_workouts)]

    html("""
    <div class="header-container">
        <div>
            <div class="eyebrow">POSE-TO-PERFORMANCE • WORKOUT INTELLIGENCE</div>
            <div class="page-title">Performance <span>Analytics</span></div>
            <div class="page-description">
                Turn your live pose analysis into measurable workout performance,
                form quality and session progress.
            </div>
        </div>
    </div>
    """)

    with trainer_lock:
        current_exercise = trainer_state["exercise"]
        current_reps = trainer_state["reps"]
        current_score = trainer_state["score"]
        current_angle = trainer_state["angle"]
        current_feedback = trainer_state["feedback"]
        session_start = trainer_state["session_start"]

    duration = 0
    if session_start:
        duration = max(0, int(time.time() - session_start))

    mins = duration // 60
    secs = duration % 60
    duration_text = f"{mins}m {secs}s"

    # Current session metrics.
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Exercise", current_exercise)
    with c2:
        if current_exercise == "Plank":
            st.metric("Hold Time", f"{current_reps}s")
        else:
            st.metric("Repetitions", current_reps)
    with c3:
        st.metric("Form Score", f"{current_score}/100")
    with c4:
        st.metric("Session Time", duration_text)

    html(f"""
    <div class="hero">
        <div class="hero-label">CURRENT SESSION ANALYSIS</div>
        <div class="hero-title">Your movement quality: <span style="color:#2ED4C2;">{current_score}/100</span></div>
        <div class="hero-text">
            VitalIQ combines repetition/hold performance, pose quality and joint-angle
            information from the AI Gym Trainer to create this performance snapshot.
        </div>
        <div class="hero-chip">● {current_exercise.upper()} • LIVE DATA</div>
    </div>
    """)

    left, right = st.columns([1.4, 1])

    with left:
        html(f"""
        <div class="section-heading">
            <div class="section-title">Form & Movement Analysis</div>
            <div class="section-subtitle">Based on the latest pose frames</div>
        </div>
        <div class="action-card">
            <div class="action-icon">📐</div>
            <div class="action-title">Joint Angle</div>
            <div class="action-text">Latest measured angle: {current_angle}°</div>
        </div>
        <div class="action-card">
            <div class="action-icon">🎯</div>
            <div class="action-title">AI Form Feedback</div>
            <div class="action-text">{current_feedback}</div>
        </div>
        """)

    with right:
        html(f"""
        <div class="motivation">
            <div class="motivation-label">✦ PERFORMANCE INSIGHT</div>
            <div class="motivation-text">
                {'Excellent form consistency. Keep the movement controlled.' if current_score >= 85 else 'Focus on controlled movement and maintain the recommended posture.' if current_score >= 60 else 'Improve body positioning before increasing workout intensity.'}
            </div>
            <div class="motivation-sub">Performance is based on pose quality detected by the camera.</div>
        </div>
        """)

    st.markdown("### 💾 Save Workout Session")
    st.caption("Save the current exercise snapshot to build your personal performance history.")

    if st.button("Save Current Session", type="primary"):
        record = {
            "Exercise": current_exercise,
            "Reps / Hold": current_reps,
            "Score": current_score,
            "Angle": current_angle,
            "Duration": duration_text,
        }
        st.session_state.performance_history.append(record)
        save_ok, save_message = save_workout_session(current_exercise, current_reps, current_score, current_angle, duration, current_feedback)
        if save_ok:
            st.success(save_message)
        else:
            st.error(save_message)

    if st.session_state.performance_history:
        html("""
        <div class="section-heading">
            <div class="section-title">Workout History</div>
            <div class="section-subtitle">Saved sessions from your account</div>
        </div>
        """)
        st.dataframe(
            st.session_state.performance_history,
            use_container_width=True,
            hide_index=True,
        )

        scores = [int(x["Score"]) for x in st.session_state.performance_history]
        reps_values = [int(x["Reps / Hold"]) for x in st.session_state.performance_history]
        avg_score = round(sum(scores) / len(scores), 1)
        total_reps = sum(reps_values)

        a, b, c = st.columns(3)
        a.metric("Sessions Saved", len(scores))
        b.metric("Average Score", f"{avg_score}/100")
        c.metric("Total Reps / Holds", total_reps)
    else:
        st.info("No saved sessions yet. Start an exercise in AI Gym Trainer, then save the result here.")


elif page == "📍  Gym Finder":

    # --------------------------------------------------------
    # OPENSTREETMAP GYM FINDER
    # --------------------------------------------------------
    if "gym_results" not in st.session_state:
        st.session_state.gym_results = []
    if "gym_location" not in st.session_state:
        st.session_state.gym_location = None
    if "gym_location_label" not in st.session_state:
        st.session_state.gym_location_label = ""

    html("""
    <div class="header-container">
        <div>
            <div class="eyebrow">OPENSTREETMAP • LOCAL FITNESS DISCOVERY</div>
            <div class="page-title">Gym <span>Finder</span></div>
            <div class="page-description">
                Find real nearby gyms and fitness locations from OpenStreetMap,
                calculate their distance and view them on a live map.
            </div>
        </div>
    </div>
    """)

    html("""
    <div class="hero">
        <div class="hero-label">NO LLM REQUIRED</div>
        <div class="hero-title">Discover fitness locations using <span style="color:#2ED4C2;">real map data.</span></div>
        <div class="hero-text">
            Enter a city, neighbourhood, landmark or address. VitalIQ geocodes
            the location with OpenStreetMap and searches nearby fitness places.
        </div>
        <div class="hero-chip">● OPENSTREETMAP DATA SOURCE</div>
    </div>
    """)

    st.markdown("### 📍 Search Location")
    location_col, radius_col, search_col = st.columns([2.5, 1, 1])

    with location_col:
        location_query = st.text_input(
            "City / Area / Landmark",
            placeholder="Example: Hassan, Karnataka or Bengaluru, Karnataka",
            key="gym_location_query",
        )

    with radius_col:
        radius_km = st.selectbox(
            "Search Radius",
            [1, 2, 3, 5, 10],
            index=2,
            format_func=lambda x: f"{x} km",
            key="gym_radius",
        )

    with search_col:
        st.markdown("<div style='height:29px'></div>", unsafe_allow_html=True)
        search_gym_button = st.button("🔎 Find Gyms", type="primary", use_container_width=True)

    if search_gym_button:
        if not location_query.strip():
            st.warning("Enter a city, area, landmark or address first.")
        else:
            try:
                with st.spinner("Finding your location on OpenStreetMap..."):
                    location = geocode_location(location_query.strip())

                if not location:
                    st.warning("OpenStreetMap could not find that location. Try a more specific place name.")
                else:
                    with st.spinner(f"Searching for gyms within {radius_km} km..."):
                        results = search_osm_gyms(
                            location["lat"],
                            location["lon"],
                            int(radius_km * 1000),
                        )

                    st.session_state.gym_location = location
                    st.session_state.gym_location_label = location["display_name"]
                    st.session_state.gym_results = results

                    if results:
                        st.success(f"Found {len(results)} fitness locations near {location['display_name']}.")
                    else:
                        st.info("No mapped gyms were found in that radius. Try increasing the search radius.")

            except requests.exceptions.Timeout:
                st.error("The OpenStreetMap service took too long to respond. Please try again.")
            except requests.exceptions.RequestException as exc:
                st.error(f"OpenStreetMap search failed: {type(exc).__name__}. Please try again in a moment.")
            except Exception as exc:
                st.error(f"Gym search could not be completed: {type(exc).__name__}.")

    results = st.session_state.gym_results
    location = st.session_state.gym_location

    if location and results:
        st.markdown("### 🗺️ Nearby Fitness Locations")

        map_points = pd.DataFrame([
            {"lat": location["lat"], "lon": location["lon"]}
        ] + [
            {"lat": gym["lat"], "lon": gym["lon"]}
            for gym in results
        ])
        st.map(map_points, latitude="lat", longitude="lon", use_container_width=True)
        st.caption("Map data and place information come from OpenStreetMap. The first marker represents your searched location.")

        st.markdown("### 🏋️ Results")
        st.caption(f"Sorted by distance from: {st.session_state.gym_location_label}")

        for index, gym in enumerate(results, start=1):
            distance_text = f"{gym['distance_km']:.2f} km away"
            address_text = gym["address"] or "Address not provided in OpenStreetMap"

            with st.container(border=True):
                a, b = st.columns([3.2, 1.1])
                with a:
                    st.markdown(f"### {index}. {gym['name']}")
                    st.write(f"**{gym['category']}**  •  {distance_text}")
                    st.caption(address_text)

                    details = []
                    if gym["opening_hours"]:
                        details.append(f"Hours: {gym['opening_hours']}")
                    if gym["phone"]:
                        details.append(f"Phone: {gym['phone']}")
                    if details:
                        st.caption(" • ".join(details))

                with b:
                    directions_url = (
                        "https://www.openstreetmap.org/directions?from="
                        f"{location['lat']},{location['lon']}&to={gym['lat']},{gym['lon']}"
                    )
                    st.link_button("🧭 Directions", directions_url, use_container_width=True)

                    osm_url = f"https://www.openstreetmap.org/{gym['osm_type']}/{gym['osm_id']}"
                    st.link_button("🌐 OSM Details", osm_url, use_container_width=True)

                    if gym["website"]:
                        st.link_button("🔗 Website", gym["website"], use_container_width=True)

    elif location and not results:
        html("""
        <div class="motivation">
            <div class="motivation-label">✦ NO RESULTS IN CURRENT RADIUS</div>
            <div class="motivation-text">Try a larger search radius.</div>
            <div class="motivation-sub">Not every gym is mapped in OpenStreetMap, so availability of results depends on local map coverage.</div>
        </div>
        """)
    else:
        html("""
        <div class="motivation">
            <div class="motivation-label">✦ HOW IT WORKS</div>
            <div class="motivation-text">Location → OpenStreetMap → Nearby gyms → Distance → Map</div>
            <div class="motivation-sub">This module uses map data rather than an LLM to identify nearby fitness locations.</div>
        </div>
        """)

else:

    html(f"""
    <div class="header-container">
        <div>
            <div class="eyebrow">VITALIQ AI</div>
            <div class="page-title">{page}</div>
            <div class="page-description">
                Intelligent tools designed to personalize your fitness journey.
            </div>
        </div>
    </div>
    """)

    html("""
    <div class="hero">
        <div class="hero-label">MODULE READY</div>
        <div class="hero-title">🚀 Intelligence layer coming next</div>
        <div class="hero-text">
            The visual foundation is ready. We are connecting the real AI
            functionality to this module step by step.
        </div>
        <div class="hero-chip">● UI READY</div>
    </div>
    """)

    st.info(
        "This module is currently under development. "
        "The AI Gym Trainer is the first live AI module being implemented."
    )

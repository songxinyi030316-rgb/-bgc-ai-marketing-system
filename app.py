"""AI Marketing Command Center prototype for BGC London.

Run with:
    python -m streamlit run app.py

This is a mock-only Streamlit prototype. It uses local data, simple scoring
logic, and session state to demonstrate a complete nonprofit marketing workflow.
"""

from __future__ import annotations

import base64
import html
from datetime import date, timedelta
from pathlib import Path
from urllib.parse import unquote

import streamlit as st
import streamlit.components.v1 as components


# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="BGC London | AI Marketing Command Center",
    page_icon="BGC",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------------------------
# CSS brand system
# ---------------------------------------------------------------------------

def load_css() -> None:
    """Apply a polished BGC-inspired marketing product visual system."""

    st.markdown(
        """
        <style>
            :root {
                --navy: #10313a;
                --teal: #0c4b4f;
                --green: #1f6f4a;
                --green-dark: #155a3c;
                --green-soft: #edf6f1;
                --yellow: #ffd234;
                --yellow-soft: #fff6cf;
                --ink: #1c2b2f;
                --muted: #607276;
                --line: #dfe8e4;
                --soft: #f6f8f7;
                --white: #ffffff;
            }

            .stApp {
                background: #ffffff;
                color: var(--ink);
                font-family: Inter, "Avenir Next", "Helvetica Neue", Arial, sans-serif;
            }

            .block-container {
                max-width: 1320px;
                padding-top: 1.25rem;
                padding-bottom: 3rem;
            }

            section[data-testid="stSidebar"] {
                background: #ffffff;
                border-right: 1px solid #E5ECE7;
                min-width: 280px !important;
                width: 280px !important;
                max-width: 280px !important;
                overflow-y: auto;
            }

            section[data-testid="stSidebar"] > div {
                width: 280px !important;
            }

            section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {
                padding: 24px 20px;
            }

            section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
                gap: 0.22rem !important;
            }

            section[data-testid="stSidebar"] [data-testid="stElementContainer"],
            section[data-testid="stSidebar"] .element-container {
                margin: 0 !important;
                overflow: visible !important;
            }

            .bgc-side-v2 {
                display: block;
                width: 100%;
            }

            .bgc-brand-v2 {
                padding: 0 0 18px;
                margin: 0 0 16px;
                border-bottom: 1px solid #E5ECE7;
            }

            .bgc-brand-top-v2 {
                display: flex;
                align-items: flex-start;
                justify-content: space-between;
                gap: 12px;
            }

            .bgc-brand-title-v2 {
                color: #10313a;
                font-size: 1.38rem;
                font-weight: 900;
                line-height: 1.1;
            }

            .bgc-brand-subtitle-v2 {
                color: #5d7073;
                font-size: 0.86rem;
                font-weight: 700;
                margin-top: 0.32rem;
                line-height: 1.25;
            }

            .bgc-dot-cluster-v2 {
                display: grid;
                grid-template-columns: repeat(2, 8px);
                gap: 5px;
                padding-top: 2px;
                flex: 0 0 auto;
            }

            .bgc-dot-cluster-v2 span {
                width: 8px;
                height: 8px;
                border-radius: 999px;
                background: #2F7A55;
                display: block;
            }

            .bgc-dot-cluster-v2 span:nth-child(4) {
                background: var(--yellow);
            }

            .bgc-user-card-v2 {
                background: #F8FAF7;
                border: 1px solid #E5ECE7;
                border-radius: 14px;
                padding: 0.72rem 0.78rem;
                margin: 0 0 8px;
                color: #10313a;
                box-shadow: none;
                font-size: 0.9rem;
                line-height: 1.25;
            }

            .bgc-user-label-v2 {
                color: #7A8A8D;
                font-size: 0.72rem;
                font-weight: 800;
                letter-spacing: 0.06em;
                text-transform: uppercase;
                margin-bottom: 0.25rem;
            }

            .bgc-user-email-v2 {
                color: #10313a;
                font-weight: 850;
                overflow-wrap: anywhere;
            }

            .bgc-user-dept-v2 {
                color: #607276;
                margin-top: 0.35rem;
                font-size: 0.84rem;
            }

            .bgc-nav-section-v2 {
                display: block;
                margin: 0 0 10px;
            }

            .bgc-nav-title-v2 {
                color: #7A8A8D;
                font-size: 11px;
                font-weight: 700;
                letter-spacing: 1.2px;
                text-transform: uppercase;
                margin: 0;
                padding: 1rem 0 0.45rem;
                line-height: 1.25;
                display: block;
                position: relative;
                z-index: 2;
                background: #ffffff;
            }

            .bgc-nav-link-v2,
            .bgc-nav-link-active-v2 {
                display: flex;
                align-items: center;
                gap: 10px;
                width: 100%;
                min-height: 44px;
                box-sizing: border-box;
                border-radius: 12px;
                margin: 0 0 6px;
                box-shadow: none;
                font-size: 15px;
                line-height: 1.2;
                white-space: normal;
            }

            .bgc-nav-link-v2 {
                background: #ffffff;
                color: #16343A;
                border: 1px solid transparent;
                font-weight: 600;
                padding: 10px 12px;
                text-decoration: none !important;
            }

            .bgc-nav-link-active-v2 {
                background: #EAF6EE;
                border: 1px solid #CFE6D8;
                color: #145C3B;
                font-weight: 700;
                padding: 10px 12px;
                text-decoration: none !important;
            }

            .bgc-nav-link-v2:hover {
                background: #F3F8F5;
                color: #145C3B;
                text-decoration: none !important;
            }

            .bgc-nav-icon-v2 {
                width: 20px;
                min-width: 20px;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                font-size: 16px;
                line-height: 1;
            }

            .bgc-nav-label-v2 {
                white-space: normal;
            }

            .bgc-flow-helper-v3 {
                background: linear-gradient(135deg, #f8fbf9 0%, #fffaf0 100%);
                border: 1px solid #dfe8e4;
                border-radius: 16px;
                padding: 0.8rem;
                margin: 0 0 0.9rem;
                color: #10313a;
            }

            .bgc-flow-helper-v3 strong {
                display: block;
                font-size: 0.86rem;
                margin-bottom: 0.25rem;
            }

            .bgc-flow-helper-v3 span {
                color: #607276;
                font-size: 0.8rem;
                line-height: 1.28;
                display: block;
            }

            .bgc-workflow-step-v3 {
                display: grid;
                grid-template-columns: 30px 1fr;
                gap: 0.7rem;
                align-items: start;
                width: 100%;
                box-sizing: border-box;
                border: 1px solid #e5ece7;
                border-radius: 14px;
                padding: 0.72rem;
                margin: 0 0 0.55rem;
                background: #ffffff;
            }

            .bgc-workflow-step-active-v3 {
                background: #eaf6ee;
                border-color: #cfe6d8;
                box-shadow: inset 4px 0 0 #2f7a55;
            }

            .bgc-step-number-v3 {
                width: 28px;
                height: 28px;
                border-radius: 999px;
                background: #eef3ef;
                color: #165c3a;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                font-size: 0.78rem;
                font-weight: 950;
            }

            .bgc-workflow-step-active-v3 .bgc-step-number-v3 {
                background: #2f7a55;
                color: #ffffff;
            }

            .bgc-step-title-v3 {
                color: #10313a;
                font-size: 0.92rem;
                font-weight: 900;
                line-height: 1.18;
                margin-bottom: 0.12rem;
            }

            .bgc-step-help-v3 {
                color: #607276;
                font-size: 0.76rem;
                line-height: 1.25;
            }

            .bgc-step-pages-v3 {
                color: #7a8a8d;
                font-size: 0.72rem;
                font-weight: 800;
                margin-top: 0.32rem;
            }

            .bgc-team-link-v3,
            .bgc-team-link-active-v3 {
                border-radius: 12px;
                min-height: 40px;
                padding: 0.62rem 0.72rem;
                margin-bottom: 0.45rem;
                display: flex;
                align-items: center;
                gap: 0.55rem;
                font-size: 0.9rem;
                font-weight: 750;
                line-height: 1.2;
            }

            .bgc-team-link-active-v3 {
                background: #eaf6ee;
                color: #145c3b;
                border: 1px solid #cfe6d8;
            }

            .bgc-sidebar-link-v4 {
                display: flex;
                align-items: center;
                gap: 0.62rem;
                min-height: 48px;
                border-radius: 16px;
                padding: 0.62rem 0.72rem;
                margin: 0 0 0.38rem;
                background: linear-gradient(135deg, #f7fbf8 0%, #ffffff 100%);
                border: 1px solid #dfeae3;
                color: #16343a;
                box-sizing: border-box;
                font-size: 0.9rem;
                font-weight: 820;
                line-height: 1.18;
                position: relative;
                z-index: 1;
            }

            .bgc-sidebar-link-active-v4 {
                background: linear-gradient(135deg, #eaf6ee 0%, #f8fbf9 100%);
                border-color: #bdddc9;
                color: #145c3b;
                box-shadow: inset 5px 0 0 #2f7a55, 0 8px 18px rgba(16, 49, 58, 0.055);
                font-weight: 900;
            }

            .bgc-sidebar-step-v4 {
                width: 24px;
                height: 24px;
                min-width: 24px;
                border-radius: 999px;
                background: #eef3ef;
                color: #165c3a;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                font-size: 0.72rem;
                font-weight: 950;
            }

            .bgc-sidebar-link-active-v4 .bgc-sidebar-step-v4 {
                background: #2f7a55;
                color: #ffffff;
            }

            .bgc-sidebar-link-sub-v4 {
                display: block;
                color: #738386;
                font-size: 0.72rem;
                font-weight: 700;
                margin-top: 0.08rem;
            }

            section[data-testid="stSidebar"] div.stButton > button {
                width: 100%;
                min-height: 46px;
                border-radius: 15px;
                background: linear-gradient(135deg, #f8fbf9 0%, #ffffff 100%);
                border: 1px solid #e0ebe5;
                color: #17573b;
                box-shadow: none;
                font-size: 0.86rem;
                font-weight: 850;
                padding: 0.58rem 0.68rem;
                justify-content: flex-start;
                margin-bottom: 0.18rem;
            }

            section[data-testid="stSidebar"] div.stButton {
                margin: 0 0 0.24rem !important;
            }

            section[data-testid="stSidebar"] div.stButton > button p {
                font-size: 0.88rem !important;
                font-weight: 850 !important;
                line-height: 1.15 !important;
                white-space: nowrap !important;
                overflow: hidden !important;
                text-overflow: ellipsis !important;
                margin: 0 !important;
            }

            section[data-testid="stSidebar"] div.stButton > button:hover {
                background: #eef8f2;
                border-color: #b9d9c6;
                color: #145c3b;
                box-shadow: none;
            }

            div[data-testid="stRadio"] {
                background: #ffffff;
                border: 1px solid #e5ece7;
                border-radius: 16px;
                padding: 0.55rem 0.7rem;
                box-shadow: 0 8px 18px rgba(16, 49, 58, 0.035);
                margin-bottom: 0.85rem;
            }

            div[data-testid="stRadio"] label p {
                font-size: 0.94rem !important;
                font-weight: 800 !important;
            }

            .mode-helper-card {
                background: linear-gradient(135deg, #f5f9f6 0%, #fffaf0 100%);
                border: 1px solid #dfe8e4;
                border-radius: 18px;
                padding: 1rem;
                margin: 0.5rem 0 1rem;
                box-shadow: 0 10px 24px rgba(16, 49, 58, 0.045);
            }

            .planner-color-strip {
                display: grid;
                grid-template-columns: repeat(4, minmax(0, 1fr));
                gap: 0.8rem;
                margin: 0.8rem 0 1rem;
            }

            .planner-color-card {
                border-radius: 18px;
                padding: 1rem;
                border: 1px solid #dfe8e4;
                box-shadow: 0 10px 24px rgba(16, 49, 58, 0.045);
                min-height: 112px;
            }

            .planner-color-card strong {
                display: block;
                color: #10313a;
                font-size: 1rem;
                margin-bottom: 0.35rem;
            }

            .planner-color-card span {
                color: #607276;
                font-size: 0.86rem;
                line-height: 1.35;
            }

            .planner-card-rose { background: #fff4f5; border-color: #f4d0d4; }
            .planner-card-blue { background: #eef5ff; border-color: #cfddf4; }
            .planner-card-green { background: #edf8f2; border-color: #cfe6d8; }
            .planner-card-yellow { background: #fff8db; border-color: #eadb9c; }

            .bgc-selected-campaign-v2 {
                background: #F8FAF7;
                border: 1px solid #E5ECE7;
                border-radius: 12px;
                padding: 0.7rem 0.75rem;
                color: #10313a;
                font-weight: 750;
                line-height: 1.25;
                margin-bottom: 12px;
            }

            .command-header {
                position: relative;
                background: #ffffff;
                border-radius: 18px;
                color: var(--ink);
                padding: 1.35rem 1.5rem;
                margin-bottom: 1.6rem;
                overflow: hidden;
                border: 1px solid var(--line);
                box-shadow: 0 12px 30px rgba(16, 49, 58, 0.07);
            }

            .command-header::before {
                content: "";
                position: absolute;
                right: 1.4rem;
                top: 1rem;
                width: 86px;
                height: 72px;
                background:
                    radial-gradient(circle at 50% 12%, var(--green) 0 8px, transparent 9px),
                    radial-gradient(circle at 20% 62%, var(--green) 0 12px, transparent 13px),
                    radial-gradient(circle at 80% 62%, var(--green) 0 12px, transparent 13px),
                    radial-gradient(circle at 50% 92%, var(--yellow) 0 7px, transparent 8px);
                opacity: 0.8;
            }

            .command-header::after {
                content: "";
                position: absolute;
                right: -36px;
                bottom: -48px;
                width: 130px;
                height: 130px;
                border: 16px solid rgba(31, 111, 74, 0.08);
                border-radius: 50%;
            }

            .command-header h1 {
                color: var(--navy);
                font-size: 2rem;
                line-height: 1.1;
                margin: 0 0 0.4rem;
                max-width: 780px;
                letter-spacing: 0;
            }

            .command-header p {
                color: var(--muted);
                margin: 0;
                font-size: 1.03rem;
                max-width: 760px;
            }

            .dashboard-hero {
                position: relative;
                width: 100%;
                min-height: 280px;
                max-height: 300px;
                border-radius: 18px;
                overflow: hidden;
                margin: -0.35rem 0 1.45rem;
                background-size: cover;
                background-position: center;
                box-shadow: 0 18px 42px rgba(16, 49, 58, 0.12);
                border: 1px solid var(--line);
            }

            .dashboard-hero::before {
                content: "";
                position: absolute;
                inset: 0;
                background: linear-gradient(90deg, rgba(12, 75, 79, 0.76) 0%, rgba(12, 75, 79, 0.44) 34%, rgba(12, 75, 79, 0.10) 64%, rgba(12, 75, 79, 0.02) 100%);
            }

            .dashboard-hero-content {
                position: absolute;
                left: 1.35rem;
                top: 50%;
                transform: translateY(-50%);
                max-width: 520px;
                padding: 1.05rem 1.15rem;
                border-radius: 16px;
                background: rgba(16, 49, 58, 0.34);
                border: 1px solid rgba(255, 255, 255, 0.18);
                backdrop-filter: blur(2px);
            }

            .dashboard-hero h2 {
                color: var(--yellow);
                font-size: 2.05rem;
                line-height: 1.08;
                margin: 0 0 0.35rem;
                letter-spacing: 0;
            }

            .dashboard-hero p {
                color: #ffffff;
                font-size: 1.08rem;
                margin: 0;
            }

            .hero-pill {
                display: inline-block;
                margin-top: 0.9rem;
                padding: 0.34rem 0.7rem;
                border-radius: 999px;
                background: rgba(255, 255, 255, 0.92);
                color: var(--green-dark);
                font-size: 0.78rem;
                font-weight: 900;
                border: 1px solid rgba(255, 255, 255, 0.6);
            }

            .dashboard-hero-placeholder {
                background:
                    radial-gradient(circle at 85% 20%, rgba(31, 111, 74, 0.16), transparent 28%),
                    radial-gradient(circle at 10% 85%, rgba(255, 210, 52, 0.18), transparent 25%),
                    #f6f8f7;
            }

            .header-eyebrow {
                color: var(--green-dark);
                font-weight: 900;
                letter-spacing: 0.06em;
                text-transform: uppercase;
                font-size: 0.76rem;
                margin-bottom: 0.45rem;
            }

            .green-band {
                background: #ffffff;
                color: var(--ink);
                border-radius: 16px;
                padding: 1.1rem;
                border: 1px solid var(--line);
                border-left: 7px solid var(--green);
                box-shadow: 0 10px 24px rgba(16, 49, 58, 0.06);
            }

            .green-band h2, .green-band h3, .green-band p {
                color: var(--navy);
                margin-top: 0;
            }

            .card {
                background: var(--white);
                border: 1px solid var(--line);
                border-radius: 14px;
                padding: 1rem;
                min-height: 118px;
                box-shadow: 0 8px 22px rgba(16, 49, 58, 0.055);
            }

            .card-green {
                background: #ffffff;
                border: 1px solid #cdded5;
                border-left: 5px solid var(--green);
                border-radius: 14px;
                padding: 1rem;
                min-height: 124px;
                box-shadow: 0 8px 22px rgba(16, 49, 58, 0.055);
            }

            .card-yellow {
                background: #ffffff;
                border: 1px solid #f1dd87;
                border-left: 5px solid var(--yellow);
                border-radius: 14px;
                padding: 1rem;
                min-height: 124px;
                box-shadow: 0 8px 22px rgba(16, 49, 58, 0.055);
            }

            .panel-card {
                background: #ffffff;
                border: 1px solid var(--line);
                border-radius: 18px;
                padding: 1.15rem;
                box-shadow: 0 12px 30px rgba(16, 49, 58, 0.065);
            }

            .form-section-title {
                color: var(--green-dark);
                font-size: 0.82rem;
                font-weight: 950;
                letter-spacing: 0.06em;
                text-transform: uppercase;
                margin: 0.9rem 0 0.45rem;
            }

            .helper-text {
                color: var(--muted);
                font-size: 0.82rem;
                margin: -0.35rem 0 0.65rem;
            }

            .chip {
                display: inline-block;
                border-radius: 999px;
                padding: 0.22rem 0.55rem;
                margin: 0.12rem 0.16rem 0.12rem 0;
                background: var(--soft);
                border: 1px solid var(--line);
                color: var(--navy);
                font-size: 0.76rem;
                font-weight: 850;
            }

            .check-row {
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 0.75rem;
                padding: 0.52rem 0;
                border-bottom: 1px solid #edf1ef;
            }

            .check-row:last-child {
                border-bottom: none;
            }

            .check-ok {
                color: var(--green-dark);
                font-weight: 950;
            }

            .check-warn {
                color: #7b5b00;
                font-weight: 950;
            }

            .radar-card {
                background: #ffffff;
                border: 1px solid var(--line);
                border-radius: 16px;
                padding: 1rem;
                box-shadow: 0 12px 28px rgba(16, 49, 58, 0.06);
            }

            .trend-signal {
                border: 1px solid var(--line);
                border-radius: 14px;
                padding: 0.85rem;
                background: var(--soft);
                min-height: 150px;
            }

            .matrix-card {
                background: #ffffff;
                border: 1px solid var(--line);
                border-radius: 14px;
                padding: 0.9rem;
                min-height: 138px;
                box-shadow: 0 8px 20px rgba(16, 49, 58, 0.045);
            }

            .matrix-act {
                border-top: 5px solid var(--green);
            }

            .matrix-build {
                border-top: 5px solid var(--yellow);
            }

            .trend-row {
                display: grid;
                grid-template-columns: auto 1.2fr 1fr 0.8fr;
                gap: 0.8rem;
                align-items: center;
                background: #ffffff;
                border: 1px solid var(--line);
                border-radius: 16px;
                padding: 0.85rem;
                margin-bottom: 0.7rem;
                box-shadow: 0 8px 22px rgba(16, 49, 58, 0.045);
            }

            .trend-icon {
                width: 42px;
                height: 42px;
                border-radius: 12px;
                display: flex;
                align-items: center;
                justify-content: center;
                background: var(--green-soft);
                color: var(--green-dark);
                font-size: 1.25rem;
            }

            .mini-progress {
                height: 8px;
                border-radius: 999px;
                background: #edf1ef;
                overflow: hidden;
                margin-top: 0.4rem;
            }

            .mini-progress span {
                display: block;
                height: 100%;
                border-radius: 999px;
                background: var(--green);
            }

            .rec-summary {
                background: #ffffff;
                border: 1px solid var(--line);
                border-radius: 18px;
                padding: 1.15rem;
                box-shadow: 0 12px 30px rgba(16, 49, 58, 0.06);
                margin-bottom: 1rem;
            }

            .mini-metric {
                background: var(--soft);
                border: 1px solid var(--line);
                border-radius: 14px;
                padding: 0.85rem;
            }

            .campaign-list-card {
                background: #ffffff;
                border: 1px solid var(--line);
                border-radius: 16px;
                padding: 0.9rem;
                margin-bottom: 0.65rem;
                box-shadow: 0 8px 20px rgba(16, 49, 58, 0.045);
            }

            .campaign-list-card-active {
                background: var(--green-soft);
                border-color: #bcd5c8;
                border-left: 5px solid var(--green);
            }

            .rank-pill {
                display: inline-block;
                min-width: 2.1rem;
                text-align: center;
                border-radius: 999px;
                padding: 0.2rem 0.48rem;
                background: var(--navy);
                color: white;
                font-weight: 950;
                font-size: 0.78rem;
                margin-right: 0.35rem;
            }

            .detail-panel {
                background: #ffffff;
                border: 1px solid var(--line);
                border-radius: 18px;
                padding: 1.2rem;
                box-shadow: 0 14px 34px rgba(16, 49, 58, 0.07);
            }

            .idea-card {
                background: #ffffff;
                border: 1px solid var(--line);
                border-top: 4px solid var(--yellow);
                border-radius: 14px;
                padding: 0.9rem;
                min-height: 130px;
                box-shadow: 0 8px 20px rgba(16, 49, 58, 0.045);
            }

            .recommendation-hero-card {
                background: #ffffff;
                border: 1px solid var(--line);
                border-radius: 20px;
                padding: 1.2rem;
                box-shadow: 0 16px 38px rgba(16, 49, 58, 0.075);
                margin-bottom: 1.1rem;
            }

            .campaign-recommendation-hero {
                min-height: 320px;
                max-height: 340px;
                border-radius: 26px;
                overflow: hidden;
                background-size: cover;
                background-position: center;
                box-shadow: 0 18px 44px rgba(16, 49, 58, 0.11);
                border: 1px solid #dfe8e4;
                margin: 0.4rem 0 1.3rem;
                position: relative;
                display: flex;
                align-items: center;
                padding: 1.45rem;
            }

            .campaign-recommendation-hero::after {
                content: "";
                position: absolute;
                inset: 0;
                background: linear-gradient(90deg, rgba(16, 49, 58, 0.76) 0%, rgba(16, 49, 58, 0.48) 38%, rgba(16, 49, 58, 0.06) 78%);
                pointer-events: none;
            }

            .campaign-recommendation-hero-content {
                position: relative;
                z-index: 1;
                max-width: 560px;
                background: rgba(255, 255, 255, 0.13);
                border: 1px solid rgba(255, 255, 255, 0.24);
                border-radius: 22px;
                padding: 1.15rem 1.2rem;
                backdrop-filter: blur(4px);
            }

            .campaign-recommendation-hero-content h2 {
                color: var(--yellow);
                margin: 0 0 0.35rem;
                font-size: 2rem;
                line-height: 1.05;
                font-weight: 950;
                letter-spacing: -0.02em;
            }

            .campaign-recommendation-hero-content p {
                color: #ffffff;
                margin: 0 0 0.75rem;
                font-size: 1rem;
                line-height: 1.42;
                font-weight: 700;
            }

            .campaign-recommendation-hero-placeholder {
                background:
                    radial-gradient(circle at 88% 18%, rgba(255, 210, 52, 0.24), transparent 24%),
                    radial-gradient(circle at 72% 74%, rgba(31, 111, 74, 0.28), transparent 26%),
                    linear-gradient(135deg, #10313a 0%, #0c4b4f 100%);
            }

            .hero-metric-grid {
                display: grid;
                grid-template-columns: repeat(3, minmax(0, 1fr));
                gap: 0.75rem;
                margin: 0.85rem 0;
            }

            .hero-metric {
                background: var(--soft);
                border: 1px solid var(--line);
                border-radius: 14px;
                padding: 0.75rem;
            }

            .score-text {
                color: var(--navy);
                font-size: 1.55rem;
                font-weight: 950;
                line-height: 1;
            }

            .progress-row {
                display: grid;
                grid-template-columns: 130px 1fr 42px;
                gap: 0.65rem;
                align-items: center;
                margin: 0.55rem 0;
                color: var(--muted);
                font-size: 0.86rem;
                font-weight: 800;
            }

            .recommendation-grid-card {
                background: #ffffff;
                border: 1px solid var(--line);
                border-radius: 16px;
                padding: 0.95rem;
                min-height: 226px;
                box-shadow: 0 8px 20px rgba(16, 49, 58, 0.045);
                transition: transform 140ms ease, box-shadow 140ms ease, border-color 140ms ease;
                margin-bottom: 0.45rem;
            }

            .recommendation-grid-card:hover {
                transform: translateY(-2px);
                box-shadow: 0 12px 26px rgba(16, 49, 58, 0.08);
                border-color: #c7d8d0;
            }

            .recommendation-grid-card-active {
                background: var(--green-soft);
                border-color: #b9d3c5;
                box-shadow: 0 12px 28px rgba(16, 49, 58, 0.08);
            }

            .recommendation-card-top {
                display: flex;
                align-items: flex-start;
                justify-content: space-between;
                gap: 0.75rem;
                margin-bottom: 0.45rem;
            }

            .recommendation-card-title {
                color: var(--navy);
                font-weight: 950;
                line-height: 1.18;
            }

            .recommendation-card-meta {
                display: grid;
                grid-template-columns: repeat(2, minmax(0, 1fr));
                gap: 0.5rem;
                margin: 0.65rem 0 0.55rem;
            }

            .recommendation-card-chip {
                background: #f8faf8;
                border: 1px solid #e5ece7;
                border-radius: 12px;
                padding: 0.5rem 0.55rem;
                min-height: 58px;
            }

            div[class*="st-key-rec_secondary_actions"] div.stButton > button,
            div[class*="st-key-rec_select_button_"] div.stButton > button {
                background: #ffffff !important;
                border: 1px solid #cfe1d8 !important;
                color: var(--green-dark) !important;
                box-shadow: none !important;
                padding: 0.38rem 0.72rem !important;
                min-height: 2.35rem !important;
                font-size: 0.88rem !important;
            }

            div[class*="st-key-rec_secondary_actions"] div.stButton > button:hover,
            div[class*="st-key-rec_select_button_"] div.stButton > button:hover {
                background: var(--green-soft) !important;
                border-color: #b9d3c5 !important;
                color: var(--green-dark) !important;
                box-shadow: none !important;
            }

            div[class*="st-key-rec_select_button_"] div.stButton > button {
                width: auto !important;
                min-height: 2rem !important;
                padding: 0.26rem 0.62rem !important;
                border-radius: 999px !important;
                font-size: 0.78rem !important;
            }

            .indicator-dots {
                margin: 0.45rem 0;
            }

            .indicator-dot {
                display: inline-block;
                width: 8px;
                height: 8px;
                border-radius: 50%;
                margin-right: 0.28rem;
                background: var(--line);
            }

            .indicator-dot-on {
                background: var(--green);
            }

            .detail-grid {
                display: grid;
                grid-template-columns: repeat(2, minmax(0, 1fr));
                gap: 0.8rem;
                margin-top: 0.85rem;
            }

            .detail-item {
                background: var(--soft);
                border: 1px solid var(--line);
                border-radius: 14px;
                padding: 0.85rem;
            }

            .ad-idea-card {
                background: #ffffff;
                border: 1px solid var(--line);
                border-radius: 16px;
                padding: 0.95rem;
                min-height: 134px;
                box-shadow: 0 8px 20px rgba(16, 49, 58, 0.045);
            }

            .ad-idea-icon {
                font-size: 1.35rem;
                margin-bottom: 0.35rem;
            }

            .planner-focus-card {
                background: #ffffff;
                border: 1px solid var(--line);
                border-radius: 20px;
                padding: 1.2rem;
                box-shadow: 0 14px 34px rgba(16, 49, 58, 0.065);
                margin-bottom: 1rem;
            }

            .focus-action-card {
                background: #ffffff;
                border: 1px solid var(--line);
                border-left: 5px solid var(--green);
                border-radius: 16px;
                padding: 0.95rem;
                min-height: 132px;
                box-shadow: 0 8px 20px rgba(16, 49, 58, 0.045);
            }

            .strategy-card {
                background: var(--soft);
                border: 1px solid var(--line);
                border-radius: 14px;
                padding: 0.8rem;
                min-height: 96px;
            }

            .timeline-row {
                display: grid;
                grid-template-columns: 72px 1fr;
                gap: 0.85rem;
                align-items: stretch;
                margin-bottom: 0.65rem;
            }

            .timeline-day {
                background: var(--navy);
                color: white;
                border-radius: 14px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: 950;
                letter-spacing: 0.04em;
                min-height: 76px;
            }

            .timeline-card {
                background: #ffffff;
                border: 1px solid var(--line);
                border-radius: 14px;
                padding: 0.85rem;
                box-shadow: 0 7px 18px rgba(16, 49, 58, 0.045);
            }

            .planner-pipeline {
                background: var(--soft);
                border: 1px solid var(--line);
                border-radius: 16px;
                padding: 0.85rem;
                min-height: 230px;
            }

            .pipeline-title-row {
                display: flex;
                align-items: center;
                justify-content: space-between;
                margin-bottom: 0.6rem;
            }

            .pipeline-count {
                display: inline-block;
                min-width: 1.65rem;
                text-align: center;
                border-radius: 999px;
                background: #ffffff;
                border: 1px solid var(--line);
                color: var(--green-dark);
                font-weight: 950;
                font-size: 0.78rem;
                padding: 0.12rem 0.4rem;
            }

            .pipeline-content-card {
                background: #ffffff;
                border: 1px solid var(--line);
                border-radius: 12px;
                padding: 0.7rem;
                margin-bottom: 0.55rem;
                box-shadow: 0 5px 14px rgba(16, 49, 58, 0.04);
            }

            .bottleneck-panel {
                background: #ffffff;
                border: 1px solid #f1dd87;
                border-left: 5px solid var(--yellow);
                border-radius: 16px;
                padding: 1rem;
                box-shadow: 0 10px 24px rgba(16, 49, 58, 0.055);
            }

            .asset-filter-label {
                color: var(--muted);
                font-size: 0.76rem;
                font-weight: 950;
                letter-spacing: 0.06em;
                text-transform: uppercase;
                margin: 0.55rem 0 0.25rem;
            }

            .asset-filter-panel {
                background: #ffffff;
                border: 1px solid var(--line);
                border-radius: 18px;
                padding: 1rem 1.1rem;
                box-shadow: 0 10px 26px rgba(16, 49, 58, 0.055);
                margin-bottom: 1.2rem;
            }

            .asset-filter-panel h3 {
                margin: 0 0 0.2rem;
                color: var(--navy);
            }

            div[data-testid="stPills"] {
                margin: 0.4rem 0 1rem;
                background: #f8fbf9;
                border: 1px solid #e0ebe5;
                border-radius: 18px;
                padding: 0.45rem;
                box-shadow: 0 10px 22px rgba(16, 49, 58, 0.035);
            }

            div[data-testid="stPills"] button {
                background: #ffffff !important;
                border: 1px solid var(--line) !important;
                color: var(--ink) !important;
                box-shadow: none !important;
                padding: 0.56rem 0.9rem !important;
                min-height: 2.4rem !important;
                font-weight: 850 !important;
                border-radius: 999px !important;
            }

            div[data-testid="stPills"] button:hover {
                background: var(--green-soft) !important;
                border-color: #c7d9cf !important;
                color: var(--green-dark) !important;
                transform: none !important;
                box-shadow: none !important;
            }

            div[data-testid="stPills"] button[aria-pressed="true"],
            div[data-testid="stPills"] button[aria-selected="true"],
            div[data-testid="stPills"] button[aria-checked="true"],
            div[data-testid="stPills"] button[data-selected="true"],
            div[data-testid="stPills"] button[kind="primary"],
            div[data-testid="stPills"] button[data-baseweb="tag"][aria-selected="true"] {
                background: linear-gradient(135deg, #eaf6ee 0%, #fff8dc 100%) !important;
                border-color: #2f7a55 !important;
                color: var(--green-dark) !important;
                box-shadow: inset 0 0 0 1px rgba(47, 122, 85, 0.12) !important;
            }

            div[data-testid="stTabs"] [role="tablist"] {
                gap: 0.55rem;
                background: #f8fbf9;
                border: 1px solid #e0ebe5;
                border-radius: 18px;
                padding: 0.45rem;
                margin: 0.8rem 0 1.1rem;
                box-shadow: 0 10px 22px rgba(16, 49, 58, 0.035);
            }

            div[data-testid="stTabs"] [role="tab"] {
                border-radius: 999px !important;
                border: 1px solid #dfe8e4 !important;
                background: #ffffff !important;
                color: #16343a !important;
                padding: 0.42rem 0.9rem !important;
                min-height: 2.35rem !important;
            }

            div[data-testid="stTabs"] [role="tab"] p {
                font-weight: 850 !important;
                font-size: 0.92rem !important;
                color: inherit !important;
            }

            div[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
                background: linear-gradient(135deg, #eaf6ee 0%, #fff8dc 100%) !important;
                border-color: #2f7a55 !important;
                color: #145c3b !important;
                box-shadow: 0 6px 14px rgba(16, 49, 58, 0.06) !important;
            }

            div[data-testid="stTabs"] [role="tab"][aria-selected="true"] p {
                color: #145c3b !important;
            }

            div[data-testid="stTabs"] [role="tablist"] button::after {
                display: none !important;
            }

            div[data-testid="stExpander"] {
                border: 1px solid #dfe8e4 !important;
                border-radius: 16px !important;
                overflow: hidden;
                box-shadow: 0 8px 18px rgba(16, 49, 58, 0.035);
                margin-bottom: 0.78rem;
            }

            div[data-testid="stExpander"] details > summary {
                background: linear-gradient(135deg, #f8fbf9 0%, #fffaf0 100%) !important;
                min-height: 3rem;
                font-weight: 850 !important;
                color: #16343a !important;
            }

            .asset-card {
                background: #ffffff;
                border: 1px solid var(--line);
                border-radius: 18px;
                overflow: hidden;
                box-shadow: 0 12px 28px rgba(16, 49, 58, 0.065);
                min-height: 420px;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
            }

            .asset-grid {
                display: grid;
                grid-template-columns: repeat(3, minmax(0, 1fr));
                gap: 24px;
                align-items: stretch;
                margin-top: 0.85rem;
            }

            .asset-preview {
                position: relative;
                height: 180px;
                background:
                    radial-gradient(circle at 28% 24%, rgba(31, 111, 74, 0.18), transparent 18%),
                    radial-gradient(circle at 74% 32%, rgba(255, 210, 52, 0.22), transparent 18%),
                    linear-gradient(135deg, #f3f6f5 0%, #e8eeee 100%);
                display: flex;
                align-items: center;
                justify-content: center;
                color: var(--muted);
                font-weight: 900;
            }

            .asset-preview-icon {
                font-size: 2rem;
                display: block;
                text-align: center;
                margin-bottom: 0.2rem;
            }

            .asset-suggestion-strip {
                position: absolute;
                left: 0.65rem;
                right: 0.65rem;
                bottom: 0.65rem;
                background: rgba(16, 49, 58, 0.78);
                color: white;
                border-radius: 12px;
                padding: 0.48rem 0.6rem;
                font-size: 0.78rem;
                font-weight: 750;
            }

            .asset-body {
                padding: 0.95rem 1rem 0.75rem;
                flex: 1;
                display: flex;
                flex-direction: column;
                gap: 0.65rem;
            }

            .asset-title {
                color: var(--navy);
                font-weight: 950;
                line-height: 1.22;
                min-height: 2.45rem;
            }

            .asset-best-for {
                color: var(--green-dark);
                background: #f1f8f4;
                border: 1px solid #d5e7dc;
                border-radius: 12px;
                padding: 0.58rem 0.65rem;
                font-size: 0.82rem;
                line-height: 1.3;
                font-weight: 800;
            }

            .asset-tags-row {
                display: flex;
                flex-wrap: wrap;
                align-items: center;
                gap: 0.28rem;
                margin-top: auto;
            }

            .asset-card-footer {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 0.55rem;
                padding: 0.85rem 1rem 1rem;
                border-top: 1px solid #e7eeeb;
                background: #fbfdfc;
            }

            .asset-footer-button {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                min-height: 38px;
                border-radius: 12px;
                border: 1px solid #cfe1d8;
                color: var(--green-dark) !important;
                background: #ffffff;
                font-size: 0.84rem;
                font-weight: 900;
                text-decoration: none !important;
                transition: background 0.16s ease, border-color 0.16s ease;
            }

            .asset-footer-button:hover {
                background: var(--green-soft);
                border-color: #b8d7c5;
                color: var(--green-dark) !important;
                text-decoration: none !important;
            }

            .asset-footer-button-primary {
                background: var(--yellow);
                border-color: #e4bb18;
                color: var(--navy) !important;
            }

            .asset-footer-button-primary:hover {
                background: #ffe06f;
                border-color: #d5ad14;
                color: var(--navy) !important;
            }

            .asset-detail-card {
                background: #ffffff;
                border: 1px solid var(--line);
                border-radius: 20px;
                padding: 1rem;
                box-shadow: 0 14px 34px rgba(16, 49, 58, 0.07);
                margin-top: 1rem;
            }

            .asset-large-preview {
                aspect-ratio: 16 / 9;
                border-radius: 16px;
                background:
                    radial-gradient(circle at 25% 25%, rgba(31, 111, 74, 0.18), transparent 16%),
                    radial-gradient(circle at 72% 30%, rgba(255, 210, 52, 0.22), transparent 18%),
                    linear-gradient(135deg, #f6f8f7 0%, #e6ece9 100%);
                border: 1px solid var(--line);
                display: flex;
                align-items: center;
                justify-content: center;
                color: var(--muted);
                font-weight: 950;
            }

            .selected-asset-card {
                background: #ffffff;
                border: 1px solid #cdded5;
                border-left: 5px solid var(--green);
                border-radius: 16px;
                padding: 0.9rem;
                box-shadow: 0 8px 22px rgba(16, 49, 58, 0.055);
                margin-bottom: 1rem;
            }

            .calendar-header-card {
                background: #ffffff;
                border: 1px solid var(--line);
                border-radius: 18px;
                padding: 1rem 1.1rem;
                box-shadow: 0 12px 30px rgba(16, 49, 58, 0.06);
                margin-bottom: 1rem;
            }

            .calendar-day-card {
                background: #ffffff;
                border: 1px solid var(--line);
                border-radius: 16px;
                padding: 0.72rem;
                min-height: 360px;
                box-shadow: 0 8px 20px rgba(16, 49, 58, 0.05);
            }

            .calendar-day-today {
                background: #f2f7f4;
                border-color: var(--green);
                box-shadow: 0 10px 24px rgba(16, 49, 58, 0.07);
            }

            .calendar-day-label {
                color: var(--navy);
                font-weight: 950;
                font-size: 0.95rem;
                padding-bottom: 0.55rem;
                border-bottom: 1px solid var(--line);
                margin-bottom: 0.65rem;
            }

            .calendar-content-block {
                background: var(--soft);
                border: 1px solid var(--line);
                border-left: 4px solid var(--green);
                border-radius: 12px;
                padding: 0.58rem;
                margin-bottom: 0.5rem;
                min-height: 92px;
            }

            .calendar-content-block strong {
                color: var(--navy);
                display: block;
                margin: 0.3rem 0 0.12rem;
                line-height: 1.2;
            }

            .calendar-meta-row {
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 0.35rem;
                margin-top: 0.4rem;
                color: var(--muted);
                font-size: 0.76rem;
                font-weight: 850;
            }

            .priority-dot {
                display: inline-block;
                width: 8px;
                height: 8px;
                border-radius: 50%;
                margin-right: 0.3rem;
                background: var(--line);
            }

            .priority-high {
                background: var(--yellow);
            }

            .priority-medium {
                background: var(--green);
            }

            .campaign-structure {
                background: #ffffff;
                border: 1px solid var(--line);
                border-radius: 18px;
                padding: 1rem;
                box-shadow: 0 12px 30px rgba(16, 49, 58, 0.06);
                margin-bottom: 1rem;
            }

            .campaign-structure-grid {
                display: grid;
                grid-template-columns: 1.05fr 1.4fr 1fr;
                gap: 0.9rem;
                align-items: start;
            }

            .week-summary-card {
                background: #ffffff;
                border: 1px solid var(--line);
                border-radius: 18px;
                padding: 1rem;
                box-shadow: 0 12px 30px rgba(16, 49, 58, 0.06);
                margin-top: 1.1rem;
            }

            .weekly-focus-card {
                background: #ffffff;
                border: 1px solid var(--line);
                border-left: 6px solid var(--green);
                border-radius: 20px;
                padding: 1.35rem;
                box-shadow: 0 14px 34px rgba(16, 49, 58, 0.07);
                margin-bottom: 1.15rem;
            }

            .weekly-focus-grid {
                display: grid;
                grid-template-columns: 1.25fr 0.75fr;
                gap: 1.2rem;
                align-items: center;
            }

            .planning-action-card {
                background: #ffffff;
                border: 1px solid var(--line);
                border-radius: 18px;
                padding: 1rem;
                min-height: 150px;
                box-shadow: 0 10px 26px rgba(16, 49, 58, 0.06);
            }

            .planning-action-instagram {
                background: linear-gradient(135deg, #fff7f7 0%, #ffffff 100%);
                border-left: 5px solid #e89aa3;
            }

            .planning-action-facebook {
                background: linear-gradient(135deg, #f2f7ff 0%, #ffffff 100%);
                border-left: 5px solid #8fb4e8;
            }

            .planning-action-google {
                background: linear-gradient(135deg, #fff9df 0%, #ffffff 100%);
                border-left: 5px solid #e4c85d;
            }

            .planning-action-partner {
                background: linear-gradient(135deg, #f3faf6 0%, #ffffff 100%);
                border-left: 5px solid #9fc9ac;
            }

            .planning-action-card h3 {
                margin: 0.35rem 0 0.35rem;
                color: var(--navy);
                font-size: 1.05rem;
            }

            .planning-meta {
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 0.65rem;
                margin-top: 0.8rem;
                color: var(--muted);
                font-size: 0.82rem;
                font-weight: 850;
            }

            .timeline-card {
                background: #ffffff;
                border: 1px solid var(--line);
                border-radius: 18px;
                padding: 1rem;
                box-shadow: 0 10px 26px rgba(16, 49, 58, 0.055);
                margin-top: 1.1rem;
            }

            .timeline-row {
                display: grid;
                grid-template-columns: repeat(5, 1fr);
                gap: 0.8rem;
                margin-top: 0.8rem;
            }

            .timeline-day {
                background: var(--soft);
                border: 1px solid var(--line);
                border-radius: 14px;
                padding: 0.75rem;
                text-align: center;
                color: var(--navy);
                font-weight: 900;
            }

            .timeline-day-main {
                background: #fff8dc;
                border-color: #e9d46c;
            }

            .timeline-dots {
                display: block;
                color: var(--green);
                font-size: 1rem;
                letter-spacing: 0.08em;
                margin-top: 0.25rem;
            }

            .pipeline-summary-grid {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 0.8rem;
                margin-top: 1.1rem;
            }

            .pipeline-summary-item {
                background: #ffffff;
                border: 1px solid var(--line);
                border-radius: 16px;
                padding: 0.9rem;
                box-shadow: 0 8px 20px rgba(16, 49, 58, 0.045);
            }

            .pipeline-summary-item strong {
                color: var(--navy);
                font-size: 1.6rem;
                display: block;
                line-height: 1;
            }

            .kpi-label {
                color: var(--muted);
                font-size: 0.76rem;
                font-weight: 900;
                letter-spacing: 0.05em;
                text-transform: uppercase;
                margin-bottom: 0.38rem;
            }

            .kpi-value {
                color: var(--navy);
                font-size: 2rem;
                font-weight: 950;
                line-height: 1;
            }

            .muted {
                color: var(--muted);
            }

            .badge {
                display: inline-block;
                border-radius: 999px;
                padding: 0.22rem 0.58rem;
                margin: 0.12rem 0.18rem 0.12rem 0;
                font-size: 0.76rem;
                font-weight: 900;
                border: 1px solid transparent;
            }

            .badge-green {
                background: var(--green);
                color: white;
                border-color: var(--green);
            }

            .badge-softgreen {
                background: var(--green-soft);
                color: var(--green-dark);
                border-color: #bfe9cc;
            }

            .badge-yellow {
                background: var(--yellow);
                color: var(--navy);
                border-color: #e4bb18;
            }

            .badge-navy {
                background: #e8f0f1;
                color: var(--navy);
                border-color: #cfdfe0;
            }

            .badge-red {
                background: #ffe8e8;
                color: #9b2c2c;
                border-color: #ffc9c9;
            }

            .workflow-step {
                border: 1px solid var(--line);
                background: #ffffff;
                border-radius: 14px;
                padding: 0.78rem;
                min-height: 112px;
                position: relative;
                overflow: hidden;
                box-shadow: 0 8px 18px rgba(16, 49, 58, 0.045);
            }

            .workflow-step-active {
                border-color: #b8d1c4;
                border-top: 5px solid var(--green);
                background: var(--green-soft);
            }

            .workflow-icon {
                font-size: 1.1rem;
                margin-bottom: 0.3rem;
            }

            .dashboard-section-label {
                color: var(--navy);
                font-size: 1.05rem;
                font-weight: 950;
                margin: 1.45rem 0 0.75rem;
                letter-spacing: -0.01em;
            }

            .dashboard-main-card {
                background:
                    radial-gradient(circle at 96% 10%, rgba(255, 210, 52, 0.18), transparent 28%),
                    linear-gradient(135deg, #ffffff 0%, #f8fbf9 100%);
                border: 1px solid #dfe8e4;
                border-left: 6px solid var(--green);
                border-radius: 22px;
                padding: 1.25rem 1.35rem;
                box-shadow: 0 16px 36px rgba(16, 49, 58, 0.07);
                min-height: 230px;
            }

            .dashboard-main-card h2 {
                margin: 0.18rem 0 0.6rem;
                color: var(--navy);
                font-size: 1.85rem;
                line-height: 1.05;
                letter-spacing: -0.02em;
            }

            .dashboard-mini-grid {
                display: grid;
                grid-template-columns: repeat(2, minmax(0, 1fr));
                gap: 0.75rem;
                margin-top: 0.95rem;
            }

            .dashboard-mini-metric {
                background: rgba(255, 255, 255, 0.78);
                border: 1px solid #e4ece8;
                border-radius: 14px;
                padding: 0.72rem 0.78rem;
            }

            .dashboard-action-panel {
                background: #ffffff;
                border: 1px solid #dfe8e4;
                border-radius: 22px;
                padding: 1.05rem;
                box-shadow: 0 16px 36px rgba(16, 49, 58, 0.06);
                min-height: 230px;
            }

            .dashboard-action-row {
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 0.75rem;
                background: #f8faf8;
                border: 1px solid #e5ece7;
                border-radius: 14px;
                padding: 0.72rem 0.78rem;
                margin-bottom: 0.55rem;
            }

            .dashboard-action-row:last-child {
                margin-bottom: 0;
            }

            .dashboard-kpi-card,
            .dashboard-priority-card,
            .dashboard-status-card {
                background: #ffffff;
                border: 1px solid #dfe8e4;
                border-radius: 18px;
                padding: 0.95rem;
                min-height: 118px;
                box-shadow: 0 12px 26px rgba(16, 49, 58, 0.055);
            }

            .dashboard-kpi-card {
                display: flex;
                align-items: center;
                gap: 0.8rem;
            }

            .dashboard-kpi-icon,
            .dashboard-priority-icon,
            .dashboard-status-icon {
                width: 42px;
                height: 42px;
                border-radius: 14px;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                background: var(--green-soft);
                color: var(--green-dark);
                font-size: 1.25rem;
                flex: 0 0 auto;
            }

            .dashboard-priority-card {
                border-top: 4px solid #d7e8dd;
            }

            .dashboard-priority-card strong,
            .dashboard-status-card strong {
                color: var(--navy);
                display: block;
                margin: 0.45rem 0 0.25rem;
                line-height: 1.2;
            }

            .dashboard-card-note {
                color: var(--muted);
                font-size: 0.86rem;
                line-height: 1.35;
            }

            .dashboard-flow-row {
                display: grid;
                grid-template-columns: repeat(5, minmax(0, 1fr));
                gap: 0.7rem;
                position: relative;
            }

            .dashboard-flow-card {
                background: #ffffff;
                border: 1px solid #dfe8e4;
                border-radius: 16px;
                padding: 0.82rem;
                min-height: 105px;
                box-shadow: 0 10px 22px rgba(16, 49, 58, 0.045);
            }

            .dashboard-flow-card strong {
                display: block;
                color: var(--navy);
                margin: 0.22rem 0 0.45rem;
                line-height: 1.2;
            }

            .dashboard-status-card {
                min-height: 112px;
            }

            div[class*="st-key-dashboard_recommended_card"] [data-testid="stVerticalBlockBorderWrapper"] {
                background:
                    radial-gradient(circle at 96% 10%, rgba(255, 210, 52, 0.18), transparent 26%),
                    linear-gradient(135deg, #f8fcf9 0%, #ffffff 48%, #fffaf0 100%);
                border: 1px solid #d7e7dd;
                border-left: 6px solid var(--green);
                border-radius: 24px;
                box-shadow: 0 18px 42px rgba(16, 49, 58, 0.075);
                padding: 0.35rem;
            }

            div[class*="st-key-dashboard_recommended_card"] h3 {
                color: var(--navy);
                font-size: 1.78rem;
                font-weight: 950;
                letter-spacing: -0.025em;
            }

            div[class*="st-key-dashboard_recommended_card"] [data-testid="stMetric"] {
                background: rgba(255, 255, 255, 0.72);
                border: 1px solid #e1ece6;
                border-radius: 16px;
                padding: 0.72rem 0.8rem;
            }

            div[class*="st-key-dashboard_recommended_card"] [data-testid="stMetricValue"] {
                color: var(--green-dark);
                font-weight: 950;
            }

            div[class*="st-key-dashboard_actions_panel"] [data-testid="stVerticalBlockBorderWrapper"],
            div[class*="st-key-dashboard_priorities_panel"] [data-testid="stVerticalBlockBorderWrapper"] {
                background: linear-gradient(135deg, #ffffff 0%, #f8fbf9 100%);
                border: 1px solid #dfe8e4;
                border-radius: 22px;
                box-shadow: 0 14px 32px rgba(16, 49, 58, 0.06);
            }

            div[class*="st-key-dashboard_action_row_"] [data-testid="stVerticalBlockBorderWrapper"] {
                background: #ffffff;
                border: 1px solid #e5ece7;
                border-radius: 16px;
                box-shadow: 0 8px 18px rgba(16, 49, 58, 0.04);
                padding: 0.15rem 0.2rem;
            }

            div[class*="st-key-dashboard_workflow_step_"] [data-testid="stVerticalBlockBorderWrapper"] {
                background:
                    radial-gradient(circle at 88% 10%, rgba(221, 238, 227, 0.75), transparent 30%),
                    #ffffff;
                border: 1px solid #dfe8e4;
                border-top: 4px solid #d7e8dd;
                border-radius: 18px;
                box-shadow: 0 10px 24px rgba(16, 49, 58, 0.045);
                min-height: 150px;
                height: 150px;
            }

            div[class*="st-key-dashboard_workflow_active"] [data-testid="stVerticalBlockBorderWrapper"] {
                background:
                    radial-gradient(circle at 86% 8%, rgba(255, 210, 52, 0.18), transparent 32%),
                    linear-gradient(135deg, #ffffff 0%, #fffaf0 100%);
                border-color: #eadb9c;
                border-top-color: var(--yellow);
                box-shadow: 0 14px 30px rgba(16, 49, 58, 0.07);
            }

            .workflow-connector {
                min-height: 150px;
                height: 150px;
                display: flex;
                align-items: center;
                justify-content: center;
                color: #9eb7aa;
                font-size: 1.35rem;
                font-weight: 900;
            }

            div[class*="st-key-dashboard_workflow_step_"] p,
            div[class*="st-key-dashboard_workflow_active"] p {
                white-space: nowrap !important;
                overflow: visible !important;
                font-size: 0.88rem !important;
                line-height: 1.22 !important;
                text-align: center !important;
                margin-left: auto !important;
                margin-right: auto !important;
            }

            div[class*="st-key-dashboard_workflow_step_"] [data-testid="stCaptionContainer"],
            div[class*="st-key-dashboard_workflow_active"] [data-testid="stCaptionContainer"] {
                white-space: nowrap !important;
                text-align: center !important;
            }

            div[class*="st-key-dashboard_workflow_step_"] [data-testid="stVerticalBlock"],
            div[class*="st-key-dashboard_workflow_active"] [data-testid="stVerticalBlock"] {
                min-height: 128px;
                display: flex !important;
                flex-direction: column !important;
                justify-content: center !important;
                align-items: center !important;
                text-align: center !important;
            }

            .dashboard-workflow-timeline {
                display: grid;
                grid-template-columns: 1fr 42px 1fr 42px 1fr 42px 1fr 42px 1fr;
                gap: 10px;
                align-items: center;
                margin: 0.45rem 0 1.35rem;
            }

            .dashboard-workflow-card-v2 {
                height: 150px;
                box-sizing: border-box;
                background:
                    radial-gradient(circle at 88% 10%, rgba(221, 238, 227, 0.68), transparent 30%),
                    #ffffff;
                border: 1px solid #dfe8e4;
                border-top: 4px solid #d7e8dd;
                border-radius: 18px;
                box-shadow: 0 10px 24px rgba(16, 49, 58, 0.045);
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                text-align: center;
                padding: 16px 12px;
                overflow: hidden;
            }

            .dashboard-workflow-card-v2-active {
                background:
                    radial-gradient(circle at 86% 8%, rgba(255, 210, 52, 0.18), transparent 32%),
                    linear-gradient(135deg, #ffffff 0%, #fffaf0 100%);
                border-color: #eadb9c;
                border-top-color: var(--yellow);
                box-shadow: 0 14px 30px rgba(16, 49, 58, 0.07);
            }

            .dashboard-workflow-step-v2 {
                color: #718083;
                font-size: 0.9rem;
                font-weight: 700;
                line-height: 1.2;
                margin-bottom: 0.62rem;
                white-space: nowrap;
            }

            .dashboard-workflow-title-v2 {
                color: var(--navy);
                font-size: 0.98rem;
                font-weight: 900;
                line-height: 1.15;
                margin-bottom: 0.72rem;
                white-space: nowrap;
            }

            .dashboard-workflow-status-v2 {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                border-radius: 999px;
                padding: 0.2rem 0.42rem;
                font-size: 0.84rem;
                font-weight: 800;
                line-height: 1.1;
                white-space: nowrap;
            }

            .dashboard-workflow-status-ready-v2 {
                color: #0b7a32;
                background: #dcfce7;
            }

            .dashboard-workflow-status-progress-v2 {
                color: #c2410c;
                background: #ffedd5;
            }

            .dashboard-workflow-status-needs-v2 {
                color: #6b7280;
                background: #e5e7eb;
            }

            .dashboard-workflow-arrow-v2 {
                height: 150px;
                display: flex;
                align-items: center;
                justify-content: center;
                color: #9eb7aa;
                font-size: 1.42rem;
                font-weight: 950;
            }

            div[class*="st-key-dashboard_quick_status_"] [data-testid="stVerticalBlockBorderWrapper"] {
                background: linear-gradient(135deg, #ffffff 0%, #f5f9f6 100%);
                border: 1px solid #dfe8e4;
                border-radius: 18px;
                box-shadow: 0 10px 24px rgba(16, 49, 58, 0.045);
                min-height: 104px;
            }

            div[class*="st-key-dashboard_quick_status_"] [data-testid="stMetricValue"] {
                color: var(--navy);
                font-size: 1.45rem;
                font-weight: 950;
            }

            div[class*="st-key-dashboard_priority_item_"] [data-testid="stVerticalBlockBorderWrapper"] {
                background: #f8fbf9;
                border: 1px solid #e1ece6;
                border-radius: 16px;
                box-shadow: none;
            }

            div[class*="st-key-region_intel_summary_"] [data-testid="stVerticalBlockBorderWrapper"],
            div[class*="st-key-region_intel_card_"] [data-testid="stVerticalBlockBorderWrapper"],
            div[class*="st-key-region_focus_panel"] [data-testid="stVerticalBlockBorderWrapper"] {
                background: linear-gradient(135deg, #ffffff 0%, #f6faf7 100%);
                border: 1px solid #dfe8e4;
                border-radius: 20px;
                box-shadow: 0 12px 28px rgba(16, 49, 58, 0.055);
            }

            div[class*="st-key-region_intel_summary_"] [data-testid="stVerticalBlockBorderWrapper"] {
                min-height: 118px;
            }

            div[class*="st-key-region_intel_card_"] [data-testid="stVerticalBlockBorderWrapper"] {
                min-height: 270px;
            }

            div[class*="st-key-region_intel_card_0"] [data-testid="stVerticalBlockBorderWrapper"] {
                border-left: 5px solid #7fb091;
            }

            div[class*="st-key-region_intel_card_1"] [data-testid="stVerticalBlockBorderWrapper"] {
                border-left: 5px solid #e0c85f;
            }

            div[class*="st-key-region_intel_card_2"] [data-testid="stVerticalBlockBorderWrapper"] {
                border-left: 5px solid #7aaeb0;
            }

            div[class*="st-key-region_intel_card_3"] [data-testid="stVerticalBlockBorderWrapper"] {
                border-left: 5px solid #a9c8b4;
            }

            div[class*="st-key-region_intel_card_4"] [data-testid="stVerticalBlockBorderWrapper"] {
                border-left: 5px solid #b8c8bd;
            }

            div[class*="st-key-region_focus_panel"] [data-testid="stVerticalBlockBorderWrapper"] {
                border-left: 5px solid var(--green);
                background:
                    radial-gradient(circle at 92% 8%, rgba(255, 210, 52, 0.13), transparent 26%),
                    linear-gradient(135deg, #ffffff 0%, #f3faf6 100%);
                min-height: 420px;
            }

            div[class*="st-key-shared_week_day_"] [data-testid="stVerticalBlockBorderWrapper"],
            div[class*="st-key-shared_month_day_"] [data-testid="stVerticalBlockBorderWrapper"] {
                background: #ffffff;
                border: 1px solid #dfe8e4;
                border-radius: 18px;
                box-shadow: 0 10px 24px rgba(16, 49, 58, 0.045);
                min-height: 248px;
            }

            div[class*="st-key-shared_month_day_"] [data-testid="stVerticalBlockBorderWrapper"] {
                min-height: 190px;
            }

            .calendar-grid {
                display: grid;
                grid-template-columns: repeat(7, minmax(0, 1fr));
                gap: 12px;
                width: 100%;
                margin-top: 0.8rem;
            }

            .calendar-weekday {
                color: var(--muted);
                font-size: 0.78rem;
                font-weight: 950;
                letter-spacing: 0.06em;
                text-transform: uppercase;
                padding: 0 0.35rem;
            }

            .calendar-day-cell {
                height: 135px;
                min-height: 135px;
                box-sizing: border-box;
                padding: 10px;
                border-radius: 16px;
                background: #ffffff;
                border: 1px solid #e2ece6;
                box-shadow: 0 8px 20px rgba(16, 49, 58, 0.04);
                overflow: hidden;
            }

            .calendar-day-empty {
                background: #f8faf9;
                border-style: dashed;
                box-shadow: none;
            }

            .calendar-day-today {
                border-color: #b8d8c4;
                background: #f5fbf7;
            }

            .calendar-day-number {
                color: var(--navy);
                font-size: 0.92rem;
                font-weight: 950;
                line-height: 1;
                margin-bottom: 0.45rem;
            }

            .calendar-event {
                border-radius: 10px;
                padding: 0.38rem 0.45rem;
                margin-bottom: 0.35rem;
                border: 1px solid #e2ece6;
                border-left: 4px solid #a9c8b4;
                font-size: 0.76rem;
                line-height: 1.18;
                box-shadow: 0 4px 12px rgba(16, 49, 58, 0.035);
            }

            .calendar-event strong {
                display: block;
                color: var(--navy);
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
                margin-bottom: 0.2rem;
            }

            .calendar-event-meta {
                color: #53676b;
                display: block;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }

            .calendar-status {
                display: inline-block;
                border-radius: 999px;
                padding: 0.08rem 0.34rem;
                margin-top: 0.2rem;
                font-size: 0.66rem;
                font-weight: 950;
                border: 1px solid transparent;
            }

            .calendar-status-scheduled {
                background: #e8f6ed;
                color: #165c3a;
                border-color: #cde5d6;
            }

            .calendar-status-draft {
                background: #eef2f1;
                color: #53676b;
                border-color: #dfe8e4;
            }

            .calendar-status-planned {
                background: #edf8f7;
                color: #0c4b4f;
                border-color: #cae3e0;
            }

            .calendar-status-needs {
                background: #fff8db;
                color: #6d5910;
                border-color: #eadb9c;
            }

            .calendar-event-instagram {
                background: #fff1f3;
                border-left-color: #d96b78;
            }

            .calendar-event-facebook {
                background: #eef5ff;
                border-left-color: #5f90d6;
            }

            .calendar-event-newsletter {
                background: #edf8f2;
                border-left-color: #5ca37a;
            }

            .calendar-event-linkedin {
                background: #edf8f7;
                border-left-color: #509a98;
            }

            .calendar-event-asset {
                background: #fff8db;
                border-left-color: #d9bd49;
            }

            .calendar-event-activity {
                background: #f3f8f5;
                border-left-color: #9fc9ac;
            }

            .calendar-more {
                color: var(--green-dark);
                font-size: 0.75rem;
                font-weight: 900;
            }

            div[class*="st-key-calendar_event_"] [data-testid="stVerticalBlockBorderWrapper"] {
                background: #fbfdfc;
                border: 1px solid #e3ebe7;
                border-left: 4px solid var(--green);
                border-radius: 14px;
                box-shadow: 0 6px 16px rgba(16, 49, 58, 0.04);
            }

            div[class*="st-key-asset_native_card_"] [data-testid="stVerticalBlockBorderWrapper"] {
                background: #ffffff;
                border: 1px solid #dfe8e4;
                border-radius: 20px;
                box-shadow: 0 12px 28px rgba(16, 49, 58, 0.06);
                min-height: 420px;
            }

            div[class*="st-key-asset_preview_"] [data-testid="stVerticalBlockBorderWrapper"] {
                background:
                    radial-gradient(circle at 28% 24%, rgba(31, 111, 74, 0.14), transparent 18%),
                    radial-gradient(circle at 74% 32%, rgba(255, 210, 52, 0.18), transparent 18%),
                    linear-gradient(135deg, #f3f6f5 0%, #e8eeee 100%);
                border: 1px solid #e2ebe7;
                border-radius: 16px;
                min-height: 180px;
                display: flex;
                align-items: center;
                justify-content: center;
            }

            .score {
                width: 72px;
                height: 72px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                background: var(--navy);
                color: var(--yellow);
                font-weight: 950;
                font-size: 1.2rem;
                border: 5px solid var(--green-soft);
            }

            .pipeline {
                border: 1px dashed #a8c7bd;
                border-radius: 14px;
                background: var(--soft);
                padding: 0.8rem;
                min-height: 170px;
            }

            .draggable {
                background: white;
                border: 1px solid var(--line);
                border-left: 5px solid var(--green);
                border-radius: 10px;
                padding: 0.65rem;
                margin-top: 0.55rem;
                box-shadow: 0 5px 14px rgba(16, 49, 58, 0.05);
            }

            .copy-box {
                white-space: pre-wrap;
                background: #f8fbf8;
                border: 1px solid var(--line);
                border-left: 5px solid #2F7A55;
                border-radius: 18px;
                padding: 1.2rem 1.25rem;
                line-height: 1.65;
                font-size: 1rem;
                box-shadow: 0 10px 26px rgba(16, 49, 58, 0.055);
            }

            .ai-output-panel {
                background:
                    radial-gradient(circle at 96% 8%, rgba(221, 238, 227, 0.55), transparent 26%),
                    linear-gradient(135deg, #ffffff 0%, #fbfdfb 100%);
                border: 1px solid #dfe8e4;
                border-radius: 24px;
                padding: 1.55rem;
                margin: 1rem 0 0.85rem;
                box-shadow: 0 18px 44px rgba(16, 49, 58, 0.09);
            }

            .ai-output-header {
                display: flex;
                align-items: flex-start;
                justify-content: space-between;
                gap: 1rem;
                margin-bottom: 1.15rem;
                padding-bottom: 0.9rem;
                border-bottom: 1px solid #e7eeeb;
            }

            .ai-output-title {
                color: var(--navy);
                font-size: 1.28rem;
                font-weight: 950;
                margin: 0 0 0.25rem;
            }

            .ai-content-grid {
                display: grid;
                grid-template-columns: minmax(0, 1.45fr) minmax(260px, 0.75fr);
                gap: 1.1rem;
                align-items: start;
            }

            .ai-hook-block {
                background: #f3faf6;
                border: 1px solid #d8e8df;
                border-left: 5px solid #2F7A55;
                border-radius: 18px;
                padding: 1rem 1rem 0.95rem;
                margin-bottom: 1rem;
            }

            .ai-hook-text {
                color: var(--navy);
                font-size: 1.22rem;
                line-height: 1.38;
                font-weight: 900;
                margin: 0;
            }

            .ai-body-copy {
                color: var(--ink);
                font-size: 1.02rem;
                line-height: 1.72;
                white-space: pre-wrap;
            }

            .ai-cta-block {
                background: #fff9dd;
                border: 1px solid #f1df91;
                border-radius: 16px;
                padding: 0.9rem 1rem;
                margin-top: 1rem;
                color: var(--navy);
                font-weight: 850;
            }

            .ai-hashtag-block {
                background: #f8faf8;
                border: 1px solid #e4ece8;
                border-radius: 16px;
                padding: 0.85rem 1rem;
                margin-top: 1rem;
                color: var(--green-dark);
                font-weight: 850;
                line-height: 1.6;
            }

            .ai-score-card,
            .ai-why-card {
                background: #ffffff;
                border: 1px solid #e2ebe6;
                border-radius: 18px;
                padding: 1rem;
                box-shadow: 0 8px 22px rgba(16, 49, 58, 0.045);
                margin-bottom: 0.9rem;
            }

            div[class*="st-key-ai_output_actions_"] div.stButton > button {
                background: #ffffff;
                color: var(--green-dark);
                border: 1px solid #cfe3d6;
                box-shadow: none;
                padding: 0.42rem 0.72rem;
                font-size: 0.86rem;
            }

            div[class*="st-key-ai_output_actions_"] div.stButton > button:hover {
                background: #f3faf6;
                color: var(--green-dark);
                border-color: #accdbb;
                box-shadow: none;
            }

            .ai-score-big {
                color: var(--navy);
                font-size: 2.1rem;
                line-height: 1;
                font-weight: 950;
                margin: 0.2rem 0 0.7rem;
            }

            div[class*="st-key-ai_output_panel_"] {
                background:
                    radial-gradient(circle at 4% 8%, rgba(221, 238, 227, 0.74), transparent 28%),
                    radial-gradient(circle at 96% 10%, rgba(255, 243, 184, 0.62), transparent 24%),
                    radial-gradient(circle at 50% 38%, rgba(255, 255, 255, 0.92), transparent 34%),
                    linear-gradient(135deg, #f7fbf8 0%, #ffffff 44%, #fffdf4 100%) !important;
                border-color: #dfeae4 !important;
                border-radius: 24px !important;
                box-shadow: 0 18px 44px rgba(16, 49, 58, 0.09) !important;
                padding: 1.45rem !important;
            }

            div[class*="st-key-ai_hook_"] {
                background: #edf8f2 !important;
                border-color: #cfe6d8 !important;
                border-left: 5px solid #2F7A55 !important;
                border-radius: 18px !important;
            }

            div[class*="st-key-ai_hook_"] h4 {
                font-size: 18px !important;
                font-weight: 700 !important;
                line-height: 1.38 !important;
                letter-spacing: 0 !important;
            }

            div[class*="st-key-ai_body_"] {
                background: #ffffff !important;
                border-color: #dfece5 !important;
                border-radius: 18px !important;
            }

            div[class*="st-key-ai_body_"] p,
            div[class*="st-key-ai_cta_"] p,
            div[class*="st-key-ai_hashtags_"] p {
                font-size: 15.5px !important;
                font-weight: 400 !important;
                line-height: 1.6 !important;
                letter-spacing: 0 !important;
            }

            div[class*="st-key-ai_cta_"] {
                background: #fff8db !important;
                border-color: #f0dd8a !important;
                border-radius: 18px !important;
            }

            div[class*="st-key-ai_hashtags_"] {
                background: #eef8f7 !important;
                border-color: #cbe4e1 !important;
                border-radius: 18px !important;
            }

            div[class*="st-key-ai_score_card_"] {
                background: rgba(255, 255, 255, 0.86) !important;
                border-color: #dfece5 !important;
                border-radius: 18px !important;
                box-shadow: 0 8px 22px rgba(16, 49, 58, 0.045) !important;
            }

            div[class*="st-key-ai_why_card_"] {
                background: #f0f8f3 !important;
                border-color: #d6e8de !important;
                border-radius: 18px !important;
                box-shadow: 0 8px 22px rgba(16, 49, 58, 0.04) !important;
            }

            div[class*="st-key-score_emotional_"] div[data-testid="stProgress"] div {
                background: linear-gradient(90deg, #cfe7d7, #7faf92) !important;
            }

            div[class*="st-key-score_shareability_"] div[data-testid="stProgress"] div {
                background: linear-gradient(90deg, #cfe8e5, #6ea8a0) !important;
            }

            div[class*="st-key-score_parent_"] div[data-testid="stProgress"] div {
                background: linear-gradient(90deg, #fff3bd, #e4c85d) !important;
            }

            div[class*="st-key-score_authenticity_"] div[data-testid="stProgress"] div {
                background: linear-gradient(90deg, #dff1e6, #8fc9a5) !important;
            }

            @media (max-width: 980px) {
                .ai-output-header,
                .ai-content-grid {
                    display: block;
                }
            }

            .funnel {
                background: var(--navy);
                color: white;
                text-align: center;
                border-radius: 14px;
                padding: 0.9rem;
                border-bottom: 7px solid var(--green);
                min-height: 92px;
            }

            .funnel strong {
                color: var(--yellow);
                display: block;
                font-size: 1.45rem;
            }

            div.stButton > button {
                border-radius: 999px;
                border: 1px solid #e0b91a;
                background: var(--yellow);
                color: var(--navy);
                font-weight: 900;
                padding: 0.45rem 0.9rem;
                box-shadow: 0 4px 10px rgba(16, 49, 58, 0.08);
            }

            div.stButton > button:hover {
                border-color: #c9a000;
                background: #ffe071;
                color: var(--navy);
                box-shadow: 0 7px 16px rgba(16, 49, 58, 0.12);
            }

            section[data-testid="stSidebar"] div.stButton > button {
                display: flex;
                align-items: center;
                gap: 10px;
                width: 100%;
                justify-content: flex-start;
                background: #ffffff;
                color: #16343A;
                border: 1px solid transparent;
                border-radius: 12px;
                box-shadow: none;
                padding: 10px 12px;
                text-align: left;
                height: auto;
                min-height: 44px;
                font-size: 15px;
                line-height: 1.2;
                margin-bottom: 6px;
                white-space: normal;
                transition: background 140ms ease, color 140ms ease;
            }

            section[data-testid="stSidebar"] div.stButton > button:hover {
                background: #F3F8F5;
                border-color: transparent;
                color: #145C3B;
                box-shadow: none;
            }

            section[data-testid="stSidebar"] div.stButton > button p {
                white-space: normal;
                overflow: visible;
                text-overflow: clip;
                margin: 0;
                line-height: 1.2;
            }

            section[data-testid="stSidebar"] .st-key-bgc_logout_v2 button {
                min-height: 0;
                padding: 4px 0;
                margin: 4px 0 10px;
                background: transparent;
                color: #607276;
                border: 0;
                font-size: 0.84rem;
                font-weight: 800;
            }

            section[data-testid="stSidebar"] .st-key-bgc_logout_v2 button:hover {
                background: transparent;
                color: #145C3B;
            }

            div[data-testid="stProgress"] div {
                background-color: var(--green);
            }

            div[data-testid="stMetric"] {
                background: white;
                border: 1px solid var(--line);
                border-radius: 14px;
                padding: 0.95rem;
                box-shadow: 0 8px 20px rgba(16, 49, 58, 0.05);
            }

            .login-card-marker {
                display: none;
            }

            .stApp:has(.login-card-marker) {
                background: #F8FAF7;
            }

            .block-container:has(.login-card-marker) {
                max-width: 100%;
                min-height: 100vh;
                padding: 0;
                background: #F8FAF7;
            }

            .stVerticalBlock.st-key-login_page {
                min-height: 100vh;
                width: 100%;
                background: #F8FAF7;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                padding: 40px !important;
                box-sizing: border-box;
                position: relative;
                overflow: hidden;
            }

            .stVerticalBlock.st-key-login_page::before {
                content: "";
                position: fixed;
                width: 420px;
                height: 420px;
                right: -130px;
                top: -120px;
                border-radius: 50%;
                background: rgba(204, 224, 210, 0.42);
                pointer-events: none;
            }

            .stVerticalBlock.st-key-login_page::after {
                content: "";
                position: fixed;
                width: 300px;
                height: 300px;
                left: -120px;
                bottom: -110px;
                border-radius: 50%;
                background: rgba(204, 224, 210, 0.22);
                pointer-events: none;
            }

            .stHorizontalBlock.st-key-login_card {
                width: min(1120px, calc(100vw - 32px)) !important;
                max-width: calc(100vw - 32px);
                height: 660px !important;
                min-height: 660px !important;
                background: #ffffff !important;
                border: 1px solid #E5ECE7 !important;
                border-radius: 32px !important;
                padding: 0 !important;
                box-shadow: 0 30px 80px rgba(16, 47, 52, 0.16) !important;
                box-sizing: border-box !important;
                position: relative;
                z-index: 1;
                margin: 0 auto !important;
                display: grid !important;
                grid-template-columns: 1.05fr 0.95fr;
                align-items: stretch !important;
                gap: 0 !important;
                overflow: hidden !important;
            }

            .stHorizontalBlock.st-key-login_card > div {
                min-width: 0 !important;
                padding: 0 !important;
                margin: 0 !important;
            }

            .stHorizontalBlock.st-key-login_card > div:first-child {
                align-self: stretch !important;
                height: 660px !important;
                min-height: 660px !important;
                background: #0f3738 !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                padding: 18px !important;
                overflow: hidden !important;
                box-sizing: border-box !important;
            }

            .stHorizontalBlock.st-key-login_card > div:nth-child(2) {
                align-self: stretch !important;
                height: 660px !important;
                min-height: 660px !important;
                padding: 40px 44px 24px !important;
                display: flex !important;
                flex-direction: column !important;
                align-items: center !important;
                justify-content: center !important;
                background: #ffffff !important;
                overflow: visible !important;
                box-shadow: -14px 0 36px rgba(16, 47, 52, 0.035) !important;
            }

            .st-key-login_hero_image img {
                width: 100% !important;
                height: auto !important;
                max-height: 92% !important;
                object-fit: contain !important;
                object-position: center !important;
                display: block !important;
                background: #0f3738;
            }

            .st-key-login_hero_image,
            .st-key-login_hero_image [data-testid="stImage"] {
                width: 100% !important;
                height: 100% !important;
                min-height: 624px !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                background: #0f3738 !important;
            }

            .st-key-login_form_panel {
                width: 100% !important;
                max-width: 430px !important;
                overflow: visible !important;
                margin-top: 28px !important;
            }

            .st-key-login_card div[data-testid="stForm"] {
                border: 0;
                padding: 0;
                background: transparent;
                box-shadow: none;
                overflow: visible !important;
            }

            .st-key-login_card div[data-testid="stForm"] [data-testid="stVerticalBlock"] {
                gap: 8px !important;
            }

            .st-key-login_card div[data-testid="stTextInput"],
            .st-key-login_card div[data-testid="stSelectbox"],
            .st-key-login_card div[data-testid="stFormSubmitButton"],
            .st-key-login_card div[data-baseweb="input"],
            .st-key-login_card div[data-baseweb="select"] {
                width: 100% !important;
                max-width: 100% !important;
                min-width: 0 !important;
                box-sizing: border-box !important;
            }

            .st-key-login_card input,
            .st-key-login_card div[data-testid="stTextInput"] *,
            .st-key-login_card div[data-testid="stSelectbox"] * {
                max-width: 100% !important;
                min-width: 0 !important;
                box-sizing: border-box !important;
            }

            .login-brand {
                color: var(--green-dark);
                font-size: 0.88rem;
                font-weight: 950;
                letter-spacing: 0;
                margin: 0 0 0.2rem;
            }

            .login-dots {
                display: none;
            }

            .login-dots span {
                width: 10px;
                height: 10px;
                border-radius: 50%;
                background: var(--green);
                display: block;
            }

            .login-dots span:nth-child(4) {
                background: var(--yellow);
            }

            .login-tagline {
                color: var(--muted);
                font-size: 0.9rem;
                font-weight: 800;
                margin: 0 0 0.58rem;
            }

            .login-system-title {
                color: var(--navy) !important;
                margin: 0 0 10px !important;
                font-size: 28px;
                line-height: 1.08;
                letter-spacing: 0;
                font-weight: 800;
            }

            .login-subtitle {
                color: var(--muted) !important;
                font-size: 0.88rem;
                line-height: 1.32;
                margin: 0 0 16px;
            }

            .st-key-login_card label {
                color: var(--navy) !important;
                font-weight: 850;
                font-size: 0.86rem;
            }

            .st-key-login_card input,
            .st-key-login_card div[data-baseweb="select"] > div {
                min-height: 2.25rem;
                border-radius: 14px;
                font-size: 0.9rem;
            }

            .st-key-login_card div[data-testid="stFormSubmitButton"] button {
                width: 100%;
                justify-content: center;
                min-height: 2.2rem;
                font-size: 0.9rem;
                margin-top: 0;
                border-radius: 14px;
            }

            .st-key-login_card div[data-testid="stFormSubmitButton"] button[kind="primary"],
            .st-key-login_card div[data-testid="stFormSubmitButton"] button[data-testid="stBaseButton-primaryFormSubmit"] {
                background: var(--yellow) !important;
                color: var(--navy) !important;
                border-color: #e0b91a !important;
            }

            .st-key-login_card div[data-testid="stFormSubmitButton"] button[kind="secondary"],
            .st-key-login_card div[data-testid="stFormSubmitButton"] button[data-testid="stBaseButton-secondaryFormSubmit"] {
                background: #ffffff !important;
                color: var(--green-dark) !important;
                border: 1px solid #b8d1c4 !important;
                box-shadow: none !important;
            }

            .st-key-login_form_panel div.stButton > button {
                width: 100%;
                justify-content: center;
                min-height: 2.2rem;
                font-size: 0.9rem;
                border-radius: 14px;
                background: #ffffff !important;
                color: var(--green-dark) !important;
                border: 1px solid #b8d1c4 !important;
                box-shadow: none !important;
            }

            .st-key-login_form_panel div.stButton > button:hover {
                background: var(--green-soft) !important;
                border-color: #9fc7af !important;
                color: var(--green-dark) !important;
                box-shadow: none !important;
            }

            .login-divider {
                display: flex;
                align-items: center;
                gap: 0.8rem;
                color: var(--muted);
                font-weight: 850;
                font-size: 0.82rem;
                margin: 14px 0 12px;
            }

            .login-divider::before,
            .login-divider::after {
                content: "";
                height: 1px;
                background: var(--line);
                flex: 1;
            }

            .login-helper {
                background: var(--soft);
                border: 1px solid var(--line);
                border-radius: 12px;
                padding: 0.34rem 0.5rem;
                color: var(--muted);
                font-size: 0.72rem;
                line-height: 1.22;
                margin-top: 0.08rem;
            }

            .message-card {
                background: #ffffff;
                border: 1px solid var(--line);
                border-left: 5px solid var(--green);
                border-radius: 16px;
                padding: 0.95rem;
                box-shadow: 0 10px 24px rgba(16, 49, 58, 0.055);
                margin-bottom: 0.75rem;
            }

            .channel-card {
                background: #ffffff;
                border: 1px solid var(--line);
                border-radius: 14px;
                padding: 0.72rem 0.78rem;
                margin-bottom: 0.58rem;
                box-shadow: 0 6px 16px rgba(16, 49, 58, 0.035);
            }

            .channel-card-active {
                background: #EAF6EE;
                border-color: #CFE6D8;
                border-left: 5px solid #2F7A55;
            }

            .chat-message-card {
                background: #ffffff;
                border: 1px solid var(--line);
                border-radius: 18px;
                padding: 0.95rem 1rem;
                margin-bottom: 0.8rem;
                box-shadow: 0 8px 22px rgba(16, 49, 58, 0.045);
            }

            .chat-meta-row {
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 0.8rem;
                margin-bottom: 0.45rem;
            }

            .chat-sender {
                color: var(--navy);
                font-weight: 950;
                line-height: 1.1;
            }

            .chat-time {
                color: var(--muted);
                font-size: 0.78rem;
                font-weight: 800;
                white-space: nowrap;
            }

            .chat-composer {
                background: #ffffff;
                border: 1px solid var(--line);
                border-radius: 18px;
                padding: 0.95rem;
                box-shadow: 0 10px 26px rgba(16, 49, 58, 0.055);
                margin-top: 1rem;
            }

            .context-panel-card {
                background: #ffffff;
                border: 1px solid var(--line);
                border-radius: 18px;
                padding: 0.95rem;
                box-shadow: 0 8px 22px rgba(16, 49, 58, 0.045);
                margin-bottom: 0.8rem;
            }

            div[class*="st-key-message_composer_main"] {
                background:
                    radial-gradient(circle at 96% 10%, rgba(255, 243, 184, 0.42), transparent 24%),
                    linear-gradient(135deg, #ffffff 0%, #f7fbf8 100%) !important;
                border-color: #d8e8df !important;
                border-left: 5px solid #2F7A55 !important;
                border-radius: 22px !important;
                box-shadow: 0 14px 34px rgba(16, 49, 58, 0.075) !important;
                padding: 1.2rem !important;
                margin-bottom: 1.15rem !important;
            }

            div[class*="st-key-dept_channel_0"] {
                background: #EAF6EE !important;
                border-color: #CFE6D8 !important;
                border-left: 4px solid #2F7A55 !important;
            }

            div[class*="st-key-dept_channel_"] {
                border-radius: 14px !important;
                box-shadow: none !important;
            }

            div[class*="st-key-message_update_"] {
                background: #ffffff !important;
                border-color: #e2ebe6 !important;
                border-radius: 18px !important;
                box-shadow: 0 8px 22px rgba(16, 49, 58, 0.045) !important;
                margin-bottom: 0.8rem !important;
            }

            .shared-week-grid {
                display: grid;
                grid-template-columns: repeat(7, minmax(0, 1fr));
                gap: 0.7rem;
            }

            .shared-day {
                background: #ffffff;
                border: 1px solid var(--line);
                border-radius: 16px;
                min-height: 220px;
                padding: 0.75rem;
                box-shadow: 0 8px 20px rgba(16, 49, 58, 0.045);
            }

            .shared-day-today {
                border-color: #b9d2c5;
                background: #f8fbf9;
            }

            .calendar-item {
                background: var(--soft);
                border: 1px solid var(--line);
                border-left: 4px solid var(--green);
                border-radius: 11px;
                padding: 0.55rem;
                margin-top: 0.5rem;
                font-size: 0.86rem;
            }

            .month-grid {
                display: grid;
                grid-template-columns: repeat(7, minmax(0, 1fr));
                gap: 0.55rem;
            }

            .month-cell {
                background: #ffffff;
                border: 1px solid var(--line);
                border-radius: 14px;
                min-height: 126px;
                padding: 0.55rem;
                box-shadow: 0 6px 16px rgba(16, 49, 58, 0.035);
            }

            .month-cell-muted {
                background: #f8f9f8;
                color: #9aa6a8;
            }

            .month-number {
                color: var(--navy);
                font-weight: 950;
                font-size: 0.9rem;
            }

            .mini-calendar-item {
                display: block;
                margin-top: 0.35rem;
                padding: 0.28rem 0.38rem;
                border-radius: 8px;
                background: var(--green-soft);
                color: var(--green-dark);
                font-size: 0.72rem;
                font-weight: 850;
                line-height: 1.15;
            }

            .idea-card {
                background: #ffffff;
                border: 1px solid var(--line);
                border-radius: 18px;
                padding: 1rem;
                min-height: 245px;
                box-shadow: 0 10px 24px rgba(16, 49, 58, 0.055);
            }

            .video-template-card {
                background: #ffffff;
                border: 1px solid var(--line);
                border-left: 5px solid var(--green);
                border-radius: 18px;
                padding: 1rem;
                box-shadow: 0 12px 28px rgba(16, 49, 58, 0.06);
            }

            .content-score-panel {
                background: #ffffff;
                border: 1px solid var(--line);
                border-radius: 18px;
                padding: 1rem;
                margin-top: 1rem;
                box-shadow: 0 12px 28px rgba(16, 49, 58, 0.06);
            }

            .score-hero {
                display: grid;
                grid-template-columns: 120px 1fr;
                gap: 1rem;
                align-items: center;
                margin-bottom: 0.75rem;
            }

            .score-circle {
                width: 104px;
                height: 104px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                background:
                    radial-gradient(circle at center, #ffffff 0 58%, transparent 59%),
                    conic-gradient(var(--green) var(--score-deg), #edf1ef 0);
                color: var(--navy);
                font-size: 1.35rem;
                font-weight: 950;
            }

            .score-grid {
                display: grid;
                grid-template-columns: repeat(3, minmax(0, 1fr));
                gap: 0.65rem 0.9rem;
                margin-top: 0.75rem;
            }

            .score-feedback-grid {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 0.85rem;
                margin-top: 0.95rem;
            }

            .viral-hero {
                background:
                    radial-gradient(circle at 96% 8%, rgba(255, 210, 52, 0.22), transparent 22%),
                    radial-gradient(circle at 8% 90%, rgba(31, 111, 74, 0.13), transparent 24%),
                    #ffffff;
                border: 1px solid var(--line);
                border-left: 6px solid var(--green);
                border-radius: 22px;
                padding: 1.25rem;
                box-shadow: 0 16px 38px rgba(16, 49, 58, 0.075);
                margin-bottom: 1.1rem;
            }

            .viral-engine-hero {
                min-height: 300px;
                max-height: 320px;
                border-radius: 24px;
                overflow: hidden;
                background-size: cover;
                background-position: center;
                box-shadow: 0 18px 44px rgba(16, 49, 58, 0.11);
                border: 1px solid #dfe8e4;
                margin: 0.4rem 0 1.3rem;
                position: relative;
                display: flex;
                align-items: center;
                padding: 1.4rem;
            }

            .viral-engine-hero::after {
                content: "";
                position: absolute;
                inset: 0;
                background: linear-gradient(90deg, rgba(16, 49, 58, 0.74) 0%, rgba(16, 49, 58, 0.42) 38%, rgba(16, 49, 58, 0.04) 76%);
                pointer-events: none;
            }

            .viral-engine-hero-content {
                position: relative;
                z-index: 1;
                max-width: 520px;
                background: rgba(255, 255, 255, 0.12);
                border: 1px solid rgba(255, 255, 255, 0.22);
                border-radius: 22px;
                padding: 1.15rem 1.2rem;
                backdrop-filter: blur(4px);
            }

            .viral-engine-hero-content h2 {
                color: var(--yellow);
                margin: 0 0 0.35rem;
                font-size: 2rem;
                line-height: 1.05;
                font-weight: 950;
                letter-spacing: -0.02em;
            }

            .viral-engine-hero-content p {
                color: #ffffff;
                margin: 0 0 0.75rem;
                font-size: 1rem;
                line-height: 1.42;
                font-weight: 700;
            }

            .viral-engine-hero-placeholder {
                background:
                    radial-gradient(circle at 88% 18%, rgba(255, 210, 52, 0.24), transparent 24%),
                    radial-gradient(circle at 72% 74%, rgba(31, 111, 74, 0.28), transparent 26%),
                    linear-gradient(135deg, #10313a 0%, #0c4b4f 100%);
            }

            .content-studio-hero {
                min-height: 310px;
                max-height: 340px;
                width: 100%;
                border-radius: 26px;
                overflow: hidden;
                background-size: cover;
                background-position: center;
                box-shadow: 0 18px 44px rgba(16, 49, 58, 0.11);
                border: 1px solid #dfe8e4;
                margin: 0.4rem 0 1.3rem;
                position: relative;
                display: flex;
                align-items: center;
                padding: 1.45rem;
            }

            .content-studio-hero::after {
                content: "";
                position: absolute;
                inset: 0;
                background: linear-gradient(90deg, rgba(16, 49, 58, 0.76) 0%, rgba(16, 49, 58, 0.46) 40%, rgba(16, 49, 58, 0.05) 78%);
                pointer-events: none;
            }

            .content-studio-hero-content {
                position: relative;
                z-index: 1;
                max-width: 540px;
                background: rgba(255, 255, 255, 0.13);
                border: 1px solid rgba(255, 255, 255, 0.24);
                border-radius: 22px;
                padding: 1.15rem 1.2rem;
                backdrop-filter: blur(4px);
            }

            .content-studio-hero-content h2 {
                color: var(--yellow);
                margin: 0 0 0.35rem;
                font-size: 2rem;
                line-height: 1.05;
                font-weight: 950;
                letter-spacing: -0.02em;
            }

            .content-studio-hero-content p {
                color: #ffffff;
                margin: 0 0 0.75rem;
                font-size: 1rem;
                line-height: 1.42;
                font-weight: 700;
            }

            .content-studio-hero-placeholder {
                background:
                    radial-gradient(circle at 88% 18%, rgba(255, 210, 52, 0.24), transparent 24%),
                    radial-gradient(circle at 72% 74%, rgba(31, 111, 74, 0.28), transparent 26%),
                    linear-gradient(135deg, #10313a 0%, #0c4b4f 100%);
            }

            .viral-trend-card,
            .viral-match-card,
            .viral-hook-card,
            .viral-guide-card {
                background: #ffffff;
                border: 1px solid var(--line);
                border-radius: 18px;
                padding: 1rem;
                box-shadow: 0 10px 26px rgba(16, 49, 58, 0.055);
                min-height: 220px;
            }

            .viral-trend-card {
                border-top: 5px solid #d9e8df;
            }

            .viral-match-card {
                min-height: 250px;
                border-left: 5px solid var(--green);
            }

            .viral-hook-card {
                min-height: 148px;
                background:
                    radial-gradient(circle at 92% 14%, rgba(255, 210, 52, 0.18), transparent 24%),
                    #ffffff;
            }

            .viral-guide-card {
                min-height: 150px;
            }

            .platform-pill {
                display: inline-block;
                border-radius: 999px;
                padding: 0.22rem 0.58rem;
                margin: 0.12rem 0.18rem 0.12rem 0;
                background: #eef3ef;
                border: 1px solid #dfe8e4;
                color: var(--navy);
                font-size: 0.76rem;
                font-weight: 900;
            }

            .viral-score-panel {
                background:
                    radial-gradient(circle at 95% 12%, rgba(255, 210, 52, 0.18), transparent 24%),
                    linear-gradient(135deg, #ffffff 0%, #f7faf8 100%);
                border: 1px solid var(--line);
                border-radius: 22px;
                padding: 1.1rem;
                box-shadow: 0 14px 34px rgba(16, 49, 58, 0.065);
            }

            div[class*="st-key-region_card_"],
            div[class*="st-key-online_card_"],
            .st-key-regional_recommendation {
                border-radius: 22px !important;
                border-color: #E6F0EA !important;
                background:
                    radial-gradient(circle at 92% 8%, rgba(221, 238, 227, 0.42), transparent 30%),
                    linear-gradient(135deg, #ffffff 0%, #F5F9F6 100%) !important;
                box-shadow: 0 12px 30px rgba(16, 47, 52, 0.06) !important;
                padding: 1.5rem !important;
                min-height: 360px !important;
            }

            .st-key-region_card_1,
            .st-key-online_card_0 {
                background:
                    radial-gradient(circle at 92% 8%, rgba(246, 239, 207, 0.55), transparent 30%),
                    linear-gradient(135deg, #ffffff 0%, #fffdf2 100%) !important;
            }

            .st-key-region_card_2,
            .st-key-online_card_2 {
                background:
                    radial-gradient(circle at 92% 8%, rgba(230, 240, 234, 0.68), transparent 30%),
                    linear-gradient(135deg, #ffffff 0%, #F5F9F6 100%) !important;
            }

            .st-key-regional_recommendation {
                border-left: 5px solid #DDEEE3 !important;
                background:
                    radial-gradient(circle at 96% 10%, rgba(246, 239, 207, 0.45), transparent 30%),
                    linear-gradient(135deg, #ffffff 0%, #EAF6EE 100%) !important;
            }

            div[class*="st-key-region_card_"] h3,
            div[class*="st-key-online_card_"] h3,
            .st-key-regional_recommendation h3 {
                color: var(--navy);
                font-size: 1.25rem;
                margin-top: 0.45rem;
            }

            div[class*="st-key-region_card_"] [data-testid="stMetric"],
            .st-key-regional_recommendation [data-testid="stMetric"] {
                background: rgba(255, 255, 255, 0.78);
                border-color: #E6F0EA;
                border-radius: 18px;
                box-shadow: none;
            }

            div[class*="st-key-online_card_"] [data-testid="stAlert"] {
                background: #F5F9F6;
                border-color: #E6F0EA;
                border-radius: 18px;
            }

            @media (max-width: 900px) {
                .score-hero,
                .score-feedback-grid,
                .score-grid {
                    grid-template-columns: 1fr;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Mock data and simple scoring
# ---------------------------------------------------------------------------

TODAY = date.today()

PROGRAMS = [
    {
        "name": "MAP Education Support",
        "segment": "MAP",
        "audience": "Youth and families planning for school success",
        "date": TODAY + timedelta(days=18),
        "urgency": "High",
        "assets": ["Photos", "Testimonials"],
        "asset_quality": "High",
        "past_engagement": 91,
        "mission_alignment": 96,
        "audience_fit": 94,
        "proof": "$1,000/year scholarship proof point",
        "angle": "Back-to-school confidence, tutoring support, and youth opportunity.",
        "required_assets": "Student story, caregiver quote, scholarship visual",
        "channels": ["Instagram", "Facebook", "Newsletter", "Partners"],
    },
    {
        "name": "After-School Recreation",
        "segment": "Children",
        "audience": "Young parents and caregivers",
        "date": TODAY + timedelta(days=10),
        "urgency": "High",
        "assets": ["Photos", "Graphics"],
        "asset_quality": "Medium",
        "past_engagement": 86,
        "mission_alignment": 93,
        "audience_fit": 92,
        "proof": "Safe, supervised daily program environment",
        "angle": "Affordable care, belonging, and safe after-school routines.",
        "required_assets": "Activity photos, registration link, staff quote",
        "channels": ["Facebook", "Instagram", "Google Ads Grant", "Partners"],
    },
    {
        "name": "Supper Club",
        "segment": "Supper Club",
        "audience": "Families, volunteers, and community supporters",
        "date": TODAY + timedelta(days=6),
        "urgency": "Medium",
        "assets": ["Photos", "Testimonials"],
        "asset_quality": "Quick phone photo",
        "past_engagement": 82,
        "mission_alignment": 90,
        "audience_fit": 87,
        "proof": "Community meals and volunteer participation",
        "angle": "Food security, shared meals, and neighbours supporting neighbours.",
        "required_assets": "Real meal photos, volunteer quote",
        "channels": ["Facebook", "Newsletter", "Local Media Pitch"],
    },
    {
        "name": "DCAC Media Program",
        "segment": "DCAC",
        "audience": "Youth creators and partners",
        "date": TODAY + timedelta(days=24),
        "urgency": "Medium",
        "assets": ["Videos", "Graphics"],
        "asset_quality": "High",
        "past_engagement": 78,
        "mission_alignment": 88,
        "audience_fit": 84,
        "proof": "Youth-created media and skill-building workshops",
        "angle": "Creative youth voice, digital skills, and confidence.",
        "required_assets": "Short video, youth quote, workshop schedule",
        "channels": ["Instagram", "YouTube", "LinkedIn"],
    },
    {
        "name": "50+ Wellness Programs",
        "segment": "50+",
        "audience": "Older adults and caregivers",
        "date": TODAY + timedelta(days=20),
        "urgency": "Medium",
        "assets": ["Newsletter snippets", "Photos"],
        "asset_quality": "Medium",
        "past_engagement": 72,
        "mission_alignment": 86,
        "audience_fit": 80,
        "proof": "Social, fitness, and wellness activities",
        "angle": "Reducing isolation through connection, movement, and routine.",
        "required_assets": "Participant-friendly photo, schedule, testimonial",
        "channels": ["Newsletter", "Facebook", "Local Media Pitch"],
    },
    {
        "name": "Inclusion Programs",
        "segment": "Inclusion",
        "audience": "Families, partners, donors",
        "date": TODAY + timedelta(days=15),
        "urgency": "High",
        "assets": ["Graphics"],
        "asset_quality": "Medium",
        "past_engagement": 74,
        "mission_alignment": 95,
        "audience_fit": 79,
        "proof": "Barrier-free participation and inclusive play",
        "angle": "Belonging for every participant and practical barrier removal.",
        "required_assets": "Consent-safe visual, accessibility proof point",
        "channels": ["LinkedIn", "Facebook", "Partners"],
    },
]

TRENDS = [
    ("Back-to-school preparation", "MAP Education Support", "Parents and youth", "Newsletter", "Planning support and confidence before September", 96),
    ("Youth mental wellness", "MAP Education Support", "Youth and caregivers", "Instagram", "Belonging, confidence, and caring adult support", 91),
    ("Affordable after-school care", "After-School Recreation", "Young parents", "Facebook", "Safe, affordable routines after school", 93),
    ("Senior social isolation", "50+ Wellness Programs", "Older adults", "Newsletter", "Connection and healthy aging close to home", 82),
    ("Community sports engagement", "Sports Programs", "Children and youth", "Instagram", "Teamwork, movement, and inclusive play", 80),
    ("Food security for children", "Supper Club", "Community supporters", "Facebook", "Real meals, local care, volunteer action", 88),
]

SOCIAL_INSIGHTS = [
    "Parents respond well to safety + affordability messages.",
    "Youth stories perform better with short-form video.",
    "Partner updates perform better on LinkedIn.",
    "Supper Club posts perform well when paired with real photos.",
]

LONDON_HEATMAP = [
    {
        "area": "North London",
        "heat": 78,
        "engagement": "High parent engagement",
        "awareness": "Medium awareness",
        "opportunity": "Parents are responsive to safety, affordability, and routine messages.",
        "campaign": "Parent-focused after-school safety campaign",
    },
    {
        "area": "Downtown",
        "heat": 86,
        "engagement": "Strong volunteer engagement",
        "awareness": "High community awareness",
        "opportunity": "Community supporters respond to visible stories of belonging and practical support.",
        "campaign": "Supper Club community storytelling content",
    },
    {
        "area": "East London",
        "heat": 64,
        "engagement": "Growing youth engagement",
        "awareness": "Low awareness",
        "opportunity": "High youth and family relevance; needs clearer program visibility.",
        "campaign": "After-school registration and MAP referral campaign",
    },
    {
        "area": "West London",
        "heat": 72,
        "engagement": "Medium recreation engagement",
        "awareness": "Medium awareness",
        "opportunity": "Sports and recreation content can create entry points for families.",
        "campaign": "Sports and recreation engagement push",
    },
    {
        "area": "South London",
        "heat": 58,
        "engagement": "Untapped wellness interest",
        "awareness": "Low-to-medium awareness",
        "opportunity": "Caregivers and older adults need simple calendar-driven reminders.",
        "campaign": "50+ wellness awareness campaign",
    },
]

BROAD_ONLINE_SIGNALS = [
    {
        "opportunity": "Trending short-form content",
        "format": "Phone-shot Reels with fast text overlays",
        "campaign": "MAP day-in-the-life or Supper Club behind-the-scenes Reel",
        "why": "Authentic vertical video makes nonprofit stories feel current, human, and easier to share.",
    },
    {
        "opportunity": "Donor storytelling",
        "format": "Human moment plus practical proof point",
        "campaign": "Scholarship proof point, Supper Club meal impact, or inclusion barrier-removal story",
        "why": "Donors respond when they can see both the person helped and the concrete outcome.",
    },
    {
        "opportunity": "Volunteer recruitment",
        "format": "Task preview plus community payoff",
        "campaign": "Supper Club volunteer shift preview or sports event support ask",
        "why": "Showing the task clearly makes volunteering feel approachable and worth doing.",
    },
    {
        "opportunity": "Youth creator content",
        "format": "Before/after reveal or creator reaction clip",
        "campaign": "DCAC project transformation or MAP student goal story",
        "why": "Youth-led creative content carries energy, peer relevance, and strong social proof.",
    },
]

OFFLINE_ACTIVATIONS = [
    {
        "name": "Backpack Campaign",
        "goal": "Create 300 backpacks for families in need before back-to-school season.",
        "audience": "Families, donors, school partners, campus volunteers",
        "partners": ["Local schools", "Western clubs", "Fanshawe clubs", "Local media"],
        "tactics": ["QR donation posters", "Partner school donation links", "Local news pitch", "Campus club volunteers"],
        "digital_support": ["Milestone counter", "Packing day Reel", "Donor thank-you posts", "School newsletter blurb"],
        "cta": "Sponsor one backpack",
        "impact": "300 students start school with practical supplies and a stronger sense of support.",
        "message": "One backpack. One student. One stronger start.",
        "milestone": "0 / 300 backpacks",
    },
    {
        "name": "Angel Tree — BGC Edition",
        "goal": "Help kids receive sports equipment, activity supplies, or wishlist items.",
        "audience": "Donors, local businesses, sports families, community supporters",
        "partners": ["Local businesses", "Sports clubs", "Community sponsors", "Drop-off locations"],
        "tactics": ["Community sponsor wall", "Sports equipment donation drive", "Business drop-off points", "Donor thank-you content"],
        "digital_support": ["Wishlist graphics", "Sponsor spotlight posts", "Reveal Reel", "LinkedIn partner thank-you"],
        "cta": "Fulfill one child’s wish",
        "impact": "More children can participate, play, and feel included without cost barriers.",
        "message": "Kids deserve the chance to simply be kids.",
        "milestone": "Wishlist items matched weekly",
    },
    {
        "name": "Campus Ambassador Program",
        "goal": "Get Western and Fanshawe students involved in youth-created content and volunteer promotion.",
        "audience": "Western students, Fanshawe students, student clubs, youth volunteers",
        "partners": ["Western clubs", "Fanshawe clubs", "Student unions", "Youth ambassadors"],
        "tactics": ["Student club partnerships", "Short-form video challenges", "Youth ambassador content", "Volunteer recruitment push"],
        "digital_support": ["Ambassador intro Reel", "Volunteer story carousel", "Campus email copy", "TikTok-style challenge prompt"],
        "cta": "Join the ambassador team",
        "impact": "A sustainable volunteer and content pipeline that keeps BGC visible on campus.",
        "message": "Future leaders help future leaders.",
        "milestone": "10 ambassador leads this month",
    },
]

OFFLINE_RECOMMENDATIONS = [
    {
        "name": "Backpack Campaign",
        "why": "Back-to-school timing gives BGC a clear community need, simple donation ask, and memorable local story.",
        "audience_fit": 94,
        "partner_fit": 92,
        "donor_potential": 91,
        "content_potential": 88,
        "local_awareness": 95,
        "best_action": "Launch QR donation posters with a weekly backpack milestone counter.",
    },
    {
        "name": "Angel Tree BGC Edition",
        "why": "The giving concept is familiar, but the BGC version connects donations directly to play, belonging, and childhood dignity.",
        "audience_fit": 88,
        "partner_fit": 90,
        "donor_potential": 94,
        "content_potential": 86,
        "local_awareness": 89,
        "best_action": "Recruit local business drop-off points and publish a sponsor wall.",
    },
    {
        "name": "Campus Ambassador Program",
        "why": "Western and Fanshawe students can help BGC generate youth-relevant content while building a volunteer pipeline.",
        "audience_fit": 86,
        "partner_fit": 95,
        "donor_potential": 78,
        "content_potential": 96,
        "local_awareness": 90,
        "best_action": "Invite campus clubs to co-create a short-form volunteer challenge.",
    },
    {
        "name": "Community Story Booth",
        "why": "A portable story booth can capture short participant, volunteer, and donor moments at events without needing a full production day.",
        "audience_fit": 83,
        "partner_fit": 86,
        "donor_potential": 84,
        "content_potential": 94,
        "local_awareness": 88,
        "best_action": "Set up at Supper Club, sports events, and campus partner days.",
    },
    {
        "name": "Donor Impact Breakfast",
        "why": "A small in-person breakfast creates donor visibility, relationship-building, and reusable proof-point content.",
        "audience_fit": 80,
        "partner_fit": 88,
        "donor_potential": 96,
        "content_potential": 82,
        "local_awareness": 85,
        "best_action": "Pair one impact stat with one participant story and one clear funding need.",
    },
]

OFFLINE_TO_DIGITAL_IDEAS = [
    {
        "moment": "Backpack Campaign",
        "reel": "Packing 300 backpacks in fast cuts.",
        "hook": "What does a stronger school year look like?",
        "cta": "Scan the QR code to sponsor one backpack.",
        "fit": "Parents: Facebook + Instagram + school newsletters",
    },
    {
        "moment": "Angel Tree",
        "reel": "Sports equipment donation reveal.",
        "hook": "Every kid deserves the chance to play.",
        "cta": "Help fulfill one child’s wish.",
        "fit": "Donors: LinkedIn + impact reports + email updates",
    },
    {
        "moment": "Campus Ambassador Program",
        "reel": "Western/Fanshawe students explaining why they volunteer.",
        "hook": "Future leaders help future leaders.",
        "cta": "Join the ambassador team.",
        "fit": "Youth: TikTok/Reels + peer ambassadors",
    },
    {
        "moment": "50+ Wellness Outreach",
        "reel": "A morning routine montage with calendar reminders and friendly arrivals.",
        "hook": "Connection is wellness too.",
        "cta": "Ask about this month’s 50+ wellness calendar.",
        "fit": "50+ adults: Facebook + newsletters + referrals",
    },
]

DONOR_PROOF_POINTS = [
    "100 meals served today",
    "$1,000/year MAP scholarship support",
    "40,000 rides provided to older adults",
    "sports equipment access for kids",
    "mentorship and confidence-building stories",
]

VIRAL_MODES = {
    "Parent Engagement": {
        "audience": "parents and caregivers",
        "cta": "Save this program update or ask BGC London how to get involved.",
        "angle": "safety, affordability, routine, and real confidence",
        "best_time": "weekday evenings when caregivers are planning family routines",
    },
    "Youth Engagement": {
        "audience": "youth and young creators",
        "cta": "Share this with someone who should know BGC is here for them.",
        "angle": "belonging, identity, confidence, and peer energy",
        "best_time": "after school and early evenings",
    },
    "Volunteer Recruitment": {
        "audience": "volunteers and community helpers",
        "cta": "Volunteer for one shift and see the difference up close.",
        "angle": "approachable service, visible impact, and community connection",
        "best_time": "weekday lunch or Sunday evening planning windows",
    },
    "Donor Storytelling": {
        "audience": "donors, partners, and civic supporters",
        "cta": "Support practical programs that turn care into measurable opportunity.",
        "angle": "human stories plus concrete proof points",
        "best_time": "Tuesday to Thursday mornings",
    },
    "Community Awareness": {
        "audience": "local families, partners, and neighbours",
        "cta": "Follow BGC London and help more people discover these supports.",
        "angle": "community pride, trusted programs, and local belonging",
        "best_time": "late afternoon and early evening",
    },
}

VIRAL_TRENDS = {
    "Parent Engagement": [
        ("POV storytelling", "Relatable first-person framing helps parents quickly imagine their child in a safe, supported place.", "Instagram Reels", "Parents 30-45", "POV: you found an after-school place where your child is safe, active, and known by name."),
        ("Day in the life", "Simple routines make programs feel trustworthy and easy to understand.", "Facebook + Reels", "Caregivers", "Show arrival, snack, activity, staff encouragement, and pick-up for After-School Recreation."),
        ("Fast text-overlay reels", "Parents can absorb practical information without turning sound on.", "Instagram", "Busy families", "Use short text beats: safe space, caring staff, active play, registration support."),
        ("Behind-the-scenes nonprofit content", "Shows credibility without feeling like an ad.", "Facebook", "Community families", "Film staff setting up supper, activities, or learning spaces before participants arrive."),
    ],
    "Youth Engagement": [
        ("POV: someone finally believes in you", "Emotional youth-centered hooks create instant identification and save/share behaviour.", "TikTok-style Reels", "Youth", "MAP confidence journey from walking in unsure to setting a goal with a mentor."),
        ("Before / after reveal", "Transformation arcs are easy to understand in seconds.", "Instagram Reels", "Youth creators", "DCAC first idea to finished video reveal."),
        ("Interview reaction clips", "Short authentic answers feel creator-led and less scripted.", "Instagram", "Teens", "Ask: what is one thing BGC helped you feel more confident doing?"),
        ("Come with me format", "Invites viewers into the experience instead of explaining it from outside.", "TikTok-style Reels", "Youth", "Come with me to sports night, DCAC, or MAP tutoring."),
    ],
    "Volunteer Recruitment": [
        ("One shift, real impact", "Low-commitment framing makes volunteering feel accessible.", "Facebook Reels", "Prospective volunteers", "Show a Supper Club shift from setup to shared meal to cleanup."),
        ("Behind-the-scenes nonprofit content", "Practical task previews reduce uncertainty.", "Instagram Reels", "Community volunteers", "Show what volunteers actually do in 15 seconds."),
        ("Community transformation stories", "Connects individual action to visible local impact.", "LinkedIn + Facebook", "Volunteer teams", "One volunteer, one evening, dozens of welcoming moments."),
        ("Interview reaction clips", "Volunteer quotes create social proof.", "Facebook", "New volunteers", "Ask a volunteer: what surprised you about helping at BGC?"),
    ],
    "Donor Storytelling": [
        ("Proof point storytelling", "Donors respond to emotion plus measurable outcomes.", "LinkedIn", "Donors and partners", "MAP scholarship proof point paired with a student goal story."),
        ("Community transformation stories", "Mission impact becomes easier to remember when tied to one person or moment.", "LinkedIn + Newsletter", "Supporters", "Show how a meal, mentor, or inclusive program removes a barrier."),
        ("Before / after reveal", "Makes progress visible and concrete.", "Instagram + LinkedIn", "Donors", "Before support: uncertainty. After support: plan, confidence, next step."),
        ("Fast text-overlay reels", "Turns impact stats into a fast, visual story.", "Instagram", "Supporters", "Text beats: one program, one caring adult, one stronger future."),
    ],
    "Community Awareness": [
        ("Behind-the-scenes nonprofit content", "Authentic local footage builds trust and familiarity.", "Instagram Reels", "Community members", "Show the real people and spaces behind BGC programs."),
        ("Day in the life", "Makes the organization feel active, welcoming, and easy to understand.", "Instagram + Facebook", "Families and neighbours", "A day across BGC: after-school, supper, sports, DCAC, 50+ wellness."),
        ("Come with me format", "Creates an invitation instead of a brochure.", "TikTok-style Reels", "Local community", "Come with me to see what belonging looks like at BGC London."),
        ("Community transformation stories", "Connects programs to a bigger civic purpose.", "LinkedIn + Facebook", "Partners", "Show how BGC turns local support into opportunity across ages."),
    ],
}

VIRAL_PROGRAM_MATCHES = [
    {
        "program": "MAP Education Support",
        "score": 92,
        "trend": "Day in the life",
        "why": "Real youth progression stories perform strongly because viewers can see confidence building in small, believable steps.",
        "platform": "Instagram Reels",
        "style": "Phone-shot montage with mentor interaction, notebook close-ups, and one proof-point text overlay.",
    },
    {
        "program": "Supper Club",
        "score": 88,
        "trend": "Behind-the-scenes nonprofit content",
        "why": "Food, volunteers, and real community moments are easy to understand and emotionally warm in short video.",
        "platform": "Facebook Reels",
        "style": "Kitchen prep, plates being served, quick volunteer reaction, and a simple support CTA.",
    },
    {
        "program": "DCAC Media Program",
        "score": 86,
        "trend": "Before / after reveal",
        "why": "Youth creator transformation is visual, energetic, and naturally suited to short-form reveal edits.",
        "platform": "Instagram Reels",
        "style": "Start with rough idea sketch, cut to filming, then reveal the finished student project.",
    },
    {
        "program": "Sports Programs",
        "score": 82,
        "trend": "Come with me format",
        "why": "Movement, teamwork, and peer energy create immediate visual momentum.",
        "platform": "TikTok-style Reels",
        "style": "Walk-in shot, warm-up, team moment, celebration, and invite to join.",
    },
    {
        "program": "Inclusion Programs",
        "score": 79,
        "trend": "Community transformation stories",
        "why": "Belonging and barrier removal work best when the message is human, specific, and consent-safe.",
        "platform": "LinkedIn + Facebook",
        "style": "Gentle storytelling with accessible visuals, staff quote, and partner-friendly CTA.",
    },
    {
        "program": "After-School Recreation",
        "score": 84,
        "trend": "Fast text-overlay reels",
        "why": "Parents need quick clarity: safety, affordability, routine, and registration next steps.",
        "platform": "Facebook + Instagram",
        "style": "Fast activity clips with big text overlays and a parent-focused CTA.",
    },
]

VIRAL_HOOKS = {
    "emotional": [
        "POV: you finally found a place that believes in your future.",
        "This is what confidence can look like after one supportive moment.",
        "A safe place after school can change the whole evening.",
        "Nobody talks enough about the small moments that help youth keep going.",
    ],
    "curiosity": [
        "What after-school support actually looks like at BGC London.",
        "Here is what happens before the program doors open.",
        "You see a meal. We see community showing up.",
        "Watch this idea become a finished youth media project.",
    ],
    "parent": [
        "Looking for a safe, welcoming after-school routine?",
        "Here is what your child can experience after the school day ends.",
        "A few hours of support can make family routines feel easier.",
        "What parents should know about BGC programs this month.",
    ],
    "youth": [
        "Come with me to a place where your goals matter.",
        "From first idea to finished project in one BGC session.",
        "POV: you show up nervous and leave with a plan.",
        "This is your sign to try something new after school.",
    ],
}

REEL_SCENES = [
    {
        "scene": "Scene 1",
        "flow": "Open with the hook and a real program moment.",
        "camera": "Close-up phone shot, vertical, participant entering space or hands starting an activity.",
        "text": "POV: you found a place that believes in your future.",
        "voiceover": "Every goal starts with someone believing in you.",
    },
    {
        "scene": "Scene 2",
        "flow": "Show the support system.",
        "camera": "Medium shot of staff, mentor, volunteer, or peer interaction.",
        "text": "Support that feels real.",
        "voiceover": "At BGC London, support is practical, welcoming, and close to home.",
    },
    {
        "scene": "Scene 3",
        "flow": "Add a transformation or proof point.",
        "camera": "Quick cut from challenge to progress: notebook, meal prep, edit timeline, or sport drill.",
        "text": "Small moments. Big confidence.",
        "voiceover": "One program moment can help a young person take the next step.",
    },
    {
        "scene": "Scene 4",
        "flow": "Bring in a human reaction.",
        "camera": "Short reaction clip, smile, high-five, quote card, or consent-safe over-the-shoulder shot.",
        "text": "Belonging changes what feels possible.",
        "voiceover": "This is what community care looks like in motion.",
    },
    {
        "scene": "Scene 5",
        "flow": "End with a clear CTA.",
        "camera": "Program sign, group moment, resource table, or simple branded end card.",
        "text": "Learn more. Share this. Get involved.",
        "voiceover": "Follow BGC London or connect with us to learn more.",
    },
]

TREND_ADAPTATION_GUIDE = [
    ("Use faster cuts", "Keep clips to 0.5-1.5 seconds unless someone is speaking. Short-form pacing should feel alive."),
    ("Caption everything", "Assume sound is off. Put the core message in readable on-screen text."),
    ("Film like a creator", "Use authentic phone-shot footage, natural light, and real program moments instead of polished corporate visuals."),
    ("Lead with emotion", "Start with a feeling or situation before explaining the program details."),
    ("Use reaction moments", "Smiles, relief, pride, laughter, and small wins help viewers feel the story quickly."),
    ("Keep the CTA simple", "Ask for one action only: save, share, register, volunteer, refer, or learn more."),
]

LOW_EFFORT_VIRAL_PLAN = [
    "Use a phone camera in vertical mode with natural light.",
    "Combine 3 existing photos with text overlays if no new video is available.",
    "Ask a staff member, volunteer, or youth worker to record a 10-second voiceover.",
    "Use simple Canva-style title cards for proof points and CTAs.",
    "Film hands, activities, spaces, or over-the-shoulder moments when privacy or consent is sensitive.",
    "Post as a Reel first, then repurpose the same idea for Facebook and newsletter snippets.",
]

ASSETS = [
    ("MAP scholarship student quote", "Testimonials", "MAP", "Newsletter", "Approved", "Consent confirmed", "Suitable for donor and parent communication."),
    ("After-school gym photos", "Past program photos", "Children", "Facebook", "Approved", "Consent confirmed", "Best for Facebook parent outreach."),
    ("Supper Club meal photo set", "Past program photos", "Supper Club", "Facebook", "Needs Review", "Consent check needed", "Pair with volunteer recruitment copy."),
    ("DCAC creator montage", "Short videos", "DCAC", "Instagram", "Approved", "Consent confirmed", "Can become an Instagram Reel."),
    ("50+ wellness calendar block", "Newsletter snippets", "50+", "Newsletter", "Scheduled", "Not applicable", "Use in the monthly summary."),
    ("Inclusion program graphic", "Upcoming event graphics", "Inclusion", "LinkedIn", "Needs Review", "Not applicable", "Good for partner and donor updates."),
    ("Sports team huddle clip", "Short videos", "Sports", "Instagram", "Draft", "Consent check needed", "Use as a youth energy story."),
]

IMPACT = {
    "Social engagement": 2380,
    "Newsletter clicks": 742,
    "Google Ads Grant clicks": 318,
    "Website visits": 1540,
    "Program inquiries": 188,
    "Partner referrals": 52,
    "Volunteer interest": 34,
    "Registration interest": 112,
}

FUNNEL = [
    ("Awareness", "22.4k"),
    ("Engagement", "2.4k"),
    ("Clicks", "1.1k"),
    ("Inquiry", "188"),
    ("Registration Interest", "112"),
    ("Attendance", "64"),
]

CADENCE = [
    ("Instagram", "Visual story / short video", "3-4 times weekly"),
    ("Facebook", "Parent information + registration", "2-3 times weekly"),
    ("LinkedIn", "Partner/donor impact", "Weekly"),
    ("Newsletter", "Monthly summary", "Monthly"),
    ("YouTube", "Longer program story", "2 times monthly"),
    ("Google Ads Grant", "Search intent capture", "Always-on campaign"),
]

PIPELINE = {
    "Draft": ["MAP scholarship post", "Sports reel concept"],
    "Needs Assets": ["Inclusion story photo", "Supper Club quote"],
    "Ready": ["After-school parent post", "DCAC video teaser"],
    "Scheduled": ["50+ newsletter block"],
    "Published": ["Volunteer thank-you post"],
}

DEPARTMENTS = [
    "Marketing",
    "Admin",
    "Program Staff",
    "Tutors / Education",
    "Sports Coaches",
    "Volunteers",
    "Partnerships",
    "Front Desk",
]

MOCK_MESSAGES = [
    {
        "department": "Program Staff",
        "type": "Program update",
        "message": "New after-school photos available from STEM activity.",
        "priority": "Medium",
        "date": TODAY.strftime("%b %d"),
        "status": "New",
    },
    {
        "department": "Tutors / Education",
        "type": "Program update",
        "message": "MAP scholarship story is ready for promotion.",
        "priority": "High",
        "date": (TODAY - timedelta(days=1)).strftime("%b %d"),
        "status": "Seen by Marketing",
    },
    {
        "department": "Program Staff",
        "type": "Event reminder",
        "message": "June wellness calendar needs newsletter support.",
        "priority": "Medium",
        "date": (TODAY - timedelta(days=2)).strftime("%b %d"),
        "status": "In progress",
    },
    {
        "department": "Communications",
        "type": "Asset request",
        "message": "New short video clips can be used for Instagram.",
        "priority": "Low",
        "date": (TODAY - timedelta(days=3)).strftime("%b %d"),
        "status": "New",
    },
]

SHARED_CALENDAR_ITEMS = [
    ("MAP Instagram Reel", "Tutors / Education", "Instagram", "Scheduled", TODAY + timedelta(days=1)),
    ("Supper Club volunteer post", "Volunteer Team", "Facebook", "Draft", TODAY + timedelta(days=2)),
    ("DCAC video shoot", "Communications", "Activity", "Confirmed", TODAY + timedelta(days=3)),
    ("50+ newsletter highlight", "Program Staff", "Newsletter", "Draft", TODAY + timedelta(days=4)),
    ("Inclusion partner update", "Fundraising / Partnerships", "LinkedIn", "Scheduled", TODAY + timedelta(days=6)),
    ("Sports photo collection", "Coaches / Sports", "Asset collection", "Planned", TODAY + timedelta(days=7)),
    ("After-school registration push", "Program Staff", "Facebook", "Scheduled", TODAY + timedelta(days=9)),
    ("MAP scholarship proof point", "Marketing", "Newsletter", "Draft", TODAY + timedelta(days=11)),
    ("Supper Club meal photos", "Volunteer Team", "Asset collection", "Needs consent", TODAY + timedelta(days=14)),
    ("DCAC creator reel", "Communications", "Instagram", "Draft", TODAY + timedelta(days=18)),
    ("50+ wellness calendar", "Program Staff", "Newsletter", "Scheduled", TODAY + timedelta(days=21)),
    ("Inclusion family story", "Fundraising / Partnerships", "Partner email", "Needs assets", TODAY + timedelta(days=25)),
]

FUN_CONTENT_IDEAS = {
    "MAP Education Support": [
        {
            "icon": "🎥 Reel",
            "title": "Day in the Life of a MAP Student",
            "best_for": "Best for awareness",
            "why": "This style works because audiences connect more strongly with a real student journey than with an informational graphic. It makes tutoring, confidence, and goals feel human.",
            "hook": "POV: You finally find a place that believes in your goals.",
            "first_three": ["student opening notebook", "walking into the MAP room", "mentor greeting student with a smile"],
            "format": "TikTok-style montage / voiceover story",
            "caption": "A little support can change how a young person sees the school year ahead. MAP Education Support helps youth build confidence, stay connected to their goals, and feel backed by caring adults at BGC London.",
            "cta": "Learn more about MAP and how youth can get involved.",
            "audience": "Youth, parents, caregivers, community supporters",
            "posting_time": "Weekday evenings perform best for parent and youth-focused education content.",
            "difficulty": "Medium",
            "assets": ["2 student clips with consent", "classroom or notebook footage", "mentor interaction", "caregiver or staff quote"],
        },
        {
            "icon": "📷 Carousel",
            "title": "3 Things MAP Helps With",
            "best_for": "Best for saves",
            "why": "Simple numbered posts are easy for parents and youth to save, share, and understand quickly. The format turns a broad program into practical benefits.",
            "hook": "Not sure what education support can actually look like?",
            "first_three": ["cover slide with big question", "quick benefit text", "student workspace photo"],
            "format": "Carousel",
            "caption": "MAP is more than homework help. It can mean a quieter place to focus, someone to talk through next steps with, and support that helps youth keep going when school feels heavy.",
            "cta": "Save this post or send it to a family who may want MAP support.",
            "audience": "Parents, caregivers, school partners",
            "posting_time": "Sunday or Monday evening when families are planning the week.",
            "difficulty": "Easy",
            "assets": ["1 program photo", "3 short benefit points", "brand graphic template"],
        },
        {
            "icon": "📱 TikTok",
            "title": "$1,000 Scholarship Reveal",
            "best_for": "Best for engagement",
            "why": "A clear proof point gives people a reason to stop scrolling. The reveal format creates curiosity before explaining the program value.",
            "hook": "What could $1,000 a year help unlock?",
            "first_three": ["text overlay: '$1,000/year'", "student writing a goal", "quick cut to mentor nodding"],
            "format": "Text reveal over program moments",
            "caption": "When youth can see a path forward, confidence grows. MAP Education Support includes practical encouragement, tutoring, and proof points like scholarship support that can help goals feel closer.",
            "cta": "Explore MAP Education Support with BGC London.",
            "audience": "Youth, donors, partners, families",
            "posting_time": "Midweek afternoon for youth; early evening for parents and donors.",
            "difficulty": "Easy",
            "assets": ["scholarship proof point", "student goal visual", "program logo or simple graphic"],
        },
        {
            "icon": "🎙 Interview",
            "title": "One Question: What Helped You Keep Going?",
            "best_for": "Best for trust",
            "why": "Question-led interviews create authentic emotional proof. Even one short answer from staff or a participant can make the program feel real.",
            "hook": "One question we asked at MAP today...",
            "first_three": ["staff holding phone camera", "question text on screen", "quick cut to response"],
            "format": "Interview clip",
            "caption": "Sometimes the most important support is knowing someone is in your corner. MAP creates space for youth to ask questions, build confidence, and keep moving toward what matters to them.",
            "cta": "Refer a youth or ask us about MAP.",
            "audience": "Parents, referral partners, community supporters",
            "posting_time": "Thursday evening when reflective story content performs well.",
            "difficulty": "Medium",
            "assets": ["consent-safe interview", "quiet room", "caption transcript"],
        },
    ],
    "After-School Recreation": [
        {
            "icon": "🎥 Reel",
            "title": "After School in 15 Seconds",
            "best_for": "Best for parent awareness",
            "why": "Parents need to quickly understand safety, routine, and fun. A fast montage shows the feeling of the program faster than a flyer can.",
            "hook": "What happens after the school bell rings?",
            "first_three": ["kids entering program space", "backpack drop-off", "first activity starting"],
            "format": "Reel montage",
            "caption": "After school should feel safe, active, and welcoming. BGC London's after-school recreation gives children a place to play, connect, and build healthy routines while families get trusted support.",
            "cta": "Learn more about after-school options at BGC London.",
            "audience": "Young parents, caregivers, school partners",
            "posting_time": "Weekday evenings when parents are making care decisions.",
            "difficulty": "Medium",
            "assets": ["2 activity clips", "staff welcome shot", "program schedule or registration detail"],
        },
        {
            "icon": "📷 Carousel",
            "title": "Safe, Active, Connected",
            "best_for": "Best for registration",
            "why": "Three-part message framing is easy for parents to scan and remember. It balances practical care needs with emotional belonging.",
            "hook": "Three things families look for after school.",
            "first_three": ["graphic title slide", "safe space photo", "activity photo"],
            "format": "Carousel",
            "caption": "Families deserve after-school support they can trust. At BGC London, children can move, play, make friends, and be welcomed by caring staff.",
            "cta": "Share this with a parent looking for after-school care.",
            "audience": "Parents, caregivers, front desk referrals",
            "posting_time": "Monday evening or Saturday morning.",
            "difficulty": "Easy",
            "assets": ["3 photos", "registration link", "short staff quote"],
        },
        {
            "icon": "📱 TikTok",
            "title": "Choose Your After-School Adventure",
            "best_for": "Best for engagement",
            "why": "Choice-style content invites comments and lets families picture their child in the program.",
            "hook": "Which after-school activity would you pick?",
            "first_three": ["text: 'Pick one'", "sports clip", "arts or game clip"],
            "format": "Quick choice montage",
            "caption": "Movement, creativity, teamwork, and a place to belong. Every day can look a little different at BGC London.",
            "cta": "Comment your pick or send this to a family.",
            "audience": "Parents, youth, community followers",
            "posting_time": "Friday afternoon for playful engagement.",
            "difficulty": "Easy",
            "assets": ["3 short activity clips", "text overlay", "consent-cleared group shot"],
        },
        {
            "icon": "🎙 Interview",
            "title": "Staff Answer: What Makes This Space Feel Safe?",
            "best_for": "Best for trust",
            "why": "A staff voice can answer parent concerns directly and warmly, especially around safety and belonging.",
            "hook": "We asked our team what families should know.",
            "first_three": ["staff looking at camera", "question text", "program activity in background"],
            "format": "Staff interview clip",
            "caption": "Behind every activity is a team focused on safety, belonging, and positive routines. Here's what families can expect from BGC London after school.",
            "cta": "Contact BGC London for program details.",
            "audience": "Parents, caregivers, community partners",
            "posting_time": "Tuesday evening for parent information content.",
            "difficulty": "Medium",
            "assets": ["staff interview", "quiet filming spot", "activity b-roll"],
        },
    ],
    "Supper Club": [
        {
            "icon": "🎥 Reel",
            "title": "What's for Supper at BGC Today?",
            "best_for": "Best for engagement",
            "why": "Food content is immediate and warm. It gives supporters a simple, visual way to understand community care without needing a long explanation.",
            "hook": "100+ meals, one big community table.",
            "first_three": ["close-up of meal prep", "serving spoon movement", "table being set"],
            "format": "Behind-the-scenes food prep Reel",
            "caption": "Supper Club is about more than a meal. It is a warm table, a familiar face, and a community moment that helps people feel connected.",
            "cta": "Support Supper Club or volunteer with us.",
            "audience": "Volunteers, donors, families, community supporters",
            "posting_time": "Late afternoon before dinner time, when food content feels timely.",
            "difficulty": "Easy",
            "assets": ["phone video of food prep", "serving line clip", "volunteer consent"],
        },
        {
            "icon": "📱 TikTok",
            "title": "Plate to Table in 10 Seconds",
            "best_for": "Best for shares",
            "why": "Transformation videos are satisfying and easy to understand. Viewers see care becoming community in a few seconds.",
            "hook": "Watch dinner become community.",
            "first_three": ["empty table", "meal being plated", "quick cut to table setup"],
            "format": "Before/after montage",
            "caption": "A simple meal can become a moment of belonging. Thank you to everyone who helps make Supper Club possible at BGC London.",
            "cta": "Share this with someone who loves helping locally.",
            "audience": "Community supporters, volunteers, partners",
            "posting_time": "Wednesday or Thursday evening.",
            "difficulty": "Easy",
            "assets": ["before clip", "after clip", "short food close-ups"],
        },
        {
            "icon": "🎙 Interview",
            "title": "Community Table Check-In",
            "best_for": "Best for comments",
            "why": "A simple question invites real responses and makes the program feel personal, while still being consent-safe.",
            "hook": "One question: what made you smile today?",
            "first_three": ["question text on screen", "volunteer smiling", "hands setting table"],
            "format": "Prompt-led interview clip",
            "caption": "Small moments make Supper Club special. Sometimes community starts with a plate, a conversation, and someone asking how your day was.",
            "cta": "Learn how BGC London brings neighbours together.",
            "audience": "Families, volunteers, donors",
            "posting_time": "Weekend morning for reflective community stories.",
            "difficulty": "Medium",
            "assets": ["consent-safe response", "volunteer b-roll", "meal photo"],
        },
        {
            "icon": "📷 Carousel",
            "title": "What It Takes to Make Supper Club Happen",
            "best_for": "Best for volunteer recruitment",
            "why": "Breaking the work into steps shows supporters exactly where help is needed and makes volunteering feel approachable.",
            "hook": "It starts before the first plate is served.",
            "first_three": ["slide 1: prep", "slide 2: serve", "slide 3: clean-up/community"],
            "format": "Carousel",
            "caption": "Every Supper Club night is powered by planning, volunteers, care, and community. Here's a small look at what happens behind the scenes.",
            "cta": "Ask us how to support or volunteer.",
            "audience": "Volunteers, donors, partners",
            "posting_time": "Monday morning for volunteer planning.",
            "difficulty": "Easy",
            "assets": ["3 photos", "volunteer role notes", "CTA link"],
        },
    ],
    "DCAC Media Program": [
        {
            "icon": "🎥 Reel",
            "title": "Student Creator Transformation",
            "best_for": "Best for youth engagement",
            "why": "Before/after reveals are naturally satisfying and show skill growth without overexplaining the program.",
            "hook": "From first idea to finished video.",
            "first_three": ["rough storyboard", "camera setup", "final project preview"],
            "format": "Before/after project reveal",
            "caption": "At DCAC, youth creators turn ideas into real media skills. The best part is watching confidence grow between the first draft and the final cut.",
            "cta": "Explore DCAC programs at BGC London.",
            "audience": "Youth, parents, arts partners, donors",
            "posting_time": "After school hours or early evening.",
            "difficulty": "Medium",
            "assets": ["project preview", "behind-the-scenes clip", "youth quote with consent"],
        },
        {
            "icon": "📱 TikTok",
            "title": "Show the Setup",
            "best_for": "Best for curiosity",
            "why": "Behind-the-scenes content makes media training feel accessible and lets youth imagine themselves participating.",
            "hook": "What does it take to make a video?",
            "first_three": ["camera close-up", "mic check", "editing timeline"],
            "format": "Gear and process mini-tour",
            "caption": "Behind every clip is planning, teamwork, practice, and a little courage. DCAC helps youth build skills by creating, testing, and learning together.",
            "cta": "Follow BGC London for more youth creator stories.",
            "audience": "Youth, parents, creative partners",
            "posting_time": "Thursday afternoon for youth discovery content.",
            "difficulty": "Easy",
            "assets": ["camera/mic shots", "editing screen", "room b-roll"],
        },
        {
            "icon": "🎙 Interview",
            "title": "Creator Reaction Moment",
            "best_for": "Best for emotional connection",
            "why": "Reaction clips perform well because the emotion is immediate. They show pride, surprise, and confidence in a natural way.",
            "hook": "The first time seeing the final edit.",
            "first_three": ["student watching screen", "reaction smile", "quick flash of final project"],
            "format": "Reaction clip",
            "caption": "That moment when an idea becomes real. DCAC gives youth space to try, create, and see what they are capable of.",
            "cta": "Support youth creativity in London.",
            "audience": "Donors, partners, youth, families",
            "posting_time": "Friday evening for feel-good storytelling.",
            "difficulty": "Medium",
            "assets": ["reaction shot", "final project clip", "consent confirmation"],
        },
        {
            "icon": "📷 Carousel",
            "title": "From Script to Screen",
            "best_for": "Best for education",
            "why": "A process carousel helps partners and caregivers understand the learning behind the finished media.",
            "hook": "Four steps youth creators practice at DCAC.",
            "first_three": ["script page", "filming moment", "editing screen"],
            "format": "Process carousel",
            "caption": "Media skills are built one step at a time: idea, plan, film, edit. DCAC helps youth practice creative problem-solving while building confidence.",
            "cta": "Connect with BGC London to learn more about DCAC.",
            "audience": "Partners, parents, donors",
            "posting_time": "Tuesday afternoon for educational content.",
            "difficulty": "Easy",
            "assets": ["4 process photos", "simple step labels", "program contact"],
        },
    ],
    "Inclusion Programs": [
        {
            "icon": "🎥 Reel",
            "title": "Belonging Looks Like This",
            "best_for": "Best for mission awareness",
            "why": "Inclusion is strongest when shown through small, real moments of participation and welcome rather than abstract statements.",
            "hook": "Every participant deserves to feel included.",
            "first_three": ["activity setup", "inclusive game moment", "staff supporting participation"],
            "format": "Warm montage",
            "caption": "Inclusion at BGC London means creating spaces where participants can join in, build confidence, and feel like they belong.",
            "cta": "Learn how BGC London supports inclusive participation.",
            "audience": "Families, partners, donors",
            "posting_time": "Weekday evening for family and partner audiences.",
            "difficulty": "Medium",
            "assets": ["consent-safe activity clips", "staff support moment", "accessibility proof point"],
        },
        {
            "icon": "📷 Carousel",
            "title": "3 Ways We Reduce Barriers",
            "best_for": "Best for partner education",
            "why": "Partners and donors respond to specific examples of barrier removal because it makes impact concrete.",
            "hook": "Inclusion is practical. Here's what it can look like.",
            "first_three": ["title slide", "support example", "participation example"],
            "format": "Carousel",
            "caption": "Belonging happens when barriers are noticed and reduced. BGC London works to make participation more welcoming, accessible, and supportive.",
            "cta": "Share this with a partner who cares about inclusive community spaces.",
            "audience": "Partners, donors, families",
            "posting_time": "LinkedIn weekday morning or Facebook evening.",
            "difficulty": "Easy",
            "assets": ["3 simple points", "accessible graphic", "program proof point"],
        },
        {
            "icon": "🎙 Interview",
            "title": "Staff Voice: What Inclusion Means Here",
            "best_for": "Best for trust",
            "why": "A staff voice can explain care, dignity, and participation in plain language, making the program feel accountable and human.",
            "hook": "We asked our team what inclusion looks like at BGC.",
            "first_three": ["staff on camera", "question text", "activity b-roll"],
            "format": "Interview clip",
            "caption": "Inclusion is not one moment. It is how we plan, welcome, adapt, and support participants so more people can take part.",
            "cta": "Ask us about inclusive program supports.",
            "audience": "Families, referral partners, donors",
            "posting_time": "Wednesday evening.",
            "difficulty": "Medium",
            "assets": ["staff interview", "caption transcript", "activity b-roll"],
        },
        {
            "icon": "📱 TikTok",
            "title": "Small Adaptations, Big Difference",
            "best_for": "Best for awareness",
            "why": "Quick examples of adaptation show impact without needing participant-identifying footage.",
            "hook": "One small change can open the door.",
            "first_three": ["hands arranging materials", "visual schedule", "activity option choice"],
            "format": "Quick text overlay montage",
            "caption": "Sometimes inclusion is a quieter space, a clearer instruction, an adapted activity, or an extra moment of support. Small changes can make participation possible.",
            "cta": "Support inclusive programs at BGC London.",
            "audience": "Community supporters, partners, donors",
            "posting_time": "Thursday morning for partner-focused engagement.",
            "difficulty": "Easy",
            "assets": ["non-identifying support visuals", "text overlays", "program detail"],
        },
    ],
    "Sports Programs": [
        {
            "icon": "🎥 Reel",
            "title": "Game Day Energy",
            "best_for": "Best for engagement",
            "why": "Sports content has natural motion, emotion, and teamwork. It performs well when it captures the energy before explaining the program.",
            "hook": "The best part of game day is the team feeling.",
            "first_three": ["shoes on court", "team huddle", "quick movement drill"],
            "format": "Fast-cut sports montage",
            "caption": "Sports at BGC London are about more than the score. They build teamwork, confidence, movement, and a place to belong.",
            "cta": "Follow for more BGC sports moments.",
            "audience": "Youth, parents, community supporters",
            "posting_time": "After school or Saturday morning.",
            "difficulty": "Easy",
            "assets": ["huddle clip", "activity clip", "coach encouragement"],
        },
        {
            "icon": "📱 TikTok",
            "title": "Coach Says Try This",
            "best_for": "Best for saves",
            "why": "Short skill tips are useful, repeatable, and saveable. They also show coaching quality without feeling like an ad.",
            "hook": "One quick tip from a BGC coach.",
            "first_three": ["coach points to camera", "skill demo", "text overlay with tip"],
            "format": "Skill tip clip",
            "caption": "A small tip can build confidence. BGC coaches help young people practice skills, teamwork, and encouragement one session at a time.",
            "cta": "Save this tip or share it with a young athlete.",
            "audience": "Youth, parents, coaches",
            "posting_time": "Weekday afternoon.",
            "difficulty": "Easy",
            "assets": ["coach demo", "clear floor/court space", "text overlay"],
        },
        {
            "icon": "📷 Carousel",
            "title": "Teamwork in 4 Photos",
            "best_for": "Best for community pride",
            "why": "A photo sequence can show belonging, leadership, and encouragement while staying consent-safe.",
            "hook": "What teamwork can look like at BGC.",
            "first_three": ["huddle photo", "high-five photo", "group activity photo"],
            "format": "Carousel",
            "caption": "Teamwork is practiced in small moments: listening, encouraging, trying again, and celebrating effort.",
            "cta": "Share this with someone who believes in youth sport.",
            "audience": "Parents, donors, community supporters",
            "posting_time": "Sunday afternoon.",
            "difficulty": "Easy",
            "assets": ["4 consent-cleared photos", "short captions", "program tag"],
        },
        {
            "icon": "🎙 Interview",
            "title": "One Word After Practice",
            "best_for": "Best for comments",
            "why": "One-word prompts are low pressure, quick to film, and invite viewers to add their own word in the comments.",
            "hook": "Describe today's practice in one word.",
            "first_three": ["question text", "quick youth/staff answer", "action b-roll"],
            "format": "Prompt interview clip",
            "caption": "Confidence. Teamwork. Energy. Fun. What word would you choose after a great practice?",
            "cta": "Comment your word.",
            "audience": "Youth, parents, followers",
            "posting_time": "Friday after school.",
            "difficulty": "Medium",
            "assets": ["consent-safe answers", "practice b-roll", "caption transcript"],
        },
    ],
    "50+ Wellness Programs": [
        {
            "icon": "🎥 Reel",
            "title": "A Morning at 50+ Wellness",
            "best_for": "Best for awareness",
            "why": "Routine-based content helps older adults and caregivers picture the program experience in a friendly, low-pressure way.",
            "hook": "A welcoming morning can change the whole day.",
            "first_three": ["coffee or welcome table", "gentle movement", "friendly conversation"],
            "format": "Soft montage",
            "caption": "BGC London's 50+ Wellness Programs support connection, movement, and routine in a welcoming community space.",
            "cta": "See what's coming up in the 50+ wellness calendar.",
            "audience": "Older adults, caregivers, community partners",
            "posting_time": "Morning posts perform well for older adult and caregiver audiences.",
            "difficulty": "Easy",
            "assets": ["welcome photo", "activity clip", "calendar detail"],
        },
        {
            "icon": "📷 Carousel",
            "title": "This Month's Wellness Picks",
            "best_for": "Best for attendance",
            "why": "Calendar-style content is practical and shareable, especially for caregivers and front-desk referrals.",
            "hook": "Looking for something welcoming this month?",
            "first_three": ["calendar cover", "activity highlight", "social connection highlight"],
            "format": "Carousel",
            "caption": "Movement, conversation, wellness, and connection. Here's what older adults can look forward to this month at BGC London.",
            "cta": "Save the calendar or share it with someone who may want to join.",
            "audience": "Older adults, caregivers, front desk staff",
            "posting_time": "First weekday of the month, late morning.",
            "difficulty": "Easy",
            "assets": ["monthly calendar", "2 program photos", "contact detail"],
        },
        {
            "icon": "🎙 Interview",
            "title": "Why I Keep Coming Back",
            "best_for": "Best for trust",
            "why": "Participant testimonials address isolation and belonging better than promotional copy can.",
            "hook": "We asked one participant what keeps them coming back.",
            "first_three": ["participant hands or consent-safe face", "question text", "activity room"],
            "format": "Interview clip",
            "caption": "Sometimes wellness starts with having somewhere to go and people who are glad to see you.",
            "cta": "Ask about 50+ Wellness Programs at BGC London.",
            "audience": "Older adults, caregivers, local media",
            "posting_time": "Wednesday morning.",
            "difficulty": "Medium",
            "assets": ["testimonial", "consent confirmation", "activity b-roll"],
        },
        {
            "icon": "📱 TikTok",
            "title": "Gentle Movement Moment",
            "best_for": "Best for accessibility",
            "why": "A short movement clip feels inviting and lowers the barrier for someone unsure about joining.",
            "hook": "One gentle move to start the day.",
            "first_three": ["instructor demo", "simple text cue", "participant-safe wide shot"],
            "format": "Mini wellness tip",
            "caption": "Wellness can start small. A little movement, a friendly space, and a reason to get together can make a difference.",
            "cta": "Share this with someone who may enjoy 50+ programs.",
            "audience": "Older adults, caregivers, wellness partners",
            "posting_time": "Morning or early afternoon.",
            "difficulty": "Easy",
            "assets": ["instructor demo", "plain background", "text overlay"],
        },
    ],
}

# Program name aliases keep the content studio useful even when labels differ.
FUN_CONTENT_IDEAS["Inclusion"] = FUN_CONTENT_IDEAS["Inclusion Programs"]
FUN_CONTENT_IDEAS["Sports"] = FUN_CONTENT_IDEAS["Sports Programs"]
FUN_CONTENT_IDEAS["50+ Wellness"] = FUN_CONTENT_IDEAS["50+ Wellness Programs"]

VIDEO_TEMPLATES = {
    "MAP Education Support": {
        "length": "12-20 seconds",
        "channel": "Instagram Reels, TikTok, Facebook",
        "text": "Support today. Confidence tomorrow.",
        "voiceover": "Every goal starts with someone believing in you.",
        "assets": "Student clips with consent, classroom b-roll, mentor interaction, scholarship proof point.",
        "scenes": [
            {
                "objective": "Establish emotional connection and show a youth entering a support space.",
                "camera": "Phone camera or DSLR, close-up handheld shot.",
                "framing": "Hands opening notebook, backpack, or door handle; avoid identifiable faces if consent is not confirmed.",
                "motion": "Slow push-in or gentle walking shot entering the room.",
                "text": "Support today.",
                "voiceover": "Every goal starts with someone believing in you.",
                "emotion": "Hopeful, calm, supported.",
            },
            {
                "objective": "Show the practical support MAP provides.",
                "camera": "Over-the-shoulder shot near table height.",
                "framing": "Notebook, laptop, worksheet, and mentor hand pointing to a next step.",
                "motion": "Quick cut from problem to mentor support.",
                "text": "Homework help. Goal setting. Confidence.",
                "voiceover": "MAP gives youth space to ask questions and keep moving forward.",
                "emotion": "Relief and progress.",
            },
            {
                "objective": "Introduce the proof point that makes the story memorable.",
                "camera": "Static shot of student goal sheet or simple graphic.",
                "framing": "Clean text overlay with the scholarship proof point.",
                "motion": "Text reveal timed to music beat.",
                "text": "$1,000/year scholarship support.",
                "voiceover": "With practical supports like scholarship opportunities, goals can feel closer.",
                "emotion": "Possibility.",
            },
            {
                "objective": "End with a clear action and BGC identity.",
                "camera": "Wide shot of program space or BGC sign.",
                "framing": "Leave clean space for CTA text.",
                "motion": "Hold for two seconds so the CTA can be read.",
                "text": "Learn more about MAP at BGC London.",
                "voiceover": "Learn how MAP supports youth success.",
                "emotion": "Inviting and confident.",
            },
        ],
        "editing_style": {
            "pacing": "Moderate pace with 1-2 second cuts; let emotional moments breathe.",
            "transitions": "Simple jump cuts and one text reveal for the scholarship proof point.",
            "music": "Warm, hopeful, light beat or soft piano with a modern rhythm.",
            "subtitles": "Always include captions; keep lines short and high contrast.",
            "color": "Warm natural colors, bright classroom tones, avoid overly corporate filters.",
        },
        "trend_adaptation": [
            "Use a 'day in the life' format with POV text overlays.",
            "Use authentic phone-shot footage instead of polished corporate video.",
            "Use fast text overlays common in TikTok nonprofit storytelling.",
            "Open with a relatable school-year pressure moment before showing support.",
        ],
        "low_effort": [
            "Use existing photos with slow zoom effects.",
            "Record a volunteer or staff voiceover on a phone.",
            "Add text overlays for the scholarship proof point.",
            "Use one notebook shot, one room shot, and one CTA slide.",
        ],
    },
    "After-School Recreation": {
        "length": "10-18 seconds",
        "channel": "Facebook, Instagram Reels, Google Ads landing support",
        "text": "Safe. Active. Welcoming.",
        "voiceover": "After school, children need a place where they can move, connect, and belong.",
        "assets": "Activity clips, staff welcome shot, registration detail, consent-safe group visuals.",
        "scenes": [
            {
                "objective": "Show the transition from school day to safe program space.",
                "camera": "Wide handheld shot.",
                "framing": "Backpacks, doorway, program room, no close faces without consent.",
                "motion": "Walking shot into the activity area.",
                "text": "After the bell rings...",
                "voiceover": "After school, families need support they can trust.",
                "emotion": "Relief and safety.",
            },
            {
                "objective": "Show energy and variety.",
                "camera": "Phone camera, vertical.",
                "framing": "Hands playing game, sports movement, art table, staff nearby.",
                "motion": "Three fast jump cuts.",
                "text": "Play. Move. Create.",
                "voiceover": "Children get space to move, play, and connect.",
                "emotion": "Fun and energy.",
            },
            {
                "objective": "Reassure parents about belonging and care.",
                "camera": "Medium shot of staff preparing or guiding an activity.",
                "framing": "Staff and activity materials; keep children consent-safe.",
                "motion": "Slow pan across organized space.",
                "text": "Caring adults. Positive routines.",
                "voiceover": "BGC London creates welcoming routines families can count on.",
                "emotion": "Trust.",
            },
            {
                "objective": "Drive registration interest.",
                "camera": "Static CTA slide or BGC sign.",
                "framing": "Clear text with room for link or contact note.",
                "motion": "No motion; hold to read.",
                "text": "Ask about after-school recreation.",
                "voiceover": "Learn more about after-school options at BGC London.",
                "emotion": "Clear and practical.",
            },
        ],
        "editing_style": {
            "pacing": "Fast but readable; 0.8-1.5 second cuts for activity moments.",
            "transitions": "Jump cuts with subtle sound hits.",
            "music": "Upbeat, friendly, family-safe track.",
            "subtitles": "Use captions for every spoken line and large parent-friendly text.",
            "color": "Bright, natural, energetic colors.",
        },
        "trend_adaptation": [
            "Use 'pick your after-school activity' choice format.",
            "Use quick jump cuts and reaction shots.",
            "Use parent-problem opening: 'Need after-school support?'",
            "Keep phone-shot footage authentic and real.",
        ],
        "low_effort": [
            "Use three existing activity photos as a carousel-style Reel.",
            "Add text overlays: Safe, Active, Welcoming.",
            "Use a staff voiceover instead of live interviews.",
            "End with a simple registration CTA slide.",
        ],
    },
    "Supper Club": {
        "length": "10-20 seconds",
        "channel": "Instagram Reels, Facebook, partner share",
        "text": "Warm meals. Welcoming tables. Community care.",
        "voiceover": "At BGC London, Supper Club brings neighbours together through food, care, and connection.",
        "assets": "Real meal photos or clips, volunteer consent, simple program details.",
        "scenes": [
            {
                "objective": "Create immediate warmth with food and care.",
                "camera": "Close-up phone shot.",
                "framing": "Meal prep, serving spoon, table detail.",
                "motion": "Slow close-up movement across food or table.",
                "text": "What's for supper at BGC?",
                "voiceover": "A meal can be the start of connection.",
                "emotion": "Warm and inviting.",
            },
            {
                "objective": "Show the people behind the program.",
                "camera": "Medium handheld shot.",
                "framing": "Volunteer hands, staff setup, serving line without identifying participants unless consented.",
                "motion": "Quick cut from prep to serving.",
                "text": "Prepared with care.",
                "voiceover": "Volunteers and staff help create a welcoming table.",
                "emotion": "Gratitude.",
            },
            {
                "objective": "Connect the meal to belonging.",
                "camera": "Wide table or room detail.",
                "framing": "Chairs, plates, conversation details, hands only if needed.",
                "motion": "Gentle pan across the table.",
                "text": "More than a meal.",
                "voiceover": "Supper Club is about food, dignity, and community.",
                "emotion": "Belonging.",
            },
            {
                "objective": "Invite support or volunteering.",
                "camera": "Static final frame.",
                "framing": "BGC logo, meal photo, or clean text card.",
                "motion": "Hold for readability.",
                "text": "Support or volunteer with Supper Club.",
                "voiceover": "Ask how you can support Supper Club.",
                "emotion": "Actionable and hopeful.",
            },
        ],
        "editing_style": {
            "pacing": "Warm quick cuts; keep food and volunteer moments readable.",
            "transitions": "Simple jump cuts or soft crossfade between prep and table.",
            "music": "Light upbeat acoustic or warm community feel.",
            "subtitles": "Always on; use high contrast over food/table visuals.",
            "color": "Warm natural tones, avoid dark filters over food.",
        },
        "trend_adaptation": [
            "Use 'what's for supper today?' format.",
            "Use satisfying prep-to-table transformation.",
            "Use authentic phone-shot footage instead of polished campaign footage.",
            "Pair real photos with quick text overlays.",
        ],
        "low_effort": [
            "Film three clips: food prep, table, CTA card.",
            "Use existing meal photos with text overlays.",
            "Ask one volunteer for a 10-second voiceover.",
            "Use a simple Canva end card for volunteer CTA.",
        ],
    },
    "DCAC Media Program": {
        "length": "10-18 seconds",
        "channel": "Instagram Reels, TikTok, YouTube Shorts",
        "text": "From idea to finished video.",
        "voiceover": "DCAC helps young creators turn their ideas into real media skills.",
        "assets": "Short clips, graphics, youth quote with consent, project preview.",
        "scenes": [
            {
                "objective": "Hook viewers with the creator process.",
                "camera": "Close-up of camera, mic, or editing screen.",
                "framing": "Gear details or storyboard, vertical.",
                "motion": "Fast push-in or snap cut.",
                "text": "It starts with an idea.",
                "voiceover": "Every finished video starts with a first idea.",
                "emotion": "Curiosity.",
            },
            {
                "objective": "Show skill-building in action.",
                "camera": "Handheld b-roll.",
                "framing": "Youth planning, filming, checking shot, consent-safe.",
                "motion": "Quick jump cuts synced to beat.",
                "text": "Plan. Film. Edit.",
                "voiceover": "Youth practice real media skills step by step.",
                "emotion": "Momentum.",
            },
            {
                "objective": "Create payoff through before/after reveal.",
                "camera": "Screen recording or over-the-shoulder.",
                "framing": "Rough cut transitioning to polished final clip.",
                "motion": "Before/after snap transition.",
                "text": "Then the project comes to life.",
                "voiceover": "The final cut shows what practice can become.",
                "emotion": "Pride.",
            },
            {
                "objective": "Invite youth and supporters to connect.",
                "camera": "Static CTA or group workspace shot.",
                "framing": "Clean space for text.",
                "motion": "Hold for CTA.",
                "text": "Explore DCAC at BGC London.",
                "voiceover": "Explore DCAC programs and support youth creativity.",
                "emotion": "Creative confidence.",
            },
        ],
        "editing_style": {
            "pacing": "Fast cuts with a clear final payoff.",
            "transitions": "Before/after snap, screen flash, or beat cuts.",
            "music": "Modern upbeat creator-style audio.",
            "subtitles": "Use captions plus short text labels for each production step.",
            "color": "Bright creative workspace feel; keep screens readable.",
        },
        "trend_adaptation": [
            "Use creator-transformation before/after trend.",
            "Use behind-the-scenes setup shots common in creator content.",
            "Use quick reaction shot when youth see final edit.",
            "Use phone-shot authenticity to make the program approachable.",
        ],
        "low_effort": [
            "Use one clip of gear, one editing screen, one final project screenshot.",
            "Add text labels: idea, filming, final cut.",
            "Record a staff voiceover instead of interviews.",
            "Use a short project preview as the final payoff.",
        ],
    },
    "Inclusion Programs": {
        "length": "12-20 seconds",
        "channel": "Facebook, LinkedIn, Instagram Reels",
        "text": "Belonging is built in small moments.",
        "voiceover": "Inclusion means planning spaces where more people can participate and feel welcome.",
        "assets": "Consent-safe activity visuals, accessibility proof point, staff quote.",
        "scenes": [
            {
                "objective": "Define inclusion visually without relying on abstract language.",
                "camera": "Close-up of activity materials or adapted setup.",
                "framing": "Hands, tools, visual schedule, activity options.",
                "motion": "Slow pan across prepared space.",
                "text": "Inclusion can start here.",
                "voiceover": "Belonging is built before the activity begins.",
                "emotion": "Care and intention.",
            },
            {
                "objective": "Show participation support.",
                "camera": "Medium activity shot.",
                "framing": "Staff support from behind or side; avoid identifying participants without consent.",
                "motion": "Gentle follow shot.",
                "text": "Adapt. Support. Welcome.",
                "voiceover": "Small adaptations can make participation possible.",
                "emotion": "Dignity.",
            },
            {
                "objective": "Connect inclusion to mission.",
                "camera": "Static detail or wide room shot.",
                "framing": "Inclusive activity moment with clean overlay space.",
                "motion": "Hold or slow zoom.",
                "text": "Everyone deserves a place to belong.",
                "voiceover": "BGC London works to reduce barriers so more people can join in.",
                "emotion": "Belonging.",
            },
            {
                "objective": "Invite families and partners to learn more.",
                "camera": "CTA slide or BGC exterior.",
                "framing": "Simple text, contact prompt.",
                "motion": "No motion; readable CTA.",
                "text": "Ask about inclusion supports.",
                "voiceover": "Connect with BGC London to learn more.",
                "emotion": "Reassuring.",
            },
        ],
        "editing_style": {
            "pacing": "Gentle, clear pacing with fewer cuts.",
            "transitions": "Soft cuts; avoid flashy effects that distract from accessibility.",
            "music": "Warm, calm, hopeful music.",
            "subtitles": "Always on-screen, large and easy to read.",
            "color": "Soft natural colors with high contrast text.",
        },
        "trend_adaptation": [
            "Use 'small changes, big difference' text overlay trend.",
            "Use authentic behind-the-scenes preparation footage.",
            "Use quick examples instead of abstract definitions.",
            "Use partner-friendly captions for LinkedIn and Facebook.",
        ],
        "low_effort": [
            "Film non-identifying setup details.",
            "Use three text overlays explaining adaptations.",
            "Use a staff voiceover recorded on a phone.",
            "End with a simple 'ask us about support' card.",
        ],
    },
    "Sports Programs": {
        "length": "10-16 seconds",
        "channel": "Instagram Reels, TikTok, Facebook",
        "text": "Teamwork starts with showing up.",
        "voiceover": "At BGC London, sports help youth move, connect, and build confidence.",
        "assets": "Huddle clip, movement drill, coach encouragement, consent-safe team visuals.",
        "scenes": [
            {
                "objective": "Open with energy and motion.",
                "camera": "Low-angle phone shot.",
                "framing": "Shoes on court, ball bounce, gym floor.",
                "motion": "Fast tracking shot or quick cut.",
                "text": "Game day energy.",
                "voiceover": "Sports can change the feel of a whole day.",
                "emotion": "Excitement.",
            },
            {
                "objective": "Show teamwork, not just competition.",
                "camera": "Wide shot.",
                "framing": "Team huddle, high five, partner drill.",
                "motion": "Jump cuts between teamwork moments.",
                "text": "Move together.",
                "voiceover": "Youth practice teamwork, confidence, and encouragement.",
                "emotion": "Belonging and confidence.",
            },
            {
                "objective": "Show coach support.",
                "camera": "Medium shot of coach demonstrating.",
                "framing": "Coach hands, equipment, youth listening from behind.",
                "motion": "Short demo cut.",
                "text": "A coach in your corner.",
                "voiceover": "Caring adults help young people try again.",
                "emotion": "Support.",
            },
            {
                "objective": "Close with invitation.",
                "camera": "Static team or gym shot.",
                "framing": "Clean CTA space.",
                "motion": "Hold final frame.",
                "text": "Find your team at BGC London.",
                "voiceover": "Follow BGC London for more sports moments.",
                "emotion": "Motivating.",
            },
        ],
        "editing_style": {
            "pacing": "Fast, energetic cuts with clear captions.",
            "transitions": "Jump cuts, ball bounce cuts, beat-matched edits.",
            "music": "Upbeat, sporty, positive beat.",
            "subtitles": "Use short text overlays, not long sentences.",
            "color": "Bright gym colors, crisp contrast, avoid dark footage.",
        },
        "trend_adaptation": [
            "Use quick jump cuts and reaction shots.",
            "Use 'describe practice in one word' comment prompt.",
            "Use coach tip format for saveable content.",
            "Use authentic phone footage to keep energy real.",
        ],
        "low_effort": [
            "Film one huddle, one drill, one high-five.",
            "Add three text overlays: Teamwork, Movement, Confidence.",
            "Use royalty-free upbeat music.",
            "End with a simple program CTA.",
        ],
    },
    "50+ Wellness Programs": {
        "length": "12-20 seconds",
        "channel": "Facebook, Newsletter embed, Instagram Reels",
        "text": "Connection is wellness too.",
        "voiceover": "A welcoming routine can help older adults stay active, connected, and supported.",
        "assets": "Calendar, activity b-roll, participant-friendly photo, testimonial with consent.",
        "scenes": [
            {
                "objective": "Make the program feel welcoming and approachable.",
                "camera": "Warm wide shot.",
                "framing": "Coffee table, chairs, welcome materials, calendar.",
                "motion": "Slow pan or static shot.",
                "text": "A welcoming place to start.",
                "voiceover": "Wellness can begin with somewhere friendly to go.",
                "emotion": "Comfort.",
            },
            {
                "objective": "Show activity without making it intimidating.",
                "camera": "Medium shot.",
                "framing": "Gentle movement, hands, instructor demo.",
                "motion": "Slow, steady movement.",
                "text": "Move at your pace.",
                "voiceover": "Programs support movement, routine, and confidence.",
                "emotion": "Ease.",
            },
            {
                "objective": "Show social connection.",
                "camera": "Consent-safe room or table shot.",
                "framing": "Conversation details, hands with coffee, group from behind.",
                "motion": "Soft cut to social moment.",
                "text": "Connection matters.",
                "voiceover": "Being seen and welcomed can make a real difference.",
                "emotion": "Warmth.",
            },
            {
                "objective": "Drive calendar interest.",
                "camera": "Static calendar or CTA card.",
                "framing": "Monthly schedule, contact note.",
                "motion": "Hold for readability.",
                "text": "See this month's 50+ calendar.",
                "voiceover": "Ask about upcoming 50+ Wellness Programs.",
                "emotion": "Practical and inviting.",
            },
        ],
        "editing_style": {
            "pacing": "Gentle and readable; avoid fast cuts.",
            "transitions": "Soft cuts or simple fades.",
            "music": "Warm, light, calm music.",
            "subtitles": "Always include captions and large text.",
            "color": "Natural, bright, welcoming colors.",
        },
        "trend_adaptation": [
            "Use 'morning routine' format adapted for wellness programming.",
            "Use authentic phone-shot footage instead of staged promotional footage.",
            "Use simple text overlays for calendar highlights.",
            "Use testimonial snippets for trust-building.",
        ],
        "low_effort": [
            "Use the monthly calendar as the visual anchor.",
            "Add two existing activity photos.",
            "Record a staff voiceover about what to expect.",
            "End with phone/email or 'ask us for details' CTA.",
        ],
    },
}

VIDEO_TEMPLATES["Inclusion"] = VIDEO_TEMPLATES["Inclusion Programs"]
VIDEO_TEMPLATES["Sports"] = VIDEO_TEMPLATES["Sports Programs"]
VIDEO_TEMPLATES["50+ Wellness"] = VIDEO_TEMPLATES["50+ Wellness Programs"]

CONTENT_VARIATIONS = {
    "MAP Education Support": {
        "original": (
            "MAP Education Support helps youth build confidence before the school year gets busy. "
            "Through tutoring, caring adult support, and practical encouragement, BGC London helps young people "
            "stay connected to their goals. The program also has a clear proof point through the $1,000/year scholarship."
        ),
        "short": (
            "MAP Education Support helps youth build school confidence with tutoring, encouragement, and a clear "
            "$1,000/year scholarship proof point."
        ),
        "emotional": (
            "A little support at the right moment can change how a young person sees their future. MAP Education Support "
            "gives youth a place to ask questions, feel encouraged, and believe that school success is possible."
        ),
        "cta": (
            "Help a young person start the school year with confidence. Share MAP Education Support with a family, "
            "refer a youth, or connect with BGC London to learn more about tutoring and scholarship support."
        ),
        "parent": (
            "If your teen could use extra school support, MAP Education Support offers tutoring, encouragement, and a "
            "welcoming place to stay on track. BGC London is here to help families plan for a stronger school year."
        ),
    },
    "After-School Recreation": {
        "original": (
            "After-School Recreation gives children a safe, welcoming place to play, learn, and belong after the school day. "
            "Families can count on caring staff, active programming, and routines that support confidence and connection."
        ),
        "short": (
            "After-School Recreation offers safe, active, welcoming programs where children can play, learn, and belong."
        ),
        "emotional": (
            "After school should feel safe, joyful, and full of possibility. At BGC London, children are welcomed by caring "
            "staff, encouraged through play, and reminded that they belong."
        ),
        "cta": (
            "Looking for a safe after-school option? Connect with BGC London to learn about After-School Recreation, "
            "registration details, and available program supports."
        ),
        "parent": (
            "For busy parents, after-school time matters. BGC London's After-School Recreation gives children a supervised, "
            "active, and friendly place to go while families get reliable support they can trust."
        ),
    },
    "Supper Club": {
        "original": (
            "Supper Club brings people together around warm meals, conversation, and community connection. It helps reduce "
            "barriers for families while creating space for neighbours, volunteers, and supporters to show up for one another."
        ),
        "short": (
            "Supper Club brings neighbours together through warm meals, community connection, and volunteer support."
        ),
        "emotional": (
            "A shared meal can make someone feel less alone. Supper Club creates a warm, welcoming space where families and "
            "neighbours can connect, feel cared for, and be part of community."
        ),
        "cta": (
            "Support Supper Club by sharing the program, volunteering, or helping connect families with a welcoming meal "
            "and community support at BGC London."
        ),
        "parent": (
            "Supper Club is a welcoming community meal where families can connect, share food, and feel supported. It is a "
            "simple way to build routine, comfort, and connection close to home."
        ),
    },
}


def asset_score(program: dict) -> int:
    """Score asset readiness using mock asset availability and quality."""

    base = {"High": 95, "Medium": 76, "Quick phone photo": 62}.get(program["asset_quality"], 40)
    if "Videos" in program["assets"]:
        base += 3
    if "Testimonials" in program["assets"]:
        base += 4
    return min(base, 100)


def urgency_score(program: dict) -> int:
    """Score urgency from deadline and priority label."""

    days_until = max((program["date"] - TODAY).days, 1)
    date_score = max(45, 100 - days_until * 2)
    if program["urgency"] == "High":
        date_score += 10
    return min(date_score, 100)


def recommendation_score(program: dict) -> int:
    """Mock AI score combining timing, assets, performance, fit, and mission."""

    return round(
        urgency_score(program) * 0.22
        + asset_score(program) * 0.18
        + program["past_engagement"] * 0.2
        + program["audience_fit"] * 0.18
        + program["mission_alignment"] * 0.22
    )


def ranked_programs() -> list[dict]:
    """Return programs ranked by mock AI recommendation score."""

    return sorted(PROGRAMS, key=recommendation_score, reverse=True)


def custom_program_from_state() -> dict | None:
    """Build a temporary campaign object from the latest Program Intake fields."""

    selected_name = st.session_state.get("selected_campaign", "").strip()
    known_names = {program["name"] for program in PROGRAMS}
    intake_name = st.session_state.get("intake_program_name", "").strip()
    if not selected_name and not intake_name:
        return None
    campaign_name = selected_name or intake_name
    if campaign_name in known_names:
        return None

    latest_brief = st.session_state.get("latest_intake_brief", {})
    assets = latest_brief.get("available_assets") or ["Photos"]
    if "None" in assets:
        assets = []
    audience_items = latest_brief.get("target_audience") or ["Community", "Families"]
    goal = latest_brief.get("goal", "Awareness")
    key_message = latest_brief.get("key_message") or "A BGC London program update ready for community storytelling."

    return {
        "name": campaign_name,
        "segment": latest_brief.get("segment", "Program"),
        "audience": ", ".join(audience_items),
        "date": latest_brief.get("program_date", TODAY + timedelta(days=14)),
        "urgency": latest_brief.get("urgency", "High"),
        "assets": assets or ["Photos"],
        "asset_quality": latest_brief.get("asset_quality", "Medium"),
        "past_engagement": 88,
        "mission_alignment": 92,
        "audience_fit": 90,
        "proof": "New staff-submitted program brief",
        "angle": key_message,
        "required_assets": "Program photo, staff quote, clear next step",
        "channels": ["Instagram", "Facebook", "Newsletter", "Partners"] if goal != "Partner update" else ["LinkedIn", "Newsletter", "Partners"],
    }


def ranked_programs_with_current() -> list[dict]:
    """Return ranked programs, including the latest intake campaign when custom."""

    custom_program = custom_program_from_state()
    programs = [custom_program] + PROGRAMS if custom_program else PROGRAMS
    return sorted(programs, key=recommendation_score, reverse=True)


def get_program_or_current(name: str) -> dict:
    """Find a known program or return the current custom intake campaign."""

    for program in PROGRAMS:
        if program["name"] == name:
            return program
    custom_program = custom_program_from_state()
    if custom_program and custom_program["name"] == name:
        return custom_program
    if custom_program:
        return custom_program
    return get_program(name)


# ---------------------------------------------------------------------------
# Shared UI helpers
# ---------------------------------------------------------------------------

def init_state() -> None:
    """Set default selected campaign for cross-page workflow continuity."""

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "user_email" not in st.session_state:
        st.session_state.user_email = ""
    if "department" not in st.session_state:
        st.session_state.department = "Marketing"
    if "role" not in st.session_state:
        st.session_state.role = "Marketing"
    if "selected_campaign" not in st.session_state:
        st.session_state.selected_campaign = ranked_programs()[0]["name"]
    if "intake_program_name" not in st.session_state:
        st.session_state.intake_program_name = st.session_state.selected_campaign
    if "latest_intake_brief" not in st.session_state:
        st.session_state.latest_intake_brief = {}
    if "planner_items" not in st.session_state:
        st.session_state.planner_items = ["MAP scholarship post", "After-school parent post"]
    if "active_page" not in st.session_state:
        st.session_state.active_page = "Dashboard"
    if "page" not in st.session_state:
        st.session_state.page = st.session_state.active_page
    if st.session_state.page != st.session_state.active_page:
        st.session_state.active_page = st.session_state.page
    if "submitted_messages" not in st.session_state:
        st.session_state.submitted_messages = []
    if "department_messages" not in st.session_state:
        st.session_state.department_messages = []
    if "submitted_assets" not in st.session_state:
        st.session_state.submitted_assets = []
    if "calendar_briefs" not in st.session_state:
        st.session_state.calendar_briefs = []
    if "asset_filters" not in st.session_state:
        st.session_state.asset_filters = {
            "program": "All",
            "type": "All",
            "channel": "All",
            "status": "All",
        }
    if "asset_detail" not in st.session_state:
        st.session_state.asset_detail = None


def header(title: str, subtitle: str = "Plan, create, and execute campaigns across BGC programs") -> None:
    """Render a clean product header with a small BGC-inspired dot mark."""

    st.markdown(
        f"""
        <div class="command-header">
            <div class="header-eyebrow">{title}</div>
            <h1>AI Marketing Command Center</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def dashboard_hero() -> None:
    """Render the Dashboard hero image with a safe styled fallback."""

    image_path = Path("assets/bgc_hero.png")
    if image_path.exists():
        encoded = base64.b64encode(image_path.read_bytes()).decode("utf-8")
        background = f"background-image: url('data:image/png;base64,{encoded}');"
        extra_class = ""
    else:
        background = ""
        extra_class = " dashboard-hero-placeholder"

    st.markdown(
        f"""
        <div class="dashboard-hero{extra_class}" style="{background}">
            <div class="dashboard-hero-content">
                <h2>Opportunity Changes Everything</h2>
                <p>Turn real program moments into targeted community campaigns.</p>
                <span class="hero-pill">AI campaign recommendation ready</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def viral_engine_hero() -> None:
    """Render the AI Viral Content Engine hero image with a safe fallback."""

    image_path = Path("assets/viral_engine.png")
    if image_path.exists():
        encoded = base64.b64encode(image_path.read_bytes()).decode("utf-8")
        background = f"background-image: url('data:image/png;base64,{encoded}');"
        extra_class = ""
    else:
        background = ""
        extra_class = " viral-engine-hero-placeholder"

    st.markdown(
        f"""
        <div class="viral-engine-hero{extra_class}" style="{background}">
            <div class="viral-engine-hero-content">
                <h2>AI Viral Content Engine</h2>
                <p>Turn real BGC program moments into trend-ready short-form content.</p>
                {badge('TikTok / Reels ideas', 'yellow')}
                {badge('Creator-style hooks', 'softgreen')}
                {badge('Trend adaptation', 'navy')}
                {badge('Nonprofit-safe content', 'softgreen')}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def campaign_recommendation_hero() -> None:
    """Render the AI Campaign Recommendation hero image with a safe fallback."""

    image_path = Path("assets/ai_campaign.png")
    if image_path.exists():
        encoded = base64.b64encode(image_path.read_bytes()).decode("utf-8")
        background = f"background-image: url('data:image/png;base64,{encoded}');"
        extra_class = ""
    else:
        background = ""
        extra_class = " campaign-recommendation-hero-placeholder"

    st.markdown(
        f"""
        <div class="campaign-recommendation-hero{extra_class}" style="{background}">
            <div class="campaign-recommendation-hero-content">
                <h2>AI Campaign Recommendation</h2>
                <p>Data-driven campaign prioritization for BGC programs.</p>
                {badge('Audience fit', 'softgreen')}
                {badge('Asset readiness', 'yellow')}
                {badge('Timing signal', 'navy')}
                {badge('Recommended next step', 'softgreen')}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


MARKETING_WORKFLOW_STEPS = [
    {
        "step": "1",
        "title": "Intake",
        "help": "Collect program updates and assets.",
        "pages": [("Program & Asset Intake", "📝")],
        "status": "Start here",
    },
    {
        "step": "2",
        "title": "Recommend",
        "help": "Choose the strongest campaign.",
        "pages": [("AI Campaign Recommendation", "✨")],
        "status": "AI ranked",
    },
    {
        "step": "3",
        "title": "Create",
        "help": "Build content, hooks, and drafts.",
        "pages": [("AI Viral Content Engine", "🔥"), ("AI Content Studio", "✍️")],
        "status": "Drafting",
    },
    {
        "step": "4",
        "title": "Plan",
        "help": "Schedule digital and community activity.",
        "pages": [("Campaign Planner", "📅")],
        "status": "Calendar",
    },
    {
        "step": "5",
        "title": "Measure",
        "help": "Review signals and impact.",
        "pages": [("Trend & Performance Scan", "📊"), ("Impact Dashboard", "📈")],
        "status": "Insights",
    },
]

TEAM_WORKSPACE_PAGES = [
    ("Shared Calendar", "📅", "Campaign and activity schedule"),
    ("Department Message Board", "💬", "Cross-department updates"),
    ("Asset Library", "📂", "Photos, clips, and reusable content"),
]

MARKETING_NAV_SECTIONS = [
    ("Overview", [("Dashboard", "🏠")]),
    ("Marketing Workflow", [(page_name, icon) for step in MARKETING_WORKFLOW_STEPS for page_name, icon in step["pages"]]),
    ("Team Workspace", [(page_name, icon) for page_name, icon, _help in TEAM_WORKSPACE_PAGES]),
]

DEPARTMENT_NAV_SECTIONS = [
    ("Assets & Collaboration", [("Department Message Board", "💬"), ("Shared Calendar", "📅"), ("Asset Upload / Asset Library", "📂")]),
]


def render_sidebar_v2() -> str:
    """Render the rebuilt stable sidebar navigation and return active page."""

    if st.session_state.role == "Marketing":
        allowed_pages = ["Dashboard"] + [page_name for step in MARKETING_WORKFLOW_STEPS for page_name, _icon in step["pages"]] + [
            page_name for page_name, _icon, _help in TEAM_WORKSPACE_PAGES
        ]
    else:
        nav_sections = DEPARTMENT_NAV_SECTIONS
        allowed_pages = [page_name for _section, items in nav_sections for page_name, _icon in items]
    current_page = st.session_state.get("page", st.session_state.active_page)
    if current_page not in allowed_pages:
        current_page = allowed_pages[0]
    st.session_state.page = current_page
    st.session_state.active_page = current_page

    st.sidebar.markdown(
        """
        <div class="bgc-side-v2">
            <div class="bgc-brand-v2">
                <div class="bgc-brand-top-v2">
                    <div class="bgc-brand-title-v2">BGC London</div>
                    <div class="bgc-dot-cluster-v2"><span></span><span></span><span></span><span></span></div>
                </div>
                <div class="bgc-brand-subtitle-v2">Community. Youth. Belonging.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.markdown(
        f"""
        <div class="bgc-user-card-v2">
            <div class="bgc-user-label-v2">Logged in as</div>
            <div class="bgc-user-email-v2">{st.session_state.user_email}</div>
            <div class="bgc-user-dept-v2">Department: {st.session_state.department}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.sidebar.button("Log out", key="bgc_logout_v2"):
        st.session_state.logged_in = False
        st.session_state.user_email = ""
        st.session_state.department = "Marketing"
        st.session_state.role = "Marketing"
        st.session_state.page = "Dashboard"
        st.session_state.active_page = "Dashboard"
        st.rerun()

    if st.session_state.role == "Marketing":
        if not st.session_state.calendar_briefs:
            helper_text = "Start with Program & Asset Intake."
        elif st.session_state.page in ["AI Content Studio", "AI Viral Content Engine"]:
            helper_text = "Move ready drafts into Campaign Planner."
        else:
            helper_text = "Review the AI recommendation, then create content."
        st.sidebar.markdown(
            f"""
            <div class="bgc-flow-helper-v3">
                <strong>What should I do next?</strong>
                <span>{helper_text}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.sidebar.markdown('<div class="bgc-nav-title-v2">Overview</div>', unsafe_allow_html=True)
        if st.session_state.page == "Dashboard":
            st.sidebar.markdown(
                """
                <div class="bgc-sidebar-link-v4 bgc-sidebar-link-active-v4">
                    <span class="bgc-sidebar-step-v4">🏠</span>
                    <span>Dashboard<span class="bgc-sidebar-link-sub-v4">Overview + next action</span></span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        elif st.sidebar.button("🏠 Dashboard", key="overview-nav-dashboard", use_container_width=True):
            st.session_state.page = "Dashboard"
            st.session_state.active_page = "Dashboard"
            st.rerun()

        st.sidebar.markdown('<div class="bgc-nav-title-v2">Marketing Workflow</div>', unsafe_allow_html=True)
        workflow_links = [
            ("1", "Intake", "Program & Asset Intake", "Program update + assets"),
            ("2", "Recommend", "AI Campaign Recommendation", "Best campaign to run"),
            ("3A", "Ideas", "AI Viral Content Engine", "Hooks + video ideas"),
            ("3B", "Drafts", "AI Content Studio", "Copy + scoring"),
            ("4", "Plan", "Campaign Planner", "Weekly + community plan"),
            ("5A", "Trends", "Trend & Performance Scan", "Signals + opportunities"),
            ("5", "Impact", "Impact Dashboard", "Results + donor proof"),
        ]
        for step_number, label, page_name, helper in workflow_links:
            if st.session_state.page == page_name:
                st.sidebar.markdown(
                    f"""
                    <div class="bgc-sidebar-link-v4 bgc-sidebar-link-active-v4">
                        <span class="bgc-sidebar-step-v4">{step_number}</span>
                        <span>{label}<span class="bgc-sidebar-link-sub-v4">{helper}</span></span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                if st.sidebar.button(f"{step_number} {label}", key=f"flow-nav-{page_name}", use_container_width=True):
                    st.session_state.page = page_name
                    st.session_state.active_page = page_name
                    st.rerun()

        st.sidebar.markdown('<div class="bgc-nav-title-v2">Team Workspace</div>', unsafe_allow_html=True)
        for page_name, icon, help_text in TEAM_WORKSPACE_PAGES:
            if st.session_state.page == page_name:
                st.sidebar.markdown(
                    f"""
                    <div class="bgc-sidebar-link-v4 bgc-sidebar-link-active-v4">
                        <span class="bgc-sidebar-step-v4">{icon}</span>
                        <span>{page_name}<span class="bgc-sidebar-link-sub-v4">{help_text}</span></span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                if st.sidebar.button(f"{icon} {page_name}", key=f"team-nav-{page_name}", use_container_width=True):
                    st.session_state.page = page_name
                    st.session_state.active_page = page_name
                    st.rerun()
    else:
        for section, items in nav_sections:
            st.sidebar.markdown(
                f"""
                <div class="bgc-nav-section-v2">
                    <div class="bgc-nav-title-v2">{section}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            for page_name, icon in items:
                if st.session_state.page == page_name:
                    st.sidebar.markdown(
                        f"""
                        <div class="bgc-nav-link-active-v2">
                            <span class="bgc-nav-icon-v2">{icon}</span>
                            <span class="bgc-nav-label-v2">{page_name}</span>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                else:
                    if st.sidebar.button(f"{icon} {page_name}", key=f"nav-v2-{page_name}"):
                        st.session_state.page = page_name
                        st.session_state.active_page = page_name
                        st.rerun()

    if st.session_state.role == "Marketing":
        st.sidebar.markdown(
            f"""
            <div class="bgc-nav-title-v2">Selected Campaign</div>
            <div class="bgc-selected-campaign-v2">{st.session_state.selected_campaign}</div>
            """,
            unsafe_allow_html=True,
        )

    st.sidebar.caption("Mock data only. No external API calls. Built for fast nonprofit marketing demos.")
    return st.session_state.page


def badge(text: str, kind: str = "navy") -> str:
    """Return badge HTML."""

    return f'<span class="badge badge-{kind}">{text}</span>'


def status_kind(text: str) -> str:
    """Map labels to badge styles."""

    mapping = {
        "High": "yellow",
        "Medium": "softgreen",
        "Low": "navy",
        "Approved": "softgreen",
        "Scheduled": "softgreen",
        "Published": "green",
        "Draft": "navy",
        "Ready": "softgreen",
        "Needs Review": "yellow",
        "Needs Assets": "yellow",
        "Needs consent check": "red",
        "Ready to publish": "green",
        "Low risk": "softgreen",
        "New": "yellow",
        "Seen by Marketing": "softgreen",
        "In progress": "softgreen",
        "Confirmed": "softgreen",
        "Planned": "navy",
        "Needs assets": "yellow",
        "Needs consent": "yellow",
        "Submitted": "yellow",
        "Marketing review": "yellow",
    }
    return mapping.get(text, "navy")


def status_badge(text: str) -> str:
    """Return a styled status badge."""

    return badge(text, status_kind(text))


def brief_calendar_status(assets: list[str], key_message: str) -> str:
    """Infer a simple calendar status for a mock intake brief."""

    if not key_message.strip():
        return "Draft"
    if not assets or "None" in assets:
        return "Needs Assets"
    return "Ready"


def save_brief_to_shared_calendar(brief: dict) -> None:
    """Create or update a session-state calendar item from Program Intake."""

    existing_index = None
    for index, item in enumerate(st.session_state.calendar_briefs):
        if item["program_name"].strip().lower() == brief["program_name"].strip().lower() and item["program_date"] == brief["program_date"]:
            existing_index = index
            break

    if existing_index is None:
        st.session_state.calendar_briefs.append(brief)
    else:
        st.session_state.calendar_briefs[existing_index] = brief


def kpi(label: str, value: str, note: str, green: bool = False) -> None:
    """Render a KPI card."""

    klass = "card-green" if green else "card-yellow"
    st.markdown(
        f"""
        <div class="{klass}">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="muted">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def content_studio_hero() -> None:
    """Render the AI Content Studio hero image with a safe fallback."""

    image_path = Path("assets/AI content.png")
    if image_path.exists():
        encoded = base64.b64encode(image_path.read_bytes()).decode("utf-8")
        background = f"background-image: url('data:image/png;base64,{encoded}');"
        extra_class = ""
    else:
        background = ""
        extra_class = " content-studio-hero-placeholder"

    st.markdown(
        f"""
        <div class="content-studio-hero{extra_class}" style="{background}">
            <div class="content-studio-hero-content">
                <h2>AI Content Studio</h2>
                <p>Create, adapt, and score campaign content for every channel.</p>
                {badge('Multi-channel copy', 'softgreen')}
                {badge('Content score', 'yellow')}
                {badge('Brand voice', 'navy')}
                {badge('Ready for approval', 'softgreen')}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def get_program(name: str) -> dict:
    """Find program by name."""

    return next(program for program in PROGRAMS if program["name"] == name)


def set_recommended_campaign(program_name: str) -> None:
    """Save selected recommendation for other pages."""

    st.session_state.selected_campaign = program_name


def action_buttons(program_name: str) -> None:
    """Show mock workflow action buttons for a recommendation."""

    cols = st.columns(4)
    actions = ["Create campaign brief", "Generate content", "Add to planner", "Request assets"]
    for col, action in zip(cols, actions):
        if col.button(action, key=f"{program_name}-{action}"):
            set_recommended_campaign(program_name)
            if action == "Add to planner":
                item = f"{program_name} campaign"
                if item not in st.session_state.planner_items:
                    st.session_state.planner_items.append(item)
                st.success(f"Added {program_name} to the mock planner.")
            else:
                st.success(f"{action} started for {program_name}.")


def clamp_score(value: int) -> int:
    """Keep mock AI scores in a readable range."""

    return max(35, min(98, value))


def content_score(text: str, channel: str, tone: str, program: dict) -> dict:
    """Score content with deterministic demo heuristics instead of real AI."""

    lowered = text.lower()
    words = text.split()
    length = len(words)
    emotional_keywords = [
        "belong", "confidence", "support", "community", "care", "safe", "welcoming",
        "hope", "goals", "together", "connection", "opportunity", "families", "youth",
    ]
    cta_keywords = ["learn", "share", "save", "contact", "support", "volunteer", "register", "refer", "ask", "explore"]
    hook_keywords = ["pov", "what", "why", "how", "today", "finally", "imagine", "from", "watch"]
    emotional_hits = sum(1 for word in emotional_keywords if word in lowered)
    cta_hits = sum(1 for word in cta_keywords if word in lowered)
    hook_hits = sum(1 for word in hook_keywords if word in lowered[:180])

    ideal_length = {
        "Instagram": (70, 170),
        "Facebook": (95, 230),
        "LinkedIn": (90, 220),
        "Newsletter": (130, 290),
        "Google Ads Grant": (25, 80),
        "Partner Email": (95, 230),
        "Local Media Pitch": (90, 220),
    }.get(channel, (75, 190))
    if ideal_length[0] <= length <= ideal_length[1]:
        clarity = 86
    else:
        clarity = 74 - min(18, abs(length - sum(ideal_length) // 2) // 12)

    tone_bonus = {
        "Warm": 8,
        "Parent-friendly": 7,
        "Youth-focused": 7,
        "Donor-focused": 5,
        "Informational": 2,
    }[tone]
    platform_bonus = 7 if channel in ["Instagram", "Facebook"] else 5 if channel in ["Newsletter", "Partner Email"] else 3

    scores = {
        "Emotional Impact": clamp_score(62 + emotional_hits * 5 + tone_bonus),
        "Hook Strength": clamp_score(58 + hook_hits * 9 + (8 if channel == "Instagram" else 3)),
        "Clarity": clamp_score(clarity),
        "CTA Strength": clamp_score(54 + cta_hits * 8),
        "Shareability": clamp_score(58 + emotional_hits * 3 + cta_hits * 3 + platform_bonus),
        "Parent Appeal": clamp_score(60 + (12 if tone == "Parent-friendly" else 0) + (9 if "parent" in lowered or "famil" in lowered else 0) + (8 if program["segment"] in ["Children", "MAP"] else 0)),
        "Youth Appeal": clamp_score(58 + (12 if tone == "Youth-focused" else 0) + (9 if "youth" in lowered or "goals" in lowered else 0) + (8 if program["segment"] in ["MAP", "DCAC"] else 0)),
        "Authenticity": clamp_score(64 + (8 if "story" in lowered or "real" in lowered else 0) + (6 if "quote" in lowered or "moment" in lowered else 0) + tone_bonus // 2),
        "Community Relevance": clamp_score(66 + (10 if "community" in lowered or "london" in lowered else 0) + program["mission_alignment"] // 10),
    }
    overall = round(sum(scores.values()) / len(scores))

    feedback = []
    if scores["Hook Strength"] < 78:
        feedback.append("Add a stronger opening hook in the first sentence or first on-screen text.")
    if scores["CTA Strength"] < 72:
        feedback.append("Make the CTA clearer: ask people to save, share, register, volunteer, or refer.")
    if scores["Emotional Impact"] < 78:
        feedback.append("Add a human moment, quote, reaction, or real participant outcome earlier.")
    if scores["Clarity"] < 78:
        feedback.append(f"Adjust length for {channel}; keep sentences shorter and easier to scan.")
    if scores["Authenticity"] < 78:
        feedback.append("Mention a real program moment or use a phone-shot asset to make it feel less generic.")
    if not feedback:
        feedback.append("Strong draft. The next improvement would be adding a specific quote or visual moment.")

    expected = "High" if overall >= 82 else "Medium-high" if overall >= 72 else "Medium"
    best_platform = "Instagram Reels" if channel == "Instagram" else channel
    if channel == "Google Ads Grant":
        best_platform = "Google Search"
    best_audience = {
        "Children": "Parents 30-45",
        "MAP": "Youth, parents, and school partners",
        "Supper Club": "Volunteers and community supporters",
        "DCAC": "Youth creators and creative partners",
        "50+": "Older adults and caregivers",
        "Inclusion": "Families, partners, and donors",
    }.get(program["segment"], program["audience"])
    posting_time = "Weekday evenings" if channel in ["Instagram", "Facebook"] else "Tuesday or Thursday morning"

    return {
        "overall": overall,
        "scores": scores,
        "feedback": feedback[:5],
        "expected": expected,
        "best_platform": best_platform,
        "best_audience": best_audience,
        "posting_time": posting_time,
    }


def split_generated_content(text: str) -> dict[str, str]:
    """Split generated copy into hook, body, CTA, and hashtag sections."""

    lines = [line.strip() for line in text.strip().splitlines() if line.strip()]
    if len(lines) == 1:
        single_line = lines[0]
        hashtags = " ".join(part for part in single_line.split() if part.startswith("#"))
        plain_text = " ".join(part for part in single_line.split() if not part.startswith("#"))
        sentences = []
        current = ""
        for char in plain_text:
            current += char
            if char in ".!?":
                sentences.append(current.strip())
                current = ""
        if current.strip():
            sentences.append(current.strip())

        hook = sentences[0] if sentences else plain_text
        cta_terms = ["share", "learn", "save", "connect", "contact", "support", "volunteer", "register", "explore", "refer"]
        cta_index = None
        for index in range(len(sentences) - 1, 0, -1):
            if any(term in sentences[index].lower() for term in cta_terms):
                cta_index = index
                break
        if cta_index is None and len(sentences) > 1:
            cta_index = len(sentences) - 1
        cta = sentences[cta_index] if cta_index is not None else ""
        body = " ".join(sentence for index, sentence in enumerate(sentences[1:], start=1) if index != cta_index)
        return {
            "hook": hook,
            "body": body,
            "cta": cta,
            "hashtags": hashtags,
        }

    hook = lines[0] if lines else ""
    hashtags = " ".join(line for line in lines if "#" in line)
    non_hashtag_lines = [line for line in lines[1:] if "#" not in line]
    cta_index = None
    cta_terms = ["share", "learn", "save", "connect", "contact", "support", "volunteer", "register", "explore", "refer"]
    for index in range(len(non_hashtag_lines) - 1, -1, -1):
        lowered = non_hashtag_lines[index].lower()
        if any(term in lowered for term in cta_terms):
            cta_index = index
            break
    if cta_index is None and non_hashtag_lines:
        cta_index = len(non_hashtag_lines) - 1

    cta = non_hashtag_lines[cta_index] if cta_index is not None else ""
    body_lines = [line for index, line in enumerate(non_hashtag_lines) if index != cta_index]
    return {
        "hook": hook,
        "body": "\n\n".join(body_lines),
        "cta": cta,
        "hashtags": hashtags,
    }


def render_generated_content_panel(text: str, channel: str, tone: str, score_data: dict, panel_key: str) -> None:
    """Render the generated draft as a premium AI output deliverable."""

    parts = split_generated_content(text)
    score_subset = {
        "Emotional strength": score_data["scores"]["Emotional Impact"],
        "Shareability": score_data["scores"]["Shareability"],
        "Parent engagement": score_data["scores"]["Parent Appeal"],
        "Authenticity": score_data["scores"]["Authenticity"],
    }
    why_items = [
        "Emotional hook gives the draft a human entry point.",
        "Real-life framing makes the program feel concrete.",
        "Community language connects the message to BGC's mission.",
        "Clear CTA gives the audience a next step.",
        "Authentic storytelling keeps the copy from feeling corporate.",
    ]

    with st.container(border=True, key=f"ai_output_panel_{panel_key}"):
        header_cols = st.columns([0.58, 0.42], vertical_alignment="center")
        with header_cols[0]:
            st.caption("✨ AI Generated Content")
            st.markdown(f"### {channel} Draft")
        with header_cols[1]:
            badge_cols = st.columns(3)
            badge_cols[0].badge(channel, color="green")
            badge_cols[1].badge(f"{tone} Tone", color="yellow")
            badge_cols[2].badge(f"{score_data['overall']} Score", color="yellow")

        st.divider()
        with st.container(border=True, key=f"ai_hook_{panel_key}"):
            st.caption("HOOK")
            st.markdown(f"#### {parts['hook'][:220]}")
        if parts["body"]:
            with st.container(border=True, key=f"ai_body_{panel_key}"):
                st.caption("DRAFT PREVIEW")
                st.markdown(parts["body"])

        with st.expander("Content score analysis", expanded=False):
            st.metric("Overall Content Score", f"{score_data['overall']} / 100")
            st.progress(score_data["overall"] / 100)
            st.caption(f"Expected performance: {score_data['expected']} · Best platform: {score_data['best_platform']}")
        with st.expander("Emotional breakdown", expanded=False):
            score_keys = {
                "Emotional strength": "emotional",
                "Shareability": "shareability",
                "Parent engagement": "parent",
                "Authenticity": "authenticity",
            }
            for label, value in score_subset.items():
                with st.container(key=f"score_{score_keys[label]}_{panel_key}"):
                    st.caption(f"{label}: {value}")
                    st.progress(value / 100)
        with st.expander("Why this works", expanded=False):
            bullet_colors = ["green", "blue", "green", "orange", "green"]
            for color, item in zip(bullet_colors, why_items):
                st.markdown(f":{color}[●] {item}")
            st.markdown("**What could improve this content?**")
            for item in score_data["feedback"]:
                st.markdown(f"- {item}")
        with st.expander("Hashtags & CTA", expanded=False):
            if parts["cta"]:
                st.markdown("**CTA**")
                st.info(parts["cta"])
            if parts["hashtags"]:
                st.markdown("**Hashtags**")
                st.caption(parts["hashtags"])
        with st.expander("Multi-platform adaptation", expanded=False):
            st.markdown(
                "- Adapt the hook as the first on-screen text for Reels.\n"
                "- Use the proof point as the newsletter or partner email anchor.\n"
                "- Keep the CTA consistent across channels so the campaign feels memorable.\n"
                "- Pair the draft with one consent-safe visual moment."
            )


def channel_copy(program: dict, channel: str, tone: str, emotional_angle: str = "Belonging", audience_frame: str = "Parents") -> str:
    """Generate deterministic mock channel copy without external AI calls."""

    tone_profile = {
        "Warm": {
            "hook": "Support can completely change what a day feels like.",
            "context": "At BGC London, the most meaningful moments are often small: a caring adult noticing effort, a young person trying again, or a family finding a place that feels steady.",
            "cta": "Share this with someone who could use a welcoming next step.",
        },
        "Informational": {
            "hook": f"Program update: {program['name']} is an important part of BGC London's community support network.",
            "context": "This campaign should clearly explain who the program supports, why it matters now, and how families, partners, or community members can take action.",
            "cta": "Learn more, share the update, or connect someone to the right BGC contact.",
        },
        "Donor-focused": {
            "hook": "Community support becomes powerful when it turns into practical opportunity.",
            "context": "Programs like this help move beyond awareness by connecting local care to visible outcomes, trusted relationships, and stronger futures.",
            "cta": "Support BGC London programs that help turn generosity into measurable local impact.",
        },
        "Parent-friendly": {
            "hook": "Families need places they can trust, especially when schedules, school, and daily routines feel full.",
            "context": "BGC London programs are designed to feel safe, welcoming, and practical for families looking for support close to home.",
            "cta": "Save this update, ask about program details, or share it with another parent or caregiver.",
        },
        "Youth-focused": {
            "hook": "Your goals, your voice, and your future all deserve space to grow.",
            "context": "BGC London programs give youth a place to try, create, ask questions, build confidence, and feel like they belong.",
            "cta": "Explore what is available, bring a friend, or take one small step toward something new.",
        },
    }[tone]
    proof = f"Proof point: {program['proof']}."
    angle_sentence = f"{program['name']} supports {program['angle'].lower()}"
    audience_sentence = f"The strongest audience for this message is {program['audience'].lower()}."
    angle_guidance = {
        "Confidence": "Frame the story around someone gaining confidence after being supported by BGC.",
        "Belonging": "Frame the story around a participant realizing they have a place where they are known and welcomed.",
        "Safety": "Frame the story around trust, reliable routines, and caring adults.",
        "Future success": "Frame the story around long-term goals, momentum, and a next step becoming possible.",
        "Community support": "Frame the story around neighbours, staff, partners, and donors showing up together.",
        "Kids being kids": "Frame the story around play, joy, friendship, and the freedom to simply participate.",
        "Donor impact": "Frame the story around how generosity becomes practical local change.",
    }[emotional_angle]
    audience_guidance = {
        "Parents": "Speak to safety, trust, support systems, development, and emotional reassurance.",
        "Youth": "Speak to identity, belonging, opportunity, aspiration, and the feeling of being taken seriously.",
        "Older adults": "Speak to routine, wellness, connection, dignity, and community.",
        "Donors": "Speak to impact, transformation, credibility, proof points, and measurable outcomes.",
    }[audience_frame]
    transformation_line = (
        "Lead with transformation, not announcement: a person arrives unsure, receives steady support, "
        "and leaves with more confidence, connection, or momentum."
    )

    snippets = {
        "Instagram": (
            f"{tone_profile['hook']}\n\n"
            f"{tone_profile['context']} {angle_sentence} "
            f"Think of the real-life moments behind the campaign: walking into a familiar room, being greeted by name, getting help with a question, sharing a meal, joining a team, or seeing a creative idea come to life. "
            f"{angle_guidance} {audience_guidance} {proof} "
            f"This post should feel human first and promotional second, with a real program moment leading the story.\n\n"
            f"{tone_profile['cta']}\n\n"
            "#BGCLondon #Belonging #Community #YouthOpportunity"
        ),
        "Facebook": (
            f"{tone_profile['hook']}\n\n"
            f"{program['name']} is one way BGC London helps create belonging, confidence, and connection for local families. "
            f"{angle_sentence} For parents, caregivers, and community members, the value is not only the program activity itself; it is the reliable support system around it. "
            f"{transformation_line} {angle_guidance} {proof} {audience_sentence}\n\n"
            "If you know a family, youth, volunteer, partner, or neighbour who should hear about this, please share this update. "
            f"{tone_profile['cta']}"
        ),
        "LinkedIn": (
            f"{program['name']} reflects BGC London's broader role as a community organization focused on inclusion, opportunity, and practical support across generations.\n\n"
            f"This campaign highlights {program['angle'].lower()} It is a strong fit for partners and community stakeholders because it connects a clear local need with an established program response. "
            f"{angle_guidance} {proof} The campaign can also help partners understand where referrals, awareness, volunteer support, or funding can make a visible difference.\n\n"
            "For organizations, funders, and community leaders, this is an opportunity to amplify work that is already trusted by families and participants. "
            "Connect with BGC London to learn how partnership can help extend the reach of this program."
        ),
        "Newsletter": (
            f"Featured program: {program['name']}\n\n"
            f"{tone_profile['hook']} This month, BGC London is highlighting {program['name']} because it speaks directly to the kind of support our community asks for: programs that are welcoming, practical, and rooted in belonging. "
            f"{angle_sentence} {transformation_line} {proof}\n\n"
            f"{audience_sentence} A newsletter feature can give readers more context than a social post: who the program is for, what kind of moment it creates, and why it matters now. "
            "This is also a good place to include a real quote, a program photo, or a simple next-step link.\n\n"
            f"{tone_profile['cta']}"
        ),
        "Google Ads Grant": (
            f"Headline 1: {program['name']}\n"
            "Headline 2: BGC London Programs\n"
            f"Headline 3: Support, Belonging, Opportunity\n"
            f"Description 1: Explore {program['segment']} programs at BGC London that help people connect with trusted support close to home.\n"
            f"Description 2: {program['angle']} {emotional_angle} starts with support. Learn more today."
        ),
        "Partner Email": (
            f"Hello,\n\n"
            f"BGC London is sharing a campaign update about {program['name']}, and we would appreciate your help getting it to the right people in the community. "
            f"{angle_sentence} {angle_guidance} {proof}\n\n"
            f"This update is especially relevant for {program['audience'].lower()}. If someone in your network could benefit, please consider sharing the program information, making a referral, or connecting them with BGC London. "
            "Even a simple forward from a trusted partner can help a family, youth, participant, or volunteer discover support at the right time.\n\n"
            f"{tone_profile['cta']}\n\n"
            "Thank you for helping strengthen community connection,\nBGC London"
        ),
        "Local Media Pitch": (
            f"Story idea: BGC London's {program['name']} is helping address {program['angle'].lower()}\n\n"
            f"This is a timely local story because it connects community need with practical support, real participant experiences, and the broader role BGC London plays across children, youth, families, and older adults. "
            f"{angle_guidance} {proof} A strong media angle could focus on one human story, one program moment, and one clear community outcome.\n\n"
            "Possible visuals include program activity photos, a staff or participant quote, and a short explanation of how local residents can get involved or learn more. "
            "BGC London can provide background, program context, and suggested interview contacts where appropriate."
        ),
    }
    return snippets[channel]


def content_variation(
    program: dict,
    channel: str,
    tone: str,
    version: str,
    emotional_angle: str = "Belonging",
    audience_frame: str = "Parents",
) -> str:
    """Return a predefined rewrite variation, with a safe fallback for other campaigns."""

    original = channel_copy(program, channel, tone, emotional_angle, audience_frame)
    base_context = (
        f"{program['name']} supports {program['angle'].lower()} "
        f"The campaign should speak to {program['audience'].lower()}, use a {emotional_angle.lower()} angle, "
        f"frame the audience as {audience_frame.lower()}, and include this proof point: {program['proof']}."
    )
    fallback_variations = {
        "original": original,
        "short": (
            f"{program['name']} helps turn everyday program moments into real support, confidence, and connection. "
            f"{base_context} "
            "Share this update with someone who could benefit, or connect with BGC London to learn the next step."
        ),
        "emotional": (
            "A supportive place can change how someone sees the rest of their day, and sometimes how they see their future. "
            f"Through {program['name']}, BGC London creates moments where people feel noticed, encouraged, and welcomed into community. "
            f"{base_context} "
            "The strongest version of this post should lead with a real human moment: a smile after trying again, a conversation with a mentor, a shared meal, a team huddle, or a participant realizing they belong. "
            "Invite people to share the story, make a referral, volunteer, or help someone discover BGC London."
        ),
        "cta": (
            f"{program['name']} is ready to be shared with the people who need it most. "
            f"{base_context} "
            "If you are a parent, caregiver, youth, partner, volunteer, or community supporter, there is a clear next step: save this update, share it with someone in your network, or contact BGC London for details. "
            "A simple share can help someone find support at the exact moment they are looking for it."
        ),
        "parent": (
            f"For parents and caregivers, trusted support matters because the small details of the day matter. "
            f"{program['name']} offers a welcoming BGC London connection point where families can feel more confident about safety, routine, belonging, and next steps. "
            f"{base_context} "
            "This message should make it easy for a parent to understand who the program is for, why it matters, and how to ask questions without feeling overwhelmed. "
            "Save this update, share it with another family, or reach out to BGC London to learn more."
        ),
    }
    return fallback_variations[version]


def draft_key(program_name: str, channel: str) -> str:
    """Create a stable session key for a content draft."""

    return f"content_draft::{program_name}::{channel}"


def campaign_from_asset_program(program: str) -> str:
    """Map asset program labels to the closest campaign name."""

    mapping = {
        "Children": "After-School Recreation",
        "Youth": "MAP Education Support",
        "MAP": "MAP Education Support",
        "Supper Club": "Supper Club",
        "DCAC": "DCAC Media Program",
        "50+": "50+ Wellness Programs",
        "Inclusion": "Inclusion Programs",
        "Sports": "After-School Recreation",
    }
    return mapping.get(program, st.session_state.selected_campaign)


def asset_icon(asset_type: str) -> str:
    """Return a visual placeholder icon for an asset type."""

    if "video" in asset_type.lower():
        return "🎥"
    if "graphic" in asset_type.lower():
        return "🎨"
    if "testimonial" in asset_type.lower():
        return "💬"
    if "newsletter" in asset_type.lower():
        return "📰"
    return "🖼️"


def asset_suggestion_parts(asset: tuple) -> tuple[str, str, str]:
    """Create short suggestion lines for asset cards and detail view."""

    _name, asset_type, program, channel, _approval, _consent, suggestion = asset
    best_for = f"Best for: {channel}"
    if "video" in asset_type.lower():
        use_for = "Use for: Short-form story"
        pair_with = "Pair with: youth voice"
    elif program == "Children":
        use_for = "Use for: Parent outreach"
        pair_with = "Pair with: registration CTA"
    elif program == "Supper Club":
        use_for = "Use for: Volunteer outreach"
        pair_with = "Pair with: real photo"
    elif "testimonial" in asset_type.lower():
        use_for = "Use for: Donor/partner proof"
        pair_with = "Pair with: impact stat"
    else:
        use_for = "Use for: Campaign support"
        pair_with = "Pair with: clear CTA"
    return best_for, use_for, pair_with or suggestion


def login_page() -> None:
    """Render a mock login gate for department participation."""

    with st.container(key="login_page"):
        with st.container(key="login_card", horizontal=True, gap=None, vertical_alignment="center"):
            with st.container(key="login_hero_image"):
                st.image("assets/login_hero.png", use_container_width=True)
            with st.container(key="login_form_panel"):
                st.markdown(
                    """
                    <span class="login-card-marker"></span>
                    <h1 class="login-system-title">Marketing Collaboration System</h1>
                    <p class="login-subtitle">
                        Campaign planning, shared assets, and department updates in one workspace.
                    </p>
                    """,
                    unsafe_allow_html=True,
                )
                with st.form("login-form"):
                    email = st.text_input("Email", placeholder="name@bgc.ca")
                    password = st.text_input("Password", type="password", placeholder="test")
                    department = st.selectbox("Department", DEPARTMENTS)
                    submitted = st.form_submit_button("Log in", type="primary")
                st.markdown('<div class="login-divider">or</div>', unsafe_allow_html=True)
                demo_submitted = st.button("Demo Easy Login", key="login-demo-easy", use_container_width=True)
                st.markdown(
                    """
                    <div class="login-helper">
                        Demo rule: use any <strong>@bgc.ca</strong> email and password <strong>test</strong>.
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        if demo_submitted:
            st.session_state.logged_in = True
            st.session_state.user_email = "demo.marketing@bgc.ca"
            st.session_state.department = "Marketing"
            st.session_state.role = "Marketing"
            st.session_state.page = "Dashboard"
            st.session_state.active_page = "Dashboard"
            st.rerun()

        if submitted:
            if not email.lower().endswith("@bgc.ca"):
                st.error("Please use a BGC email address ending in @bgc.ca.")
                return
            if password != "test":
                st.error("Incorrect demo password. Use: test")
                return
            st.session_state.logged_in = True
            st.session_state.user_email = email
            st.session_state.department = department
            st.session_state.role = "Marketing" if department == "Marketing" else "Department"
            st.session_state.page = "Dashboard" if department == "Marketing" else "Department Message Board"
            st.session_state.active_page = st.session_state.page
            st.rerun()


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------

def dashboard_page() -> None:
    """Executive summary dashboard for the marketing workspace."""

    header("Dashboard")
    dashboard_hero()
    recommended = get_program_or_current(st.session_state.selected_campaign)

    left, right = st.columns([0.65, 0.35], gap="large")
    with left:
        with st.container(border=True, key="dashboard_recommended_card"):
            st.caption("Recommended Campaign")
            st.subheader(recommended["name"])
            metric_cols = st.columns(3)
            metric_cols[0].metric("Priority score", recommendation_score(recommended))
            metric_cols[1].metric("Urgency", "High")
            metric_cols[2].metric("Next step", "Generate content")

            info_cols = st.columns(2)
            with info_cols[0]:
                st.caption("Best audience")
                st.write("Parents + youth")
            with info_cols[1]:
                st.caption("Best channel")
                st.write("Instagram + Newsletter")

            button_cols = st.columns(3)
            if button_cols[0].button("Create brief", key="dashboard-create-brief", use_container_width=True):
                st.session_state.page = "Program & Asset Intake"
                st.session_state.active_page = "Program & Asset Intake"
                st.rerun()
            if button_cols[1].button("Generate content", key="dashboard-generate-content", use_container_width=True):
                st.session_state.page = "AI Content Studio"
                st.session_state.active_page = "AI Content Studio"
                st.rerun()
            if button_cols[2].button("Add to planner", key="dashboard-add-planner", use_container_width=True):
                item = f"{recommended['name']} campaign"
                if item not in st.session_state.planner_items:
                    st.session_state.planner_items.append(item)
                st.success("Added to planner.")

        with st.expander("System workflow", expanded=False):
            steps = [
                ("📝", "1", "Intake", "Ready"),
                ("✨", "2", "Recommend", "In progress"),
                ("✍️", "3", "Create Content", "Ready"),
                ("📅", "4", "Plan", "Needs input"),
                ("📊", "5", "Measure", "Ready"),
            ]
            workflow_blocks = []
            for index, (icon, number, title, status) in enumerate(steps):
                status_class = "ready" if status == "Ready" else "progress" if status == "In progress" else "needs"
                active_class = " dashboard-workflow-card-v2-active" if status == "In progress" else ""
                workflow_blocks.append(
                    f"""
                    <div class="dashboard-workflow-card-v2{active_class}">
                        <div class="dashboard-workflow-step-v2">Step {html.escape(number)}</div>
                        <div class="dashboard-workflow-title-v2">{icon} {html.escape(title)}</div>
                        <div class="dashboard-workflow-status-v2 dashboard-workflow-status-{status_class}-v2">
                            {html.escape(status)}
                        </div>
                    </div>
                    """
                )
                if index < len(steps) - 1:
                    workflow_blocks.append('<div class="dashboard-workflow-arrow-v2">→</div>')

            st.markdown(
                f'<div class="dashboard-workflow-timeline">{"".join(workflow_blocks)}</div>',
                unsafe_allow_html=True,
            )

        with st.expander("Quick status", expanded=False):
            status_cols = st.columns(4)
            quick_status = [
                ("✍️", "5", "Drafts ready"),
                ("📂", "2", "Missing assets"),
                ("📅", "3", "Scheduled campaigns"),
                ("📍", "Downtown London", "Strongest engagement"),
            ]
            for index, (col, (icon, value, label)) in enumerate(zip(status_cols, quick_status)):
                with col:
                    with st.container(border=True, key=f"dashboard_quick_status_{index}"):
                        st.caption(icon)
                        st.metric(label, value)

    with right:
        with st.expander("Today’s actions", expanded=True):
            actions = [
                (f"Generate {recommended['name']} Instagram draft", "Ready"),
                ("Request student quote asset", "Needs Assets"),
                ("Add Supper Club post to calendar", "Draft"),
                ("Review viral content idea", "Ready"),
            ]
            with st.container(border=True, key="dashboard_actions_panel"):
                for index, (action, status) in enumerate(actions):
                    with st.container(border=True, key=f"dashboard_action_row_{index}"):
                        row_left, row_right = st.columns([0.66, 0.34])
                        row_left.write(f"**{action}**")
                        row_right.markdown(status_badge(status), unsafe_allow_html=True)

        with st.expander("Validated priorities", expanded=False):
            priorities = [
                ("Fun social content", "Short-form Reels and trend support"),
                ("Shared communication", "Department updates in one place"),
                ("Weekly/monthly calendar", "Campaigns and activities visible"),
                ("Asset contribution", "Photos and clips from staff"),
            ]
            with st.container(border=True, key="dashboard_priorities_panel"):
                for index, (title, note) in enumerate(priorities):
                    with st.container(border=True, key=f"dashboard_priority_item_{index}"):
                        st.write(f"**✓ {title}**")
                        st.caption(note)

        with st.expander("Donor engagement", expanded=False):
            with st.container(border=True, key="dashboard_donor_tools_panel"):
                donor_tools = [
                    ("Quarterly report", "Package proof points for supporters"),
                    ("Story library", "Save participant-safe impact moments"),
                    ("Value match", "Match donors to causes they care about"),
                    ("Proof points", DONOR_PROOF_POINTS[0]),
                ]
                for index, (tool, note) in enumerate(donor_tools):
                    row = st.columns([0.18, 0.82])
                    row[0].badge("●", color="green" if index != 3 else "orange")
                    row[1].markdown(f"**{tool}**")
                    row[1].caption(note)

        with st.expander("Positioning insight", expanded=False):
            with st.container(border=True, key="dashboard_positioning_panel"):
                st.markdown("**BGC’s marketing challenge is not only low reach.**")
                st.caption("It is a positioning and memorability challenge.")
                value_cols = st.columns(2)
                values = ["mentorship", "belonging", "confidence", "meals", "scholarships", "leadership", "wellness", "community transformation"]
                for index, value in enumerate(values):
                    value_cols[index % 2].badge(value.title(), color="green" if index % 3 else "orange")


def intake_page() -> None:
    """Combined program and asset intake with brief preview and missing info."""

    header("Program & Asset Intake")
    left, right = st.columns([1.25, 0.95])
    with left:
        st.markdown('<div class="panel-card">', unsafe_allow_html=True)
        st.markdown("### Internal Campaign Brief")
        st.markdown('<div class="form-section-title">Program Basics</div>', unsafe_allow_html=True)
        program_name = st.text_input("Program name", key="intake_program_name")
        if program_name.strip():
            st.session_state.selected_campaign = program_name.strip()
        st.markdown('<div class="helper-text">Use the public-facing program name staff and families recognize.</div>', unsafe_allow_html=True)
        basic_cols = st.columns(2)
        with basic_cols[0]:
            segment = st.selectbox("Segment", ["Children", "Youth", "50+", "Inclusion", "Supper Club", "MAP", "DCAC", "Sports"])
        with basic_cols[1]:
            activity = st.radio("Activity timing", ["Upcoming", "Past"], horizontal=True)
        date_goal_cols = st.columns(2)
        with date_goal_cols[0]:
            program_date = st.date_input("Program date", value=TODAY + timedelta(days=14))
        with date_goal_cols[1]:
            goal = st.selectbox("Goal", ["Awareness", "Registration", "Volunteer recruitment", "Donor support", "Partner update"])

        st.markdown('<div class="form-section-title">Audience & Message</div>', unsafe_allow_html=True)
        audience = st.multiselect(
            "Target audience",
            ["Young parents", "Youth", "Older adults", "Donors", "Partners", "Community", "Volunteers"],
            default=["Young parents", "Community"],
        )
        st.markdown('<div class="helper-text">Select every audience this update should reach. The AI will adapt channel copy by audience.</div>', unsafe_allow_html=True)
        key_message = st.text_area(
            "Key message",
            value="A welcoming BGC London program that creates belonging, support, and opportunity.",
            height=115,
        )

        st.markdown('<div class="form-section-title">Assets & Readiness</div>', unsafe_allow_html=True)
        assets = st.multiselect("Available assets", ["Photos", "Videos", "Graphics", "Testimonials", "None"], default=["Photos"])
        asset_cols = st.columns(2)
        with asset_cols[0]:
            quality = st.selectbox("Asset quality", ["High", "Medium", "Quick phone photo"])
        with asset_cols[1]:
            urgency = st.select_slider("Urgency level", options=["Low", "Medium", "High"], value="High")
        st.markdown('<div class="helper-text">Higher quality visuals and testimonials improve campaign confidence.</div>', unsafe_allow_html=True)
        current_brief = {
            "program_name": program_name.strip() or "Untitled campaign brief",
            "segment": segment,
            "activity_timing": activity,
            "program_date": program_date,
            "goal": goal,
            "target_audience": list(audience),
            "key_message": key_message.strip(),
            "available_assets": list(assets),
            "asset_quality": quality,
            "urgency": urgency,
            "department": st.session_state.department,
            "user_email": st.session_state.user_email,
            "status": brief_calendar_status(list(assets), key_message),
            "source": "Program Intake",
        }
        st.session_state.latest_intake_brief = current_brief
        action_cols = st.columns([1, 1, 1.45])
        with action_cols[0]:
            if st.button("Save brief", key="save-brief"):
                st.session_state.selected_campaign = current_brief["program_name"]
                st.success("Brief saved in the mock workspace.")
        with action_cols[1]:
            if st.button("Send to AI recommendation", key="send-brief"):
                st.session_state.selected_campaign = current_brief["program_name"]
                st.session_state.selected_recommendation = current_brief["program_name"]
                st.session_state.page = "AI Campaign Recommendation"
                st.session_state.active_page = "AI Campaign Recommendation"
                st.success("Brief sent to the mock recommendation engine.")
                st.rerun()
        with action_cols[2]:
            if st.button("Save brief to shared calendar", key="save-brief-calendar"):
                st.session_state.selected_campaign = current_brief["program_name"]
                st.session_state.selected_recommendation = current_brief["program_name"]
                save_brief_to_shared_calendar(current_brief)
                st.success("Brief saved to shared calendar.")
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        audience_chips = "".join(f'<span class="chip">{item}</span>' for item in audience) or '<span class="chip">Audience needed</span>'
        asset_chips = "".join(f'<span class="chip">{item}</span>' for item in assets) or '<span class="chip">Assets needed</span>'
        completed = [
            bool(program_name),
            bool(segment),
            bool(audience),
            bool(key_message),
            bool(assets) and "None" not in assets,
            quality != "Quick phone photo",
            bool(goal),
        ]
        readiness = round(sum(completed) / len(completed) * 100)

        st.markdown("### Live Campaign Brief")
        st.markdown(
            f"""
            <div class="detail-panel">
                {badge(activity + ' ' + segment + ' Campaign', 'softgreen')}
                <h2 style="margin:0.45rem 0 0.35rem;">{program_name or 'Untitled campaign brief'}</h2>
                {status_badge(urgency)} {badge(goal, 'yellow')}
                <div style="margin-top:0.9rem;"><strong>Audience</strong><br>{audience_chips}</div>
                <p><strong>Date:</strong> {program_date.strftime('%B %d, %Y')}</p>
                <p><strong>Message preview:</strong><br>{key_message or 'Add a concise program message for stronger AI output.'}</p>
                <div><strong>Asset readiness</strong><br>{asset_chips}<span class="chip">{quality}</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        checklist = [
            ("Program name", bool(program_name)),
            ("Target audience selected", bool(audience)),
            ("Clear key message", bool(key_message)),
            ("Usable visual or testimonial", bool(assets) and "None" not in assets),
            ("High or medium asset quality", quality != "Quick phone photo"),
            ("Campaign goal selected", bool(goal)),
        ]
        rows = ""
        for label, ok in checklist:
            marker = "✓" if ok else "!"
            state = "Ready" if ok else "Missing"
            klass = "check-ok" if ok else "check-warn"
            chip_kind = "softgreen" if ok else "yellow"
            rows += f'<div class="check-row"><span class="{klass}">{marker} {label}</span>{badge(state, chip_kind)}</div>'
        st.markdown(
            f"""
            <div class="panel-card" style="margin-top:1rem;">
                <div class="kpi-label">Missing Information Checklist</div>
                <h3 style="margin-top:0;">Brief readiness: {readiness}%</h3>
                <div class="mini-progress"><span style="width:{readiness}%;"></span></div>
                <div style="margin-top:0.85rem;">{rows}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def trends_page() -> None:
    """Trend and performance scan with mock social listening insights."""

    header("Trend & Performance Scan")
    st.subheader("Opportunity Radar")
    radar_cols = st.columns(3)
    for col, (trend, program, audience, channel, angle, score) in zip(radar_cols, TRENDS[:3]):
        with col:
            st.markdown(
                f"""
                <div class="trend-signal">
                    <div class="kpi-label">{trend}</div>
                    <h3 style="margin:0.2rem 0;">{program}</h3>
                    {badge(str(score) + ' priority score', 'softgreen')}
                    <p><strong>Trend strength:</strong> High</p>
                    <p><strong>Recommended action:</strong> Draft {channel} campaign angle.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    detail_tabs = st.tabs(["Trend Matrix", "Trend Intelligence", "Social Listening"])
    with detail_tabs[0]:
        st.caption("X-axis: audience urgency | Y-axis: asset readiness")
        matrix_cols = st.columns(4)
        matrix_items = [
            ("Act Now", "High urgency, strong assets", "MAP Education Support, After-School Recreation", "matrix-act"),
            ("Build Assets", "High urgency, weaker assets", "Supper Club real-photo set", "matrix-build"),
            ("Monitor", "Lower urgency, strong assets", "DCAC media stories", ""),
            ("Low Priority", "Lower urgency, weaker assets", "Evergreen partner updates", ""),
        ]
        for col, (title, note, examples, klass) in zip(matrix_cols, matrix_items):
            with col:
                st.markdown(
                    f"""
                    <div class="matrix-card {klass}">
                        <div class="kpi-label">{title}</div>
                        <strong>{note}</strong>
                        <p class="muted">{examples}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    with detail_tabs[1]:
        icons = ["🎒", "🧠", "🏠", "🤝", "🏀", "🍽️"]
        for icon, (trend, program, audience, channel, angle, score) in zip(icons, TRENDS):
            kind = "softgreen" if score >= 90 else "yellow"
            st.markdown(
                f"""
                <div class="trend-row">
                    <div class="trend-icon">{icon}</div>
                    <div>
                        <strong>{trend}</strong><br>
                        <span class="muted">{program} · {audience}</span>
                    </div>
                    <div>
                        {badge(channel, 'navy')} {badge(str(score) + ' score', kind)}
                        <div class="mini-progress"><span style="width:{score}%;"></span></div>
                    </div>
                    <div class="muted">{angle}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with detail_tabs[2]:
        insight_rows = "".join(
            f'<div class="check-row"><span class="check-ok">✓ {insight}</span>{badge("Signal", "softgreen")}</div>'
            for insight in SOCIAL_INSIGHTS
        )
        st.markdown(
            f"""
            <div class="panel-card">
                <div class="kpi-label">Mock community and channel insights</div>
                {insight_rows}
            </div>
            """,
            unsafe_allow_html=True,
        )


def recommendation_page() -> None:
    """Ranked campaign recommendation engine page."""

    header("AI Campaign Recommendation")
    campaign_recommendation_hero()
    st.markdown(
        """
        <div class="mode-helper-card">
            <strong>Choose recommendation type</strong><br>
            <span class="muted">Switch between digital posts, offline community activations, or hybrid campaign plans.</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    recommendation_mode = st.pills(
        "Recommendation mode",
        ["Digital Campaign", "Offline Activation", "Hybrid Campaign"],
        default="Digital Campaign",
        key="recommendation-mode-pills",
        help="Switch between channel-first campaign recommendations and real-world community activation ideas.",
    )
    recommendation_mode = recommendation_mode or "Digital Campaign"
    if recommendation_mode != "Digital Campaign":
        st.subheader(f"{recommendation_mode} Recommendations")
        st.caption("Mock scoring combines community visibility, donor appeal, partnership fit, and content potential.")
        rec_cols = st.columns(2)
        for index, item in enumerate(OFFLINE_RECOMMENDATIONS):
            overall = round(
                (
                    item["local_awareness"]
                    + item["donor_potential"]
                    + item["partner_fit"]
                    + item["content_potential"]
                )
                / 4
            )
            with rec_cols[index % 2]:
                with st.container(border=True, key=f"offline_rec_{recommendation_mode}_{index}"):
                    st.badge(f"{overall} overall score", color="green")
                    st.markdown(f"### {item['name']}")
                    st.write(item["why"])
                    metric_cols = st.columns(2)
                    metric_cols[0].metric("Visibility", item["local_awareness"])
                    metric_cols[1].metric("Donor appeal", item["donor_potential"])
                    st.caption("Partner fit")
                    st.progress(item["partner_fit"] / 100)
                    st.caption("Content potential")
                    st.progress(item["content_potential"] / 100)
                    st.markdown(f"**Recommended next step:** {item['best_action']}")
        st.subheader("Offline Idea Fit")
        rows = [
            {
                "Campaign": item["name"],
                "Audience Fit": item["audience_fit"],
                "Partner Fit": item["partner_fit"],
                "Donor Potential": item["donor_potential"],
                "Content Potential": item["content_potential"],
                "Local Awareness": item["local_awareness"],
            }
            for item in OFFLINE_RECOMMENDATIONS
        ]
        st.dataframe(rows, width="stretch", hide_index=True)
        return

    ranked = ranked_programs_with_current()
    if "selected_recommendation" not in st.session_state:
        st.session_state.selected_recommendation = st.session_state.selected_campaign
    if st.session_state.selected_recommendation not in [program["name"] for program in ranked]:
        st.session_state.selected_recommendation = st.session_state.selected_campaign if st.session_state.selected_campaign in [program["name"] for program in ranked] else ranked[0]["name"]
    selected_program = next(program for program in ranked if program["name"] == st.session_state.selected_recommendation)
    top_program = selected_program if selected_program["name"] == st.session_state.selected_campaign else ranked[0]

    st.subheader("#1 Recommended Campaign")
    st.markdown(
        f"""
            <div class="recommendation-hero-card">
                <div class="kpi-label">Primary recommendation</div>
                <h2 style="margin:0.2rem 0;">{top_program['name']}</h2>
            {badge(top_program['segment'], 'softgreen')} {badge(top_program['urgency'] + ' urgency', 'softgreen')} {badge(top_program['channels'][0], 'navy')}
            <div class="hero-metric-grid">
                <div class="hero-metric"><div class="kpi-label">Score</div><div class="score-text">{recommendation_score(top_program)}</div></div>
                <div class="hero-metric"><div class="kpi-label">Audience Fit</div><div class="score-text">{top_program['audience_fit']}%</div></div>
                <div class="hero-metric"><div class="kpi-label">Asset Readiness</div><div class="score-text">{asset_score(top_program)}%</div></div>
            </div>
            <div class="progress-row"><span>Urgency</span><div class="mini-progress"><span style="width:{urgency_score(top_program)}%;"></span></div><span>{urgency_score(top_program)}%</span></div>
            <div class="progress-row"><span>Asset readiness</span><div class="mini-progress"><span style="width:{asset_score(top_program)}%;"></span></div><span>{asset_score(top_program)}%</span></div>
            <div class="progress-row"><span>Audience fit</span><div class="mini-progress"><span style="width:{top_program['audience_fit']}%;"></span></div><span>{top_program['audience_fit']}%</span></div>
            <p><strong>Why this campaign:</strong> {top_program['angle']} The timing, proof point, and channel fit make this the strongest near-term campaign.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    hero_actions = st.columns([1, 1, 1, 3.2])
    if hero_actions[0].button("Generate Content", key="hero-generate-content"):
        set_recommended_campaign(top_program["name"])
        st.session_state.selected_recommendation = top_program["name"]
        st.session_state.page = "AI Content Studio"
        st.session_state.active_page = "AI Content Studio"
        st.rerun()
    with hero_actions[1].container(key="rec_secondary_actions_use"):
        if st.button("Use Campaign", key="hero-use-campaign"):
            set_recommended_campaign(top_program["name"])
            st.session_state.selected_recommendation = top_program["name"]
            st.success(f"{top_program['name']} selected for the workflow.")
    with hero_actions[2].container(key="rec_secondary_actions_planner"):
        if st.button("Add to Planner", key="hero-add-planner"):
            item = f"{top_program['name']} campaign"
            if item not in st.session_state.planner_items:
                st.session_state.planner_items.append(item)
            st.success("Added to the mock planner.")

    reason_tabs = st.tabs(["Why this campaign", "Audience fit", "Asset readiness", "Offline activation", "Donor opportunity"])
    with reason_tabs[0]:
        st.write(f"{top_program['angle']} The timing, proof point, and channel fit make this the strongest near-term campaign.")
    with reason_tabs[1]:
        st.metric("Audience fit", f"{top_program['audience_fit']}%")
        st.caption(top_program["audience"])
    with reason_tabs[2]:
        st.metric("Asset readiness", f"{asset_score(top_program)}%")
        st.caption(", ".join(top_program["assets"]))
    with reason_tabs[3]:
        st.write("Hybrid or offline support can extend the campaign through partner referrals, school/community visibility, and real-world proof points.")
        st.badge("Community visibility", color="green")
        st.badge("Local partner fit", color="orange")
    with reason_tabs[4]:
        st.write("Use the campaign proof point as the donor-facing memory hook, then repeat it across newsletter, LinkedIn, and partner updates.")
        st.badge("Impact proof", color="green")

    with st.expander("Compare with other campaigns", expanded=False):
        st.subheader("Campaign Comparison")
        grid_cols = st.columns(3)
        for index, program in enumerate(ranked):
            with grid_cols[index % 3]:
                rank = index + 1
                active = program["name"] == selected_program["name"]
                active_class = " recommendation-grid-card-active" if active else ""
                filled_dots = min(5, max(1, round(recommendation_score(program) / 20)))
                dots = "".join(
                    f'<span class="indicator-dot {"indicator-dot-on" if dot < filled_dots else ""}"></span>'
                    for dot in range(5)
                )
                urgency_kind = "softgreen" if program["urgency"] == "High" else "navy"
                st.markdown(
                    f"""
                    <div class="recommendation-grid-card{active_class}">
                        <div class="recommendation-card-top">
                            <div><span class="rank-pill">#{rank}</span><div class="recommendation-card-title">{program['name']}</div></div>
                        </div>
                        <div>{badge(str(recommendation_score(program)) + ' score', 'softgreen')} {badge(program['urgency'] + ' urgency', urgency_kind)}</div>
                        <div class="recommendation-card-meta">
                            <div class="recommendation-card-chip"><div class="kpi-label">Audience</div>{program['audience']}</div>
                            <div class="recommendation-card-chip"><div class="kpi-label">Asset readiness</div>{asset_score(program)}%</div>
                        </div>
                        <div class="indicator-dots">{dots}</div>
                        <div class="progress-row" style="grid-template-columns:76px 1fr 38px;margin:0.35rem 0;"><span>Assets</span><div class="mini-progress"><span style="width:{asset_score(program)}%;"></span></div><span>{asset_score(program)}%</span></div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                with st.container(key=f"rec_select_button_{index}"):
                    if st.button("Select", key=f"select-rec-{program['name']}", use_container_width=False):
                        st.session_state.selected_recommendation = program["name"]
                        st.rerun()

    channel_tags = " ".join(badge(channel, "navy") for channel in selected_program["channels"])
    st.subheader("Selected Campaign Detail")
    st.markdown(
        f"""
        <div class="detail-panel">
            {badge(selected_program['segment'], 'softgreen')} {badge(str(recommendation_score(selected_program)) + ' priority score', 'softgreen')}
            <h2 style="margin:0.45rem 0;">{selected_program['name']}</h2>
            <div class="detail-grid">
                <div class="detail-item"><div class="kpi-label">Why this campaign</div>{selected_program['angle']} Strong timing, clear audience fit, and mission alignment of {selected_program['mission_alignment']}%.</div>
                <div class="detail-item"><div class="kpi-label">Best audience</div>{selected_program['audience']}</div>
                <div class="detail-item"><div class="kpi-label">Best channels</div>{channel_tags}</div>
                <div class="detail-item"><div class="kpi-label">Required assets</div>{selected_program['required_assets']}</div>
            </div>
            <p style="margin-bottom:0;"><strong>Suggested angle:</strong> {selected_program['angle']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("Comparison Table")
    rows = []
    for program in ranked_programs_with_current():
        rows.append(
            {
                "Program": program["name"],
                "Urgency": program["urgency"],
                "Asset Readiness": asset_score(program),
                "Audience Fit": program["audience_fit"],
                "Mission Alignment": program["mission_alignment"],
                "Recommended Action": "Generate content" if recommendation_score(program) >= 88 else "Collect assets",
            }
        )
    st.dataframe(rows, width="stretch", hide_index=True)

    st.subheader("Future Ad Ideas")
    ad_cols = st.columns(5)
    suggestions = [
        ("🔍", "Google Ads", "After-school search intent."),
        ("🎥", "Instagram Reel", "Short youth story."),
        ("👨‍👩‍👧", "Facebook", "Parent-focused post."),
        ("🤝", "LinkedIn", "Partner impact update."),
        ("📰", "Newsletter", "Belong, learn, and thrive headline."),
    ]
    for col, (icon, title, text) in zip(ad_cols, suggestions):
        with col:
            st.markdown(
                f"""
                <div class="ad-idea-card">
                    <div class="ad-idea-icon">{icon}</div>
                    <strong>{title}</strong>
                    <p class="muted">{text}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )


def viral_content_engine_page() -> None:
    """Mock AI-assisted trend strategist for short-form nonprofit content."""

    header(
        "AI Viral Content Engine",
        "Identify trend signals, match them to BGC programs, and turn ideas into filmable short-form content.",
    )
    viral_engine_hero()

    with st.expander("Offline Moment → Viral Content", expanded=False):
        st.caption("Translate real-world community activations into trend-ready short-form content and channel plans.")
        offline_tabs = st.tabs([idea["moment"] for idea in OFFLINE_TO_DIGITAL_IDEAS])
        for index, (tab, idea) in enumerate(zip(offline_tabs, OFFLINE_TO_DIGITAL_IDEAS)):
            with tab:
                st.badge(idea["moment"], color="orange" if index < 2 else "green")
                st.markdown(f"**Reel idea:** {idea['reel']}")
                st.caption(f"Hook: {idea['hook']}")
                st.markdown(f"**CTA:** {idea['cta']}")
                st.caption(idea["fit"])

    mode = st.radio(
        "Trend mode",
        ["Parent Engagement", "Youth Engagement", "Volunteer Recruitment", "Donor Storytelling", "Community Awareness"],
        horizontal=True,
    )
    mode_data = VIRAL_MODES[mode]
    match_names = [item["program"] for item in VIRAL_PROGRAM_MATCHES]
    selected_program = st.selectbox(
        "Creative focus program",
        match_names,
        index=0,
        help="This controls the mock viral structure, hooks, and scoring focus.",
    )
    selected_match = next(item for item in VIRAL_PROGRAM_MATCHES if item["program"] == selected_program)

    st.markdown(
        f"""
        <div class="viral-hero">
            {badge('Mock trend intelligence', 'softgreen')} {badge(mode, 'yellow')} {badge(selected_match['platform'], 'navy')}
            <h2 style="margin:0.5rem 0 0.3rem;">Short-form strategy for {selected_program}</h2>
            <p class="muted" style="margin-bottom:0;">
                This demo simulates how an AI creative strategist could translate current Reels/TikTok-style formats
                into practical BGC content plans for {mode_data['audience']}. Recommended angle: <strong>{mode_data['angle']}</strong>.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("Current Viral Content Signals")
    for index, (trend, why, platform, audience, adaptation) in enumerate(VIRAL_TRENDS[mode]):
        with st.expander(f"{trend} · {platform}", expanded=index == 0):
            st.badge("Trend signal", color="green")
            st.badge(platform, color="blue")
            st.write(f"**Why it performs well:** {why}")
            st.write(f"**Best audience:** {audience}")
            st.write(f"**Suggested BGC adaptation:** {adaptation}")

    st.subheader("Best Program for Current Trends")
    selected_match_score = min(
        98,
        selected_match["score"]
        + (4 if mode in ["Youth Engagement", "Parent Engagement"] and selected_match["program"] in ["MAP Education Support", "After-School Recreation"] else 0),
    )
    st.markdown(
        f"""
        <div class="viral-match-card" style="background:linear-gradient(135deg,#f7fbf8 0%,#fffaf0 100%);border-color:#cfe3d6;">
            {badge(str(selected_match_score) + ' Viral Potential', 'yellow')} {badge(selected_match['platform'], 'softgreen')}
            <h3 style="margin:0.55rem 0 0.25rem;">{selected_match['program']}</h3>
            <p><strong>Best trend:</strong> {selected_match['trend']}</p>
            <p><strong>Why it fits:</strong> {selected_match['why']}</p>
            <p style="margin-bottom:0;"><strong>Filming style:</strong> {selected_match['style']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.expander("Compare other program matches", expanded=False):
        match_cols = st.columns(3)
        for index, item in enumerate(VIRAL_PROGRAM_MATCHES):
            score_adjustment = 4 if mode in ["Youth Engagement", "Parent Engagement"] and item["program"] in ["MAP Education Support", "After-School Recreation"] else 0
            adjusted_score = min(98, item["score"] + score_adjustment)
            with match_cols[index % 3]:
                st.markdown(
                    f"""
                    <div class="viral-match-card">
                        {badge(str(adjusted_score) + ' Viral Potential', 'yellow')}
                        <h3 style="margin:0.55rem 0 0.25rem;">{item['program']}</h3>
                        <p><strong>Best trend:</strong> {item['trend']}</p>
                        <p><strong>Platform:</strong> {item['platform']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.subheader("Viral Hook Generator")
    mode_hook_groups = {
        "Parent Engagement": [
            ("Emotional hooks", ["A safe place after school can change the whole evening.", "This is what relief looks like for a busy parent.", "Confidence starts with a place where kids feel known."]),
            ("Curiosity hooks", ["What after-school support actually looks like at BGC London.", "Here is what happens between school pickup and dinner.", "Why parents keep asking about this program."]),
            ("Parent-focused hooks", VIRAL_HOOKS["parent"]),
            ("CTA hooks", ["Save this for registration season.", "Share this with a parent who needs after-school options.", "Ask BGC London how your family can connect."]),
        ],
        "Youth Engagement": [
            ("Emotional hooks", VIRAL_HOOKS["emotional"]),
            ("Curiosity hooks", ["What happens when youth get space to try?", "From first idea to finished project in one session.", "This is your sign to show up after school."]),
            ("Youth-focused hooks", VIRAL_HOOKS["youth"]),
            ("CTA hooks", ["Send this to a friend who should come with you.", "Try one program and see what fits.", "Follow BGC London for youth opportunities."]),
        ],
        "Volunteer Recruitment": [
            ("Emotional hooks", ["One shift can create a moment someone remembers.", "This is what community care looks like up close.", "You do not need to be perfect to make a difference."]),
            ("Curiosity hooks", ["What volunteers actually do at BGC London.", "Come with us for one Supper Club shift.", "The easiest way to start helping locally."]),
            ("Volunteer hooks", ["Have two hours to give back?", "This is your sign to try one volunteer shift.", "Meet the people behind the community table."]),
            ("CTA hooks", ["Volunteer for one shift this month.", "Share this with someone who loves helping people.", "Ask BGC London where help is needed next."]),
        ],
        "Donor Storytelling": [
            ("Emotional hooks", ["A scholarship is not just money. It is momentum.", "This is what opportunity looks like when support arrives on time.", "One practical gift can help a young person keep going."]),
            ("Curiosity hooks", ["Where your support shows up at BGC London.", "The proof point behind this youth success story.", "How one program moment becomes a bigger future."]),
            ("Donor hooks", ["Support today. Confidence tomorrow.", "Help turn local care into measurable opportunity.", "Invest in the programs families already trust."]),
            ("CTA hooks", ["Support BGC programs that create belonging.", "Share this impact story with a community partner.", "Help fund practical youth opportunity."]),
        ],
        "Community Awareness": [
            ("Emotional hooks", ["Belonging is built in everyday moments.", "This is what community looks like in motion.", "Opportunity can start in a familiar local place."]),
            ("Curiosity hooks", ["A day inside BGC London.", "Come with us behind the scenes.", "What people do not always see about BGC programs."]),
            ("Community hooks", ["London families deserve spaces like this.", "Meet the programs helping neighbours connect.", "One organization, many ways to belong."]),
            ("CTA hooks", ["Follow BGC London and share this local story.", "Help more people discover these programs.", "Send this to someone new to BGC."]),
        ],
    }
    hook_groups = mode_hook_groups[mode]
    if st.session_state.get("viral_hook_mode") != mode:
        st.session_state.viral_hook_mode = mode
        st.session_state.viral_selected_hook = hook_groups[0][1][0]
    hook_category = st.pills(
        "Hook category",
        [title for title, _hooks in hook_groups],
        default=hook_groups[0][0],
        key=f"viral-hook-category-{mode}",
    )
    hook_category = hook_category or hook_groups[0][0]
    active_hooks = next(hooks for title, hooks in hook_groups if title == hook_category)
    selected_hook = st.radio(
        "Select one hook",
        active_hooks[:3],
        index=0,
        key=f"viral-hook-radio-{mode}-{hook_category}",
    )
    hook_preview_cols = st.columns([0.72, 0.28])
    with hook_preview_cols[0]:
        st.markdown(
            f"""
            <div class="viral-hook-card">
                {badge(hook_category, 'softgreen')}
                <h3 style="margin:0.6rem 0 0;">{selected_hook}</h3>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with hook_preview_cols[1]:
        if st.button("Use selected hook", key=f"viral-use-selected-hook-{mode}", use_container_width=True):
            st.session_state.viral_selected_hook = selected_hook
            st.toast("Hook loaded into the reel structure.")

    active_hook = st.session_state.get("viral_selected_hook", hook_groups[0][1][0])
    st.subheader("Reel Structure Builder")
    st.markdown(
        f"""
        <div class="video-template-card">
            {badge('10-20 seconds', 'softgreen')} {badge(selected_match['trend'], 'yellow')} {badge(mode_data['best_time'], 'navy')}
            <h3 style="margin:0.55rem 0 0.35rem;">Opening hook: {active_hook}</h3>
            <p style="margin-bottom:0;"><strong>CTA ending:</strong> {mode_data['cta']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    scene_cols = st.columns(2)
    for index, scene in enumerate(REEL_SCENES):
        with scene_cols[index % 2]:
            with st.expander(f"{scene['scene']}: {scene['flow']}", expanded=index < 2):
                st.markdown(
                    f"""
                    <div class="card">
                        <p><strong>Scene objective:</strong> {scene['flow']}</p>
                        <p><strong>Camera suggestion:</strong> {scene['camera']}</p>
                        <p><strong>Text overlay:</strong> {scene['text']}</p>
                        <p style="margin-bottom:0;"><strong>Voiceover:</strong> {scene['voiceover']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.subheader("Trend Adaptation Guide")
    guide_cols = st.columns(3)
    for index, (title, detail) in enumerate(TREND_ADAPTATION_GUIDE):
        with guide_cols[index % 3]:
            st.markdown(
                f"""
                <div class="viral-guide-card">
                    {badge('Creator technique', 'softgreen')}
                    <h3 style="margin:0.55rem 0 0.35rem;">{title}</h3>
                    <p class="muted" style="margin-bottom:0;">{detail}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.subheader("Low-Effort Version")
    low_effort_cols = st.columns([1.1, 0.9])
    with low_effort_cols[0]:
        low_effort_items = "".join(f"<li>{item}</li>" for item in LOW_EFFORT_VIRAL_PLAN)
        st.markdown(
            f"""
            <div class="card-yellow">
                {badge('Built for small teams', 'yellow')}
                <h3 style="margin:0.55rem 0 0.35rem;">How to make this with limited resources</h3>
                <ul style="margin-bottom:0;">{low_effort_items}</ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with low_effort_cols[1]:
        st.markdown(
            f"""
            <div class="card">
                <div class="kpi-label">Posting Plan</div>
                <p><strong>Best platform:</strong> {selected_match['platform']}</p>
                <p><strong>Best posting time:</strong> {mode_data['best_time']}</p>
                <p><strong>Caption style:</strong> Short, human, and written like a real staff member inviting the community in.</p>
                <p style="margin-bottom:0;"><strong>CTA style:</strong> {mode_data['cta']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.subheader("Expected Viral Potential")
    base = selected_match["score"]
    mode_bonus = 5 if mode == "Youth Engagement" and selected_program in ["MAP Education Support", "DCAC Media Program", "Sports Programs"] else 3
    subscores = {
        "Emotional relatability": min(98, base + mode_bonus),
        "Shareability": min(96, base - 2 + (4 if "Reels" in selected_match["platform"] else 0)),
        "Authenticity": min(97, base + 1),
        "Youth appeal": min(98, base + (7 if mode == "Youth Engagement" else -3)),
        "Parent engagement": min(96, base + (7 if mode == "Parent Engagement" else -2)),
        "Hook strength": min(98, base + 2),
    }
    overall = round(sum(subscores.values()) / len(subscores))
    score_cols = st.columns([0.85, 1.15])
    with score_cols[0]:
        st.markdown(
            f"""
            <div class="viral-score-panel">
                <div class="kpi-label">Viral Potential Score</div>
                <div class="score-circle" style="--score-deg:{overall * 3.6}deg;margin:0.55rem 0 0.8rem;">{overall}<span style="font-size:0.8rem;">/100</span></div>
                {badge('Expected engagement: High', 'softgreen')}
                {badge('Best for: ' + mode, 'yellow')}
                <p class="muted" style="margin-top:0.8rem;margin-bottom:0;">
                    Mock score based on hook strength, fit with trend format, audience match, authenticity, and BGC mission relevance.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with score_cols[1]:
        with st.container(border=True):
            for label, value in subscores.items():
                st.markdown(f"**{label}**")
                st.progress(value / 100)
                st.caption(f"{value} / 100")
            st.markdown("#### What could improve performance?")
            st.markdown(
                "- Film one real reaction moment instead of relying only on graphics.\n"
                "- Put the strongest emotional hook in the first three seconds.\n"
                "- Keep captions short enough to read before the next cut.\n"
                "- Add a single clear CTA that matches the selected mode."
            )


def content_studio_page() -> None:
    """Channel-specific mock content studio using selected recommendation."""

    header("AI Content Studio")
    content_studio_hero()
    program_names = [program["name"] for program in ranked_programs_with_current()]
    if st.session_state.selected_campaign not in program_names:
        program_names.insert(0, st.session_state.selected_campaign)
    selected_name = st.selectbox(
        "Recommended campaign",
        program_names,
        index=program_names.index(st.session_state.selected_campaign),
    )
    set_recommended_campaign(selected_name)
    program = get_program_or_current(selected_name)
    st.markdown(
        """
        <div class="mode-helper-card">
            <strong>Choose content mode</strong><br>
            <span class="muted">Pick whether staff need finished copy, fun social ideas, or a video production guide.</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    mode = st.pills(
        "Content mode",
        ["Standard Campaign Copy", "Fun Social Content Ideas", "Video Inspiration Builder"],
        default="Standard Campaign Copy",
        key="content-mode-pills",
    )
    mode = mode or "Standard Campaign Copy"

    selected_asset = st.session_state.get("selected_asset")
    if selected_asset:
        best_for = selected_asset.get("best_for", f"Best for: {selected_asset['channel']}")
        use_for = selected_asset.get("use_for", "Use for: Campaign support")
        st.markdown(
            f"""
            <div class="selected-asset-card">
                <div class="kpi-label">Using asset</div>
                <strong>{selected_asset['name']}</strong><br>
                {badge(selected_asset['type'], 'navy')} {badge(selected_asset['channel'], 'softgreen')}
                <p class="muted" style="margin-bottom:0;">{best_for} · {use_for}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    idea_key = selected_name if selected_name in FUN_CONTENT_IDEAS else "Supper Club"
    if mode == "Fun Social Content Ideas":
        st.markdown(
            f"""
            <div class="card-green">
                <div class="kpi-label">Trend-Inspired Social Ideas</div>
                <h2 style="margin:0.2rem 0;">{selected_name}</h2>
                <p class="muted" style="margin-bottom:0;">
                    Mock creative strategy engine for playful, high-engagement Instagram/TikTok-style content.
                    Each concept includes a hook, first-shot plan, caption, audience, timing, and asset checklist.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        for index, idea in enumerate(FUN_CONTENT_IDEAS[idea_key], start=1):
            difficulty_kind = {"Easy": "softgreen", "Medium": "yellow", "Advanced": "navy"}.get(idea["difficulty"], "navy")
            first_three = "".join(f"<li>{item}</li>" for item in idea["first_three"])
            assets = "".join(f"<li>{item}</li>" for item in idea["assets"])
            with st.expander(f"{idea['icon']} {index}. {idea['title']}"):
                st.markdown(
                    f"""
                    <div class="idea-card">
                        {badge(idea['icon'], 'navy')}
                        {badge(idea['best_for'], 'softgreen')}
                        {badge(idea['difficulty'], difficulty_kind)}
                        <h3 style="margin:0.7rem 0 0.45rem;">{idea['title']}</h3>
                        <p><strong>Why this works:</strong> {idea['why']}</p>
                        <div class="detail-grid" style="margin-top:0.85rem;">
                            <div class="detail-item">
                                <div class="kpi-label">Suggested hook</div>
                                {idea['hook']}
                            </div>
                            <div class="detail-item">
                                <div class="kpi-label">Recommended format</div>
                                {idea['format']}
                            </div>
                            <div class="detail-item">
                                <div class="kpi-label">Audience target</div>
                                {idea['audience']}
                            </div>
                            <div class="detail-item">
                                <div class="kpi-label">Suggested posting time</div>
                                {idea['posting_time']}
                            </div>
                        </div>
                        <p style="margin:0.9rem 0 0.35rem;"><strong>Suggested first 3 seconds:</strong></p>
                        <ul style="margin-top:0.2rem;">{first_three}</ul>
                        <p><strong>Suggested caption:</strong><br>{idea['caption']}</p>
                        <p><strong>CTA:</strong> {idea['cta']}</p>
                        <p style="margin:0.9rem 0 0.35rem;"><strong>Asset requirements:</strong></p>
                        <ul style="margin-top:0.2rem;margin-bottom:0;">{assets}</ul>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        return

    if mode == "Video Inspiration Builder":
        template = VIDEO_TEMPLATES.get(idea_key, VIDEO_TEMPLATES["Supper Club"])
        st.markdown(
            f"""
            <div class="video-template-card">
                <div class="kpi-label">Guided Video Template</div>
                <h2 style="margin:0.2rem 0;">{selected_name} short-form video</h2>
                {badge('Length: ' + template['length'], 'softgreen')}
                {badge('Best channel: ' + template['channel'], 'navy')}
                <p><strong>On-screen text:</strong> {template['text']}</p>
                <p><strong>Voiceover/caption idea:</strong> {template['voiceover']}</p>
                <p style="margin-bottom:0;"><strong>Required assets:</strong> {template['assets']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        left, right = st.columns([1.05, 0.95])
        with left:
            st.subheader("Scene-by-Scene Production Guide")
            for index, scene in enumerate(template["scenes"], start=1):
                with st.expander(f"Scene {index}: {scene['objective']}"):
                    st.markdown(
                        f"""
                        <div class="card">
                            <p><strong>Scene objective:</strong> {scene['objective']}</p>
                            <p><strong>Camera suggestion:</strong> {scene['camera']}</p>
                            <p><strong>Shot framing:</strong> {scene['framing']}</p>
                            <p><strong>Motion suggestion:</strong> {scene['motion']}</p>
                            <p><strong>Suggested on-screen text:</strong> {scene['text']}</p>
                            <p><strong>Suggested voiceover:</strong> {scene['voiceover']}</p>
                            <p style="margin-bottom:0;"><strong>Emotion goal:</strong> {scene['emotion']}</p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
        with right:
            st.subheader("Editing Style")
            editing = template["editing_style"]
            st.markdown(
                f"""
                <div class="card">
                    <p><strong>Pacing recommendation:</strong> {editing['pacing']}</p>
                    <p><strong>Transition style:</strong> {editing['transitions']}</p>
                    <p><strong>Music vibe:</strong> {editing['music']}</p>
                    <p><strong>Subtitle recommendation:</strong> {editing['subtitles']}</p>
                    <p style="margin-bottom:0;"><strong>Color style:</strong> {editing['color']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.subheader("Trend Adaptation")
            trend_items = "".join(f"<li>{item}</li>" for item in template["trend_adaptation"])
            st.markdown(
                f"""
                <div class="card-yellow">
                    {badge('Trend-ready', 'yellow')}
                    <ul style="margin-top:0.75rem;margin-bottom:0;">{trend_items}</ul>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.subheader("Low-Effort Version")
            low_effort = "".join(f"<li>{item}</li>" for item in template["low_effort"])
            st.markdown(
                f"""
                <div class="card">
                    {badge('Nonprofit-friendly', 'softgreen')}
                    <p style="margin:0.75rem 0 0.35rem;">If filming resources are limited, this can still be made using:</p>
                    <ul style="margin-top:0.2rem;margin-bottom:0;">{low_effort}</ul>
                </div>
                """,
                unsafe_allow_html=True,
            )
        return

    framework_cols = st.columns([0.48, 0.52], gap="large")
    with framework_cols[0]:
        emotional_angle = st.selectbox(
            "Emotional campaign angle",
            ["Confidence", "Belonging", "Safety", "Future success", "Community support", "Kids being kids", "Donor impact"],
            index=1,
        )
    with framework_cols[1]:
        audience_frame = st.radio(
            "Audience framing",
            ["Parents", "Youth", "Older adults", "Donors"],
            horizontal=True,
        )
    with st.expander("Quick message examples"):
        example_cols = st.columns(3)
        examples = [
            "More than a program.",
            "A place to belong after school.",
            "Future leaders start here.",
            "100 meals served today.",
            "One student. One scholarship. One future changed.",
            "40,000 rides provided to older adults.",
        ]
        for index, example in enumerate(examples):
            example_cols[index % 3].badge(example, color="green" if index % 2 else "orange")

    tone = st.radio("Tone controls", ["Warm", "Informational", "Donor-focused", "Parent-friendly", "Youth-focused"], horizontal=True)
    st.markdown(
        f"""
        <div class="card-green">
            {badge(program['segment'], 'green')} {badge(program['angle'], 'yellow')}
            <p><strong>Proof point:</strong> {program['proof']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    channels = ["Instagram", "Facebook", "LinkedIn", "Newsletter", "Google Ads Grant", "Partner Email", "Local Media Pitch"]
    tabs = st.tabs(channels)
    for tab, channel in zip(tabs, channels):
        with tab:
            st.markdown(f"#### {channel} Draft")
            channel_key = channel.lower().replace(" ", "_").replace("/", "_")
            key = draft_key(selected_name, channel)
            asset_context_key = f"{key}::asset"
            message_context_key = f"{key}::message_framework"
            active_asset_name = selected_asset["name"] if selected_asset else None
            message_signature = f"{tone}|{emotional_angle}|{audience_frame}|{active_asset_name}"

            def with_asset_context(text: str) -> str:
                if not selected_asset:
                    return text
                return (
                    f"{text}\n\nAsset context: use {selected_asset['name']} for {selected_asset['channel']} "
                    f"with the angle '{selected_asset.get('use_for', 'campaign support')}'."
                )

            if key not in st.session_state or st.session_state.get(message_context_key) != message_signature:
                draft = with_asset_context(
                    content_variation(program, channel, tone, "original", emotional_angle, audience_frame)
                )
                st.session_state[key] = draft
                st.session_state[asset_context_key] = active_asset_name
                st.session_state[message_context_key] = message_signature

            score_data = content_score(st.session_state[key], channel, tone, program)
            render_generated_content_panel(st.session_state[key], channel, tone, score_data, channel_key)
            with st.expander(f"Suggested visual direction - {channel}"):
                st.markdown(
                    "- Use phone-shot footage with natural lighting.\n"
                    "- Add subtitle overlays for the hook and CTA.\n"
                    "- Keep pacing quick for social channels and calmer for email/newsletter.\n"
                    "- Prioritize authentic reactions, real program spaces, and consent-safe moments.\n"
                    "- Pair the copy with one clear image or short vertical clip whenever possible."
                )

            actions = ["Make shorter", "Make more emotional", "Add call-to-action", "Rewrite for young parents", "Save draft"]
            variation_map = {
                "Make shorter": "short",
                "Make more emotional": "emotional",
                "Add call-to-action": "cta",
                "Rewrite for young parents": "parent",
            }
            with st.container(key=f"ai_output_actions_{channel_key}"):
                action_cols = st.columns(5)
                for col, action in zip(action_cols, actions):
                    if col.button(action, key=f"{channel}-{action}"):
                        if action == "Save draft":
                            st.success("Saved to the mock content workspace.")
                        else:
                            st.session_state[key] = with_asset_context(
                                content_variation(program, channel, tone, variation_map[action], emotional_angle, audience_frame)
                            )
                            st.session_state[asset_context_key] = active_asset_name
                            st.session_state[message_context_key] = message_signature
                            st.toast(f"{action} applied to this draft.")
                            st.rerun()


def planner_page() -> None:
    """Strategic weekly planning view for the marketing team."""

    header("Campaign Planner")
    focus_program = get_program("Supper Club")
    planner_tabs = st.tabs(["Weekly Plan", "Offline Activation", "Regional Intelligence", "Partnership Ideas"])

    with planner_tabs[0]:
        st.markdown(
            """
            <div class="planner-color-strip">
                <div class="planner-color-card planner-card-rose"><strong>Instagram</strong><span>Warm awareness story for Supper Club.</span></div>
                <div class="planner-color-card planner-card-blue"><strong>Facebook</strong><span>Parent/community CTA on Wednesday.</span></div>
                <div class="planner-color-card planner-card-green"><strong>Newsletter</strong><span>Monthly retention and referral block.</span></div>
                <div class="planner-color-card planner-card-yellow"><strong>Partners</strong><span>Referral message and local sharing.</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
            <div class="weekly-focus-card">
                <div class="weekly-focus-grid">
                    <div>
                        <div class="kpi-label">Weekly Focus</div>
                        <h2 style="margin:0.2rem 0 0.45rem;">This Week: {focus_program['name']} Campaign</h2>
                        <p class="muted" style="font-size:1rem; margin-bottom:0.85rem;">
                            Build warm community awareness for Supper Club, then drive a clear mid-week action for
                            referrals, volunteers, and families who could benefit from a welcoming meal.
                        </p>
                        {badge('Awareness', 'softgreen')}
                        {badge('Registration', 'yellow')}
                        {badge('Community connection', 'navy')}
                    </div>
                    <div>
                        <div class="detail-item" style="margin-bottom:0.75rem;">
                            <div class="kpi-label">Main Push Day</div>
                            <strong>Wednesday – conversion</strong>
                        </div>
                        <div class="detail-item">
                            <div class="kpi-label">Primary Channel</div>
                            <strong>Facebook parent + community post</strong>
                        </div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.subheader("Key Actions")
        actions = [
            ("Wed – Facebook", "Main Conversion Post", "Parent info + CTA for families, referral partners, and volunteers.", "High", "CTA", "planning-action-facebook"),
            ("Tue – Instagram", "Awareness Video", "Short real-photo story showing the warmth and welcome of Supper Club.", "Medium", "", "planning-action-instagram"),
            ("Fri – Google Ads", "Search Capture", "Refresh search ad copy for local food support and community meal intent.", "Medium", "Conversion", "planning-action-google"),
            ("Mon – Partners", "Referral Message", "Simple partner note that explains who Supper Club supports and how to refer.", "Medium", "", "planning-action-partner"),
        ]
        action_cols = st.columns(2)
        for index, (timing, title, description, priority, marker, channel_class) in enumerate(actions):
            with action_cols[index % 2]:
                marker_badge = badge(marker, "yellow") if marker else ""
                priority_class = "priority-high" if priority == "High" else "priority-medium"
                st.markdown(
                    f"""
                    <div class="planning-action-card {channel_class}">
                        {badge(timing, 'softgreen')} {marker_badge}
                        <h3>{'🔥 ' if priority == 'High' else ''}{title}</h3>
                        <p class="muted" style="margin-bottom:0;">{description}</p>
                        <div class="planning-meta">
                            <span><span class="priority-dot {priority_class}"></span>{priority} priority</span>
                            <span>{focus_program['name']}</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        st.markdown(
            """
            <div class="pipeline-summary-grid">
                <div class="pipeline-summary-item"><div class="kpi-label">Draft</div><strong>3</strong><span class="muted">Content items in progress</span></div>
                <div class="pipeline-summary-item"><div class="kpi-label">Ready</div><strong>2</strong><span class="muted">Prepared for scheduling</span></div>
                <div class="pipeline-summary-item"><div class="kpi-label">Scheduled</div><strong>4</strong><span class="muted">Ready for the week</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with planner_tabs[1]:
        st.subheader("Community Activation Planner")
        st.caption("Plan offline campaigns, partnerships, donation drives, ambassador programs, and the digital content that supports them.")
        activation_type = st.pills(
            "Campaign type",
            [
                "Digital campaign",
                "Offline community activation",
                "Hybrid campaign",
                "Donation drive",
                "School / campus partnership",
                "Ambassador program",
            ],
            default="Hybrid campaign",
            key="planner-activation-type",
        ) or "Hybrid campaign"
        st.badge(f"Planning mode: {activation_type}", color="green")
        activation_tabs = st.tabs([campaign["name"].replace(" — BGC Edition", "") for campaign in OFFLINE_ACTIVATIONS])
        for index, (tab, campaign) in enumerate(zip(activation_tabs, OFFLINE_ACTIVATIONS)):
            with tab:
                with st.container(border=True, key=f"community_activation_{index}"):
                    st.badge(campaign["name"], color="orange" if index == 0 else "green")
                    st.markdown(f"### {campaign['message']}")
                    st.caption(campaign["goal"])
                    summary_cols = st.columns(2)
                    summary_cols[0].markdown(f"**Target audience:** {campaign['audience']}")
                    summary_cols[1].markdown(f"**Best CTA:** {campaign['cta']}")
                    with st.expander("Offline tactics", expanded=False):
                        for tactic in campaign["tactics"][:4]:
                            st.caption(f"• {tactic}")
                    with st.expander("Partners and digital support", expanded=False):
                        st.markdown(f"**Potential partners:** {', '.join(campaign['partners'][:3])}")
                        st.markdown(f"**Digital support content:** {', '.join(campaign['digital_support'][:3])}")
                    st.progress(0 if index == 0 else 0.35 if index == 1 else 0.18)
                    st.caption(f"Milestone: {campaign['milestone']}")
                    st.info(campaign["impact"])

    with planner_tabs[2]:
        st.subheader("Regional Intelligence Dashboard")
        targeting_mode = st.pills(
            "Outreach intelligence mode",
            ["Local London targeting", "Broad online engagement"],
            default="Local London targeting",
            key="planner-targeting-mode",
        ) or "Local London targeting"
        if targeting_mode == "Local London targeting":
            top_region = max(LONDON_HEATMAP, key=lambda item: item["heat"])
            fastest_region = next(region for region in LONDON_HEATMAP if region["area"] == "East London")
            volunteer_region = next(region for region in LONDON_HEATMAP if region["area"] == "Downtown")
            summary_cols = st.columns(3)
            for index, (label, region, note) in enumerate([
                ("Highest engagement", top_region, f"{top_region['heat']} heat"),
                ("Fastest growing", fastest_region, "Youth + family reach"),
                ("Best volunteer response", volunteer_region, "Community storytelling"),
            ]):
                with summary_cols[index]:
                    with st.container(border=True, key=f"region_intel_summary_{index}"):
                        st.caption(label)
                        st.markdown(f"### {region['area']}")
                        st.caption(note)
            selected_region_name = st.selectbox("Focused region", [region["area"] for region in LONDON_HEATMAP], index=1)
            selected_region = next(region for region in LONDON_HEATMAP if region["area"] == selected_region_name)
            left_regions, right_focus = st.columns([0.36, 0.64], gap="large")
            with left_regions:
                with st.container(border=True, key="region_selector_summary"):
                    st.caption("Selected region")
                    st.markdown(f"### {selected_region['area']}")
                    st.progress(selected_region["heat"] / 100)
                    st.caption(f"{selected_region['heat']} / 100 heat score")
                    st.badge(selected_region["awareness"], color="green")
            with right_focus:
                with st.container(border=True, key="region_focus_panel"):
                    st.badge("Focused recommendation", icon="🎯", color="green")
                    st.markdown(f"### {selected_region['engagement']}")
                    st.write(f"**Recommended campaign:** {selected_region['campaign']}")
                    st.caption(selected_region["opportunity"])
                    st.write(f"**Awareness:** {selected_region['awareness']}")
                    with st.expander("Suggested partnerships and local activation ideas", expanded=False):
                        st.markdown("- School newsletter or referral partner mention.\n- Local business poster or QR handout.\n- Community story booth or volunteer photo moment.\n- Partner email with one clear CTA.")
        else:
            st.markdown("### Broad Online Engagement")
            signal_cols = st.columns(2)
            for index, signal in enumerate(BROAD_ONLINE_SIGNALS):
                with signal_cols[index % 2]:
                    with st.container(border=True, key=f"online_card_{index}"):
                        st.badge("Online opportunity", icon="✨", color="green")
                        st.markdown(f"### {signal['opportunity']}")
                        st.info(f"Best format: {signal['format']}")
                        st.markdown(f"**Suggested campaign:** {signal['campaign']}")
                        st.markdown(f"**Why it matters:** {signal['why']}")

    with planner_tabs[3]:
        st.subheader("Partnership Ideas")
        partner_cols = st.columns(3)
        for index, label in enumerate(["Schools", "Western / Fanshawe", "Local Businesses"]):
            with partner_cols[index]:
                st.metric(label, ["Donation links", "Student volunteers", "Drop-off points"][index])
                st.caption(["Newsletter mentions and backpack drives", "Campus ambassador content and volunteers", "Drop-off points, sponsor wall, and local visibility"][index])


def message_board_page() -> None:
    """Shared department message board for marketing collaboration."""

    header("Department Message Board", "Post department updates, asset notes, questions, and marketing handoffs in one shared place")
    channels = [
        ("# marketing", "3", "Campaign notes ready"),
        ("# tutors-education", "1", "Scholarship story ready"),
        ("# sports-coaches", "", "Team huddle clip"),
        ("# volunteers", "1", "Supper Club note"),
        ("# partnerships", "", "Partner update draft"),
    ]
    default_messages = [
        {
            "sender": "Maya Chen",
            "department": "Program Staff",
            "time": "Today 10:20 AM",
            "message": "New after-school STEM photos are ready. Marketing can use them for next week's parent outreach post.",
            "tags": ["Asset ready", "Program update"],
            "priority": "Medium",
        },
        {
            "sender": "Jordan Lee",
            "department": "Tutors / Education",
            "time": "Yesterday 3:45 PM",
            "message": "MAP scholarship student story is approved for promotion. Please mention the $1,000/year scholarship point.",
            "tags": ["Ready for content", "High priority"],
            "priority": "High",
        },
        {
            "sender": "Alex Brown",
            "department": "Sports Coaches",
            "time": "May 10",
            "message": "We have a short team huddle clip that could work well for an Instagram Reel.",
            "tags": ["Video asset", "Social idea"],
            "priority": "Low",
        },
        {
            "sender": "Priya Singh",
            "department": "Volunteer Team",
            "time": "May 09",
            "message": "Supper Club could use a simple volunteer recruitment post before next week's meal service.",
            "tags": ["Support needed", "Volunteer"],
            "priority": "Medium",
        },
    ]
    posted_messages = st.session_state.department_messages

    left, main, context = st.columns([0.22, 0.52, 0.26], gap="large")
    with left:
        st.subheader("Department Channels")
        for index, (channel, unread, preview) in enumerate(channels):
            with st.container(border=True, key=f"dept_channel_{index}"):
                row = st.columns([0.68, 0.32])
                row[0].markdown(f"**{channel}**")
                if unread:
                    row[1].badge(f"{unread} new", color="green" if index == 0 else "gray")
                st.caption(preview)

    with main:
        st.subheader("# marketing-updates")
        with st.container(border=True, key="message_composer_main"):
            st.markdown("### Post an Update")
            st.caption("What does Marketing or another department need to know?")
            with st.form("chat-message-composer", clear_on_submit=True):
                meta_cols = st.columns([0.32, 0.34, 0.24])
                with meta_cols[0]:
                    department = st.selectbox(
                        "Department",
                        DEPARTMENTS,
                        index=DEPARTMENTS.index(st.session_state.department) if st.session_state.department in DEPARTMENTS else 0,
                    )
                with meta_cols[1]:
                    message_type = st.selectbox("Message type", ["Program update", "Asset update", "Content request", "Event reminder", "Question"])
                with meta_cols[2]:
                    priority = st.selectbox("Priority", ["Low", "Medium", "High"], index=1)
                message = st.text_area(
                    "Message",
                    placeholder="What does Marketing or another department need to know?",
                    height=132,
                )
                send_cols = st.columns([0.72, 0.28])
                with send_cols[1]:
                    submitted = st.form_submit_button("Send Update", type="primary")
            if submitted:
                if not message.strip():
                    st.error("Add a short update before sending.")
                else:
                    st.session_state.department_messages.insert(
                        0,
                        {
                            "sender": st.session_state.user_email.split("@")[0].replace(".", " ").title() or "BGC Staff",
                            "department": department,
                            "time": "Just now",
                            "message": message.strip(),
                            "tags": [message_type],
                            "priority": priority,
                        },
                    )
                    st.success("Update posted to #marketing-updates.")
                    st.rerun()

        st.subheader("Recent Department Updates")
        filter_choice = st.pills(
            "Filter updates",
            ["All", "Asset updates", "Content requests", "Event reminders", "Questions"],
            default="All",
            label_visibility="collapsed",
        )
        with st.container(border=True):
            st.markdown("**Pinned campaign focus**")
            st.caption("This week’s focus: MAP back-to-school confidence campaign.")

        messages = posted_messages + default_messages
        filter_map = {
            "Asset updates": ["Asset ready", "Video asset", "Asset update"],
            "Content requests": ["Ready for content", "Content request", "Support needed"],
            "Event reminders": ["Event reminder"],
            "Questions": ["Question"],
        }
        if filter_choice != "All":
            allowed_tags = filter_map[filter_choice]
            messages = [item for item in messages if any(tag in allowed_tags for tag in item["tags"])]

        for index, item in enumerate(messages):
            with st.expander(f"{item['sender']} · {item['department']} · {item['time']}", expanded=index < 2):
                st.write(item["message"])
                tag_cols = st.columns(3)
                for tag_col, tag in zip(tag_cols, item["tags"][:2] + [item["priority"]]):
                    color = "orange" if tag in ["High", "High priority"] else "green" if tag in ["Asset ready", "Asset update", "Ready for content", "Program update"] else "gray"
                    tag_col.badge(tag, color=color)
                with st.expander(f"Message context and actions · {index + 1}", expanded=False):
                    st.caption("Asset links, campaign references, calendar actions, and reply options would appear here in a future connected version.")

    with context:
        st.subheader("Context")
        with st.container(border=True, key="message_context_focus"):
            st.caption("Pinned campaign focus")
            st.markdown("**MAP back-to-school confidence campaign**")
        with st.expander("Asset requests", expanded=False):
            st.markdown("- Student quote needed\n- Supper Club meal photo pending\n- DCAC video clip available")
        with st.expander("Calendar references", expanded=False):
            st.markdown("- May 22: MAP campaign push\n- May 24: Supper Club Facebook post\n- May 27: Sports Reel draft")


def calendar_items_by_date() -> dict[date, list[dict]]:
    """Group mock shared calendar items and intake-saved briefs by date."""

    grouped: dict[date, list[dict]] = {}
    for name, department, channel, status, item_date in SHARED_CALENDAR_ITEMS:
        grouped.setdefault(item_date, []).append(
            {
                "name": name,
                "department": department,
                "channel": channel,
                "status": status,
                "goal": channel,
                "audience": "",
                "source": "Shared Calendar",
            }
        )
    for brief in st.session_state.calendar_briefs:
        audience = ", ".join(brief["target_audience"]) if brief["target_audience"] else "Audience TBD"
        grouped.setdefault(brief["program_date"], []).append(
            {
                "name": brief["program_name"],
                "department": brief["department"],
                "channel": brief["activity_timing"],
                "status": brief["status"],
                "goal": brief["goal"],
                "audience": audience,
                "source": brief["source"],
            }
        )
    return grouped


def shared_calendar_page() -> None:
    """Week and month calendar for campaigns and department activities."""

    header("Shared Calendar", "See marketing campaigns and department activities in one shared planning view")
    view = st.radio("Calendar view", ["Week View", "Month View"], horizontal=True)
    grouped = calendar_items_by_date()
    calendar_detail_items = [
        (item_date, item)
        for item_date, items in sorted(grouped.items(), key=lambda entry: entry[0])
        for item in items
    ]
    if calendar_detail_items:
        detail_labels = [
            f"{item_date.strftime('%b %d')} · {item['name']} · {item['channel'] or item['goal']}"
            for item_date, item in calendar_detail_items
        ]
        selected_detail_label = st.selectbox("View campaign/activity details", ["Summary only"] + detail_labels)
        if selected_detail_label != "Summary only":
            detail_index = detail_labels.index(selected_detail_label)
            detail_date, detail_item = calendar_detail_items[detail_index]
            with st.expander("Calendar item detail", expanded=True):
                detail_cols = st.columns(4)
                detail_cols[0].metric("Date", detail_date.strftime("%b %d"))
                detail_cols[1].metric("Status", detail_item["status"])
                detail_cols[2].metric("Department", detail_item["department"])
                detail_cols[3].metric("Source", detail_item["source"])
                st.write(f"**Campaign/activity:** {detail_item['name']}")
                st.caption(f"Goal: {detail_item.get('goal', 'Campaign support')} · Audience: {detail_item.get('audience', 'Audience TBD') or 'Audience TBD'}")

    def channel_color(label: str) -> str:
        lowered = label.lower()
        if "instagram" in lowered:
            return "red"
        if "facebook" in lowered:
            return "blue"
        if "newsletter" in lowered:
            return "green"
        if "linkedin" in lowered or "partner" in lowered:
            return "blue"
        return "gray"

    def status_color(label: str) -> str:
        lowered = label.lower()
        if "scheduled" in lowered or "ready" in lowered:
            return "green"
        if "asset" in lowered or "review" in lowered:
            return "orange"
        return "gray"

    def event_class(item: dict) -> str:
        label = f"{item.get('channel', '')} {item.get('goal', '')} {item.get('name', '')}".lower()
        if "instagram" in label:
            return "calendar-event-instagram"
        if "facebook" in label:
            return "calendar-event-facebook"
        if "newsletter" in label:
            return "calendar-event-newsletter"
        if "linkedin" in label:
            return "calendar-event-linkedin"
        if "asset" in label or "photo" in label or "shoot" in label:
            return "calendar-event-asset"
        return "calendar-event-activity"

    def status_class(status: str) -> str:
        lowered = status.lower()
        if "scheduled" in lowered or "ready" in lowered:
            return "calendar-status-scheduled"
        if "planned" in lowered:
            return "calendar-status-planned"
        if "asset" in lowered or "consent" in lowered or "review" in lowered:
            return "calendar-status-needs"
        return "calendar-status-draft"

    def calendar_event_card(item: dict, key: str) -> None:
        event_platform = item["channel"] or item["goal"]
        st.badge(event_platform, color=channel_color(event_platform))
        st.caption(f"**{item['name']}**")

    if view == "Week View":
        start = TODAY - timedelta(days=TODAY.weekday())
        days = [start + timedelta(days=offset) for offset in range(7)]
        columns = st.columns(7)
        for day_index, (col, day) in enumerate(zip(columns, days)):
            with col:
                with st.container(border=True, key=f"shared_week_day_{day_index}"):
                    st.markdown(f"### {day.strftime('%a')}")
                    st.caption(day.strftime("%b %d"))
                    if day == TODAY:
                        st.badge("Today", color="green")
                    items = grouped.get(day, [])
                    if not items:
                        st.caption("No shared items")
                    for item_index, item in enumerate(items[:3]):
                        calendar_event_card(item, f"calendar_event_week_{day_index}_{item_index}")
                    if len(items) > 3:
                        st.caption(f"+ {len(items) - 3} more")
    else:
        first_day = TODAY.replace(day=1)
        next_month = (first_day.replace(day=28) + timedelta(days=4)).replace(day=1)
        days_in_month = (next_month - first_day).days
        blanks = first_day.weekday()
        cells: list[date | None] = [None] * blanks + [first_day + timedelta(days=offset) for offset in range(days_in_month)]
        while len(cells) % 7:
            cells.append(None)

        st.markdown(f"### {TODAY.strftime('%B %Y')}")
        grid_parts = [
            """
            <style>
                body {
                    margin: 0;
                    font-family: Inter, "Avenir Next", "Helvetica Neue", Arial, sans-serif;
                    background: transparent;
                    color: #1c2b2f;
                }
                .calendar-grid {
                    display: grid;
                    grid-template-columns: repeat(7, minmax(0, 1fr));
                    gap: 12px;
                    width: 100%;
                    box-sizing: border-box;
                }
                .calendar-weekday {
                    color: #607276;
                    font-size: 12px;
                    font-weight: 900;
                    letter-spacing: 0.06em;
                    text-transform: uppercase;
                    padding: 0 6px 2px;
                }
                .calendar-day-cell {
                    height: 145px;
                    min-height: 145px;
                    box-sizing: border-box;
                    padding: 12px;
                    border-radius: 16px;
                    background: #ffffff;
                    border: 1px solid #e2ece6;
                    box-shadow: 0 8px 20px rgba(16, 49, 58, 0.04);
                    overflow: hidden;
                }
                .calendar-day-empty {
                    background: #f8faf9;
                    border-style: dashed;
                    box-shadow: none;
                }
                .calendar-day-today {
                    border-color: #b8d8c4;
                    background: #f5fbf7;
                }
                .calendar-day-number {
                    color: #10313a;
                    font-size: 14px;
                    font-weight: 950;
                    line-height: 1;
                    margin-bottom: 8px;
                }
                .calendar-event {
                    border-radius: 10px;
                    padding: 6px 7px;
                    margin-bottom: 6px;
                    border: 1px solid #e2ece6;
                    border-left: 4px solid #a9c8b4;
                    font-size: 12px;
                    line-height: 1.18;
                    box-shadow: 0 4px 12px rgba(16, 49, 58, 0.035);
                }
                .calendar-event strong {
                    display: block;
                    color: #10313a;
                    white-space: nowrap;
                    overflow: hidden;
                    text-overflow: ellipsis;
                    margin-bottom: 3px;
                }
                .calendar-event-meta {
                    color: #53676b;
                    display: block;
                    white-space: nowrap;
                    overflow: hidden;
                    text-overflow: ellipsis;
                }
                .calendar-event-instagram { background: #fff1f3; border-left-color: #d96b78; }
                .calendar-event-facebook { background: #eef5ff; border-left-color: #5f90d6; }
                .calendar-event-newsletter { background: #edf8f2; border-left-color: #5ca37a; }
                .calendar-event-linkedin { background: #edf8f7; border-left-color: #509a98; }
                .calendar-event-asset { background: #fff8db; border-left-color: #d9bd49; }
                .calendar-event-activity { background: #f3f8f5; border-left-color: #9fc9ac; }
                .calendar-status {
                    display: inline-block;
                    border-radius: 999px;
                    padding: 2px 6px;
                    margin-top: 4px;
                    font-size: 10px;
                    font-weight: 900;
                    border: 1px solid transparent;
                }
                .calendar-status-scheduled { background: #e8f6ed; color: #165c3a; border-color: #cde5d6; }
                .calendar-status-draft { background: #eef2f1; color: #53676b; border-color: #dfe8e4; }
                .calendar-status-planned { background: #edf8f7; color: #0c4b4f; border-color: #cae3e0; }
                .calendar-status-needs { background: #fff8db; color: #6d5910; border-color: #eadb9c; }
                .calendar-more {
                    color: #155a3c;
                    font-size: 12px;
                    font-weight: 900;
                }
            </style>
            <div class="calendar-grid">
            """
        ]
        for label in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]:
            grid_parts.append(f'<div class="calendar-weekday">{label}</div>')
        for cell in cells:
            if cell is None:
                grid_parts.append('<div class="calendar-day-cell calendar-day-empty"></div>')
                continue
            items = grouped.get(cell, [])
            today_class = " calendar-day-today" if cell == TODAY else ""
            event_parts = []
            for item in items[:2]:
                event_parts.append(
                    f"""
                    <div class="calendar-event {event_class(item)}">
                        <strong>{html.escape(item['name'])}</strong>
                        <span class="calendar-event-meta">{html.escape(item['channel'] or item['goal'])}</span>
                    </div>
                    """
                )
            if len(items) > 2:
                event_parts.append(f'<div class="calendar-more">+{len(items) - 2} more</div>')
            grid_parts.append(
                f"""
                <div class="calendar-day-cell{today_class}">
                    <div class="calendar-day-number">{cell.day}</div>
                    {''.join(event_parts)}
                </div>
                """
            )
        grid_parts.append("</div>")
        components.html("".join(grid_parts), height=835, scrolling=False)


def impact_page() -> None:
    """Impact dashboard with deeper metrics and learning loop."""

    header("Impact Dashboard")
    st.subheader("Donor-ready summary")
    summary_cols = st.columns(4)
    top_metrics = [
        ("Program inquiries", IMPACT["Program inquiries"]),
        ("Registration interest", IMPACT["Registration interest"]),
        ("Volunteer interest", IMPACT["Volunteer interest"]),
        ("Partner referrals", IMPACT["Partner referrals"]),
    ]
    for index, (label, value) in enumerate(top_metrics):
        with summary_cols[index]:
            kpi(label, f"{value:,}", "Mock 30-day signal", index % 2 == 0)

    impact_tabs = st.tabs(["Funnel", "Performance Details", "Learning Loop", "Donor Proof Points"])
    with impact_tabs[0]:
        funnel_cols = st.columns(6)
        for col, (label, value) in zip(funnel_cols, FUNNEL):
            with col:
                st.markdown(f'<div class="funnel"><strong>{value}</strong>{label}</div>', unsafe_allow_html=True)

    with impact_tabs[1]:
        cols = st.columns(4)
        for index, (label, value) in enumerate(IMPACT.items()):
            with cols[index % 4]:
                kpi(label, f"{value:,}", "Mock 30-day signal", index % 2 == 0)
        st.subheader("Performance Mix")
        st.bar_chart(IMPACT)

    with impact_tabs[2]:
        learnings = [
            ("What performed well", "Parent-focused Facebook posts with clear registration details."),
            ("Audience response", "Young parents and school partners clicked most often."),
            ("Content type", "Real photos and short youth stories outperformed generic graphics."),
            ("Promote next", "After-School Recreation should follow MAP while back-to-school intent is high."),
        ]
        for title, detail in learnings:
            st.markdown(f'<div class="card-green"><strong>{title}</strong><p>{detail}</p></div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="card-yellow"><strong>Next Best Campaign:</strong><p>After-School Recreation, using parent safety and affordability messaging.</p></div>',
            unsafe_allow_html=True,
        )

    with impact_tabs[3]:
        proof_cols = st.columns(3)
        for index, proof in enumerate(DONOR_PROOF_POINTS):
            with proof_cols[index % 3]:
                st.markdown(f'<div class="card-green"><strong>{proof}</strong><p>Reusable donor-facing proof point.</p></div>', unsafe_allow_html=True)


def asset_library_page() -> None:
    """Visual asset library with gallery filters and campaign handoff."""

    header("Asset Library")
    submitted_asset_tuples = [
        (
            item["title"],
            item["type"],
            item["program"],
            item["suggested_use"],
            "Submitted",
            item["consent"],
            item["notes"] or "Submitted by department for marketing review.",
        )
        for item in st.session_state.submitted_assets
    ]
    all_assets = submitted_asset_tuples + ASSETS

    asset_detail_param = st.query_params.get("asset_detail")
    asset_use_param = st.query_params.get("asset_use")
    if asset_detail_param:
        st.session_state.asset_detail = unquote(asset_detail_param)
        del st.query_params["asset_detail"]
        st.rerun()
    if asset_use_param:
        selected_name = unquote(asset_use_param)
        selected_asset = next((asset for asset in all_assets if asset[0] == selected_name), None)
        if selected_asset:
            name, asset_type, program, channel, _approval, _consent, _suggestion = selected_asset
            best_for, use_for, pair_with = asset_suggestion_parts(selected_asset)
            campaign_name = campaign_from_asset_program(program)
            st.session_state.selected_asset = {
                "name": name,
                "program": program,
                "campaign": campaign_name,
                "type": asset_type,
                "channel": channel,
                "best_for": best_for,
                "use_for": use_for,
                "pair_with": pair_with,
            }
            st.session_state.selected_campaign = campaign_name
            st.session_state.active_page = "AI Content Studio"
            st.session_state.page = "AI Content Studio"
            del st.query_params["asset_use"]
            st.toast("Asset added to content studio")
            st.rerun()
        del st.query_params["asset_use"]

    if st.session_state.role != "Marketing":
        st.subheader("Submit Asset to Marketing")
        with st.form("asset-upload-form"):
            uploaded_file = st.file_uploader("Optional file", type=["png", "jpg", "jpeg", "mp4", "mov", "pdf", "docx", "txt"])
            asset_title = st.text_input("Asset title", placeholder="After-school STEM photos")
            department = st.selectbox(
                "Department",
                DEPARTMENTS,
                index=DEPARTMENTS.index(st.session_state.department) if st.session_state.department in DEPARTMENTS else 0,
            )
            program = st.selectbox("Program", ["Children", "Youth", "50+", "Inclusion", "Supper Club", "MAP", "DCAC", "Sports"])
            asset_type = st.selectbox("Asset type", ["Photo", "Video", "Graphic", "Testimonial", "Newsletter snippet"])
            suggested_use = st.selectbox("Suggested use", ["Instagram", "Facebook", "Newsletter", "Partner email", "Local media", "Internal"])
            consent = st.selectbox("Consent status", ["Confirmed", "Needs check", "Not applicable"])
            notes = st.text_area("Notes for marketing team")
            submitted = st.form_submit_button("Submit asset to Marketing")
        if submitted:
            if not asset_title.strip():
                st.error("Please add an asset title.")
            else:
                st.session_state.submitted_assets.insert(
                    0,
                    {
                        "title": asset_title.strip(),
                        "department": department,
                        "program": program,
                        "type": asset_type,
                        "suggested_use": suggested_use,
                        "consent": consent,
                        "notes": notes.strip(),
                        "file_name": uploaded_file.name if uploaded_file else "No file attached",
                    },
                )
                st.success("Asset submitted to Marketing review.")
                st.rerun()
    elif st.session_state.submitted_assets:
        st.subheader("Department Asset Submissions")
        cols = st.columns(3)
        for index, item in enumerate(st.session_state.submitted_assets[:3]):
            with cols[index % 3]:
                st.markdown(
                    f"""
                    <div class="card">
                        {badge(item['department'], 'softgreen')} {status_badge('Marketing review')}
                        <h3 style="margin:0.45rem 0;">{item['title']}</h3>
                        <p class="muted">{item['program']} · {item['type']} · {item['suggested_use']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    filter_config = {
        "program": ["All", "Children", "Youth", "50+", "Inclusion", "Supper Club", "MAP", "DCAC", "Sports"],
        "type": ["All", "Photos", "Videos", "Graphics", "Testimonials", "Newsletter"],
        "channel": ["All", "Instagram", "Facebook", "LinkedIn", "Newsletter"],
        "status": ["All", "Approved", "Needs Review", "Submitted", "Missing Consent"],
    }
    filter_labels = {
        "program": "Program filters",
        "type": "Asset type",
        "channel": "Channel fit",
        "status": "Status",
    }

    with st.container(border=True):
        st.markdown(
            """
            <div class="asset-filter-panel" style="border:none;box-shadow:none;padding:0;margin-bottom:0.4rem;">
                <h3>Filter Assets</h3>
                <p class="muted" style="margin:0;">Find the right content by program, asset type, channel, and review status.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        for filter_key, options in filter_config.items():
            st.markdown(f'<div class="asset-filter-label">{filter_labels[filter_key]}</div>', unsafe_allow_html=True)
            selected_filter = st.pills(
                filter_labels[filter_key],
                options,
                default=st.session_state.asset_filters[filter_key],
                key=f"asset-filter-{filter_key}",
                label_visibility="collapsed",
            )
            st.session_state.asset_filters[filter_key] = selected_filter or "All"

    filtered = []
    for asset in all_assets:
        name, asset_type, program, channel, approval, consent, suggestion = asset
        program_filter = st.session_state.asset_filters["program"]
        type_filter = st.session_state.asset_filters["type"]
        channel_filter = st.session_state.asset_filters["channel"]
        status_filter = st.session_state.asset_filters["status"]
        type_group = (
            "Videos" if "video" in asset_type.lower()
            else "Graphics" if "graphic" in asset_type.lower()
            else "Testimonials" if "testimonial" in asset_type.lower()
            else "Newsletter" if "newsletter" in asset_type.lower()
            else "Photos"
        )
        status_group = "Missing Consent" if consent == "Consent check needed" else approval
        if program_filter != "All" and program != program_filter:
            continue
        if type_filter != "All" and type_group != type_filter:
            continue
        if channel_filter != "All" and channel != channel_filter:
            continue
        if status_filter != "All" and status_group != status_filter:
            continue
        filtered.append(asset)

    st.subheader(f"{len(filtered)} Assets")
    if filtered:
        asset_cols = st.columns(3)
        for index, (name, asset_type, program, channel, approval, consent, suggestion) in enumerate(filtered):
            with asset_cols[index % 3]:
                preview_icon = asset_icon(asset_type)
                best_for, use_for, pair_with = asset_suggestion_parts((name, asset_type, program, channel, approval, consent, suggestion))
                with st.container(border=True, key=f"asset_native_card_{index}"):
                    with st.container(border=True, key=f"asset_preview_{index}"):
                        st.markdown(f"## {preview_icon}")
                        st.caption("No preview")
                    st.caption(best_for)
                    st.write(f"**{name}**")
                    tag_cols = st.columns(2)
                    tag_cols[0].badge(program, color="green")
                    tag_cols[1].badge(channel, color="blue")
                    status_cols = st.columns(2)
                    status_cols[0].badge(approval, color="green" if approval == "Approved" else "orange")
                    status_cols[1].badge(consent, color="green" if consent == "Consent confirmed" else "orange" if consent == "Consent check needed" else "gray")
                    st.caption(use_for)
                    button_cols = st.columns(2)
                    if button_cols[0].button("View details", key=f"asset-detail-{index}", use_container_width=True):
                        st.session_state.asset_detail = name
                        st.rerun()
                    if button_cols[1].button("Use in campaign", key=f"asset-use-{index}", use_container_width=True):
                        campaign_name = campaign_from_asset_program(program)
                        st.session_state.selected_asset = {
                            "name": name,
                            "program": program,
                            "campaign": campaign_name,
                            "type": asset_type,
                            "channel": channel,
                            "best_for": best_for,
                            "use_for": use_for,
                            "pair_with": pair_with,
                        }
                        st.session_state.selected_campaign = campaign_name
                        st.session_state.active_page = "AI Content Studio"
                        st.session_state.page = "AI Content Studio"
                        st.toast("Asset added to content studio")
                        st.rerun()
    if not filtered:
        with st.container(border=True, key="asset_empty_state"):
            st.markdown("## 🗂️")
            st.write("**No preview**")
            st.caption("No mock assets match these filters.")

    detail_name = st.session_state.get("asset_detail")
    detail_asset = next((asset for asset in all_assets if asset[0] == detail_name), None)
    if detail_asset:
        name, asset_type, program, channel, approval, consent, suggestion = detail_asset
        best_for, use_for, pair_with = asset_suggestion_parts(detail_asset)
        st.subheader("Asset Detail")
        left, right = st.columns([1.1, 0.9])
        with left:
            with st.container(border=True, key="asset_detail_preview"):
                st.markdown(f"# {asset_icon(asset_type)}")
                st.write("**No preview**")
                st.caption("Placeholder preview for this mock asset.")
        with right:
            with st.container(border=True, key="asset_detail_card_native"):
                st.caption(asset_type)
                st.markdown(f"## {name}")
                tag_cols = st.columns(2)
                tag_cols[0].badge(program, color="green")
                tag_cols[1].badge(channel, color="blue")
                status_cols = st.columns(2)
                status_cols[0].badge(approval, color="green" if approval == "Approved" else "yellow")
                status_cols[1].badge(consent, color="green" if consent == "Consent confirmed" else "yellow" if consent == "Consent check needed" else "gray")
                st.caption(suggestion)
                st.badge(best_for, color="green")
                st.badge(use_for, color="orange")
                st.badge(pair_with, color="gray")
                st.write("**Suggested caption angle:** Connect the asset to a real BGC program moment with a clear next step.")


# ---------------------------------------------------------------------------
# App shell
# ---------------------------------------------------------------------------

def main() -> None:
    """Render navigation and the selected command-center page."""

    init_state()
    load_css()
    if not st.session_state.logged_in:
        login_page()
        return

    page = render_sidebar_v2()

    if page == "Dashboard":
        dashboard_page()
    elif page == "Program & Asset Intake":
        intake_page()
    elif page == "Trend & Performance Scan":
        trends_page()
    elif page == "AI Campaign Recommendation":
        recommendation_page()
    elif page == "AI Viral Content Engine":
        viral_content_engine_page()
    elif page == "AI Content Studio":
        content_studio_page()
    elif page == "Campaign Planner":
        planner_page()
    elif page == "Impact Dashboard":
        impact_page()
    elif page in ["Asset Library", "Asset Upload / Asset Library"]:
        asset_library_page()
    elif page == "Department Message Board":
        message_board_page()
    elif page == "Shared Calendar":
        shared_calendar_page()
    else:
        dashboard_page()


if __name__ == "__main__":
    main()

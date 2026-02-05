from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
import os, re, json, random, logging, requests
from enum import Enum

# =====================================================
# CONFIG (FINAL SUBMISSION)
# =====================================================

API_KEY = os.getenv("HONEYPOT_API_KEY", "testkey")

MIN_ENGAGEMENT_TURNS = 5
MAX_HISTORY = 20

# 🔴 FINAL SUBMISSION SETTINGS
ENABLE_CALLBACK = True
CALLBACK_MODE = "guvi"

GUVI_CALLBACK_URL = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"

# =====================================================
# APP
# =====================================================

app = FastAPI(title="Agentic Honeypot API – Final Submission")
logging.basicConfig(level=logging.INFO)

# =====================================================
# MODELS
# =====================================================

class Sender(str, Enum):
    scammer = "scammer"
    user = "user"

class Message(BaseModel):
    sender: Sender
    text: str
    timestamp: int

class Metadata(BaseModel):
    channel: Optional[str] = None
    language: Optional[str] = None
    locale: Optional[str] = None

class HoneypotRequest(BaseModel):
    sessionId: str
    message: Message
    conversationHistory: Optional[List[Message]] = []
    metadata: Optional[Metadata] = None

class Engagement(BaseModel):
    turnsSoFar: int
    agentTurns: int

class Intelligence(BaseModel):
    bankAccounts: List[str]
    upiIds: List[str]
    phishingLinks: List[str]
    phoneNumbers: List[str]
    suspiciousKeywords: List[str]

class HoneypotResponse(BaseModel):
    status: str
    scamDetected: bool
    agentActive: bool
    engagement: Engagement
    reply: str
    extractedIntelligence: Intelligence

# =====================================================
# SESSION STORE (IN-MEMORY)
# =====================================================

sessions: Dict[str, dict] = {}

# =====================================================
# AUTH
# =====================================================

def verify_key(key: Optional[str]):
    if key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

# =====================================================
# REGEX PATTERNS
# =====================================================

UPI_REGEX = re.compile(r"\b[a-zA-Z0-9.\-_]{2,}@(upi|ybl|okicici|oksbi|okaxis|paytm)\b")
LINK_REGEX = re.compile(r"https?://[^\s]+")
PHONE_REGEX = re.compile(r"\b(?:\+91[\-\s]?)?[6-9]\d{9}\b")
BANK_REGEX = re.compile(r"\b\d{9,18}\b")

SUSPICIOUS_KEYWORDS = [
    "urgent", "verify", "blocked", "freeze",
    "suspend", "otp", "password", "transaction"
]

# =====================================================
# INTELLIGENCE EXTRACTION
# =====================================================

def extract_intel(text: str, intel: dict):
    t = text.lower()

    for m in UPI_REGEX.finditer(t):
        if m.group() not in intel["upiIds"]:
            intel["upiIds"].append(m.group())

    for m in LINK_REGEX.finditer(t):
        if m.group() not in intel["phishingLinks"]:
            intel["phishingLinks"].append(m.group())

    for m in PHONE_REGEX.finditer(t):
        if m.group() not in intel["phoneNumbers"]:
            intel["phoneNumbers"].append(m.group())

    for m in BANK_REGEX.finditer(t):
        if not PHONE_REGEX.fullmatch(m.group()):
            if m.group() not in intel["bankAccounts"]:
                intel["bankAccounts"].append(m.group())

    for kw in SUSPICIOUS_KEYWORDS:
        if kw in t and kw not in intel["suspiciousKeywords"]:
            intel["suspiciousKeywords"].append(kw)

def has_actionable_intel(intel: dict) -> bool:
    return any([
        intel["upiIds"],
        intel["phishingLinks"],
        intel["phoneNumbers"],
        intel["bankAccounts"]
    ])

# =====================================================
# SCAM CONFIRMATION LOGIC
# =====================================================

SCAM_TRIGGERS = ["blocked", "verify", "upi", "kyc", "pay", "suspend"]

def confirm_scam(history: List[Message]) -> bool:
    score = 0
    for msg in history:
        score += sum(1 for k in SCAM_TRIGGERS if k in msg.text.lower())
    return score >= 3

# =====================================================
# AGENT BEHAVIOR
# =====================================================

BASE_REPLIES = [
    "Why is my account being blocked?",
    "I did not receive any message earlier.",
    "What verification is required?",
    "Why is payment needed?",
    "The app is not responding."
]

FAILURES = [
    "I tried but it did not work.",
    "It shows an error.",
    "Nothing happened after clicking.",
    "It got stuck on confirmation."
]

def human_reply(base: str, turn: int) -> str:
    prefix = (
        "I am not sure, but" if turn <= 1 else
        "This is confusing," if turn <= 3 else
        "Please help quickly,"
    )
    msg = f"{prefix} {base}"
    if random.random() < 0.5:
        msg += " " + random.choice(FAILURES)
    return msg

# =====================================================
# FINAL CALLBACK (GUVI)
# =====================================================

def handle_final_result(session_id: str, state: dict):
    payload = {
        "sessionId": session_id,
        "scamDetected": True,
        "totalMessagesExchanged": state["total_messages"],
        "extractedIntelligence": state["intel"],
        "agentNotes": "Scammer used urgency and payment redirection tactics"
    }

    logging.info("FINAL_PAYLOAD_READY")
    logging.info(json.dumps(payload, indent=2))

    if ENABLE_CALLBACK and CALLBACK_MODE == "guvi":
        try:
            response = requests.post(
                GUVI_CALLBACK_URL,
                json=payload,
                timeout=5
            )
            logging.info(f"GUVI_CALLBACK_SENT → {response.status_code}")
        except Exception:
            logging.exception("GUVI_CALLBACK_FAILED")

# =====================================================
# API ENDPOINT
# =====================================================

@app.post("/honeypot", response_model=HoneypotResponse)
def honeypot(req: HoneypotRequest, x_api_key: Optional[str] = Header(None)):
    verify_key(x_api_key)
    sid = req.sessionId

    if sid not in sessions:
        sessions[sid] = {
            "agent_turns": 0,
            "total_messages": 0,
            "intel": {
                "bankAccounts": [],
                "upiIds": [],
                "phishingLinks": [],
                "phoneNumbers": [],
                "suspiciousKeywords": []
            },
            "scam_confirmed": False,
            "final_sent": False
        }

    state = sessions[sid]
    state["total_messages"] += 1

    history = ((req.conversationHistory or []) + [req.message])[-MAX_HISTORY:]

    extract_intel(req.message.text, state["intel"])

    if not state["scam_confirmed"] and len(history) >= 2:
        state["scam_confirmed"] = confirm_scam(history)

    base = BASE_REPLIES[min(state["agent_turns"], len(BASE_REPLIES) - 1)]
    state["agent_turns"] += 1
    reply = human_reply(base, state["agent_turns"])

    if (
        state["scam_confirmed"]
        and state["agent_turns"] >= MIN_ENGAGEMENT_TURNS
        and not state["final_sent"]
        and has_actionable_intel(state["intel"])
    ):
        handle_final_result(sid, state)
        state["final_sent"] = True

    return HoneypotResponse(
        status="success",
        scamDetected=state["scam_confirmed"],
        agentActive=state["scam_confirmed"],
        engagement=Engagement(
            turnsSoFar=state["total_messages"],
            agentTurns=state["agent_turns"]
        ),
        reply=reply,
        extractedIntelligence=Intelligence(**state["intel"])
    )

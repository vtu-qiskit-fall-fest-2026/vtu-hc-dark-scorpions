import streamlit as st
from streamlit.components.v1 import html

st.set_page_config(page_title="Dark Scorpions", page_icon="🦂", layout="wide")

st.markdown("""
<style>
    #MainMenu, footer, header, [data-testid="stSidebar"] {visibility: hidden; display: none;}
    .block-container {padding: 0; margin: 0; max-width: 100%;}
    .stApp {background: #0a0a1a;}
    [data-testid="stMain"] {padding: 0;}
</style>
""", unsafe_allow_html=True)

page = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/ScrollTrigger.min.js"></script>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
html { scroll-behavior: smooth; }
html, body {
    background: #0a0a1a;
    color: #fff;
    font-family: 'Segoe UI', sans-serif;
    overflow-x: hidden;
    cursor: none !important; 
    height: 100%;
}

/* ─── LOADER ─── */
.loader {
    position: fixed;
    inset: 0;
    background: #0a0a1a;
    z-index: 10000;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    gap: 1.5rem;
}
.loader .scorpion {
    font-size: 4rem;
    animation: pulse 1.5s ease-in-out infinite;
}
@keyframes pulse {
    0%, 100% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.2); opacity: 0.7; }
}
.loader .bar {
    width: 200px;
    height: 3px;
    background: rgba(124,58,237,0.2);
    border-radius: 3px;
    overflow: hidden;
}
.loader .bar::after {
    content: '';
    display: block;
    width: 40%;
    height: 100%;
    background: linear-gradient(90deg, #7c3aed, #3b82f6);
    border-radius: 3px;
    animation: load 1.2s ease-in-out infinite;
}
@keyframes load {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(250%); }
}

/* ─── CUSTOM CURSOR ─── */
.cursor {
    width: 8px; height: 8px;
    background: #a78bfa;
    border-radius: 50%;
    position: fixed;
    pointer-events: none;
    z-index: 9999;
    box-shadow: 0 0 10px #a78bfa, 0 0 20px #a78bfa55;
}
.cursor-ring {
    width: 35px; height: 35px;
    border: 1.5px solid #a78bfa88;
    border-radius: 50%;
    position: fixed;
    pointer-events: none;
    z-index: 9998;
    transition: all 0.15s ease-out;
}
.cursor-ring.hover {
    transform: scale(2);
    border-color: #3b82f6;
    background: #3b82f611;
}

/* ─── 3D CANVAS ─── */
#bg-canvas {
    position: fixed;
    top: 0; left: 0;
    width: 100vw; height: 100vh;
    z-index: 0;
}

/* ─── GLOW ORBS ─── */
.orb {
    position: fixed;
    width: 500px; height: 500px;
    border-radius: 50%;
    filter: blur(130px);
    opacity: 0.1;
    z-index: 0;
    pointer-events: none;
    top: 50%; left: 50%;
}
.orb-1 {
    background: #7c3aed;
    transform: translate(-75%, -65%);
    animation: float1 10s ease-in-out infinite;
}
.orb-2 {
    background: #3b82f6;
    transform: translate(-25%, -35%);
    animation: float2 12s ease-in-out infinite;
}
@keyframes float1 {
    0%,100% { transform: translate(-75%, -65%); }
    50%     { transform: translate(-70%, -60%); }
}
@keyframes float2 {
    0%,100% { transform: translate(-25%, -35%); }
    50%     { transform: translate(-30%, -40%); }
}

/* ─── CONTENT ─── */
.content { position: relative; z-index: 1; }

/* ─── HERO ─── */
.hero {
    height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 2rem;
}
.hero h1 {
    font-size: 4rem;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 0.8rem;
}
.hero h1 .scorpion-icon {
    font-size: 4rem;
    -webkit-text-fill-color: initial;
    color: #a78bfa;
    text-shadow: 0 0 30px #7c3aed, 0 0 60px #7c3aed44;
    display: inline-block;
}
.hero h1 .team-name {
    display: inline-flex;
    overflow: hidden;
}
.hero h1 .team-name .letter {
    display: inline-block;
    background: linear-gradient(135deg, #7c3aed, #3b82f6, #a78bfa);
    background-size: 200%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: gradientShift 3s ease infinite, letterIn 0.6s cubic-bezier(0.22, 1, 0.36, 1) forwards;
    opacity: 0;
    transform: translateY(100%);
}
@keyframes gradientShift {
    0%, 100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
}
@keyframes letterIn {
    to { opacity: 1; transform: translateY(0); }
}
.hero p {
    font-size: 1.3rem;
    color: #c4b5fd;
    max-width: 500px;
    opacity: 0;
    letter-spacing: 1px;
}
.scroll-hint {
    position: absolute;
    bottom: 3rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
    color: #a78bfa;
    font-size: 0.75rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    opacity: 0;
}
.scroll-hint .line {
    width: 1px;
    height: 40px;
    background: linear-gradient(to bottom, #a78bfa, transparent);
    animation: scrollLine 2s ease-in-out infinite;
}
@keyframes scrollLine {
    0%, 100% { transform: scaleY(1); opacity: 1; }
    50% { transform: scaleY(0.5); opacity: 0.3; }
}

/* ─── DIVIDER ─── */
.divider {
    width: 100%;
    height: 1px;
    background: linear-gradient(90deg, transparent, #7c3aed55, #3b82f655, transparent);
    margin: 0 auto;
}

/* ─── STATS ─── */
.stats {
    padding: 5rem 2rem;
    max-width: 900px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 2rem;
    text-align: center;
}
.stat-item {
    opacity: 0;
    transform: translateY(30px);
}
.stat-item .number {
    font-size: 2.5rem;
    font-weight: 800;
    background: linear-gradient(135deg, #7c3aed, #3b82f6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.stat-item .label {
    color: #94a3b8;
    font-size: 0.85rem;
    margin-top: 0.5rem;
    letter-spacing: 1px;
    text-transform: uppercase;
}

/* ─── TEAM SECTION ─── */
.team-section {
    padding: 5rem 2rem;
    max-width: 1100px;
    margin: 0 auto;
    text-align: center;
}
.team-section h2 {
    font-size: 2.2rem;
    margin-bottom: 3rem;
    background: linear-gradient(90deg, #7c3aed, #3b82f6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.team-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 2rem;
    perspective: 1200px;
}
.team-card {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(124,58,237,0.15);
    border-radius: 20px;
    padding: 2.5rem 2rem;
    backdrop-filter: blur(20px);
    transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    opacity: 0;
    transform: translateY(50px);
    position: relative;
    overflow: hidden;
    transform-style: preserve-3d;
}
.team-card::before {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(600px circle at var(--mx, 50%) var(--my, 50%), rgba(124,58,237,0.1), transparent 40%);
    opacity: 0;
    transition: opacity 0.4s;
    pointer-events: none;
}   
.team-card:hover::before { opacity: 1; }
.team-card:hover {
    border-color: #7c3aed;
    box-shadow: 0 30px 80px rgba(124,58,237,0.15), 0 0 40px rgba(124,58,237,0.05);
    transform: translateY(-8px);
}
.team-card .avatar {
    width: 70px;
    height: 70px;
    border-radius: 50%;
    background: linear-gradient(135deg, #7c3aed, #3b82f6);
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 1.2rem;
    font-size: 1.8rem;
    font-weight: 800;
    color: #fff;
    box-shadow: 0 8px 30px rgba(124,58,237,0.3);
}
.team-card h3 {
    color: #fff;
    font-size: 1.1rem;
    margin-bottom: 0.3rem;
}
.team-card .role {
    color: #a78bfa;
    font-size: 0.85rem;
    font-weight: 600;
    letter-spacing: 0.5px;
    margin-bottom: 1.2rem;
}
.team-card .socials {
    display: flex;
    justify-content: center;
    gap: 1rem;
}
.team-card .socials a {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 38px;
    height: 38px;
    border-radius: 10px;
    background: rgba(124,58,237,0.1);
    border: 1px solid rgba(124,58,237,0.25);
    color: #a78bfa;
    text-decoration: none;
    font-size: 1rem;
    transition: all 0.3s;
}
.team-card .socials a:hover {
    background: rgba(124,58,237,0.25);
    border-color: #7c3aed;
    transform: translateY(-3px);
    box-shadow: 0 8px 20px rgba(124,58,237,0.3);
}

/* ─── NAVIGATION ─── */
.nav-section {
    padding: 5rem 2rem;
    max-width: 1100px;
    margin: 0 auto;
    text-align: center;
}
.nav-section h2 {
    font-size: 2.2rem;
    margin-bottom: 3rem;
    background: linear-gradient(90deg, #7c3aed, #3b82f6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.nav-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 2rem;
    perspective: 1200px;
}
.nav-btn {
    display: block;
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(124,58,237,0.15);
    border-radius: 20px;
    padding: 2.5rem 2rem;
    text-decoration: none;
    color: #fff;
    backdrop-filter: blur(20px);
    transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    opacity: 0;
    transform: translateY(50px);
    position: relative;
    overflow: hidden;
    transform-style: preserve-3d;
}
.nav-btn::before {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(600px circle at var(--mx, 50%) var(--my, 50%), rgba(124,58,237,0.12), transparent 40%);
    opacity: 0;
    transition: opacity 0.4s;
    pointer-events: none;
}   
.nav-btn:hover::before { opacity: 1; }
.nav-btn:hover {
    border-color: #7c3aed;
    box-shadow: 0 30px 80px rgba(124,58,237,0.15), 0 0 40px rgba(124,58,237,0.05);
    background: rgba(124,58,237,0.03);
}
.nav-btn.disabled {
    opacity: 0.4;
    pointer-events: none;
    filter: blur(2px) grayscale(0.4);
}
.nav-btn .icon { font-size: 2.8rem; margin-bottom: 1.2rem; display: block; }
.nav-btn h3 { color: #a78bfa; margin-bottom: 0.6rem; font-size: 1.15rem; }
.nav-btn p { color: #94a3b8; line-height: 1.6; font-size: 0.9rem; }
.nav-btn .tag {
    display: inline-block;
    margin-top: 1.2rem;
    padding: 0.35rem 0.9rem;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 600;
    background: rgba(124,58,237,0.1);
    border: 1px solid rgba(124,58,237,0.25);
    color: #a78bfa;
    letter-spacing: 0.5px;
}
.coming-soon {
    position: absolute;
    top: 1.2rem;
    right: 1.2rem;
    background: linear-gradient(135deg, #7c3aed, #3b82f6);
    color: #fff;
    font-size: 0.65rem;
    font-weight: 700;
    padding: 0.35rem 0.8rem;
    border-radius: 20px;
    letter-spacing: 1px;
    text-transform: uppercase;
    box-shadow: 0 4px 20px rgba(124,58,237,0.4);
}

/* ─── FOOTER ─── */
.footer {
    text-align: center;
    padding: 4rem 2rem;
    color: #445;
    font-size: 0.85rem;
    border-top: 1px solid rgba(255,255,255,0.03);
    margin-top: 5rem;
}
</style>
</head>
<body>

<!-- LOADER -->
<div class="loader" id="loader">
    <div class="scorpion">🦂</div>
    <div class="bar"></div>
</div>

<!-- CURSOR -->
<div class="cursor"></div>
<div class="cursor-ring"></div>

<!-- 3D -->
<canvas id="bg-canvas"></canvas>

<!-- ORBS -->
<div class="orb orb-1"></div>
<div class="orb orb-2"></div>

<!-- CONTENT -->
<div class="content">
    <section class="hero">
        <h1>
            <span class="scorpion-icon">🦂</span>
            <span class="team-name" id="team-name"></span>
        </h1>
        <p id="hero-sub">Our first step into the Quantum World.</p>
        <div class="scroll-hint" id="scroll-hint">
            <span>Scroll</span>
            <div class="line"></div>
        </div>
    </section>

    <div class="divider"></div>

    <section class="stats">
        <div class="stat-item">
            <div class="number">1</div>
            <div class="label">Labs Built</div>
        </div>
        <div class="stat-item">
            <div class="number">2</div>
            <div class="label">Algorithms</div>
        </div>
        <div class="stat-item">
            <div class="number">1</div>
            <div class="label">Quantum World</div>
        </div>
    </section>

    <div class="divider"></div>

    <!-- ─── TEAM SECTION ─── -->
    <section class="team-section">
        <h2>Meet the Team</h2>
        <div class="team-grid">
            <div class="team-card">
                <div class="avatar">AK</div>
                <h3>Aditya B Koparde</h3>
                <div class="role">Team Lead</div>
                <div class="socials">
                    <a onclick="window.open('https://github.com/AdityaKoparde', '_blank')" title="GitHub">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
                    </a>
                    <a onclick="window.open('https://www.linkedin.com/in/aditya-koparde-2b89b0430', '_blank')" title="LinkedIn">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
                    </a>
                </div>
            </div>
            <div class="team-card">
                <div class="avatar">JL</div>
                <h3>Jeswin J Lazarus</h3>
                <div class="role">Developer</div>
                <div class="socials">
                    <a onclick="window.open('https://github.com/Jeswin2008-arc', '_blank')" title="GitHub">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
                    </a>
                    <a onclick="window.open('https://www.linkedin.com/in/jeswin-lazarus-801895431/', '_blank')" title="LinkedIn">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
                    </a>
                </div>
            </div>
            <div class="team-card">
                <div class="avatar">TK</div>
                <h3>Tejas Vithal Kadam</h3>
                <div class="role">Developer</div>
                <div class="socials">
                    <a onclick="window.open('https://github.com/kadamtejas407-lang', '_blank')" title="GitHub">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
                    </a>
                    <a onclick="window.open('https://www.linkedin.com/in/tejas-kadam-095731410/', '_blank')" title="LinkedIn">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
                    </a>
                </div>
            </div>
        </div>
    </section>

    <div class="divider"></div>

    <section class="nav-section">
        <h2>Explore Our Labs</h2>
        <div class="nav-grid">
            <a class="nav-btn" href="/1_Quantum_Lab">
                <span class="icon">📊</span>
                <h3>Quantum Optimisation Lab</h3>
                <p>Solve MaxCut with QAOA vs classical brute force. Compare speed, accuracy & trade-offs.</p>
                <span class="tag">QAOA · Streamlit</span>
            </a>
            <div class="nav-btn">
                <span class="coming-soon">Coming Soon</span>
                <span class="icon">🔐</span>
                <h3>Quantum Cryptography</h3>
                <p>Simulate BB84 QKD. Watch eavesdroppers get detected via QBER analysis.</p>
                <span class="tag">BB84 · QKD</span>
            </div>
            <div class="nav-btn">
                <span class="coming-soon">Coming Soon</span>
                <span class="icon">🎲</span>
                <h3>Quantum Randomness</h3>
                <p>Generate truly random numbers using superposition. Test with chi-squared.</p>
                <span class="tag">QRNG · Stats</span>
            </div>
        </div>
    </section>

    <div class="footer">
        Dark Scorpions · Qiskit Fall Fest 2026
    </div>
</div>

<script>
// ─── LOADER ───
window.addEventListener('load', () => {
    setTimeout(() => {
        const loader = document.getElementById('loader');
        loader.style.transition = 'opacity 0.8s, visibility 0.8s';
        loader.style.opacity = '0';
        loader.style.visibility = 'hidden';
        startHeroAnimation();
    }, 1500);
});

// ─── LETTER-BY-LETTER TITLE ───
function startHeroAnimation() {
    const text = "Dark Scorpions";
    const container = document.getElementById('team-name');
    text.split('').forEach((char, i) => {
        const span = document.createElement('span');
        span.className = 'letter';
        span.textContent = char === ' ' ? '\\u00A0' : char;
        span.style.animationDelay = `${i * 0.05}s, ${i * 0.05}s`;
        container.appendChild(span);
    });
    gsap.to('#hero-sub', { opacity: 1, y: 0, duration: 1, delay: 1.2 });
    gsap.to('#scroll-hint', { opacity: 1, duration: 1, delay: 1.8 });
}

// ─── CURSOR ───
const cursor = document.querySelector('.cursor');
const ring = document.querySelector('.cursor-ring');
document.addEventListener('mousemove', e => {
    cursor.style.left = e.clientX - 4 + 'px';
    cursor.style.top = e.clientY - 4 + 'px';
    ring.style.left = e.clientX - 17 + 'px';
    ring.style.top = e.clientY - 17 + 'px';
});
document.querySelectorAll('.nav-btn:not(.disabled), .team-card, a, button').forEach(el => {
    el.addEventListener('mouseenter', () => ring.classList.add('hover'));
    el.addEventListener('mouseleave', () => ring.classList.remove('hover'));
});

// ─── 3D CARD TILT (labs + team) ───
document.querySelectorAll('.nav-btn:not(.disabled), .team-card').forEach(card => {
    card.addEventListener('mousemove', e => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;
        const rotateX = (y - centerY) / centerY * -6;
        const rotateY = (x - centerX) / centerX * 6;
        card.style.transform = `translateY(-8px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(1.02)`;
        card.style.setProperty('--mx', (x / rect.width * 100) + '%');
        card.style.setProperty('--my', (y / rect.height * 100) + '%');
    });
    card.addEventListener('mouseleave', () => {
        card.style.transform = 'translateY(0) rotateX(0) rotateY(0) scale(1)';
    });
});

// ─── THREE.JS ───
const canvas = document.getElementById('bg-canvas');
const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.z = 30;

let mouseX = 0, mouseY = 0;
document.addEventListener('mousemove', e => {
    mouseX = (e.clientX / window.innerWidth - 0.5) * 2;
    mouseY = (e.clientY / window.innerHeight - 0.5) * 2;
});

const particleGeo = new THREE.BufferGeometry();
const count = 3000;
const positions = new Float32Array(count * 3);
for (let i = 0; i < count * 3; i++) positions[i] = (Math.random() - 0.5) * 100;
particleGeo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
const particleMat = new THREE.PointsMaterial({ color: 0x7c3aed, size: 0.12, transparent: true, opacity: 0.5 });
const particles = new THREE.Points(particleGeo, particleMat);
scene.add(particles);

const lineGeo = new THREE.BufferGeometry();
const linePositions = [];
const posAttr = particleGeo.attributes.position;
for (let i = 0; i < 100; i++) {
    const a = Math.floor(Math.random() * count);
    const b = Math.floor(Math.random() * count);
    linePositions.push(
        posAttr.getX(a), posAttr.getY(a), posAttr.getZ(a),
        posAttr.getX(b), posAttr.getY(b), posAttr.getZ(b)
    );
}
lineGeo.setAttribute('position', new THREE.Float32BufferAttribute(linePositions, 3));
const lineMat = new THREE.LineBasicMaterial({ color: 0x3b82f6, transparent: true, opacity: 0.08 });
const lines = new THREE.LineSegments(lineGeo, lineMat);
scene.add(lines);

const icoGeo = new THREE.IcosahedronGeometry(10, 1);
const icoMat = new THREE.MeshBasicMaterial({ color: 0x3b82f6, wireframe: true, transparent: true, opacity: 0.25 });
const ico = new THREE.Mesh(icoGeo, icoMat);
ico.position.set(0, 0, -15);
scene.add(ico);

const torusGeo = new THREE.TorusKnotGeometry(3, 0.8, 64, 8);
const torusMat = new THREE.MeshBasicMaterial({ color: 0x7c3aed, wireframe: true, transparent: true, opacity: 0.2 });
const torus = new THREE.Mesh(torusGeo, torusMat);
torus.position.set(0, 0, -15);
scene.add(torus);

const sphereGeo = new THREE.SphereGeometry(2, 32, 32);
const sphereMat = new THREE.MeshBasicMaterial({ color: 0x7c3aed, transparent: true, opacity: 0.1 });
const sphere = new THREE.Mesh(sphereGeo, sphereMat);
sphere.position.set(0, 0, -15);
scene.add(sphere);

function animate() {
    requestAnimationFrame(animate);
    ico.rotation.x += 0.002 + mouseY * 0.001;
    ico.rotation.y += 0.003 + mouseX * 0.001;
    torus.rotation.x += 0.004;
    torus.rotation.y += 0.002;
    torus.rotation.z += 0.001;
    sphere.scale.setScalar(1 + 0.15 * Math.sin(Date.now() * 0.002));
    particles.rotation.y += 0.0003;
    particles.rotation.x += 0.0001;
    lines.rotation.y += 0.0003;
    lines.rotation.x += 0.0001;
    camera.position.x += (mouseX * 2 - camera.position.x) * 0.02;
    camera.position.y += (-mouseY * 2 - camera.position.y) * 0.02;
    camera.lookAt(0, 0, -15);
    renderer.render(scene, camera);
}
animate();

window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

// ─── GSAP SCROLL ANIMATIONS ───
gsap.registerPlugin(ScrollTrigger);

gsap.utils.toArray('.stat-item').forEach((item, i) => {
    gsap.to(item, {
        opacity: 1, y: 0, duration: 0.8, delay: i * 0.15,
        scrollTrigger: { trigger: item, start: 'top 85%', toggleActions: 'play none none reverse' }
    });
});

gsap.utils.toArray('.team-card').forEach((card, i) => {
    gsap.to(card, {
        opacity: 1, y: 0, duration: 0.9, delay: i * 0.2,
        scrollTrigger: { trigger: card, start: 'top 85%', toggleActions: 'play none none reverse' }
    });
});

gsap.utils.toArray('.nav-btn').forEach((btn, i) => {
    gsap.to(btn, {
        opacity: i === 0 ? 1 : 0.4,
        y: 0, duration: 0.9, delay: i * 0.2,
        scrollTrigger: { trigger: btn, start: 'top 85%', toggleActions: 'play none none reverse' }
    });
});

gsap.to('.orb-1', { y: -80, scrollTrigger: { scrub: 1 } });
gsap.to('.orb-2', { y: 80, scrollTrigger: { scrub: 1 } });
</script>
</body>
</html>
"""

html(page, height=1400)   

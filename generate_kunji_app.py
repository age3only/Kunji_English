# -*- coding: utf-8 -*-
"""
Generator for Kunji's English Racing Adventure Web Application.
Embeds all 239 Malayalam dialogues, Hamster & Car racing UI,
personalized Kunji appreciations, persistent per-topic progress bars,
and dedicated Malayalam Voice TTS for Quiz questions.
"""

import json
import os

with open("kunji_spoken_english_malayalam.json", "r", encoding="utf-8") as f:
    chapters_data = json.load(f)

json_data_str = json.dumps(chapters_data, ensure_ascii=False)

html_template = """<!DOCTYPE html>
<html lang="ml">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1, user-scalable=no, viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Kunji English">
<title>കുഞ്ഞിയുടെ ഇംഗ്ലീഷ് റേസിംഗ് സാഹസിക യാത്ര! 🐹🏎️</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700;800;900&family=Fredoka+One&family=Noto+Sans+Malayalam:wght@500;600;700;800;900&family=Quicksand:wght@600;700;800&display=swap" rel="stylesheet">
<style>
  :root {
    --track-navy: #0D1B2A;
    --track-slate: #1B263B;
    --card-dark: #24344D;
    --turbo-orange: #FF6D00;
    --turbo-yellow: #FFD600;
    --speed-red: #FF3D00;
    --electric-blue: #00B0FF;
    --hamster-gold: #FFB300;
    --hamster-cream: #FFFDF5;
    --asphalt-gray: #415A77;
    --track-border: #778DA9;
    --go-green: #00E676;
    --text-white: #FFFFFF;
    --text-sub: #E0E1DD;
    --shadow-turbo: rgba(255, 109, 0, 0.35);
  }

  * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }

  html, body {
    margin: 0; padding: 0; height: 100%;
    font-family: 'Quicksand', 'Noto Sans Malayalam', sans-serif;
    background: radial-gradient(circle at 10% 15%, #1F314D 0%, transparent 40%),
                radial-gradient(circle at 90% 85%, #2C1810 0%, transparent 45%),
                linear-gradient(180deg, #0B131F 0%, #111D2E 50%, #0D1B2A 100%);
    color: var(--text-white);
    overflow-x: hidden;
    -webkit-user-select: none;
    user-select: none;
  }

  /* Floating animated car/hamster sparkles */
  .bg-sparkles {
    position: fixed; inset: 0; pointer-events: none; z-index: 0; overflow: hidden;
  }
  .bg-sparkle {
    position: absolute; font-size: 20px; opacity: 0.25;
    animation: floatRacer 5s ease-in-out infinite alternate;
  }
  @keyframes floatRacer {
    0% { transform: translateY(0px) rotate(0deg) scale(0.9); opacity: 0.2; }
    50% { transform: translateY(-20px) rotate(10deg) scale(1.1); opacity: 0.45; }
    100% { transform: translateY(10px) rotate(-8deg) scale(0.95); opacity: 0.3; }
  }

  h1, h2, h3, .display { font-family: 'Baloo 2', 'Noto Sans Malayalam', 'Fredoka One', sans-serif; }
  button { font-family: 'Quicksand', 'Noto Sans Malayalam', sans-serif; cursor: pointer; border: none; }
  .screen { min-height: 100vh; padding: 16px 16px 64px; position: relative; max-width: 660px; margin: 0 auto; z-index: 1; }
  .hidden { display: none !important; }

  /* ---------- TOP BAR ---------- */
  .topbar {
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 16px; gap: 8px;
  }
  .racer-badge {
    background: linear-gradient(135deg, #FF6D00, #FF3D00);
    color: #FFF; padding: 7px 16px; border-radius: 999px; font-weight: 900;
    font-size: 14px; letter-spacing: 0.5px;
    box-shadow: 0 4px 12px rgba(255, 61, 0, 0.4), inset 0 1px 0 rgba(255,255,255,0.4);
    display: flex; align-items: center; gap: 6px; cursor: pointer;
    border: 2px solid #FFA726; transition: transform .12s ease;
  }
  .racer-badge:active { transform: scale(0.95); }

  .topbar-actions { display: flex; align-items: center; gap: 8px; }

  .voice-btn, .speed-btn {
    background: #1B263B; border-radius: 999px; padding: 7px 14px;
    font-weight: 800; font-size: 13px; border: 2px solid #415A77;
    box-shadow: 0 3px 8px rgba(0,0,0,0.3);
    display: flex; align-items: center; gap: 5px; color: #E0E1DD;
    transition: all .12s ease;
  }
  .voice-btn:active, .speed-btn:active { transform: scale(0.95); }

  .stars-pill {
    background: linear-gradient(135deg, #24344D, #1B263B);
    border-radius: 999px; padding: 7px 16px;
    font-weight: 900; font-size: 14.5px;
    border: 2px solid #FFB300;
    box-shadow: 0 4px 12px rgba(255, 179, 0, 0.3);
    display: flex; align-items: center; gap: 6px; color: #FFD54F;
  }

  .backbtn {
    background: #1B263B; width: 44px; height: 44px; border-radius: 50%;
    font-size: 20px; border: 2px solid #415A77;
    box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    display: flex; align-items: center; justify-content: center;
    color: #FFF; font-weight: 900; transition: transform .12s ease;
  }
  .backbtn:active { transform: scale(0.92); }

  /* ---------- HERO SECTION ---------- */
  .hero { text-align: center; margin-bottom: 18px; position: relative; }
  .mascot-strip {
    display: flex; align-items: center; justify-content: center; gap: 14px;
    margin-bottom: 8px;
  }
  .mascot-icon {
    font-size: 42px; display: inline-block; filter: drop-shadow(0 4px 8px rgba(0,0,0,0.4));
  }
  .mascot-icon.car { animation: revCar 1.8s ease-in-out infinite alternate; }
  .mascot-icon.hamster { animation: bounceHamster 1.4s ease-in-out infinite alternate; }
  .mascot-icon.flag { animation: waveFlag 2s ease-in-out infinite alternate; }

  @keyframes revCar {
    0% { transform: translateY(0) scale(1); }
    100% { transform: translateY(-6px) scale(1.08) rotate(-3deg); }
  }
  @keyframes bounceHamster {
    0% { transform: translateY(0) scale(1); }
    100% { transform: translateY(-8px) scale(1.1) rotate(4deg); }
  }
  @keyframes waveFlag {
    0% { transform: rotate(-5deg); }
    100% { transform: rotate(10deg); }
  }

  .hero-tag {
    display: inline-block;
    background: rgba(255, 109, 0, 0.2);
    border: 1.5px solid var(--turbo-orange);
    color: #FFB74D; font-weight: 800; font-size: 13px;
    padding: 4px 14px; border-radius: 999px; margin-bottom: 8px;
    letter-spacing: 0.5px;
  }

  .hero h1 {
    margin: 2px 0 6px; font-size: 26px; line-height: 1.25;
    background: linear-gradient(135deg, #FFFFFF 30%, #FFE082 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    text-shadow: 0 4px 12px rgba(0,0,0,0.4);
  }
  .hero p {
    margin: 0; font-size: 14px; color: #B0BEC5; font-weight: 700;
  }

  /* ---------- SPEEDOMETER OVERALL PROGRESS DASHBOARD ---------- */
  .dashboard-card {
    background: linear-gradient(145deg, #1B263B, #152238);
    border-radius: 22px; padding: 18px 20px;
    border: 2px solid #415A77;
    box-shadow: 0 8px 24px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.1);
    margin-bottom: 20px; position: relative; overflow: hidden;
  }
  .dashboard-card::after {
    content: ''; position: absolute; top: -40px; right: -40px;
    width: 120px; height: 120px;
    background: radial-gradient(circle, rgba(255,109,0,0.2) 0%, transparent 70%);
    pointer-events: none;
  }
  .dash-header {
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 12px;
  }
  .dash-title {
    font-weight: 900; font-size: 15px; color: #FFF;
    display: flex; align-items: center; gap: 8px;
  }
  .dash-percent {
    font-family: 'Fredoka One', 'Baloo 2', sans-serif;
    font-size: 22px; color: var(--turbo-yellow);
    text-shadow: 0 2px 8px rgba(255, 214, 0, 0.4);
  }

  /* Race Track Progress Bar */
  .track-bar-bg {
    background: #0B131F; border-radius: 999px; height: 18px;
    position: relative; overflow: visible; border: 1.5px solid #415A77;
    margin-bottom: 14px; box-shadow: inset 0 2px 4px rgba(0,0,0,0.5);
  }
  .track-bar-fill {
    background: linear-gradient(90deg, #FF3D00, #FF9100, #FFD600);
    height: 100%; border-radius: 999px; width: 0%;
    transition: width 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
    position: relative;
    box-shadow: 0 0 12px rgba(255, 145, 0, 0.6);
  }
  .track-racer-thumb {
    position: absolute; right: -12px; top: -8px; font-size: 22px;
    filter: drop-shadow(0 2px 4px rgba(0,0,0,0.6));
    animation: carWiggle 0.8s ease-in-out infinite alternate;
  }
  @keyframes carWiggle {
    0% { transform: translateY(0); }
    100% { transform: translateY(-3px) rotate(-4deg); }
  }

  .dash-stats-row {
    display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px;
    background: rgba(11, 19, 31, 0.6); border-radius: 14px;
    padding: 10px; text-align: center; border: 1px solid rgba(255,255,255,0.06);
  }
  .stat-col span { display: block; font-size: 11px; color: #90A4AE; font-weight: 700; margin-bottom: 2px; }
  .stat-col strong { font-size: 15px; font-weight: 900; color: #FFF; }

  /* ---------- CHAPTER LIST ---------- */
  .chapter-list { display: flex; flex-direction: column; gap: 14px; }
  .chapter-card {
    background: linear-gradient(135deg, #1B263B, #162234);
    border-radius: 20px; padding: 16px 18px;
    border: 2px solid #2B3D56;
    box-shadow: 0 6px 18px rgba(0,0,0,0.3);
    cursor: pointer; transition: all .16s ease;
    position: relative; overflow: hidden;
  }
  .chapter-card:hover { transform: translateY(-2px); border-color: var(--turbo-orange); }
  .chapter-card:active { transform: scale(0.98); }

  .ch-top-row {
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 8px;
  }
  .ch-badge-title { display: flex; align-items: center; gap: 12px; }
  .ch-badge {
    font-size: 30px; width: 50px; height: 50px; border-radius: 14px;
    background: rgba(255,255,255,0.07); display: flex; align-items: center;
    justify-content: center; border: 1.5px solid rgba(255,255,255,0.12);
    box-shadow: 0 4px 10px rgba(0,0,0,0.3);
  }
  .ch-info h3 {
    margin: 0; font-size: 17px; font-weight: 800; color: #FFF; line-height: 1.25;
  }
  .ch-info .ch-en-title {
    font-size: 12.5px; color: #90A4AE; font-weight: 700;
  }
  .ch-stars-pill {
    background: rgba(0,0,0,0.4); border-radius: 999px; padding: 5px 12px;
    font-size: 12px; font-weight: 900; color: #FFD54F;
    border: 1px solid rgba(255, 213, 79, 0.3);
  }

  .ch-sub-text {
    font-size: 12px; color: #B0BEC5; margin: 4px 0 10px; font-weight: 600; line-height: 1.35;
  }

  /* Chapter Level Topic Progress Mini Bar */
  .ch-progress-wrap {
    display: flex; align-items: center; justify-content: space-between; gap: 10px;
  }
  .ch-progress-bar {
    flex: 1; background: #0B131F; border-radius: 999px; height: 8px;
    overflow: hidden; border: 1px solid rgba(255,255,255,0.08);
  }
  .ch-progress-fill {
    height: 100%; border-radius: 999px;
    background: linear-gradient(90deg, #00B0FF, #00E676);
    transition: width 0.4s ease;
  }
  .ch-progress-label {
    font-size: 11.5px; font-weight: 800; color: #80D8FF; white-space: nowrap;
  }

  /* ---------- STATION / TOPICS SCREEN ---------- */
  .station-hero {
    text-align: center; margin-bottom: 18px;
    background: linear-gradient(145deg, #1B263B, #152238);
    border-radius: 24px; padding: 20px 16px;
    border: 2px solid #415A77; box-shadow: 0 8px 24px rgba(0,0,0,0.4);
  }
  .station-badge {
    font-size: 54px; display: inline-block; margin-bottom: 6px;
    filter: drop-shadow(0 4px 10px rgba(0,0,0,0.5));
  }
  .station-hero h2 {
    margin: 0 0 2px; font-size: 22px; font-weight: 900; color: #FFF;
  }
  .station-hero .station-en-sub {
    font-size: 13px; color: #90A4AE; font-weight: 700; margin-bottom: 12px;
  }
  .station-stars-row {
    display: inline-flex; align-items: center; gap: 4px;
    background: rgba(11, 19, 31, 0.7); padding: 6px 16px; border-radius: 999px;
    border: 1.5px solid rgba(255, 214, 0, 0.4); color: #FFD600;
    font-size: 13.5px; font-weight: 900;
  }

  /* Chapter Master Quiz Button */
  .grand-prix-quiz-btn {
    width: 100%; margin-bottom: 18px;
    background: linear-gradient(135deg, #FF6D00, #FF3D00);
    color: #FFF; padding: 15px; border-radius: 18px;
    font-weight: 900; font-size: 16px;
    box-shadow: 0 6px 0 #BF360C, 0 10px 20px rgba(255, 61, 0, 0.35);
    display: flex; align-items: center; justify-content: center; gap: 10px;
    border: 2px solid #FFA726; transition: transform .12s ease;
  }
  .grand-prix-quiz-btn:active { transform: translateY(3px); box-shadow: 0 3px 0 #BF360C; }

  .topics-header-title {
    font-size: 16px; font-weight: 900; color: #FFD54F;
    margin: 0 0 12px 4px; display: flex; align-items: center; gap: 8px;
  }

  /* TOPIC CARDS WITH PERSISTENT PROGRESS BAR */
  .topic-cards-list { display: flex; flex-direction: column; gap: 14px; }
  .topic-card {
    background: linear-gradient(135deg, #1B263B, #162030);
    border-radius: 20px; padding: 16px 18px;
    border: 2px solid #334863;
    box-shadow: 0 6px 18px rgba(0,0,0,0.3);
    position: relative; overflow: hidden;
  }
  .topic-card.completed { border-color: #00E676; }

  .topic-card-top {
    display: flex; align-items: flex-start; justify-content: space-between;
    margin-bottom: 10px; gap: 10px;
  }
  .topic-card-titles h4 {
    margin: 0 0 3px; font-size: 16px; font-weight: 800; color: #FFF; line-height: 1.3;
  }
  .topic-card-titles .topic-en-name {
    font-size: 12px; color: #90A4AE; font-weight: 700;
  }
  .topic-status-badge {
    padding: 4px 10px; border-radius: 999px; font-size: 11px; font-weight: 800;
    white-space: nowrap; display: flex; align-items: center; gap: 4px;
  }
  .status-not-started { background: rgba(255,255,255,0.1); color: #CFD8DC; border: 1px solid rgba(255,255,255,0.15); }
  .status-in-progress { background: rgba(255, 109, 0, 0.2); color: #FFB74D; border: 1px solid #FF6D00; }
  .status-completed { background: rgba(0, 230, 118, 0.2); color: #B9F6CA; border: 1px solid #00E676; }

  /* TOPIC PROGRESS BAR COMPONENT */
  .topic-progress-wrap { margin-bottom: 12px; }
  .topic-progress-info {
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 6px; font-size: 12px; font-weight: 800;
  }
  .topic-progress-items { color: #80D8FF; }
  .topic-progress-pct { color: var(--turbo-yellow); }

  .topic-bar-track {
    background: #0B131F; border-radius: 999px; height: 14px;
    border: 1.5px solid #415A77; position: relative; overflow: visible;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.5);
  }
  .topic-bar-fill {
    height: 100%; border-radius: 999px;
    background: linear-gradient(90deg, #FF6D00, #FFD600);
    width: 0%; transition: width 0.4s ease; position: relative;
    box-shadow: 0 0 10px rgba(255, 109, 0, 0.5);
  }
  .topic-bar-thumb {
    position: absolute; right: -8px; top: -6px; font-size: 17px;
    filter: drop-shadow(0 2px 3px rgba(0,0,0,0.6));
  }

  .topic-card-actions {
    display: grid; grid-template-columns: 1fr 1fr; gap: 8px;
  }
  .topic-btn {
    padding: 10px 14px; border-radius: 14px; font-weight: 800; font-size: 13px;
    display: flex; align-items: center; justify-content: center; gap: 6px;
    transition: transform .12s ease;
  }
  .topic-btn.learn {
    background: linear-gradient(135deg, #0288D1, #01579B); color: #FFF;
    box-shadow: 0 4px 0 #013A6B; border: 1.5px solid #29B6F6;
  }
  .topic-btn.quiz {
    background: linear-gradient(135deg, #FFB300, #FF8F00); color: #3E2723;
    box-shadow: 0 4px 0 #C67100; border: 1.5px solid #FFE082;
  }
  .topic-btn:active { transform: translateY(2px); }

  /* ---------- FLASHCARD LEARN SCREEN ---------- */
  .card-wrap { margin-top: 4px; }
  .flashcard {
    background: linear-gradient(145deg, #1B263B, #152238);
    border-radius: 28px; padding: 22px 18px;
    border: 2.5px solid #415A77;
    box-shadow: 0 8px 30px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.1);
  }
  .card-topic-tag {
    display: inline-block; background: rgba(0, 176, 255, 0.15);
    border: 1.5px solid #00B0FF; color: #80D8FF; font-weight: 800;
    font-size: 12.5px; padding: 5px 14px; border-radius: 999px; margin-bottom: 14px;
  }

  /* Dialogue Bubbles */
  .bubble {
    border-radius: 20px; padding: 14px 16px; margin-bottom: 14px;
    cursor: pointer; transition: transform .12s ease;
  }
  .bubble:active { transform: scale(0.98); }

  .bubble.speaker-a {
    background: linear-gradient(135deg, #2A1F17, #3D2B1B);
    border: 2px solid #FFA000;
  }
  .bubble.speaker-b {
    background: linear-gradient(135deg, #152A38, #1C3B4E);
    border: 2px solid #00B0FF;
  }

  .bubble-speaker {
    display: flex; align-items: center; justify-content: space-between;
    font-size: 12px; font-weight: 800; margin-bottom: 6px;
  }
  .speaker-a .bubble-speaker { color: #FFD54F; }
  .speaker-b .bubble-speaker { color: #80D8FF; }

  .speaker-sound-icon {
    font-size: 11.5px; background: rgba(255,255,255,0.12);
    padding: 3px 8px; border-radius: 999px;
  }

  .en-text {
    font-family: 'Baloo 2', cursive, sans-serif; font-weight: 800; font-size: 19px;
    line-height: 1.3; margin-bottom: 6px; color: #FFF;
  }
  .ml-text-row {
    display: flex; align-items: center; justify-content: space-between; gap: 8px;
  }
  .ml-text {
    font-family: 'Noto Sans Malayalam', sans-serif;
    font-weight: 700; font-size: 14px; color: #FFE082;
    background: rgba(0,0,0,0.35); padding: 6px 12px; border-radius: 12px;
    display: inline-block; line-height: 1.4; border: 1px dashed rgba(255,255,255,0.2);
    flex: 1;
  }
  .ml-sound-mini-btn {
    background: rgba(255, 179, 0, 0.2); border: 1px solid #FFB300;
    color: #FFD54F; border-radius: 50%; width: 32px; height: 32px;
    display: flex; align-items: center; justify-content: center;
    font-size: 13px; cursor: pointer; flex-shrink: 0;
  }

  .card-note {
    background: rgba(255, 179, 0, 0.12); border-left: 4px solid #FFB300;
    padding: 10px 12px; border-radius: 12px; font-size: 12.5px; font-weight: 700;
    color: #FFE082; margin: 10px 0; line-height: 1.4;
  }

  .card-audio-row {
    display: flex; justify-content: center; gap: 10px; margin-top: 14px;
  }
  .listen-all-btn {
    background: linear-gradient(135deg, #FF6D00, #FF3D00); color: #FFF;
    border-radius: 999px; padding: 11px 24px; font-weight: 900; font-size: 14.5px;
    box-shadow: 0 4px 0 #BF360C, 0 6px 16px rgba(255, 61, 0, 0.3);
    display: inline-flex; align-items: center; gap: 8px;
    border: 1.5px solid #FFA726; transition: transform .12s ease;
  }
  .listen-all-btn:active { transform: translateY(2px); box-shadow: 0 2px 0 #BF360C; }

  .card-nav {
    display: flex; justify-content: space-between; align-items: center;
    margin-top: 18px; gap: 10px;
  }
  .nav-btn {
    background: #1B263B; width: 50px; height: 50px; border-radius: 50%;
    font-size: 20px; border: 2px solid #415A77; box-shadow: 0 4px 0 #2A3B50;
    display: flex; align-items: center; justify-content: center;
    color: #FFF; font-weight: 900;
  }
  .nav-btn:disabled { opacity: 0.35; pointer-events: none; }

  .mark-mastered-btn {
    flex: 1; background: linear-gradient(135deg, #00E676, #00B248); color: #052B14;
    font-weight: 900; font-size: 15.5px; padding: 14px; border-radius: 18px;
    box-shadow: 0 4px 0 #008132, 0 6px 16px rgba(0, 230, 118, 0.3);
    text-align: center; border: 1.5px solid #B9F6CA;
    display: flex; align-items: center; justify-content: center; gap: 6px;
  }
  .mark-mastered-btn:active { transform: translateY(2px); box-shadow: 0 2px 0 #008132; }

  /* ---------- QUIZ SCREEN & KUNJI APPRECIATION ---------- */
  .quiz-wrap { margin-top: 6px; }
  .quiz-top {
    display: flex; justify-content: space-between; align-items: center;
    margin-bottom: 14px;
  }
  .quiz-progress-txt {
    font-weight: 900; font-size: 14px; color: #80D8FF;
    display: flex; align-items: center; gap: 6px;
  }
  .quiz-score-pill {
    background: rgba(255, 214, 0, 0.15); border: 1.5px solid #FFD600;
    color: #FFD600; border-radius: 999px; padding: 4px 12px;
    font-size: 13px; font-weight: 900;
  }

  .quiz-question-box {
    background: linear-gradient(145deg, #1B263B, #152238);
    border-radius: 26px; padding: 22px 18px; text-align: center;
    border: 2.5px solid #415A77;
    box-shadow: 0 8px 24px rgba(0,0,0,0.4); margin-bottom: 16px;
  }
  .quiz-kicker {
    font-weight: 900; font-size: 13px; color: #FFB74D;
    background: rgba(255, 109, 0, 0.2); display: inline-block;
    padding: 5px 14px; border-radius: 999px; margin-bottom: 12px;
    border: 1px solid rgba(255, 109, 0, 0.4);
  }
  .quiz-qtext {
    font-family: 'Noto Sans Malayalam', 'Baloo 2', sans-serif;
    font-weight: 800; font-size: 21px;
    color: #FFF; line-height: 1.35; margin-bottom: 10px;
  }
  .quiz-subhint {
    font-size: 13px; color: #90A4AE; font-weight: 700; margin-bottom: 8px;
  }
  .quiz-listen-btn {
    display: inline-flex; align-items: center; gap: 8px;
    background: linear-gradient(135deg, #FF6D00, #FF3D00);
    border: 1.5px solid #FFA726; color: #FFF;
    padding: 8px 20px; border-radius: 999px; font-size: 14px; font-weight: 900;
    cursor: pointer; margin-top: 8px; box-shadow: 0 3px 8px rgba(255, 61, 0, 0.35);
    transition: transform .12s ease;
  }
  .quiz-listen-btn:active { transform: scale(0.95); }

  /* Multiple Choice Options */
  .options-list { display: flex; flex-direction: column; gap: 10px; }
  .quiz-option {
    background: #1B263B; border-radius: 18px; padding: 15px 18px;
    font-weight: 800; font-size: 15px; text-align: left;
    border: 2px solid #334863; box-shadow: 0 4px 0 #202D42;
    color: #FFF; line-height: 1.35; transition: all .12s ease;
  }
  .quiz-option:active { transform: translateY(2px); }
  .quiz-option.correct {
    background: #00E676 !important; color: #003314 !important;
    border-color: #B9F6CA !important; box-shadow: 0 4px 0 #008132 !important;
  }
  .quiz-option.wrong {
    background: #FF3D00 !important; color: #FFF !important;
    border-color: #FF8A80 !important; box-shadow: 0 4px 0 #B71C1C !important;
  }

  /* ---------- KUNJI APPRECIATION BANNER (POPUP CELEBRATION) ---------- */
  .appreciation-banner {
    position: fixed; top: 18%; left: 50%; transform: translateX(-50%) scale(0);
    background: linear-gradient(135deg, #FF6D00, #FF3D00);
    border: 3px solid #FFD600; border-radius: 24px;
    padding: 16px 24px; text-align: center;
    box-shadow: 0 12px 36px rgba(0,0,0,0.6), 0 0 24px rgba(255, 109, 0, 0.8);
    z-index: 100; pointer-events: none; transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    max-width: 90%;
  }
  .appreciation-banner.show {
    transform: translateX(-50%) scale(1);
  }
  .apprec-emoji { font-size: 36px; margin-bottom: 4px; display: block; animation: carWiggle 0.6s infinite alternate; }
  .apprec-title {
    font-family: 'Fredoka One', 'Baloo 2', sans-serif;
    font-size: 20px; color: #FFF; margin: 0 0 2px;
    text-shadow: 0 2px 6px rgba(0,0,0,0.4);
  }
  .apprec-sub {
    font-family: 'Noto Sans Malayalam', sans-serif;
    font-size: 14px; font-weight: 800; color: #FFD54F; margin: 0;
  }

  /* Result Screen */
  .result-wrap {
    text-align: center; padding: 30px 16px;
    background: linear-gradient(145deg, #1B263B, #152238);
    border-radius: 30px; border: 2.5px solid #FFB300;
    box-shadow: 0 10px 36px rgba(0,0,0,0.5);
  }
  .result-big-mascot { font-size: 64px; display: inline-block; margin-bottom: 12px; }
  .result-wrap h2 { font-size: 24px; color: #FFF; margin: 0 0 6px; }
  .result-wrap p { font-size: 14px; color: #B0BEC5; margin: 0 0 16px; }
  .result-score-badge {
    background: rgba(255, 214, 0, 0.15); border: 2px solid #FFD600;
    color: #FFD600; display: inline-block; padding: 8px 24px;
    border-radius: 999px; font-size: 18px; font-weight: 900; margin-bottom: 20px;
  }
  .result-buttons { display: flex; flex-direction: column; gap: 10px; max-width: 320px; margin: 0 auto; }
  .result-btn {
    padding: 14px; border-radius: 16px; font-size: 15px; font-weight: 900;
    display: flex; align-items: center; justify-content: center; gap: 8px;
  }
  .result-btn.retry {
    background: linear-gradient(135deg, #FF6D00, #FF3D00); color: #FFF;
    border: 1.5px solid #FFA726; box-shadow: 0 4px 0 #BF360C;
  }
  .result-btn.home {
    background: #1B263B; color: #80D8FF;
    border: 2px solid #00B0FF; box-shadow: 0 4px 0 #005B9F;
  }

  /* Modal Dialog for Voice & Settings */
  .modal-overlay {
    position: fixed; inset: 0; background: rgba(0,0,0,0.75);
    backdrop-filter: blur(4px); z-index: 200;
    display: flex; align-items: center; justify-content: center; padding: 20px;
  }
  .modal-card {
    background: #1B263B; border-radius: 26px; padding: 22px 20px;
    width: 100%; max-width: 440px; border: 2.5px solid #415A77;
    box-shadow: 0 16px 40px rgba(0,0,0,0.6);
  }
  .modal-header {
    display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px;
  }
  .modal-header h3 { margin: 0; font-size: 17px; color: #FFF; }
  .modal-close {
    background: #0B131F; border-radius: 50%; width: 34px; height: 34px;
    display: flex; align-items: center; justify-content: center;
    color: #FFF; font-size: 16px; border: 1.5px solid #415A77;
  }
  .setting-item { margin-bottom: 14px; }
  .setting-label { display: block; font-size: 12.5px; font-weight: 800; color: #B0BEC5; margin-bottom: 6px; }
  .setting-select {
    width: 100%; background: #0B131F; color: #FFF; border: 1.5px solid #415A77;
    padding: 10px 14px; border-radius: 12px; font-size: 14px; font-family: inherit;
  }

  /* Confetti canvas */
  .confetti-canvas {
    position: fixed; inset: 0; pointer-events: none; z-index: 99;
  }
</style>
</head>
<body>

<canvas id="confettiCanvas" class="confetti-canvas"></canvas>

<!-- Floating Sparkles -->
<div class="bg-sparkles">
  <span class="bg-sparkle" style="top:8%; left:6%;">🏎️</span>
  <span class="bg-sparkle" style="top:18%; right:8%;">🐹</span>
  <span class="bg-sparkle" style="top:42%; left:4%;">🏁</span>
  <span class="bg-sparkle" style="top:60%; right:6%;">🚗</span>
  <span class="bg-sparkle" style="top:78%; left:8%;">⚡</span>
  <span class="bg-sparkle" style="top:92%; right:10%;">🏆</span>
</div>

<!-- KUNJI APPRECIATION BANNER -->
<div class="appreciation-banner" id="appreciationBanner">
  <span class="apprec-emoji" id="apprecEmoji">🏎️💨</span>
  <h3 class="apprec-title" id="apprecTitle">Good job Kunji!</h3>
  <p class="apprec-sub" id="apprecSub">നന്നായി ചെയ്തു കുഞ്ഞീ! 🐹✨</p>
</div>

<!-- ===================== HOME SCREEN ===================== -->
<section class="screen" id="screen-home">
  <div class="topbar">
    <div class="racer-badge" id="kunjiBadge" onclick="handleKunjiBadgeClick()" title="🏎️ സൂപ്പർ കുഞ്ഞി (Kunji)">
      🏎️ കുഞ്ഞി (Kunji) 🐹
    </div>
    <div class="topbar-actions">
      <button class="speed-btn" id="speedToggleBtn" onclick="toggleSpeed()" title="ശബ്ദത്തിന്റെ വേഗത മാറ്റുക">
        🏎️ 1x
      </button>
      <button class="voice-btn" onclick="openVoiceModal()" title="ശബ്ദം തിരഞ്ഞെടുക്കുക">
        🎙️ ശബ്ദം
      </button>
      <div class="stars-pill">
        ⭐ <span id="totalStars">0</span> / 110
      </div>
    </div>
  </div>

  <div class="hero">
    <div class="mascot-strip">
      <span class="mascot-icon car">🏎️</span>
      <span class="mascot-icon hamster">🐹</span>
      <span class="mascot-icon flag">🏁</span>
      <span class="mascot-icon car">🚗</span>
    </div>
    <div class="hero-tag">🏎️ Kunji's English Racing Edition 🐹</div>
    <h1>കുഞ്ഞിയുടെ ഇംഗ്ലീഷ് റേസിംഗ് യാത്ര!</h1>
    <p>ഹാംസ്റ്ററിനൊപ്പം അടിപൊളി ഇംഗ്ലീഷ് സംസാരിക്കാൻ പഠിക്കാം! 🏁💨</p>
  </div>

  <!-- OVERALL PROGRESS SPEEDOMETER -->
  <div class="dashboard-card">
    <div class="dash-header">
      <div class="dash-title">
        <span>🏆 കുഞ്ഞിയുടെ മൊത്തം സ്പീഡോമീറ്റർ</span>
      </div>
      <div class="dash-percent" id="overallPercent">0%</div>
    </div>

    <!-- Interactive Track Progress Bar -->
    <div class="track-bar-bg">
      <div class="track-bar-fill" id="overallTrackFill">
        <span class="track-racer-thumb">🏎️</span>
      </div>
    </div>

    <div class="dash-stats-row">
      <div class="stat-col">
        <span>⭐ നക്ഷത്രങ്ങൾ</span>
        <strong id="dashStarsLabel">0 / 110</strong>
      </div>
      <div class="stat-col">
        <span>🏁 ടോപ്പിക്കുകൾ</span>
        <strong id="dashTopicsLabel">0 / 51</strong>
      </div>
      <div class="stat-col">
        <span>📖 വാക്യങ്ങൾ</span>
        <strong id="dashItemsLabel">0 / 239</strong>
      </div>
    </div>
  </div>

  <!-- Chapters List -->
  <div class="chapter-list" id="chaptersList"></div>
</section>

<!-- ===================== CHAPTER / STATION SCREEN ===================== -->
<section class="screen hidden" id="screen-station">
  <div class="topbar">
    <button class="backbtn" onclick="goHome()">←</button>
    <div class="racer-badge" onclick="handleKunjiBadgeClick()">🏎️ കുഞ്ഞി 🐹</div>
    <div class="stars-pill">⭐ <span id="stationChapterStars">0</span> / 10</div>
  </div>

  <div class="station-hero">
    <span class="station-badge" id="stBadge">🏎️</span>
    <h2 id="stTitleMl">നല്ല ശീലങ്ങൾ</h2>
    <div class="station-en-sub" id="stTitleEn">Good Manners</div>
    <div class="station-stars-row" id="stStarsRow">⭐⭐⭐⭐⭐☆☆☆☆☆ (0/10)</div>
  </div>

  <!-- Grand Prix Chapter Quiz Button -->
  <button class="grand-prix-quiz-btn" onclick="startChapterQuiz()">
    <span>🏁 ചാപ്റ്റർ ഗ്രാൻഡ് പ്രീ ക്വിസ് (മലയാളത്തിൽ ചോദ്യം 🎙️)</span>
  </button>

  <div class="topics-header-title">
    <span>🏁 എല്ലാ ടോപ്പിക്കുകളുടെയും പുരോഗതി (Topic Progress):</span>
  </div>

  <!-- List of all topics with individual progress bars -->
  <div class="topic-cards-list" id="stationTopicsList"></div>
</section>

<!-- ===================== FLASHCARD LEARN SCREEN ===================== -->
<section class="screen hidden" id="screen-learn">
  <div class="topbar">
    <button class="backbtn" onclick="showStation()">←</button>
    <div class="quiz-progress-txt" id="learnCounterTxt">വാക്യം 1 / 5 🐹</div>
    <div style="display:flex; gap:6px;">
      <button class="speed-btn" onclick="toggleSpeed()" id="learnSpeedBtn">🏎️ 1x</button>
      <button class="backbtn" onclick="speakCurrentDialogue()" title="മുഴുവൻ കേൾക്കുക">🔊</button>
    </div>
  </div>

  <div class="card-wrap">
    <!-- Topic Live Progress Bar at top of flashcard -->
    <div class="topic-progress-wrap" style="margin-bottom:14px;">
      <div class="topic-progress-info">
        <span class="topic-progress-items" id="learnTopicName">ടോപ്പിക്</span>
        <span class="topic-progress-pct" id="learnTopicPct">0%</span>
      </div>
      <div class="topic-bar-track">
        <div class="topic-bar-fill" id="learnTopicBarFill">
          <span class="topic-bar-thumb">🐹</span>
        </div>
      </div>
    </div>

    <div class="flashcard">
      <div class="card-topic-tag" id="cardTopicTag">🏁 ടോപ്പിക്</div>

      <!-- Speaker A (Hamster Buddy) -->
      <div class="bubble speaker-a">
        <div class="bubble-speaker" onclick="speakSpeakerA()">
          <span>🐹 ഹാംസ്റ്റർ ചങ്ങാതി (Speaker A)</span>
          <span class="speaker-sound-icon">🔊 ഇംഗ്ലീഷ് കേൾക്കാം</span>
        </div>
        <div class="en-text" id="cardTextAEn" onclick="speakSpeakerA()">Good morning! How are you?</div>
        <div class="ml-text-row">
          <div class="ml-text" id="cardTextAMl">സുപ്രഭാതം! സുഖമാണോ?</div>
          <button class="ml-sound-mini-btn" onclick="speakMalayalamCardA()" title="മലയാളത്തിൽ കേൾക്കാം">🎙️</button>
        </div>
      </div>

      <!-- Speaker B (Super Kunji) -->
      <div class="bubble speaker-b">
        <div class="bubble-speaker" onclick="speakSpeakerB()">
          <span>🏎️ സൂപ്പർ കുഞ്ഞി (Speaker B)</span>
          <span class="speaker-sound-icon">🔊 ഇംഗ്ലീഷ് കേൾക്കാം</span>
        </div>
        <div class="en-text" id="cardTextBEn" onclick="speakSpeakerB()">I’m fine, thanks. How are you?</div>
        <div class="ml-text-row">
          <div class="ml-text" id="cardTextBMl">എനിക്ക് സുഖമാണ്, നന്ദി. നിനക്കോ?</div>
          <button class="ml-sound-mini-btn" onclick="speakMalayalamCardB()" title="മലയാളത്തിൽ കേൾക്കാം">🎙️</button>
        </div>
      </div>

      <!-- Note / Usage Tip -->
      <div class="card-note" id="cardNoteBox">
        💡 <strong>കുഞ്ഞിക്കുള്ള ടിപ്പ്:</strong> <span id="cardNoteText"></span>
      </div>

      <div class="card-audio-row">
        <button class="listen-all-btn" onclick="speakCurrentDialogue()">
          <span>🔊 സംഭാഷണം മുഴുവൻ കേൾക്കാം ✨</span>
        </button>
      </div>
    </div>

    <!-- Navigation -->
    <div class="card-nav">
      <button class="nav-btn" id="prevCardBtn" onclick="prevCard()">←</button>
      <button class="mark-mastered-btn" onclick="markCardMastered()">
        <span>🌟 പഠിച്ചു! അടുത്തതിലേക്ക് 🏎️ →</span>
      </button>
      <button class="nav-btn" id="nextCardBtn" onclick="nextCard()">→</button>
    </div>
  </div>
</section>

<!-- ===================== QUIZ SCREEN ===================== -->
<section class="screen hidden" id="screen-quiz">
  <div class="topbar">
    <button class="backbtn" onclick="showStation()">←</button>
    <div class="racer-badge" onclick="handleKunjiBadgeClick()">🏎️ കുഞ്ഞി 🐹</div>
    <div class="quiz-score-pill" id="quizScorePill">0 / 10 ⭐</div>
  </div>

  <div class="quiz-wrap">
    <div class="quiz-top">
      <div class="quiz-progress-txt" id="quizProgressTxt">ചോദ്യം 1 / 10 🏁</div>
      <div class="stars-pill" style="padding:4px 12px; font-size:13px;">
        ⭐ സ്കോർ: <span id="quizCorrectCount">0</span>
      </div>
    </div>

    <div class="quiz-question-box">
      <div class="quiz-kicker" id="quizKicker">🎯 ഇത് ഇംഗ്ലീഷിൽ എങ്ങനെ പറയും കുഞ്ഞീ?</div>
      <div class="quiz-qtext" id="quizQText">സുപ്രഭാതം! സുഖമാണോ?</div>
      <div class="quiz-subhint" id="quizSubhint"></div>
      <div>
        <button class="quiz-listen-btn" onclick="speakQuizQuestion()">
          <span>🎙️ മലയാളം ചോദ്യം കേൾക്കാം 🔊</span>
        </button>
      </div>
    </div>

    <div class="options-list" id="quizOptionsList"></div>
  </div>
</section>

<!-- ===================== RESULT SCREEN ===================== -->
<section class="screen hidden" id="screen-result">
  <div class="result-wrap">
    <div class="result-big-mascot" id="resultMascot">🏎️🏆</div>
    <h2 id="resultTitle">സൂപ്പർ കുഞ്ഞീ! ഗംഭീരം! 🏎️💨</h2>
    <p id="resultSub">കുഞ്ഞി വളരെ വിജയകരമായി ചാപ്റ്റർ പൂർത്തിയാക്കി!</p>
    <div class="result-score-badge" id="resultScoreBadge">സ്കോർ: 10 / 10 ⭐</div>
    <div class="result-buttons">
      <button class="result-btn retry" onclick="retryQuiz()">
        <span>🔁 വീണ്ടും കളിക്കാം 🏁</span>
      </button>
      <button class="result-btn home" onclick="goHome()">
        <span>🏠 പ്രധാന പേജിലേക്ക് (Home) 🐹</span>
      </button>
    </div>
  </div>
</section>

<!-- ===================== VOICE & SETTINGS MODAL ===================== -->
<div class="modal-overlay hidden" id="voiceModal" onclick="closeVoiceModalOnOutside(event)">
  <div class="modal-card">
    <div class="modal-header">
      <h3>🎙️ ശബ്ദ ക്രമീകരണങ്ങൾ (Voice Settings)</h3>
      <button class="modal-close" onclick="closeVoiceModal()">✕</button>
    </div>
    <div class="setting-item">
      <label class="setting-label" for="voiceSelect">ഇംഗ്ലീഷ് ശബ്ദം (English Voice):</label>
      <select class="setting-select" id="voiceSelect" onchange="onVoiceChange()"></select>
    </div>
    <div class="setting-item">
      <label class="setting-label" for="speedSelect">ശബ്ദത്തിന്റെ വേഗത (Speech Speed):</label>
      <select class="setting-select" id="speedSelect" onchange="onSpeedChange()">
        <option value="1.0">സാധാരണ വേഗത (Normal 1.0x) 🏎️</option>
        <option value="0.85" selected>കുട്ടികൾക്ക് എളുപ്പമുള്ള വേഗത (Gentle 0.85x) 🐹</option>
        <option value="0.7">വളരെ പതുക്കെ (Slow 0.7x) 🐢</option>
      </select>
    </div>
    <div class="setting-item">
      <label class="setting-label" for="praiseVoiceToggle">ശരിയായ ഉത്തരത്തിന് കുഞ്ഞിയെ അഭിനന്ദിക്കുക:</label>
      <select class="setting-select" id="praiseVoiceToggle" onchange="onPraiseToggleChange()">
        <option value="yes" selected>ഉറക്കെ അഭിനന്ദിക്കണം (Speak Praises) 🌟</option>
        <option value="no">ശബ്ദം വേണ്ട (Silent) 🔕</option>
      </select>
    </div>
    <div style="margin-top:16px; display:flex; flex-direction:column; gap:8px;">
      <button class="listen-all-btn" style="width:100%; justify-content:center;" onclick="testMalayalamVoice()">
        🎙️ മലയാളം ശബ്ദം ടെസ്റ്റ് ചെയ്യുക (Test Malayalam)
      </button>
      <button class="speed-btn" style="width:100%; justify-content:center; padding:10px;" onclick="testEnglishVoice()">
        🔊 ഇംഗ്ലീഷ് ശബ്ദം ടെസ്റ്റ് ചെയ്യുക (Test English)
      </button>
    </div>
  </div>
</div>

<script>
// CHAPTERS & TOPICS ENRICHED DATA
const CHAPTERS_DATA = """ + json_data_str + """;

// PERSISTENCE KEYS
const TOPIC_PROGRESS_KEY = 'kunji_topic_progress_v2';
const CHAPTER_STARS_KEY = 'kunji_chapter_stars_v2';
const SETTINGS_KEY = 'kunji_settings_v2';

// LOAD STATE
let topicProgress = {};
let chapterStars = {};
let settings = {
  voiceURI: '',
  rate: 0.85,
  speakPraise: true
};

try {
  const savedTP = localStorage.getItem(TOPIC_PROGRESS_KEY);
  if (savedTP) topicProgress = JSON.parse(savedTP);
  const savedCS = localStorage.getItem(CHAPTER_STARS_KEY);
  if (savedCS) chapterStars = JSON.parse(savedCS);
  const savedSettings = localStorage.getItem(SETTINGS_KEY);
  if (savedSettings) settings = Object.assign(settings, JSON.parse(savedSettings));
} catch(e) {
  console.error("Storage load error:", e);
}

function saveState() {
  try {
    localStorage.setItem(TOPIC_PROGRESS_KEY, JSON.stringify(topicProgress));
    localStorage.setItem(CHAPTER_STARS_KEY, JSON.stringify(chapterStars));
    localStorage.setItem(SETTINGS_KEY, JSON.stringify(settings));
  } catch(e) {
    console.error("Storage save error:", e);
  }
}

// CURRENT VIEW NAVIGATION STATE
let currentChapter = null;
let currentTopic = null;
let currentCardIndex = 0;
let quizState = null;

// ===================== SPEECH SYNTHESIS ENGINE =====================
let availableVoices = [];
let activeAudio = null;

function stopAllAudio() {
  if ('speechSynthesis' in window) {
    window.speechSynthesis.cancel();
  }
  if (activeAudio) {
    try {
      activeAudio.pause();
      activeAudio.currentTime = 0;
    } catch(e) {}
    activeAudio = null;
  }
}

function loadVoices() {
  if (!('speechSynthesis' in window)) return;
  const allVoices = window.speechSynthesis.getVoices();
  availableVoices = allVoices.filter(v => v.lang.startsWith('en'));
  if (availableVoices.length === 0) availableVoices = allVoices;

  const sel = document.getElementById('voiceSelect');
  if (!sel) return;
  sel.innerHTML = '';
  availableVoices.forEach((v) => {
    const opt = document.createElement('option');
    opt.value = v.voiceURI;
    opt.textContent = `${v.name} (${v.lang})`;
    if (settings.voiceURI && v.voiceURI === settings.voiceURI) {
      opt.selected = true;
    } else if (!settings.voiceURI && (v.name.includes('Samantha') || v.name.includes('Karen') || v.name.includes('Daniel') || v.default)) {
      opt.selected = true;
    }
    sel.appendChild(opt);
  });
}
if ('speechSynthesis' in window) {
  window.speechSynthesis.onvoiceschanged = loadVoices;
  loadVoices();
}

function getSelectedEnglishVoice() {
  if (!availableVoices.length) return null;
  if (settings.voiceURI) {
    const found = availableVoices.find(v => v.voiceURI === settings.voiceURI);
    if (found) return found;
  }
  return availableVoices.find(v => v.name.includes('Samantha') || v.name.includes('Karen') || v.name.includes('Daniel')) || availableVoices[0];
}

// Speak English Text
function speakEnglish(text, onEnd) {
  stopAllAudio();
  if (!('speechSynthesis' in window)) {
    if (onEnd) onEnd();
    return;
  }
  const utter = new SpeechSynthesisUtterance(text);
  const voice = getSelectedEnglishVoice();
  if (voice) utter.voice = voice;
  utter.lang = 'en-US';
  utter.rate = settings.rate || 0.85;
  utter.pitch = 1.05;
  if (onEnd) utter.onend = onEnd;
  window.speechSynthesis.speak(utter);
}

// Speak Malayalam Text in PROPER SMOOTH MALAYALAM VOICE
function speakMalayalam(text, audioKey, onEnd) {
  stopAllAudio();

  // 1. Try local studio MP3 audio file first (instant, 100% offline, native smooth Malayalam)
  if (audioKey) {
    const audioPath = 'audio/' + audioKey + '.mp3';
    const sound = new Audio(audioPath);
    activeAudio = sound;

    let ended = false;
    const finish = () => {
      if (!ended) {
        ended = true;
        activeAudio = null;
        if (onEnd) onEnd();
      }
    };

    sound.onended = finish;
    sound.onerror = () => {
      // 2. Fallback to Google GTX Neural Malayalam TTS
      playOnlineMalayalamTTS(text, onEnd);
    };

    const playPromise = sound.play();
    if (playPromise !== undefined) {
      playPromise.catch(() => {
        playOnlineMalayalamTTS(text, onEnd);
      });
    }
    return;
  }

  playOnlineMalayalamTTS(text, onEnd);
}

function playOnlineMalayalamTTS(text, onEnd) {
  try {
    const cleanText = text.replace(/[\/#!$%\^&\*;:{}=\-_`~()]/g, " ").trim();
    const ttsUrl = 'https://translate.googleapis.com/translate_tts?client=gtx&ie=UTF-8&tl=ml&q=' + encodeURIComponent(cleanText);
    const sound = new Audio(ttsUrl);
    activeAudio = sound;

    let ended = false;
    const finish = () => {
      if (!ended) {
        ended = true;
        activeAudio = null;
        if (onEnd) onEnd();
      }
    };

    sound.onended = finish;
    sound.onerror = () => {
      fallbackMalayalamWebSpeech(text, onEnd);
    };

    const playPromise = sound.play();
    if (playPromise !== undefined) {
      playPromise.catch(() => {
        fallbackMalayalamWebSpeech(text, onEnd);
      });
    }
  } catch(e) {
    fallbackMalayalamWebSpeech(text, onEnd);
  }
}

function fallbackMalayalamWebSpeech(text, onEnd) {
  if (!('speechSynthesis' in window)) {
    if (onEnd) onEnd();
    return;
  }
  // ONLY use Web Speech API if an authentic Malayalam voice is installed
  const allVoices = window.speechSynthesis.getVoices();
  const mlVoice = allVoices.find(v => 
    v.lang === 'ml-IN' || 
    v.lang === 'ml' || 
    v.name.toLowerCase().includes('malayalam')
  );

  if (!mlVoice) {
    // IMPORTANT: DO NOT use English or Hindi voices for Malayalam!
    if (onEnd) onEnd();
    return;
  }

  const utter = new SpeechSynthesisUtterance(text);
  utter.voice = mlVoice;
  utter.lang = 'ml-IN';
  utter.rate = settings.rate || 0.85;
  if (onEnd) utter.onend = onEnd;
  window.speechSynthesis.speak(utter);
}

// AUDIO SYNTHESIZED EFFECTS (WEB AUDIO API)
let audioCtx = null;
function getAudioContext() {
  if (!audioCtx) {
    audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  }
  if (audioCtx.state === 'suspended') {
    audioCtx.resume();
  }
  return audioCtx;
}

function playCorrectSound() {
  try {
    const ctx = getAudioContext();
    const now = ctx.currentTime;
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.connect(gain);
    gain.connect(ctx.destination);

    osc.type = 'triangle';
    osc.frequency.setValueAtTime(523.25, now); // C5
    osc.frequency.setValueAtTime(659.25, now + 0.1); // E5
    osc.frequency.setValueAtTime(783.99, now + 0.2); // G5
    osc.frequency.setValueAtTime(1046.50, now + 0.3); // C6

    gain.gain.setValueAtTime(0.3, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.6);

    osc.start(now);
    osc.stop(now + 0.6);
  } catch(e) {}
}

function playWrongSound() {
  try {
    const ctx = getAudioContext();
    const now = ctx.currentTime;
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.connect(gain);
    gain.connect(ctx.destination);

    osc.type = 'sine';
    osc.frequency.setValueAtTime(260, now);
    osc.frequency.linearRampToValueAtTime(180, now + 0.25);

    gain.gain.setValueAtTime(0.25, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.3);

    osc.start(now);
    osc.stop(now + 0.3);
  } catch(e) {}
}

// KUNJI PERSONALIZED APPRECIATIONS
const KUNJI_APPRECIATIONS = [
  {
    en: "Good job Kunji!",
    ml: "നന്നായി ചെയ്തു കുഞ്ഞീ! 🐹🏎️💨",
    emoji: "🏎️💨"
  },
  {
    en: "Great, well done Kunji!",
    ml: "വളരെ മിടുക്കൻ കുഞ്ഞി! 🏆🌟",
    emoji: "🏆✨"
  },
  {
    en: "Super fast Kunji!",
    ml: "സൂപ്പർ സ്പീഡ് കുഞ്ഞീ! 🚀💨",
    emoji: "🚀💨"
  },
  {
    en: "Kunji is a champion!",
    ml: "കുഞ്ഞി ഒരു ചാമ്പ്യൻ തന്നെ! 🥇🐹",
    emoji: "🥇🐹"
  },
  {
    en: "Awesome driving, Kunji!",
    ml: "ഗംഭീരം കുഞ്ഞീ, അടിപൊളി! 🏎️🎉",
    emoji: "🏎️🏁"
  },
  {
    en: "Turbo speed Kunji!",
    ml: "ടർബോ പവർ കുഞ്ഞീ! ⚡🏁",
    emoji: "⚡🐹"
  }
];

function showKunjiAppreciation(callback) {
  playCorrectSound();
  launchConfetti();

  const rand = KUNJI_APPRECIATIONS[Math.floor(Math.random() * KUNJI_APPRECIATIONS.length)];
  const banner = document.getElementById('appreciationBanner');
  document.getElementById('apprecEmoji').textContent = rand.emoji;
  document.getElementById('apprecTitle').textContent = rand.en;
  document.getElementById('apprecSub').textContent = rand.ml;

  banner.classList.add('show');

  if (settings.speakPraise) {
    speakEnglish(rand.en, () => {
      setTimeout(() => {
        banner.classList.remove('show');
        if (callback) callback();
      }, 700);
    });
  } else {
    setTimeout(() => {
      banner.classList.remove('show');
      if (callback) callback();
    }, 1500);
  }
}

// SCREEN TRANSITIONS
function showScreen(screenId) {
  stopAllAudio();
  document.querySelectorAll('.screen').forEach(s => s.classList.add('hidden'));
  const target = document.getElementById(screenId);
  if (target) target.classList.remove('hidden');
  window.scrollTo(0, 0);
}

function goHome() {
  currentChapter = null;
  currentTopic = null;
  quizState = null;
  renderHomeDashboard();
  showScreen('screen-home');
}

function showStation() {
  if (!currentChapter) return goHome();
  renderStation();
  showScreen('screen-station');
}

// ===================== PROGRESS CALCULATION =====================
function getTopicProgressData(topicId, totalItems) {
  const tData = topicProgress[topicId] || { learned: [] };
  const learnedCount = tData.learned ? tData.learned.length : 0;
  const pct = totalItems > 0 ? Math.min(100, Math.round((learnedCount / totalItems) * 100)) : 0;
  return {
    learnedCount,
    totalItems,
    pct,
    isCompleted: pct === 100
  };
}

function markItemLearned(topicId, itemId, totalTopicItems) {
  if (!topicProgress[topicId]) {
    topicProgress[topicId] = { learned: [] };
  }
  if (!topicProgress[topicId].learned.includes(itemId)) {
    topicProgress[topicId].learned.push(itemId);
  }
  saveState();
}

function calculateOverallStats() {
  let totalCards = 0;
  let masteredCards = 0;
  let totalTopics = 0;
  let completedTopics = 0;
  let earnedStars = 0;
  const maxStars = CHAPTERS_DATA.length * 10;

  CHAPTERS_DATA.forEach(ch => {
    earnedStars += (chapterStars[ch.id] || 0);
    ch.topics.forEach(t => {
      totalTopics++;
      totalCards += t.items.length;
      const prog = getTopicProgressData(t.id, t.items.length);
      masteredCards += prog.learnedCount;
      if (prog.isCompleted) completedTopics++;
    });
  });

  const overallPct = totalCards > 0 ? Math.round((masteredCards / totalCards) * 100) : 0;
  return {
    earnedStars,
    maxStars,
    totalTopics,
    completedTopics,
    totalCards,
    masteredCards,
    overallPct
  };
}

// ===================== RENDER HOME DASHBOARD =====================
function renderHomeDashboard() {
  const stats = calculateOverallStats();
  document.getElementById('totalStars').textContent = stats.earnedStars;
  document.getElementById('overallPercent').textContent = `${stats.overallPct}%`;
  document.getElementById('overallTrackFill').style.width = `${stats.overallPct}%`;
  document.getElementById('dashStarsLabel').textContent = `${stats.earnedStars} / ${stats.maxStars}`;
  document.getElementById('dashTopicsLabel').textContent = `${stats.completedTopics} / ${stats.totalTopics}`;
  document.getElementById('dashItemsLabel').textContent = `${stats.masteredCards} / ${stats.totalCards}`;

  const listEl = document.getElementById('chaptersList');
  listEl.innerHTML = '';

  CHAPTERS_DATA.forEach(ch => {
    let chTotalCards = 0;
    let chMasteredCards = 0;
    ch.topics.forEach(t => {
      chTotalCards += t.items.length;
      const p = getTopicProgressData(t.id, t.items.length);
      chMasteredCards += p.learnedCount;
    });
    const chPct = chTotalCards > 0 ? Math.round((chMasteredCards / chTotalCards) * 100) : 0;
    const stars = chapterStars[ch.id] || 0;

    const card = document.createElement('div');
    card.className = 'chapter-card';
    card.onclick = () => openChapter(ch.id);
    card.innerHTML = `
      <div class="ch-top-row">
        <div class="ch-badge-title">
          <div class="ch-badge">${ch.badge}</div>
          <div class="ch-info">
            <h3>${ch.number}. ${ch.title_ml}</h3>
            <div class="ch-en-title">${ch.title}</div>
          </div>
        </div>
        <div class="ch-stars-pill">⭐ ${stars} / 10</div>
      </div>
      <div class="ch-sub-text">${ch.sub_ml}</div>
      <div class="ch-progress-wrap">
        <div class="ch-progress-bar">
          <div class="ch-progress-fill" style="width:${chPct}%"></div>
        </div>
        <div class="ch-progress-label">${chMasteredCards}/${chTotalCards} (${chPct}%)</div>
      </div>
    `;
    listEl.appendChild(card);
  });
}

// ===================== CHAPTER / STATION VIEW =====================
function openChapter(chId) {
  currentChapter = CHAPTERS_DATA.find(c => c.id === chId);
  if (!currentChapter) return;
  renderStation();
  showScreen('screen-station');
}

function renderStation() {
  if (!currentChapter) return;

  document.getElementById('stBadge').textContent = currentChapter.badge;
  document.getElementById('stTitleMl').textContent = `${currentChapter.number}. ${currentChapter.title_ml}`;
  document.getElementById('stTitleEn').textContent = currentChapter.title;

  const stars = chapterStars[currentChapter.id] || 0;
  document.getElementById('stationChapterStars').textContent = stars;

  let starIcons = '';
  for (let i = 1; i <= 10; i++) {
    starIcons += (i <= stars) ? '⭐' : '☆';
  }
  document.getElementById('stStarsRow').textContent = `${starIcons} (${stars}/10)`;

  // Render EVERY topic with its dedicated persistent progress bar
  const topicsListEl = document.getElementById('stationTopicsList');
  topicsListEl.innerHTML = '';

  currentChapter.topics.forEach((t, tIdx) => {
    const prog = getTopicProgressData(t.id, t.items.length);
    let statusClass = 'status-not-started';
    let statusLabel = '🚦 തുടങ്ങാം';
    let racerThumb = '🏎️';

    if (prog.pct === 100) {
      statusClass = 'status-completed';
      statusLabel = '🏆 പൂർത്തിയായി!';
      racerThumb = '🏆';
    } else if (prog.pct > 0) {
      statusClass = 'status-in-progress';
      statusLabel = '🏎️ ഓടുന്നു...';
      racerThumb = '🐹';
    }

    const tCard = document.createElement('div');
    tCard.className = `topic-card ${prog.isCompleted ? 'completed' : ''}`;
    tCard.innerHTML = `
      <div class="topic-card-top">
        <div class="topic-card-titles">
          <h4>${t.title_ml}</h4>
          <div class="topic-en-name">${t.title}</div>
        </div>
        <div class="topic-status-badge ${statusClass}">${statusLabel}</div>
      </div>

      <!-- PERSISTENT TOPIC PROGRESS BAR -->
      <div class="topic-progress-wrap">
        <div class="topic-progress-info">
          <span class="topic-progress-items">${prog.learnedCount} / ${prog.totalItems} വാക്യങ്ങൾ</span>
          <span class="topic-progress-pct">${prog.pct}%</span>
        </div>
        <div class="topic-bar-track">
          <div class="topic-bar-fill" style="width:${prog.pct}%">
            <span class="topic-bar-thumb">${racerThumb}</span>
          </div>
        </div>
      </div>

      <div class="topic-card-actions">
        <button class="topic-btn learn" onclick="startLearnTopic(${tIdx})">
          <span>📖 കാർഡുകൾ</span>
        </button>
        <button class="topic-btn quiz" onclick="startTopicQuiz(${tIdx})">
          <span>🎯 ക്വിസ് (മലയാളം 🎙️)</span>
        </button>
      </div>
    `;
    topicsListEl.appendChild(tCard);
  });
}

// ===================== FLASHCARD LEARN MODE =====================
function startLearnTopic(tIdx) {
  if (!currentChapter) return;
  currentTopic = currentChapter.topics[tIdx];
  currentCardIndex = 0;
  renderCurrentCard();
  showScreen('screen-learn');
}

function renderCurrentCard() {
  if (!currentTopic || !currentTopic.items.length) return;
  const item = currentTopic.items[currentCardIndex];

  document.getElementById('learnCounterTxt').textContent = `വാക്യം ${currentCardIndex + 1} / ${currentTopic.items.length} 🐹`;
  document.getElementById('cardTopicTag').textContent = `🏁 ${currentTopic.title_ml}`;

  // Live Topic Progress Bar on Flashcard Screen
  const prog = getTopicProgressData(currentTopic.id, currentTopic.items.length);
  document.getElementById('learnTopicName').textContent = currentTopic.title_ml;
  document.getElementById('learnTopicPct').textContent = `${prog.pct}% (${prog.learnedCount}/${prog.totalItems})`;
  document.getElementById('learnTopicBarFill').style.width = `${prog.pct}%`;

  // Speaker A
  document.getElementById('cardTextAEn').textContent = item.q;
  document.getElementById('cardTextAMl').textContent = item.q_ml;

  // Speaker B
  document.getElementById('cardTextBEn').textContent = item.a;
  document.getElementById('cardTextBMl').textContent = item.a_ml;

  // Note Box
  const noteBox = document.getElementById('cardNoteBox');
  const noteText = document.getElementById('cardNoteText');
  if (item.note_ml || item.note) {
    noteBox.classList.remove('hidden');
    noteText.textContent = item.note_ml || item.note;
  } else {
    noteBox.classList.add('hidden');
  }

  document.getElementById('prevCardBtn').disabled = (currentCardIndex === 0);
  document.getElementById('nextCardBtn').disabled = (currentCardIndex === currentTopic.items.length - 1);
}

function speakSpeakerA() {
  if (!currentTopic) return;
  const item = currentTopic.items[currentCardIndex];
  speakEnglish(item.q);
}

function speakSpeakerB() {
  if (!currentTopic) return;
  const item = currentTopic.items[currentCardIndex];
  speakEnglish(item.a);
}

function speakMalayalamCardA() {
  if (!currentTopic) return;
  const item = currentTopic.items[currentCardIndex];
  speakMalayalam(item.q_ml, item.id);
}

function speakMalayalamCardB() {
  if (!currentTopic) return;
  const item = currentTopic.items[currentCardIndex];
  speakMalayalam(item.a_ml, item.id + '_a');
}

function speakCurrentDialogue() {
  if (!currentTopic) return;
  const item = currentTopic.items[currentCardIndex];
  speakEnglish(item.q, () => {
    setTimeout(() => speakEnglish(item.a), 400);
  });
}

function markCardMastered() {
  if (!currentTopic) return;
  const item = currentTopic.items[currentCardIndex];
  markItemLearned(currentTopic.id, item.id, currentTopic.items.length);

  showKunjiAppreciation(() => {
    if (currentCardIndex < currentTopic.items.length - 1) {
      currentCardIndex++;
      renderCurrentCard();
    } else {
      showStation();
    }
  });
}

function nextCard() {
  if (currentTopic && currentCardIndex < currentTopic.items.length - 1) {
    currentCardIndex++;
    renderCurrentCard();
  }
}

function prevCard() {
  if (currentTopic && currentCardIndex > 0) {
    currentCardIndex--;
    renderCurrentCard();
  }
}

// ===================== QUIZ MODE (MALAYALAM VOICE ASKING) =====================
function buildQuizQuestions(itemsPool, targetCount) {
  const shuffled = [...itemsPool].sort(() => 0.5 - Math.random());
  const selected = shuffled.slice(0, Math.min(targetCount, shuffled.length));

  return selected.map(item => {
    // The question is asked in MALAYALAM, and Kunji chooses the English phrase!
    const questionText = item.q_ml;
    const correctAnswer = item.q;
    const kicker = "🎯 ഇത് ഇംഗ്ലീഷിൽ എങ്ങനെ പറയും കുഞ്ഞീ?";

    // Pick 2 wrong English choices from other items
    const otherItems = itemsPool.filter(x => x.id !== item.id).sort(() => 0.5 - Math.random());
    const wrongAnswers = otherItems.slice(0, 2).map(x => x.q);

    // Shuffle options
    const options = [correctAnswer, ...wrongAnswers].sort(() => 0.5 - Math.random());

    return {
      itemId: item.id,
      kicker,
      qText: questionText,
      subhint: item.note_ml || '',
      speakText: questionText, // Spoken in Malayalam Voice!
      speakLang: 'ml',
      correct: correctAnswer,
      options
    };
  });
}

function startTopicQuiz(tIdx) {
  if (!currentChapter) return;
  currentTopic = currentChapter.topics[tIdx];
  const questions = buildQuizQuestions(currentTopic.items, Math.min(5, currentTopic.items.length));
  startQuizSession(questions, `ടോപ്പിക് ക്വിസ്: ${currentTopic.title_ml}`);
}

function startChapterQuiz() {
  if (!currentChapter) return;
  const allChapterItems = [];
  currentChapter.topics.forEach(t => allChapterItems.push(...t.items));
  const questions = buildQuizQuestions(allChapterItems, 10);
  startQuizSession(questions, `ചാപ്റ്റർ ഗ്രാൻഡ് പ്രീ ക്വിസ്: ${currentChapter.title_ml}`);
}

function startQuizSession(questions, quizTitle) {
  quizState = {
    title: quizTitle,
    questions,
    index: 0,
    score: 0,
    answered: false
  };
  renderQuizQuestion();
  showScreen('screen-quiz');
}

function renderQuizQuestion() {
  if (!quizState || quizState.index >= quizState.questions.length) {
    return finishQuiz();
  }

  quizState.answered = false;
  const q = quizState.questions[quizState.index];

  document.getElementById('quizProgressTxt').textContent = `ചോദ്യം ${quizState.index + 1} / ${quizState.questions.length} 🏁`;
  document.getElementById('quizCorrectCount').textContent = quizState.score;
  document.getElementById('quizScorePill').textContent = `${quizState.score} / ${quizState.questions.length} ⭐`;

  document.getElementById('quizKicker').textContent = q.kicker;
  document.getElementById('quizQText').textContent = q.qText;
  document.getElementById('quizSubhint').textContent = q.subhint;

  const optContainer = document.getElementById('quizOptionsList');
  optContainer.innerHTML = '';

  q.options.forEach(optText => {
    const btn = document.createElement('button');
    btn.className = 'quiz-option';
    btn.textContent = optText;
    btn.onclick = () => onSelectOption(btn, optText, q.correct);
    optContainer.appendChild(btn);
  });

  // ASK IN MALAYALAM VOICE!
  speakQuizQuestion();
}

function speakQuizQuestion() {
  if (!quizState) return;
  const q = quizState.questions[quizState.index];
  if (q && q.speakText) {
    speakMalayalam(q.speakText, q.itemId);
  }
}

function onSelectOption(buttonEl, selectedText, correctText) {
  if (!quizState || quizState.answered) return;
  quizState.answered = true;

  const isCorrect = (selectedText === correctText);
  const allOptionButtons = document.querySelectorAll('.quiz-option');

  if (isCorrect) {
    buttonEl.classList.add('correct');
    quizState.score++;
    document.getElementById('quizCorrectCount').textContent = quizState.score;

    // Mark item learned in persistent progress
    const curQ = quizState.questions[quizState.index];
    if (curQ && curQ.itemId && currentTopic) {
      markItemLearned(currentTopic.id, curQ.itemId, currentTopic.items.length);
    }

    // Pronounce the correct English sentence so Kunji learns English, then praise him!
    speakEnglish(correctText, () => {
      showKunjiAppreciation(() => {
        advanceQuiz();
      });
    });
  } else {
    buttonEl.classList.add('wrong');
    playWrongSound();

    // Highlight the correct one
    allOptionButtons.forEach(b => {
      if (b.textContent === correctText) {
        b.classList.add('correct');
      }
    });

    // Also speak correct answer
    speakEnglish(correctText, () => {
      setTimeout(() => {
        advanceQuiz();
      }, 1000);
    });
  }
}

function advanceQuiz() {
  if (!quizState) return;
  quizState.index++;
  if (quizState.index >= quizState.questions.length) {
    finishQuiz();
  } else {
    renderQuizQuestion();
  }
}

function finishQuiz() {
  if (!quizState || !currentChapter) return goHome();

  const totalQ = quizState.questions.length;
  const earned = quizState.score;

  // If Chapter Quiz (10 Qs), update chapter stars
  if (totalQ >= 8) {
    const existing = chapterStars[currentChapter.id] || 0;
    if (earned > existing) {
      chapterStars[currentChapter.id] = earned;
      saveState();
    }
  }

  document.getElementById('resultScoreBadge').textContent = `സ്കോർ: ${earned} / ${totalQ} ⭐`;
  if (earned >= totalQ * 0.8) {
    document.getElementById('resultMascot').textContent = '🏎️🏆';
    document.getElementById('resultTitle').textContent = 'സൂപ്പർ കുഞ്ഞീ! ഗംഭീരം!';
    document.getElementById('resultSub').textContent = 'കുഞ്ഞി അതിവേഗത്തിൽ എല്ലാ ഉത്തരങ്ങളും ശരിയാക്കി!';
    launchConfetti();
  } else {
    document.getElementById('resultMascot').textContent = '🐹🏁';
    document.getElementById('resultTitle').textContent = 'നന്നായി പരിശ്രമിച്ചു കുഞ്ഞീ!';
    document.getElementById('resultSub').textContent = 'കുറച്ചുകൂടി പരിശീലിച്ചാൽ കുഞ്ഞിക്ക് 10/10 നേടാം!';
  }

  showScreen('screen-result');
}

function retryQuiz() {
  if (!currentChapter) return goHome();
  if (currentTopic) {
    startTopicQuiz(currentChapter.topics.indexOf(currentTopic));
  } else {
    startChapterQuiz();
  }
}

// ===================== CONFETTI ANIMATION =====================
function launchConfetti() {
  const canvas = document.getElementById('confettiCanvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;

  const pieces = [];
  const colors = ['#FF3D00', '#FF9100', '#FFD600', '#00E676', '#00B0FF', '#FFF'];
  for (let i = 0; i < 70; i++) {
    pieces.push({
      x: canvas.width / 2,
      y: canvas.height / 2,
      vx: (Math.random() - 0.5) * 16,
      vy: (Math.random() - 0.7) * 18,
      size: Math.random() * 8 + 5,
      color: colors[Math.floor(Math.random() * colors.length)],
      alpha: 1
    });
  }

  let frames = 0;
  function step() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    frames++;
    pieces.forEach(p => {
      p.x += p.vx;
      p.y += p.vy;
      p.vy += 0.4;
      p.alpha -= 0.012;
      ctx.globalAlpha = Math.max(0, p.alpha);
      ctx.fillStyle = p.color;
      ctx.fillRect(p.x, p.y, p.size, p.size * 0.7);
    });
    if (frames < 75) requestAnimationFrame(step);
    else ctx.clearRect(0, 0, canvas.width, canvas.height);
  }
  step();
}

// ===================== SETTINGS & RESET =====================
let badgeClickCount = 0;
let badgeClickTimer = null;
function handleKunjiBadgeClick() {
  badgeClickCount++;
  clearTimeout(badgeClickTimer);
  badgeClickTimer = setTimeout(() => { badgeClickCount = 0; }, 3000);

  if (badgeClickCount >= 5) {
    badgeClickCount = 0;
    if (confirm("കുഞ്ഞിയുടെ സ്കോറും പുരോഗതിയും പൂർണ്ണമായി റീസെറ്റ് ചെയ്യണോ? (Reset all progress?)")) {
      topicProgress = {};
      chapterStars = {};
      saveState();
      renderHomeDashboard();
      alert("കുഞ്ഞിയുടെ സ്കോർ വിജയകരമായി റീസെറ്റ് ചെയ്തു! 🏁");
    }
  }
}

function openVoiceModal() {
  loadVoices();
  document.getElementById('voiceModal').classList.remove('hidden');
}

function closeVoiceModal() {
  document.getElementById('voiceModal').classList.add('hidden');
}

function closeVoiceModalOnOutside(e) {
  if (e.target.id === 'voiceModal') closeVoiceModal();
}

function onVoiceChange() {
  const sel = document.getElementById('voiceSelect');
  settings.voiceURI = sel.value;
  saveState();
}

function onSpeedChange() {
  const sel = document.getElementById('speedSelect');
  settings.rate = parseFloat(sel.value) || 0.85;
  saveState();
  updateSpeedButtons();
}

function toggleSpeed() {
  if (settings.rate <= 0.75) {
    settings.rate = 1.0;
  } else if (settings.rate >= 0.95) {
    settings.rate = 0.85;
  } else {
    settings.rate = 0.7;
  }
  saveState();
  updateSpeedButtons();
  speakEnglish(settings.rate === 1.0 ? "Normal speed" : (settings.rate === 0.85 ? "Gentle speed" : "Slow speed"));
}

function updateSpeedButtons() {
  const label = settings.rate === 1.0 ? '🏎️ 1x' : (settings.rate === 0.85 ? '🐹 0.85x' : '🐢 0.7x');
  const btn1 = document.getElementById('speedToggleBtn');
  const btn2 = document.getElementById('learnSpeedBtn');
  if (btn1) btn1.textContent = label;
  if (btn2) btn2.textContent = label;
}

function onPraiseToggleChange() {
  const sel = document.getElementById('praiseVoiceToggle');
  settings.speakPraise = (sel.value === 'yes');
  saveState();
}

function testMalayalamVoice() {
  speakMalayalam("ഹലോ കുഞ്ഞീ! നമുക്ക് ഒരുമിച്ച് അടിപൊളി ഇംഗ്ലീഷ് പഠിക്കാം!", "test_ml");
}

function testEnglishVoice() {
  speakEnglish("Good job Kunji! Let's learn English together with our fast racing car!");
}

// INITIAL STARTUP
window.addEventListener('DOMContentLoaded', () => {
  renderHomeDashboard();
  updateSpeedButtons();
});
</script>
</body>
</html>
"""

# Write to Kunji_English/index.html and Kunji_English/Kunji_English.html
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_template)

with open("Kunji_English.html", "w", encoding="utf-8") as f:
    f.write(html_template)

print("Regenerated index.html and Kunji_English.html with Malayalam Voice Quiz successfully!")

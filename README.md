# 🧠 IntelliWord - AI-Powered Word Search Game

## 🎮 Overview

IntelliWord is an advanced AI-powered word search game developed using Python and Pygame. Unlike traditional word search games, IntelliWord introduces four dynamic game modes and an intelligent AI opponent that competes against the player in real-time. The AI utilizes a directionally constrained DFS algorithm to find words with 100% accuracy, providing a challenging and engaging experience for players.

---

## 🧠 Game Modes

1. Grid Shuffle Mode  
   - Human vs AI  
   - After every word found, the grid is shuffled, increasing difficulty.  
   - Both human and AI play simultaneously.

2. Word Bomb Mode 
   - A randomly selected word carries a hidden bomb.  
   - The player must find the bomb word to defuse it within the time limit.

3. Word Chain Mode  
   - Players must find a sequence of related words in order.

4. Fog of War Mode 
   - The grid is partially hidden. Cells reveal only when nearby cells are discovered, adding exploration logic.

---

## ⚙️ Features

- Three difficulty levels: **Easy**, **Medium**, **Hard**
- Real-time AI vs Human (not turn-based)
- AI uses **Directionally Constrained DFS**
- AI slows down intentionally for fair gameplay
- **Dynamic scoring** and **visual feedback**
- Grid scales and word complexity increase with difficulty
- Includes sound effects and UI enhancements

---

## 📽️ Demo Video , 📄 Project Proposal and 📄 Project Report in this google drive 

https://drive.google.com/drive/u/1/folders/12Q46y0NH6eQrZBcXPrDRgIpijdWOCgf5


---

INTELLIWORD/
├── game_modes/
│   ├── base_game.py
│   ├── classic_game.py
│   ├── shuffle_game.py
│   └── wordbomb_game.py
├── images/
│   ├── background.png
│   ├── icon.png
│   ├── menu.png
│   └── time-bomb.png
├── music/
│   ├── aifound.mp3
│   ├── background.mp3
│   ├── bomb.mp3
│   ├── click.mp3
│   ├── fog.mp3
│   ├── gameover.mp3
│   ├── incorrect.mp3
│   ├── shuffle.mp3
│   ├── timer.mp3
│   ├── winner.mp3
│   └── wordfound.mp3
├── game.py
├── grid.py
├── main.py
├── menu.py
├── player.py
├── ui.py
├── words.txt
└── Project Report_IntelliWord.pdf


## 🚀 Getting Started

1) Make sure Python 3.x is installed on your system.
2)pip install pygame
3)clone this Repository
4)cd Intelliword (move to this directory in your IDE)
To start the game , run the file main.py
5)python main.py


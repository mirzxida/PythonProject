Star Escape

A 2D endless space survival simulator developed in Python using the Pygame library. This project was completed as a final project for the "Introduction to Programming 2" course at Astana IT University.

Star Escape is a fast-paced arcade game in which the player controls a spaceship, maneuvering through an endless stream of asteroids. The goal is to survive as long as possible, managing fuel levels and hull strength.

The game features a random space event system and three difficulty levels (Easy, Medium, and Hard), which affect the initial number of spawning threats. As your score increases, the speed of the asteroids gradually increases, making the player's job more challenging.

---

Features
Infinite gameplay loop with gradual asteroid acceleration. The main menu allows you to select one of three difficulty modes, which directly affects the density of the meteor shower. The onboard computer periodically generates status messages and warnings. When colliding with asteroids, a screen shake effect and a brief white flash are triggered. The best score is automatically overwritten and saved locally.
Technologies Used:
Python 3.11 as the primary development language
Pygame as the game engine (graphics rendering, input processing, game loop)
JSON for storing and persisting high-score data (`data/save.json`)
unittest
Automated testing

Use of OOP concepts
The project strictly follows an object-oriented approach:
Encapsulation: All game entities (Player, Asteroid, Effects, Event) encapsulate their properties (coordinates, speed, timers) and behavioral logic within classes. Inheritance: The Player and Asteroid classes inherit from the built-in pygame.sprite.Sprite class, allowing them to be efficiently managed through sprite groups (`pygame.sprite.Group`).
Polymorphism: Various game objects implement standardized update() methods, which are called within the main game loop to change the state of entities on each frame.
Installation Requirements: Python 3.10+ and pip. bash

Clone the repository git clone https://github.com/mirzxida/PythonProject/tree/master cd FinalProject
Create a virtual environment python -m venv venv Windows: venv\Scripts\activate macOS / Linux: source venv/bin/activate
Install dependencies pip install -r requirements.txt
requirements.txt contents: pygame>=2.6.0


How to Run bashpython main.py
Controls KeyAction:
Spacebar - start the game, ⬆/⬇ - select a level, ⮕/⬅ - control the spaceship, Enter - restart the game, ESC - open the menu
Screenshots 
Mine Menu
In Game
Gamay Over
Team members:
Kabdyrakmanova Aizat README file, UI design and screens, level generation
Maratova Medina UI design and screens, save system
Merzabekova Khilolakhon game logic, UI design and screens, Testing, assets, entities

# 🎮 Dodge & Survive

An AI-powered game where a neural network learns to dodge falling obstacles using the NEAT (NeuroEvolution of Augmenting Topologies) algorithm.

---

## 🧠 AI Concept

This project demonstrates **Neuroevolution** — a technique where neural networks evolve over generations like natural selection.

- **20 AI agents** (blue balls) play simultaneously each generation
- Bad agents die on collision, good ones survive longer
- Each generation the AI gets smarter at dodging
- By generation 5–10 you can see real dodging behaviour

### What the Neural Network Sees (Inputs)
- Ball's current X position
- Nearest obstacle's X position
- Nearest obstacle's Y position (how close it is)
- Horizontal distance between ball and obstacle

### What the Neural Network Does (Outputs)
- Move Left
- Move Right
- Stay Still

---

## 📁 Project Structure
```
dodge_survive/
│
├── game.py           # Main game loop + NEAT AI logic
└── config-neat.txt   # NEAT algorithm settings
```

---

## ⚙️ Requirements

- Python 3.12.x (**not** 3.13 or 3.14)
- pygame
- neat-python
- matplotlib
- numpy

Install all dependencies:
```bash
pip3 install pygame neat-python matplotlib numpy
```

---

## ▶️ How to Run
```bash
python3.12 game.py
```

---

## 🎮 How It Works

1. Generation starts — 20 balls appear on screen
2. Red obstacles fall from the top randomly
3. Each ball's neural network decides to move left, right, or stay
4. Balls that collide with obstacles are eliminated
5. Surviving balls score higher fitness
6. NEAT breeds the next generation from the best performers
7. Repeat — each generation is smarter than the last

---

## 📊 What to Watch For

| Generation | Expected Behaviour |
|---|---|
| 1–2 | Balls mostly stand still or move randomly |
| 3–5 | Some balls start moving away from obstacles |
| 6–10 | Most balls actively dodge obstacles |
| 10+ | Near-perfect dodging behaviour |

---

## 🛠️ Built With

- [pygame](https://www.pygame.org/) — Game visuals
- [neat-python](https://neat-python.readthedocs.io/) — NEAT algorithm
- Python 3.12

---

## 👤 Author

Parth Kochar — AI Project

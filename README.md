# Othello - AI Fundamentals Project (USTHB 2025)

An Othello (Reversi) game implemented in Python with a simple AI using Minimax and alpha-beta pruning.  
This project was developed as part of the "AI Fundamentals" course at USTHB (2025).

## Overview
This program provides:
- A playable Othello game (graphical UI using Pygame).
- Two game modes: Human vs Human and Human vs Computer (AI).
- An AI opponent that uses Minimax with alpha-beta pruning and a weighted board heuristic.

Main game code: `TpAi.py`

## Features
- GUI built with Pygame (board, pieces, valid-move hints, basic menu).
- Human vs Human and Human vs Computer modes.
- Configurable Minimax search depth (via menu).
- Basic heuristic that favors corners and penalizes bad positions.
- Game state handling: valid moves, captures, passing turns, and game over detection.

## Requirements
- Python 3.8+ (recommended)
- pygame

Install pygame with pip if needed:
```
pip install pygame
```

## Run the game
From the repository root (or where `TpAi.py` is located), run:
```
python TpAi.py
```

## Controls
- Mouse click:
  - In the menu: choose game mode and adjust Minimax depth (+ / -).
  - On the board: place a piece on a valid move.
  - "Nouvelle Partie" (New Game) button restarts / returns to menu.
- Keyboard:
  - SPACE: pass turn when there are no valid moves.
  - ESC: return to the menu (reset game).
- The AI will play as White in "Human vs Computer" mode. When it's the AI's turn it waits a short time and then plays.

## Game Modes
- Human vs Human: Two players alternate placing pieces.
- Human vs Computer: Player (Black) vs AI (White). The AI uses Minimax with alpha-beta pruning.

## AI Details
- Algorithm: Minimax with alpha-beta pruning.
- Heuristic: Weighted board positions. Each square has a pre-defined weight; the evaluation sums weights for the AI player minus weights for the opponent.
- You can change the search depth in the menu (default depth is 2). Increasing depth improves play but increases computation time exponentially.

Heuristic weights matrix (used in code):
```
[
 [100, -20, 10, 5, 5, 10, -20, 100],
 [-20, -50, -2, -2, -2, -2, -50, -20],
 [10, -2, 16, 3, 3, 16, -2, 10],
 [5, -2, 3, 3, 3, 3, -2, 5],
 [5, -2, 3, 3, 3, 3, -2, 5],
 [10, -2, 16, 3, 3, 16, -2, 10],
 [-20, -50, -2, -2, -2, -2, -50, -20],
 [100, -20, 10, 5, 5, 10, -20, 100]
]
```

## File structure (important files)
- `TpAi.py` — Main game code and AI implementation.
- (You can add) `README.md` — This file.
- (Optional) add requirements file: `requirements.txt` (e.g., containing `pygame`).

## Recommended improvements / future work
- Implement improved heuristics that combine mobility, stability, parity and frontier discs.
- Add iterative deepening + time limit for the AI.
- Use transposition table (Zobrist hashing) to cache positions.
- Add move ordering to improve alpha-beta pruning effectiveness.
- Add more UI/UX polish (score history, animations, highlight last move).
- Add unit tests for game logic (captures, valid moves, endgame scenarios).

## Known limitations
- The AI currently uses a static positional heuristic only — it may play poorly in some midgame/endgame situations at low depths.
- No networked multiplayer.
- No undo/redo feature.

## Contributing
Contributions are welcome. Suggested steps:
1. Fork the repository.
2. Create a feature branch.
3. Make changes and test (ensure game logic remains correct).
4. Open a PR with a clear description.

## License
Add a license file if you wish to open-source this project (for example, MIT).

## Credits
- Developed for the AI Fundamentals course at USTHB (2025).
- GUI built with [Pygame](https://www.pygame.org/).

## Contact
If you want feedback or help improving the AI, contact Soumia Hariz ,my email : soumiahariz20@gmail.com


# When It Rains

A small arcade game made with Python and pygame. Move a cat left and right to dodge the raindrops falling from the clouds. One touch ends the game.

![Gameplay](assets/demo.gif)

## Features
- Raindrops spawn at random positions and fall continuously
- Pixel-perfect collision detection using pygame masks, so only the cat's actual shape counts as a hit
- Animated, scrolling clouds
- Game over screen with restart (R) and quit (Esc)
- Written with classes (`Player`, `Raindrop`, `Cloud`) and a `reset_game()` function

## Controls
| Key | Action |
|---|---|
| Left / Right arrow | Move the cat |
| R | Restart (on the game over screen) |
| Esc | Quit (on the game over screen) |

## Run it
```bash
pip install -r ../requirements.txt
python main.py
```
The images must be in the `assets/` folder: `bg.png`, `platform.png`, `raindrop.png`, `cloud_1.png`, `cloud_2.png`, `cloud_3.png`, `cat.png`.

## Tech
Python, pygame (classes, masks, event loop, fixed 60 FPS).

## Limitations and ideas
- There is no score yet. A survival timer would be the first addition.
- Drop speed and spawn rate stay constant, so the game doesn't get harder.
- Possible next steps: score and high score, difficulty that ramps up, sound effects.

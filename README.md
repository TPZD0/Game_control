# Hand Tracking for Mouse and Keyboard Control

This project uses OpenCV and MediaPipe to track hand gestures and control the mouse and keyboard. The right hand is used for mouse movements and clicks, while the left hand controls keyboard inputs for gaming.

## Features
- **Right Hand (Mouse Control)**:
  - Move the index finger to control the mouse.
  - Specific gestures for left-click and right-click.
  - Stop mouse movement using a designated gesture.

- **Left Hand (Keyboard Control)**:
  - Gesture-based key holding for gaming controls (W, A, S, D, Space).
  - Automatically releases keys when gestures change.

## Dependencies
Ensure you have the following Python libraries installed:
```
pip install opencv-python mediapipe pydirectinput
```

## Usage
1. Run the script:
   ```
   python hand_tracking_control.py
   ```
2. Use hand gestures in front of the camera to control the mouse and keyboard.
3. Press `q` to exit the program.

## Controls
### Right Hand (Mouse)
| Gesture | Action |
|---------|--------|
| Index and Middle fingers extended | Move Mouse |
| Thumb, Index, and Middle fingers extended | Stop Mouse |
| Thumb and Middle fingers extended | Left Click |
| Thumb and Index fingers extended | Right Click |

### Left Hand (Keyboard)
| Gesture | Action |
|---------|--------|
| Index and Middle fingers extended | `W` Key |
| Index, Middle, and Ring fingers extended | `S` Key |
| Pinky extended | `A` Key |
| Thumb extended | `D` Key |
| No fingers extended | `Space` Key |

## Notes
- The script detects both hands and assigns roles accordingly.
- Borders are set to avoid unintended mouse movement near screen edges.
- `pydirectinput.FAILSAFE = False` is used to prevent accidental stops.

## License
This project is open-source and free to use and modify.

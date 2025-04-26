import cv2
import mediapipe as mp
from music_controller import pause, play_next, play_previous, is_paused

class GestureController:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.prev_gesture = None
        self.cooldown = 0

    def count_fingers(self, landmarks):
        fingers = 0
        # Check fingers (excluding thumb for better reliability)
        for tip, pip in [(8,6), (12,10), (16,14), (20,18)]:  # Index to Pinky
            if landmarks.landmark[tip].y < landmarks.landmark[pip].y:
                fingers += 1
        return fingers

    def run(self):
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_frame)

            if results.multi_hand_landmarks:
                hand = results.multi_hand_landmarks[0]
                fingers = self.count_fingers(hand)

                if self.cooldown == 0:
                    if fingers == 0:  # Fist
                        pause()  # Toggles pause/resume
                        self.cooldown = 20
                    elif fingers == 2:  # Two fingers
                        play_next()
                        self.cooldown = 20
                    elif fingers == 1:  # One finger
                        play_previous()
                        self.cooldown = 20

                # Draw hand landmarks
                mp.solutions.drawing_utils.draw_landmarks(
                    frame, hand, self.mp_hands.HAND_CONNECTIONS)

            # Cooldown counter
            if self.cooldown > 0:
                self.cooldown -= 1

            # Display instructions
            cv2.putText(frame, "FIST: Pause/Resume", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(frame, "TWO FINGERS: Next", (10, 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(frame, "ONE FINGER: Previous", (10, 90),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            cv2.imshow('Gesture Control (ESC to quit)', frame)
            if cv2.waitKey(10) & 0xFF == 27:
                break

        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    GestureController().run()
# import cv2
# import mediapipe as mp
# from music_controller import playMusic, pause, play_next, play_previous, current_index, songs, is_paused

# class GestureController:
#     def __init__(self):
#         self.cap = cv2.VideoCapture(0)
#         self.mp_hands = mp.solutions.hands
#         self.hands = self.mp_hands.Hands(
#             max_num_hands=1,
#             min_detection_confidence=0.7,
#             min_tracking_confidence=0.5
#         )
#         self.prev_gesture = None
#         self.cooldown = 0

#     def detect_gesture(self, landmarks):
#         # Count extended fingers (thumb excluded for better palm detection)
#         extended_fingers = 0
#         for tip, pip in [(8,6), (12,10), (16,14), (20,18)]:  # Index to Pinky
#             if landmarks.landmark[tip].y < landmarks.landmark[pip].y:
#                 extended_fingers += 1

#         # Palm detection (4 fingers extended, thumb doesn't matter)
#         if extended_fingers == 4:
#             return "resume"
#         # Fist detection
#         elif extended_fingers == 0:
#             return "pause"
#         # Other gestures
#         elif extended_fingers == 2:
#             return "next"
#         elif extended_fingers == 1:
#             return "previous"
#         return None

#     def run(self):
#         while self.cap.isOpened():
#             ret, frame = self.cap.read()
#             if not ret:
#                 break

#             frame = cv2.flip(frame, 1)
#             rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             results = self.hands.process(rgb_frame)

#             if results.multi_hand_landmarks:
#                 hand = results.multi_hand_landmarks[0]
#                 gesture = self.detect_gesture(hand)

#                 if gesture and gesture != self.prev_gesture and self.cooldown == 0:
#                     if gesture == "resume" and is_paused:
#                         playMusic(songs[current_index])  # Resume current song
#                     elif gesture == "pause":
#                         pause()  # Toggles pause/resume
#                     elif gesture == "next":
#                         play_next()
#                     elif gesture == "previous":
#                         play_previous()

#                     self.prev_gesture = gesture
#                     self.cooldown = 20  # 20 frame cooldown

#                 # Draw hand landmarks
#                 mp.solutions.drawing_utils.draw_landmarks(
#                     frame, hand, self.mp_hands.HAND_CONNECTIONS)

#             # Cooldown counter
#             if self.cooldown > 0:
#                 self.cooldown -= 1
#             else:
#                 self.prev_gesture = None

#             # Display instructions
#             cv2.putText(frame, "PALM: Resume | FIST: Pause/Resume", (10, 30), 
#                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
#             cv2.putText(frame, "TWO FINGERS: Next | ONE FINGER: Previous", (10, 60),
#                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
#             cv2.imshow('Gesture Control (ESC to quit)', frame)
#             if cv2.waitKey(10) & 0xFF == 27:
#                 break

#         self.cap.release()
#         cv2.destroyAllWindows()

# if __name__ == "__main__":
#     GestureController().run()

import random
import pyttsx3
import speech_recognition as sr

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # voice 1 for female (Zira), 0 for male (David)
engine.setProperty("rate", 170)  # speed of voice

def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        r.energy_threshold = 300
        print("Listening...")
        try:
            audio = r.listen(source, timeout=10, phrase_time_limit=15)  # listen with timeout
        except sr.WaitTimeoutError:
            speak("Listening timed out while waiting for phrase to start. Please try again.")
            return "none"
        except sr.RequestError as e:
            speak(f"Could not request results; {e}")
            return "none"
        except sr.UnknownValueError:
            speak("Could not understand the audio, please speak clearly.")
            return "none"
        except Exception as e:
            speak(f"An error occurred: {e}")
            return "none"

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')  # Recognize speech
        print(f"user said: {query}")
    except sr.UnknownValueError:
        speak("Sorry, I did not get that. Please say that again.")
        return "none"
    except sr.RequestError as e:
        speak(f"Could not request results from Google Speech Recognition service; {e}")
        return "none"
    except Exception as e:
        speak(f"An error occurred during recognition: {e}")
        return "none"

    return query.lower()

def tic_tac_toe():
    board = [' ' for _ in range(9)]

    def print_board():
        print()
        for i in range(3):
            print(' | '.join(board[i * 3:(i + 1) * 3]))
            if i < 2:
                print("---------")
        print()

    def check_winner(player):
        win_positions = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                         (0, 3, 6), (1, 4, 7), (2, 5, 8),
                         (0, 4, 8), (2, 4, 6)]
        for pos in win_positions:
            if board[pos[0]] == board[pos[1]] == board[pos[2]] == player:
                return True
        return False

    speak("Welcome to Tic Tac Toe!")
    print_board()

    for turn in range(9):
        if turn % 2 == 0:
            while True:
                speak("Your turn, please say a position number from 1 to 9.")
                user_input = takecommand()
                position = None
                for word in user_input.split():
                    if word.isdigit() and 1 <= int(word) <= 9:
                        position = int(word) - 1
                        break
                if position is None:
                    speak("I did not hear a valid position number. Please try again.")
                    continue
                if board[position] != ' ':
                    speak("That position is already taken, please choose another.")
                    continue
                board[position] = 'X'
                break
        else:
            move = random.choice([i for i in range(9) if board[i] == ' '])
            board[move] = 'O'
            speak(f"I choose position {move + 1}")

        print_board()

        if check_winner('X'):
            speak("Congratulations! You win!")
            return
        elif check_winner('O'):
            speak("I win! Better luck next time.")
            return

    speak("It's a draw!")

def hangman():
    words = ["python", "assistant", "speech", "microphone", "intelligence"]
    word = random.choice(words).lower()
    guessed = set()
    tries = 6

    hangman_stages = [
        """
           -----
           |   |
           O   |
          /|\\  |
          / \\  |
               |
         =========
        """,
        """
           -----
           |   |
           O   |
          /|\\  |
          /    |
               |
         =========
        """,
        """
           -----
           |   |
           O   |
          /|\\  |
               |
               |
         =========
        """,
        """
           -----
           |   |
           O   |
          /|   |
               |
               |
         =========
        """,
        """
           -----
           |   |
           O   |
           |   |
               |
               |
         =========
        """,
        """
           -----
           |   |
           O   |
               |
               |
               |
         =========
        """,
        """
           -----
           |   |
               |
               |
               |
               |
         =========
        """
    ]

    speak("Let's play Hangman! You have 6 tries.")

    while tries > 0:
        display_word = ' '.join([letter if letter in guessed else '_' for letter in word])
        print(hangman_stages[6 - tries])
        print(f"Word: {display_word}")
        print(f"Guessed letters: {' '.join(sorted(guessed))}")
        print(f"Tries left: {tries}")
        speak("Guess a letter.")

        guess = input("Guess a letter: ").lower()

        if len(guess) != 1 or not guess.isalpha():
            speak("Please guess a single alphabet letter.")
            continue

        if guess in guessed:
            speak(f"You already guessed '{guess}'. Try another letter.")
            continue

        guessed.add(guess)

        if guess in word:
            speak(f"Good job! The letter '{guess}' is in the word.")
        else:
            tries -= 1
            speak(f"Wrong guess. You have {tries} tries left.")

        if all(letter in guessed for letter in word):
            print(f"\nCongratulations! You guessed the word: {word}")
            speak(f"Congratulations! You guessed the word: {word}")
            break
    else:
        print(hangman_stages[6])
        print(f"\nGame over! The word was: {word}")
        speak(f"Game over! The word was: {word}")

if __name__ == "__main__":
    while True:
        query = takecommand()
        if "i want to play" in query:
            speak("What would you like to play, sir?")
        elif "tic tac toe" in query:
            speak("Let's play Tic Tac Toe, sir.")
            tic_tac_toe()
        elif "hangman" in query:
            speak("Starting Hangman.")
            hangman()
        else:
            speak("Sorry, I didn't understand the game name. Please try again.")

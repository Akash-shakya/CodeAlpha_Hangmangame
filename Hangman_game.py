from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required to use sessions

def select_random_word():
    words = ["python", "hangman", "challenge", "laptop","alphabet", "code", "algorithm","keyboard"]
    return random.choice(words)

def display_current_progress(word, guessed_letters):
    return " ".join([letter if letter in guessed_letters else "_" for letter in word])

@app.route('/', methods=['GET', 'POST'])
def hangman():
    if 'word' not in session:
        session['word'] = select_random_word()
        session['guessed_letters'] = []
        session['incorrect_guesses'] = []
        session['max_attempts'] = 5

    word = session['word']
    guessed_letters = set(session['guessed_letters'])
    incorrect_guesses = set(session['incorrect_guesses'])
    max_attempts = session['max_attempts']

    if request.method == 'POST':
        guess = request.form.get('guess').lower()

        if len(guess) == 1 and guess.isalpha():
            if guess in guessed_letters or guess in incorrect_guesses:
                message = "You already guessed that letter."
            elif guess in word:
                guessed_letters.add(guess)
                session['guessed_letters'] = list(guessed_letters)  # Convert set to list for session storage
                message = "Good guess!"
            else:
                incorrect_guesses.add(guess)
                session['incorrect_guesses'] = list(incorrect_guesses)  # Convert set to list for session storage
                message = f"Incorrect guess. You have {max_attempts - len(incorrect_guesses)} attempts left."
        else:
            message = "Please guess a single letter."
        
    else:
        message = ""

    current_progress = display_current_progress(word, guessed_letters)

    if set(word) <= guessed_letters:
        message = f"Congratulations! You guessed the word: {word}"
        session.clear()
        return redirect(url_for('result', message=message))
    elif len(incorrect_guesses) >= max_attempts:
        message = f"Game over! The word was: {word}"
        session.clear()
        return redirect(url_for('result', message=message))

    return render_template('game.html', current_progress=current_progress, message=message)

@app.route('/result')
def result():
    message = request.args.get('message')
    return render_template('result.html', message=message)

if __name__ == "__main__":
    app.run(debug=True)

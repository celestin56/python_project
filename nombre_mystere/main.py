import tkinter as tk
from tkinter import messagebox
import random

class NumberGuessingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Jeu du Nombre Mystère")
        self.root.geometry("400x300")

        self.score = 100
        self.max_score = 100
        self.attempts = 0
        self.history = []

        self.number_to_guess = random.randint(1, 100)

        self.create_widgets()

    def create_widgets(self):
        # Label pour l'instruction
        self.label = tk.Label(self.root, text="Devinez le nombre entre 1 et 100.", font=("Arial", 14))
        self.label.pack(pady=10)

        # Champ de saisie pour la proposition
        self.entry = tk.Entry(self.root, font=("Arial", 14), width=20)
        self.entry.pack(pady=10)

        # Bouton pour valider la proposition
        self.validate_button = tk.Button(self.root, text="Valider", font=("Arial", 14), command=self.validate_guess)
        self.validate_button.pack(pady=10)

        # Label pour afficher le résultat
        self.result_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.result_label.pack(pady=10)

        # Label pour afficher le nombre d'essais
        self.attempts_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.attempts_label.pack(pady=10)

        # Label pour afficher le score
        self.score_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.score_label.pack(pady=10)

        # Bouton pour recommencer une partie
        self.restart_button = tk.Button(self.root, text="Recommencer", font=("Arial", 14), command=self.restart_game, state=tk.DISABLED)
        self.restart_button.pack(pady=10)

    def validate_guess(self):
        try:
            guess = int(self.entry.get())
            self.attempts += 1
            self.history.append(guess)

            if guess < self.number_to_guess:
                self.result_label.config(text="Plus grand !")
            elif guess > self.number_to_guess:
                self.result_label.config(text="Plus petit !")
            else:
                self.result_label.config(text="Gagné !")
                self.restart_button.config(state=tk.NORMAL)
                self.show_summary()

            self.score -= 10
            self.score_label.config(text=f"Score : {self.score}")

        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un nombre valide.")

        self.entry.delete(0, tk.END)
        self.attempts_label.config(text=f"Essais : {self.attempts}")

    def show_summary(self):
        summary = f"Nombre de coups utilisés : {self.attempts}\nScore final : {self.score}\nHistorique des propositions : {', '.join(map(str, self.history))}"
        messagebox.showinfo("Récapitulatif", summary)

    def restart_game(self):
        self.score = self.max_score
        self.attempts = 0
        self.history = []
        self.number_to_guess = random.randint(1, 100)
        self.result_label.config(text="")
        self.attempts_label.config(text="Essais : 0")
        self.score_label.config(text=f"Score : {self.score}")
        self.restart_button.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    game = NumberGuessingGame(root)
    root.mainloop()
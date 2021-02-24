import random

print("***  Gagnez contre l'ordinateur ***")

user_sante = 50
ia_sante = 50

nb_potion = 3

while True:

    user_attaque = random.randint(5, 10)
    ia_attaque = random.randint(5, 15)

    potion = random.randint(15, 50)

    user_choice = input("Souhaitez-vous attaquer (1) ou utiliser une potion (2) ? \n")

    if user_choice == "1":
        ia_sante = ia_sante - user_attaque

        if ia_sante <= 0:
            print("Bravo vous avez gagné\n")
            break

        user_sante = user_sante - ia_attaque

        if user_sante <= 0:
            print("Vous avez perdu")
            break

        print(f"vous avez infligé {user_attaque} points de degats à l'ennemi\n")
        print(f"L'ennemi vous a infligé {ia_attaque} points de degats\n")
        print(f"Vos points de vie : {user_sante}\n")
        print(f"Les points de vie de l'ennemi : {ia_sante}\n")
        continue

    if user_choice == "2" and nb_potion > 0:

        nb_potion = nb_potion - 1
        user_sante = user_sante + potion

        user_sante = user_sante - ia_attaque

        print(f"La potion vous fait gagner {potion} points de vie et il vous reste {nb_potion} potion(s)\n")
        print(f"L'ennemi vous a infligé {ia_attaque} points de degats\n")
        print(f"Vos points de vie : {user_sante}\n")

        if user_sante <= 0:
            print("Vous avez perdu\n")
            break

        ia_attaque = random.randint(5, 15)

        user_sante = user_sante - ia_attaque

        print("Repos du à la prise d'une potion \n")
        print(f"L'ennemi vous a infligé {ia_attaque} points de degats\n")
        print(f"Vos points de vie : {user_sante}\n")

        if user_sante <= 0:
            print("Vous avez perdu\n")
            break

        continue

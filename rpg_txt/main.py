import random

print("***  Affronte l'ordinateur ***")

nombre_mystere = random.randint(0,100)

user_sante= 50
ia_sante = 50

Nb_potion = 3





while user_sante > 0:

    user_attaque = random.randint(5,10)
    ia_attaque = random.randint(5,15)


    potion = random.randint(15,50)

    user_choice = input("Souhaitez-vous attaquer (1) ou utiliser une potion (2) ? ")

    if user_choice == "1":
        user_sante = user_sante - ia_attaque
        ia_sante = ia_sante - user_attaque
        print(f"vous avez infligé {user_attaque} points de degats à l'ennemi\n")
        print(f"L'ennemi vous a infligé {ia_attaque} points de degats\n")
        print(f"Vos points de vie : {user_sante}\n")
        print(f"Les points de vie de l'ennemi : {ia_sante}\n")


#ajout d'un commentaire 
import random

print("*** Le jeu du nombre mystére ***")

nombre_mystere = random.randint(0,100)



for i in [5,4,3,2,1,0]:

    if i != 0:

        print(f'Il te reste {i} essais\n')
        client_number = input("Devine le nombre : ")

        while not client_number.isdigit():
            print("Veuillez entrer un nombre valide\n")
            print(f'Il te reste {i} essais\n')
            client_number = input("Devine le nombre : ")
            continue

        client_number = int(client_number)

        if not client_number in range(0,100):
            print("Merci d'indiquer un nombre compri entre 0 et 100\n")
            continue

        elif client_number > nombre_mystere:
            print(f'Le nombre mystere est plus petit que {client_number}\n')
            continue

        elif client_number < nombre_mystere:
            print(f'Le nombre mystere est plus grand que {client_number}\n')
            continue

        elif client_number == nombre_mystere:
            print(f'Bravo vous avez trouvé le nombre mystere = {client_number}')
            break

        continue

    print(f'Dommage ! Le nombre mystere était {nombre_mystere}')

    break




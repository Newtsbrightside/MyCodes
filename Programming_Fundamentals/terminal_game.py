import random

print('Welcome to Terminal Zombie Apocalypse Survival Game! 🧟‍♂️')
play_again = 'y'
while play_again == 'y':
    print('\nYou are in a dark room. There is a door to your left and right. Which one do you take?')
    print('1) Left')
    print('2) Right')
    choice1 = input('Type 1 or 2: ')
    if choice1 == '1':
        print('You see a zombie! What do you do?')
        print('1) Fight')
        print('2) Run')
        choice2 = input('Type 1 or 2: ')
        if choice2 == '1':
            outcome = random.choice(['win', 'lose'])
            if outcome == 'win':
                print('You bravely fight the zombie and win! You find a treasure chest behind it.')
                print('You open the chest and find a map and a flashlight.')
                while True:
                    print('Do you want to take the map or the flashlight?')
                    print('1) Map')
                    print('2) Flashlight')
                    choice3 = input('Type 1 or 2: ')
                    if choice3 == '1':
                        print('You take the map. It shows a secret tunnel under the building.')
                        print('Do you want to search for the tunnel or explore upstairs?')
                        print('1) Search for tunnel')
                        print('2) Explore upstairs')
                        choice4 = input('Type 1 or 2: ')
                        if choice4 == '1':
                            print('You find the tunnel entrance hidden behind a bookshelf.')
                            print('It is dark inside. Do you want to enter?')
                            print('1) Enter tunnel')
                            print('2) Stay in the room')
                            choice5 = input('Type 1 or 2: ')
                            if choice5 == '1':
                                print('You crawl through the tunnel and find yourself in a laboratory.')
                                print('There are vials on the table. Do you want to investigate?')
                                print('1) Investigate vials')
                                print('2) Ignore and look for exit')
                                choice6 = input('Type 1 or 2: ')
                                if choice6 == '1':
                                    print('You find a vial labeled "Cure". Do you take it?')
                                    print('1) Take the cure')
                                    print('2) Leave it')
                                    choice7 = input('Type 1 or 2: ')
                                    if choice7 == '1':
                                        print('You take the cure. Suddenly, a scientist zombie appears!')
                                        print('Do you use the cure on the zombie or run?')
                                        print('1) Use cure')
                                        print('2) Run')
                                        choice8 = input('Type 1 or 2: ')
                                        if choice8 == '1':
                                            if random.random() < 0.7:
                                                print('The cure works! The zombie turns back into a human and thanks you.')
                                                print('He shows you a secret exit. You escape safely! You win! 🏆')
                                            else:
                                                print('The cure fails! The zombie attacks you. Game over! 💀')
                                            break
                                        elif choice8 == '2':
                                            print('You run, but the zombie catches you. Game over! 💀')
                                            break
                                        else:
                                            print('Invalid choice. Game over! 💀')
                                            break
                                    elif choice7 == '2':
                                        print('You leave the cure. The zombie scientist ignores you and you find an exit.')
                                        print('You escape, but the world remains overrun. To be continued...')
                                        break
                                    else:
                                        print('Invalid choice. Game over! 💀')
                                        break
                                elif choice6 == '2':
                                    print('You ignore the vials and look for an exit.')
                                    print('You find a door, but it is locked. Do you try to break it or search for a key?')
                                    print('1) Break door')
                                    print('2) Search for key')
                                    choice7 = input('Type 1 or 2: ')
                                    if choice7 == '1':
                                        if random.random() < 0.5:
                                            print('You break the door and escape! You survive! 🎉')
                                        else:
                                            print('You break the door, but the noise attracts zombies. Game over! 💀')
                                        break
                                    elif choice7 == '2':
                                        print('You find a key under a desk and escape quietly. You survive! 🎉')
                                        break
                                    else:
                                        print('Invalid choice. Game over! 💀')
                                        break
                                else:
                                    print('Invalid choice. Game over! 💀')
                                    break
                            elif choice5 == '2':
                                print('You stay in the room. Suddenly, more zombies break in. Game over! 💀')
                                break
                            else:
                                print('Invalid choice. Game over! 💀')
                                break
                        elif choice4 == '2':
                            print('You explore upstairs and find a radio.')
                            print('Do you try to call for help or search for supplies?')
                            print('1) Call for help')
                            print('2) Search for supplies')
                            choice5 = input('Type 1 or 2: ')
                            if choice5 == '1':
                                if random.random() < 0.5:
                                    print('You call for help. A rescue team hears you and comes to save you. You win! 🏆')
                                else:
                                    print('No one answers your call. You are alone. Game over! 💀')
                                break
                            elif choice5 == '2':
                                print('You find food and water, but zombies hear you. Game over! 💀')
                                break
                            else:
                                print('Invalid choice. Game over! 💀')
                                break
                        else:
                            print('Invalid choice. Game over! 💀')
                            break
                    elif choice3 == '2':
                        print('You take the flashlight. It helps you see in the dark hallway.')
                        print('You hear noises ahead. Do you investigate or hide?')
                        print('1) Investigate')
                        print('2) Hide')
                        choice4 = input('Type 1 or 2: ')
                        if choice4 == '1':
                            print('You find another survivor. Do you team up or go alone?')
                            print('1) Team up')
                            print('2) Go alone')
                            choice5 = input('Type 1 or 2: ')
                            if choice5 == '1':
                                if random.random() < 0.8:
                                    print('Together, you fight off zombies and escape through a window. You survive! 🎉')
                                else:
                                    print('Your new friend betrays you! Game over! 💀')
                                break
                            elif choice5 == '2':
                                print('Alone, you get surrounded by zombies. Game over! 💀')
                                break
                            else:
                                print('Invalid choice. Game over! 💀')
                                break
                        elif choice4 == '2':
                            print('You hide, but a zombie finds you. Game over! 💀')
                            break
                        else:
                            print('Invalid choice. Game over! 💀')
                            break
                    else:
                        print('Invalid choice. Game over! 💀')
                        break
                break
            else:
                print('You fight bravely, but the zombie is too strong. Game over! 💀')
        elif choice2 == '2':
            if random.random() < 0.6:
                print('You run away safely and find another exit. You survive! 🎉')
            else:
                print('You run, but trip and the zombie catches you. Game over! 💀')
        else:
            print('Invalid choice. Game over! 💀')
    elif choice1 == '2':
        print('You enter a room with two chests: one gold and one silver. Which one do you open?')
        print('1) Gold')
        print('2) Silver')
        choice2 = input('Type 1 or 2: ')
        if choice2 == '1':
            if random.random() < 0.3:
                print('The gold chest contains a powerful weapon! You are lucky!')
                print('You use it to escape the building. You win! 🏆')
            else:
                print('Oh no! The gold chest is a mimic and eats you! Game over! 💀')
        elif choice2 == '2':
            print('Woah you found a weapon! You can now fight zombies! Continue your adventure! 🗡️')
            print('Behind the chest, you see a door. It seems to lead outside.')
            print('You open the door and find the cities are overrun with zombies. What do you do?')
            print('1) Sneak through')
            print('2) Charge in')
            choice3 = input('Type 1 or 2: ')
            if choice3 == '1':
                print('You successfully sneak through the zombies and see a shelter.')
                print('You quickly enter the shelter and find other survivors.')
                print('You team up and plan a way to reclaim the city.')
                while True:
                    print('Do you want to lead the group or follow?')
                    print('1) Lead')
                    print('2) Follow')
                    choice4 = input('Type 1 or 2: ')
                    if choice4 == '1':
                        print('You lead a daring raid to gather supplies. It is risky!')
                        print('Do you raid the hospital or the police station?')
                        print('1) Hospital')
                        print('2) Police station')
                        choice5 = input('Type 1 or 2: ')
                        if choice5 == '1':
                            print('You find medical supplies but encounter a zombie horde. Do you fight or flee?')
                            print('1) Fight')
                            print('2) Flee')
                            choice6 = input('Type 1 or 2: ')
                            if choice6 == '1':
                                if random.random() < 0.7:
                                    print('You fight bravely and escape with supplies. The group survives another day! 🎉')
                                else:
                                    print('You are overwhelmed by zombies. Game over! 💀')
                                break
                            elif choice6 == '2':
                                print('You flee, but some group members are lost. Morale drops. To be continued...')
                                break
                            else:
                                print('Invalid choice. Game over! 💀')
                                break
                        elif choice5 == '2':
                            print('You find weapons at the police station and defend the shelter. You become a hero! 🏆')
                            break
                        else:
                            print('Invalid choice. Game over! 💀')
                            break
                    elif choice4 == '2':
                        print('You follow the leader and help fortify the shelter.')
                        print('Do you volunteer for night watch or help cook?')
                        print('1) Night watch')
                        print('2) Cook')
                        choice5 = input('Type 1 or 2: ')
                        if choice5 == '1':
                            if random.random() < 0.8:
                                print('On night watch, you spot zombies approaching and alert everyone. The shelter is saved!')
                            else:
                                print('You fall asleep on watch. The shelter is overrun! Game over! 💀')
                            break
                        elif choice5 == '2':
                            print('You cook a great meal and boost morale. The group survives another day! 🎉')
                            break
                        else:
                            print('Invalid choice. Game over! 💀')
                            break
                    else:
                        print('Invalid choice. Game over! 💀')
                        break
                break
            elif choice3 == '2':
                print('You charge into the zombies and fight bravely, but there are too many! Game over! 💀')
            else:
                print('Invalid choice. Game over! 💀')
        else:
            print('Invalid choice. Game over! 💀')
    else:
        print('Invalid choice. Game over! 💀')
    play_again = input('\nDo you want to play again? (y/n): ')
print('Thanks for playing!')
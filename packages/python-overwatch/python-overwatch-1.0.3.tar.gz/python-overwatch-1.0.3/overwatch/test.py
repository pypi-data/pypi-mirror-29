from __init__ import Overwatch

def main():
    overwatch = Overwatch(battletag="Okush#11324", hero="mei", filter="game")
 
    stats = overwatch()

    print(stats)


main()
import argparse
import random


class Player:
    """A base class object representing a player for the Pig game."""

    # constructor that sets player's default values
    def __init__(self):
        self.hold = False
        self.roll = False
        self.score = 0
        self.potential = 0


    def check_win(self):
        """ Player method that checks if the player has won the game."""
        if self.score >= 100:
            return True

    def reset_score(self):
        """A player method that resets the players score and potential score back to 0"""
        self.score = 0
        self.potential = 0


class ComputerPlayer(Player):
    """A class object representing a computer player for the Pig game."""

    def __init__(self, name):
        Player.__init__(self)
        self.name = name + ' (Computer)'

    def hold_or_roll(self):
        """A method to manage the holding or rolling of a die."""

        # check the choice and update the player hold and role values, or ask for a valid choice
        if (self.potential >= 25) or self.potential >= (100 - self.score):
            print('\n\t{} holds.'.format(self.name))
            self.hold = True
            self.roll = False
        else:
            print('\n\t{} rolls.'.format(self.name))
            self.hold = False
            self.roll = True


class HumanPlayer(Player):
    """A class object representing a human player for the Pig game."""

    def __init__(self, name):
        Player.__init__(self)
        self.name = name + ' (Human)'

    def hold_or_roll(self):
        """A method to manage the holding or rolling of a die."""

        # get player's choice on what they want to do
        choice = input('\nDo you want to HOLD ("h") or ROLL ("r") the die?: ')

        # check the choice and update the player hold and role values, or ask for a valid choice
        if choice.lower() == 'h':
            self.hold = True
            self.roll = False
        elif choice.lower() == 'r':
            self.hold = False
            self.roll = True
        else:
            print('\n\tINVALID choice! Please enter "h" or "r".')
            self.hold_or_roll()


class PlayerFactory:
    """A class object that creates the players of the games depending on argument inputs."""

    def create_player(self, arg, name):
        """A method that checks the player argument and creates specified player."""

        if arg == 'c':
            return ComputerPlayer(name)
        elif arg == 'h':
            return HumanPlayer(name)
        else:
            print('\n\tThere is a problem with your player arguments!')
            print('\t{} was entered as a player. Please use "c" for a Computer and "h" for Human.\n'.format(arg))


class Die:
    """ A class representing a die. """

    # initial constructor setting the default rolled value, range of numbers on the die, and initial seed
    def __init__(self):
        self.rolled = 0
        self.values = list(range(1, 7))
        random.seed(0)

    def roll(self):
        """ Die method that rolls the die. """
        self.rolled = random.choice(list(range(1, 7)))
        return self.rolled


class Game:
    """ A class that represent a game of Pig. """

    # initial constructor setting the default values for the game
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.players = [player1, player2]
        self.die = Die()
        self.max_score = 100
        self.highest_score = 0

        # create counter to track current player
        self.counter = 0

        # set current player
        self.current_player = self.players[self.counter]

        # loop to keep game running until a player wins, while currently player hasn't won
        while not self.current_player.check_win():

            # print statements that display game stats
            print('\nCurrent Player: {}'.format(self.current_player.name))
            print('*' * 25)
            print('Current Stats:')
            print('\tCurrent Score: {}\n\tPotential Score: {}\n\tHighest Score: {}'.format(
                self.current_player.score, self.current_player.score + self.current_player.potential, self.highest_score))
            print('*' * 25)
            print('Scoreboard:')

            # loop to print all current player scores
            for player in self.players:
                print('\t{}\'s Score: {}'.format(player.name, player.score))

            # call current player's method to hold or roll the die
            self.current_player.hold_or_roll()

            # if current player decides to roll the die
            if self.current_player.roll:

                # call function to clear the screen
                # clear()

                # roll the die and display the details
                self.die.roll()
                print('\n\t** {} rolled a {} **'.format(self.current_player.name, self.die.rolled))

                # check to see if a 1 was rolled, display a message if yes, then set the current player to the next one
                if self.die.rolled == 1:
                    self.current_player.potential = 0
                    self.counter += 1

                    # check to see if counter value is less than the number of players
                    if self.counter < len(self.players):

                        # set current player to the next player's index and print message
                        self.current_player = self.players[self.counter]
                        print('\tRolling a "1" ends your turn. It\'s now {}\'s turn'.format(self.current_player.name))

                    # if counter is greater than number of player, set counter and player back to first player in list
                    else:
                        self.counter = 0
                        self.current_player = self.players[self.counter]
                        print('\tRolling a "1" ends your turn. It\'s now {}\'s turn'.format(self.current_player.name))

                # for all other die values, add the rolled value to the running score
                else:
                    self.current_player.potential += self.die.rolled
                    print('\tHolding will add {} to your score.'.format(self.current_player.potential))

            # if current player decides to hold, update player and highest score, and reset running score
            else:
                self.current_player.score += self.current_player.potential
                self.current_player.potential = 0

                # check if player has highest score
                if self.current_player.score > self.highest_score:
                    self.highest_score = self.current_player.score

                # check to see if player wins and print message if True, then prompt to play again
                if self.current_player.check_win():
                    print('\n\tGAME OVER, {} WINS with {} points!\n'.format(
                        self.current_player.name, self.current_player.score))

                    print('Would you like to play again with same number of players?')
                    answer = input('Enter "Y", or else the game will exit: ')

                    # if yes, clear screen, reset scores, set counter back to 0, and set current player to player1
                    if answer.lower() == 'y':
                        clear()
                        for player in self.players:
                            player.reset_score()
                        self.highest_score = 0
                        self.counter = 0
                        self.current_player = self.players[self.counter]

                # update player values for the next players turn
                else:
                    self.counter += 1

                    # check to see if counter value is less than the number of players
                    if self.counter < len(self.players):

                        # set current player to the next player's index
                        self.current_player = self.players[self.counter]

                    # if counter value is not less than number of player, set counter and player back to first player
                    else:
                        self.counter = 0
                        self.current_player = self.players[self.counter]


def clear():
    """ Function that adds 100 new lines to clear the screen. """
    print('\n' * 50)


def main():
    """Main function that calls the Pig Game """

    # initialize the argument parser
    parser = argparse.ArgumentParser(description='Parser for number of players playing the Pig game.')
    parser.add_argument('--player1', default='h', type=str, help='Player type --> "h" for Human, "c" for computer')
    parser.add_argument('--player2', default='c', type=str, help='Player type --> "h" for Human, "c" for computer')
    parser.add_argument('--timed', default='n', type=str, help='Timed Game --> "y" for Yes and "n" for No')

    args = parser.parse_args()

    # create factory object and create players using the parsed arguments
    factory = PlayerFactory()
    player1 = factory.create_player(args.player1, 'Player 1')
    player2 = factory.create_player(args.player2, 'Player 2')

    # call game and pass in the 2 players
    Game(player1, player2)


if __name__ == '__main__':

    main()

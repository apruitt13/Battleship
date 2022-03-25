# Description: A battleship game. Battleship is a turn-based, strategy, guessing game for two players.
# Each player places warships on a grid and then take turns trying to torpedo the other players ships
# through guessing the coordinates of the ships. The first player to sink all of the other players
# ships wins the game.

class ShipGame:
    """A two player game where the players each place ships on a grid and then take turns trying
    to guess the location of the ships to destroy them."""

    def __init__(self):
        """ Initializes all data members."""
        self._player = "first"
        self._letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        self._nums = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
        self._player_one_ships = []
        self._player_two_ships = []
        self._current_state = "UNFINISHED"
        self._torpedo_status = None
        self._winner = None

    def place_ship(self, player, length, coord, orientation):
        """Method that takes the arguments the player, length of the ship, coordinates of the ship,
        and the ships orientation to set up the ships location for that player.To set up the game board
        so each player can place their ships on the grid. """
        if length < 2:
            return False
        if coord[0] not in self._letters:       # Checking to see if the coordinates are on the board.
            return False
        if coord[1] not in self._nums:          # Checking to see if the coordinates are on the board.
            return False

        # Checking to see if the move overlaps with any other coordinate.
        if player == "first":                                   # Adding to the first players board.
            position = 0                                        # Starting position to check the list's items.
            while position <= len(self._player_one_ships) - 1:  # Position is <= the number of items in the list.
                inside_list = 0                                 # The position of the nested list.
                for place in self._player_one_ships[inside_list]:   # Going through each item in the nested list.
                    if place == coord:                              # If the coord is found there is a ship there.
                        return False
                    inside_list += 1
                position += 1

        if player == "second":                                  # Same process as the first players board.
            position = 0
            while position <= len(self._player_two_ships) - 1:
                inside_list = 0
                for place in self._player_two_ships[inside_list]:
                    if place == coord:
                        return False
                    inside_list += 1
                position += 1

        # All the checks have been passed. At this point a move can be made.
        if player == "first":                               # First player placing.
            if orientation == "R":                          # Process for if it's a row.
                letter = coord[0]                           # Setting the letter. The first item in the coord string.
                new_ship = []                               # Empty list.
                pos_num = int(coord[1]) - 1                 # Changing the number of the coordinate to an integer.
                if pos_num + length > 10:  # Checks to see if the next coord is off the board.
                    return False
                # pos_num is the starting number. The number in the string minus one for the position in the _nums list.
                while length > 0:
                    new_ship.append(letter + self._nums[pos_num])   # Add to the list
                    pos_num += 1
                    length -= 1
                self._player_one_ships.append(new_ship)
                return True                                 # The ship has been placed correctly.

            else:                                           # Process for if it's a column.
                num = coord[1]                              # Setting the number.
                new_ship = []                               # An empty list that represents the ship.
                pos_alpha = self._letters.index(coord[0])   # Finding the index of the number for the starting point.
                if pos_alpha + length > 10:  # Checks to see if the next coord is off the board.
                    return False
                while length > 0:                           # Continue adding a new coord while the length is >0.
                    new_ship.append(self._letters[pos_alpha] + num)       # Add the coord to the empty list.
                    pos_alpha += 1                          # New letter.
                    length -= 1
                self._player_one_ships.append(new_ship)     # Adding the new ship to the player's board.
                return True

        # If not first then it's second player placing. It's the same process as for the first player.
        if player == "second":
            if orientation == "R":                          # If it's a row.
                letter = coord[0]
                new_ship = []
                pos_num = int(coord[1]) - 1
                if pos_num + length > 10:
                    return False
                while length > 0:
                    new_ship.append(letter + self._nums[pos_num])

                    pos_num += 1
                    length -= 1
                self._player_two_ships.append(new_ship)
                return True
            else:
                num = coord[1]                              # If it's a column.
                new_ship = []
                pos_alpha = self._letters.index(coord[0])
                if pos_alpha + length > 10:
                    return False
                while length > 0:
                    new_ship.append(self._letters[pos_alpha] + num)
                    pos_alpha += 1
                    length -= 1
                self._player_two_ships.append(new_ship)
                return True

    def get_current_state(self):
        """ Method that returns the current state of the game. Either "FIRST_WON", "SECOND_WON", or "UNFINISHED" """

        return self._current_state

    def fire_torpedo(self, player, coord):
        """ Purpose: A method that will "fire" a torpedo from one player to the other. It will record the
        move, update who's turn it is, and update the current state of the game. """
        empty_list = []                                                 # A variable for an empty list.

        if player == "first" and self._player == "second":              # Making sure it's the correct players turn.
            return False

        if player == "second" and self._player == "first":              # Making sure it's the correct players turn.
            return False

        if self._current_state == "FIRST_WON" or self._current_state == "SECOND_WON":   # Can't fire if a player won.
            return False

        if player == "first":                                       # First player's move.
            position = 0
            while position <= len(self._player_two_ships) - 1:      # Going through all of the nested lists.
                inside_list = 0
                for place in self._player_two_ships[inside_list]:   # Going through the items in the nested list.
                    if place == coord:
                        self._player_two_ships[inside_list].remove(coord)   # Removes the coord. If it's hit.
                    if len(self._player_two_ships[inside_list]) == 0:
                        self._player_two_ships.remove(empty_list)           # Removes an empty list if no more coord.
                inside_list += 1                                            # Next item in nested list.
                position += 1                                               # Next nested list.

            if len(self._player_one_ships) > 0 and len(self._player_two_ships) > 0:     # No one has won.
                self._current_state = "UNFINISHED"

            if len(self._player_one_ships) == 0 and len(self._player_two_ships) > 0:    # Second player won.
                self._current_state = "SECOND_WON"

            if len(self._player_one_ships) > 0 and len(self._player_two_ships) == 0:    # First player won.
                self._current_state = "FIRST_WON"
            self._player = "second"                                                     # Setting the next player.
            return True

        if player == "second":                                      # Second player's move.
            position = 0
            while position <= len(self._player_one_ships) - 1:      # Going through all of the nested lists.
                inside_list = 0
                for place in self._player_one_ships[inside_list]:   # Going through the items in the nested list.
                    if place == coord:
                        self._player_one_ships[inside_list].remove(coord)   # Removes the coord. If it's hit.
                    if len(self._player_one_ships[inside_list]) == 0:
                        self._player_one_ships.remove(empty_list)           # Removes an empty list if no more coord.
                inside_list += 1                                            # Next item in nested list.
                position += 1                                               # Next nested list.

            if len(self._player_one_ships) > 0 and len(self._player_two_ships) > 0:     # No one has won.
                self._current_state = "UNFINISHED"

            if len(self._player_one_ships) == 0 and len(self._player_two_ships) > 0:    # Second player won.
                self._current_state = "SECOND_WON"

            if len(self._player_one_ships) > 0 and len(self._player_two_ships) == 0:    # First player won.
                self._current_state = "FIRST_WON"
            self._player = "first"
            return True

    def get_num_ships_remaining(self, player):
        """To return the number of ships remaining for the player indicated. """
        if player == "first":                           # Return the number of ships player one has.
            return len(self._player_one_ships)
        else:
            return len(self._player_two_ships)          # Return the number of ships player two has.

    def get_player_one_ships(self):
        """Returns the ships that are on player one's board."""
        return self._player_one_ships                   # Returns the coordinates of the player's ships.

    def get_player_two_ships(self):
        """Returns the ships that are on player two's board."""
        return self._player_two_ships                   # Returns the coordinates of the player's ships.




game = ShipGame()
game.place_ship('first', 5, 'B2', 'C')
#game.place_ship('first', 2, 'I8', 'R')

print(game.get_player_one_ships())
print(game.get_player_two_ships())
print(game.fire_torpedo('first', 'I2'))
print(game.get_num_ships_remaining("first"))
print(game.get_num_ships_remaining("second"))

print(game.fire_torpedo('second', 'A1'))
print(game.fire_torpedo('first', 'H2'))



print(game.get_current_state())
print(game.fire_torpedo('second', 'G1'))
print(game.fire_torpedo('first', 'A10'))




'''
game = ShipGame()
print(game.place_ship("first", 4, "B2", "R"))
print(game.place_ship("first", 3, "A1", "C"))
print(game.get_player_one_ships())
print(game.place_ship("first", 4, "B4", "C"))
print(game.get_num_ships_remaining("first"))
print(game.get_player_one_ships())
'''
"""
Idea for checking if a coord is already in a list:
ship = [['B4', 'B5', 'B6', 'B7', 'B8'], ['F4', 'G4', 'H4', 'I4']]
#ship[0].remove('1B')
print(ship)
coord = "A5"
pos_num = int(coord[1])
#print(pos_num)
print(len(ship[0]))
position = 0
inside_list = 0
while position <= len(ship) - 1:
    for coord in ship[inside_list]:
        if coord == 'B7':
            print("yes")
        inside_list += 1
    inside_list += 1
    position += 1
"""
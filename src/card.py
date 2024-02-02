import os


class Card:
    suits = ["clubs", "diamonds", "hearts", "spades"]


    def __init__(self, suit: str, value: int, down=False):
        """
        Initializes a card with a specific suit, value, and face orientation.

        Parameters:
            suit (str): The suit of the card.
            value (int): The value of the card.
            down (bool): The orientation of the card (face up or face down).

        Returns:
            None
        """
        self.suit = suit
        self.value = value
        self.down = down
        self.symbol = self.name[0].upper()


    @property
    def name(self) -> str:
        """
        Retrieves the name of the card value.

        Returns:
            str: The name of the card value.
        """
        if self.value <= 10:
            return str(self.value)
        else:
            return {
                11: 'jack',
                12: 'queen',
                13: 'king',
                14: 'ace',
            }[self.value]


    @property
    def image(self):
        """
        Retrieves the image file name of the card.

        Returns:
            str: The image file name of the card.
        """
        return (
            f"{self.symbol if self.name != '10' else '10'}" \
            f"{self.suit[0].upper()}.png" \
            if not self.down else "red_back.png"
        )


    def flip(self):
        """
        Flips the orientation of the card.

        Returns:
            Card: The card object after flipping.
        """
        self.down = not self.down
        return self


    def __str__(self) -> str:
        """
        Retrieves a string representation of the card.

        Returns:
            str: A string representation of the card.
        """
        return f'{self.name.title()} of {self.suit.title()}'


    def __repr__(self) -> str:
        """
        Retrieves a string representation of the card (used for debugging).

        Returns:
            str: A string representation of the card.
        """
        return str(self)

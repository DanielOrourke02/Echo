

from eco_support import *


class Blackjack(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @staticmethod
    def hand_to_images(hand: List[Card]) -> List[Image.Image]:
        """
        Converts a hand of cards to a list of corresponding card images.

        Parameters:
            hand (List[Card]): List of cards in the hand.

        Returns:
            List[Image.Image]: List of card images.

        Note:
            - Reads card images from the 'src/cards/' directory.
        """
        return [
            Image.open(os.path.join('src/cards/', card.image))
            for card in hand
        ]



    @staticmethod
    def center(*hands: Tuple[Image.Image]) -> Image.Image:
        """
        Creates a blackjack table with cards placed.

        Parameters:
            *hands (Tuple[Image.Image]): A tuple of card images representing the hands to be placed on the table.

        Returns:
            Image.Image: The resulting image of the blackjack table with cards.

        Note:
            - The function uses a background table image ('src/pictures/table.png').
            - Cards from each hand are placed on the table.
            - The cards are arranged in a visually centered manner.
            - Cards are spaced vertically by 15 pixels and horizontally by 10 pixels.
        """
        bg: Image.Image = Image.open('src/pictures/table.png')  # Load table image
        bg_center_x = bg.size[0] // 2  # Calculate x position for center
        bg_center_y = bg.size[1] // 2  # Calculate y position for center

        img_w = hands[0][0].size[0]  # Get card image width
        img_h = hands[0][0].size[1]  # Get card image height

        # Calculate starting y position for hands placement
        start_y = bg_center_y - (((len(hands) * img_h) + ((len(hands) - 1) * 15)) // 2)

        for hand in hands:
            # Calculate starting x position for cards placement within a hand
            start_x = bg_center_x - (((len(hand) * img_w) + ((len(hand) - 1) * 10)) // 2)
            for card in hand:
                # Overlay card onto the background image
                bg.alpha_composite(card, (start_x, start_y))
                start_x += img_w + 10  # Move to the next card position horizontally
            start_y += img_h + 15  # Move to the next hand position vertically

        return bg  # Return the resulting image of the blackjack table with cards


    def check_bet(self, ctx, bet):
        """
        Checks if a bet is valid and deducts it from the user's balance.

        Parameters:
            ctx (commands.Context): The context of the command.
            bet (int): The bet amount.

        Returns:
            bool: True if the bet is valid, False otherwise.

        Note:
            - Checks if the user has sufficient balance for the bet.
            - If the bet is valid, deducts it from the user's balance.
        """
        user_id = ctx.author.id
        bal = get_user_balance(user_id)
        
        if bet > bal:
            return False  # Bet is invalid if it exceeds the user's balance
        elif bet <= bal:
            return True  # Bet is valid


    def output(self, name, *hands: Tuple[List[Card]]) -> None:
        """
        Generates and saves an image (to your pc/machine but is deleted once game is finished) of the blackjack table with the specified hands.

        Parameters:
            name (str): The name to be used for saving the image.
            *hands (Tuple[List[Card]]): Variable number of hands, each represented as a list of cards.

        Returns:
            None

        Note:
            - Calls the center method to create a visually centered blackjack table image with the given hands.
            - Saves the resulting image with the specified name.
        """
        self.center(*map(self.hand_to_images, hands)).save(f'{name}.png')



    @staticmethod
    def calc_hand(hand: List[List[Card]]) -> int:
        """
        Calculates the sum of the card values and accounts for aces.

        Parameters:
            hand (List[List[Card]]): List of hands where each hand is a list of cards.

        Returns:
            int: The calculated sum of card values.

        Note:
            - Assumes a standard deck of cards.
            - Handles the value of aces based on the total sum.
        """
        non_aces = [c for c in hand if c.symbol != 'A']
        aces = [c for c in hand if c.symbol == 'A']
        total_sum = 0
        for card in non_aces:
            if not card.down:
                if card.symbol in 'JQK':
                    total_sum += 10
                else:
                    total_sum += card.value
        for card in aces:
            if not card.down:
                if total_sum <= 10:
                    total_sum += 11
                else:
                    total_sum += 1
        return total_sum



    @commands.command(aliases=['bj', 'blackjacks'], brief="Play a simple game of blackjack.\nBet must be greater than $0", usage=f"blackjack <bet>")
    async def blackjack(self, ctx: commands.Context, bet: int=None):
        """
        Play a simple game of blackjack.

        Parameters:
            ctx (commands.Context): The context in which the command is called.
            bet (int): The amount of money to bet on the game.

        Usage:
            .blackjack <bet>

        Note:
            - Bet must be greater than $0.
            - Uses standard deck of cards.
            - The dealer will draw cards until their hand reaches 17 or higher.
            - Blackjack (21 points) results in a win with 1.5x the bet.
            - The game follows standard blackjack rules.

        Returns:
            None
        """
        # Error handling for incorrect usage
        if bet is None:
            embed = discord.Embed(
                title="Incorrect Usage",
                description=f"Please specify an amount to gamble. Usage: `{prefix}blackjack <amount>`",
                color=discord.Color.orange()
            )
            await ctx.send(embed=embed)
            return

        # Check if the user has enough balance for the bet
        if self.check_bet(ctx, bet) == False:
            bal = get_user_balance(ctx.author.id)
            embed = discord.Embed(
                title="BROKE ASF",
                description=f'You dont have enough money to place that bet. You currently have {bal} and you need {bet - bal} more.',
                color=embed_error
            )
            await ctx.send(embed=embed)
            return

        # Initialize deck and shuffle it
        deck = [Card(suit, num) for num in range(2,15) for suit in Card.suits]
        random.shuffle(deck)

        # Initialize player and dealer hands
        player_hand: List[Card] = []
        dealer_hand: List[Card] = []

        # Initial card dealing
        player_hand.append(deck.pop())
        dealer_hand.append(deck.pop())
        player_hand.append(deck.pop())
        dealer_hand.append(deck.pop().flip())

        player_score = self.calc_hand(player_hand)
        dealer_score = self.calc_hand(dealer_hand)

        async def out_table(**kwargs) -> discord.Message:
            """Sends a picture of the current table"""
            self.output(ctx.author.id, dealer_hand, player_hand)
            embed = make_embed(**kwargs)
            file = discord.File(
                f"{ctx.author.id}.png", filename=f"{ctx.author.id}.png"
            )
            embed.set_image(url=f"attachment://{ctx.author.id}.png")
            msg: discord.Message = await ctx.send(file=file, embed=embed)
            return msg

        # Reaction check function
        def check(
            reaction: discord.Reaction,
            user: Union[discord.Member, discord.User]
        ) -> bool:
            return all((
                str(reaction.emoji) in ("🇸", "🇭"),  # correct emoji
                user == ctx.author,                  # correct user
                user != self.bot.user,           # isn't the bot
                reaction.message == msg            # correct message
            ))

        standing = False

        while True:
            player_score = self.calc_hand(player_hand)
            dealer_score = self.calc_hand(dealer_hand)

            if player_score == 21:  # win condition
                bet = int(bet*1.5)
                update_user_balance(ctx.author.id, bet)
                result = ("Blackjack!", 'won')
                break
            
            elif player_score > 21:  # losing condition
                update_user_balance(ctx.author.id, bet*-1)
                result = ("Player busts", 'lost')
                break
            
            msg = await out_table(
                title="Your Turn",
                description=f"Your hand: {player_score}\n" \
                    f"Dealer's hand: {dealer_score}"
            )

            await msg.add_reaction("🇭")
            await msg.add_reaction("🇸")
            
            try:  # reaction command
                reaction, _ = await self.bot.wait_for(
                    'reaction_add', timeout=60, check=check
                )

            except asyncio.TimeoutError:
                await msg.delete()

            if str(reaction.emoji) == "🇭":
                player_hand.append(deck.pop())
                await msg.delete()
                continue

            elif str(reaction.emoji) == "🇸":
                standing = True
                break

        if standing:
            dealer_hand[1].flip()
            player_score = self.calc_hand(player_hand)
            dealer_score = self.calc_hand(dealer_hand)

            while dealer_score < 17:  # dealer draws until 17 or greater
                dealer_hand.append(deck.pop())
                dealer_score = self.calc_hand(dealer_hand)

            if dealer_score == 21:  # winning/losing conditions
                update_user_balance(ctx.author.id, bet*-1)
                result = ('Dealer blackjack', 'lost')
            elif dealer_score > 21:
                update_user_balance(ctx.author.id, bet*1)
                result = ("Dealer busts", 'won')
            elif dealer_score == player_score:
                result = ("Tie!", 'kept')
                update_user_balance(ctx.author.id, bet*1)
            elif dealer_score > player_score:
                update_user_balance(ctx.author.id, bet*-1)
                result = ("You lose!", 'lost')
            elif dealer_score < player_score:
                update_user_balance(ctx.author.id, bet*1)
                result = ("You win!", 'won')

        color = (
            discord.Color.red() if result[1] == 'lost'
            else discord.Color.green() if result[1] == 'won'
            else discord.Color.blue()
        )
        try:
            await msg.delete()
        except:
            pass
        msg = await out_table(
            title=result[0],
            color=color,
            description=(
                f"**You {result[1]} ${bet}**\nYour hand: {player_score}\n" +
                f"Dealer's hand: {dealer_score}"
            )
        )
        os.remove(f'./{ctx.author.id}.png')



    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{Fore.LIGHTGREEN_EX}{t}{Fore.LIGHTGREEN_EX} | Blackjacks Cog Loaded! {Fore.RESET}')


def blackjack_setup(bot: commands.Bot):
    bot.add_cog(Blackjack(bot))

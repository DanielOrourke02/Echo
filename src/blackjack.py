

from eco_support import *


class Blackjack(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @staticmethod
    def hand_to_images(hand: List[Card]) -> List[Image.Image]:
        return ([
            Image.open(os.path.join('src/cards/', card.image))
            for card in hand
        ])


    @staticmethod
    def center(*hands: Tuple[Image.Image]) -> Image.Image:
        """Creates blackjack table with cards placed"""
        bg: Image.Image = Image.open('src/pictures/table.png')
        bg_center_x = bg.size[0] // 2
        bg_center_y = bg.size[1] // 2

        img_w = hands[0][0].size[0]
        img_h = hands[0][0].size[1]

        start_y = bg_center_y - (((len(hands)*img_h) + \
            ((len(hands) - 1) * 15)) // 2)
        for hand in hands:
            start_x = bg_center_x - (((len(hand)*img_w) + \
                ((len(hand) - 1) * 10)) // 2)
            for card in hand:
                bg.alpha_composite(card, (start_x, start_y))
                start_x += img_w + 10
            start_y += img_h + 15
        return bg

    def check_bet(self, ctx, bet):
        user_id = ctx.author.id
        bal = get_user_balance(user_id)
        if bet > bal:
            return False
        elif bet < bal:
            update_user_balance(ctx.author.id, -bet)

    def output(self, name, *hands: Tuple[List[Card]]) -> None:
        self.center(*map(self.hand_to_images, hands)).save(f'{name}.png')


    @staticmethod
    def calc_hand(hand: List[List[Card]]) -> int:
        """Calculates the sum of the card values and accounts for aces"""
        non_aces = [c for c in hand if c.symbol != 'A']
        aces = [c for c in hand if c.symbol == 'A']
        sum = 0
        for card in non_aces:
            if not card.down:
                if card.symbol in 'JQK': sum += 10
                else: sum += card.value
        for card in aces:
            if not card.down:
                if sum <= 10: sum += 11
                else: sum += 1
        return sum


    @commands.command(aliases=['bj', 'blackjacks'], brief="Play a simple game of blackjack.\nBet must be greater than $0", usage=f"blackjack <bet>")
    async def blackjack(self, ctx: commands.Context, bet: int=None):
        if bet is None:
            embed = discord.Embed(
                title="Incorrect Usage",
                description=f"Please specify an amount to gamble. Usage: `{prefix}blackjack <amount>`",
                color=discord.Color.orange()
            )
            await ctx.send(embed=embed)
            return
        else:
            pass

        if self.check_bet(ctx, bet) == False:
            bal = get_user_balance(ctx.author.id)
            embed = discord.Embed(
                title="BROKE ASF",
                description=f'You dont have enough money to place that bet. You currently have {bal} and you need {bet - bal} more.',
                color=embed_error
            )
            await ctx.send(embed=embed)
        else:
            pass
        
        deck = [Card(suit, num) for num in range(2,15) for suit in Card.suits]
        random.shuffle(deck) # Generate deck and shuffle it

        player_hand: List[Card] = []
        dealer_hand: List[Card] = []

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
                update_user_balance(ctx.author.id, bet)
                result = ("Dealer busts", 'won')
            elif dealer_score == player_score:
                result = ("Tie!", 'kept')
                update_user_balance(ctx.author.id, bet)
            elif dealer_score > player_score:
                update_user_balance(ctx.author.id, bet*-1)
                result = ("You lose!", 'lost')
            elif dealer_score < player_score:
                update_user_balance(ctx.author.id, bet)
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
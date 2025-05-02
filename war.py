import random
import sys
from datetime import datetime
import os


#To represent each card

class Card:
    def __init__(self,value,suit=None,is_joker=False):
        self.value=value
        self.suit=suit
        self.is_joker=is_joker

    def __str__(self):
        if self.is_joker:
            return "Joker"

        value_names= { 2:'2' , 3:'3' , 4:'4' , 5:'5' , 6:'6' , 7:'7' , 8:'8' , 9:'9' , 10:'10' , 11:'J' , 12:'Q' , 13:'K' , 14:'A' }

        symbols= { "hearts": "♥" , "diamonds": "♦" , "clubs": "♣" , "spades": "♠" }

        return f'{value_names[self.value]}{symbols[self.suit]}'

    def __lt__(self,other):
        return self.value < other.value

    
#To manage a collection of cards
    
class PlayingDeck:
    def __init__(self, cards=None):
        self.cards=cards if cards else []

    def shuffle(self):         #function to shuffle the cards
        random.shuffle(self.cards)

    def drawing_card(self):  #function to draw a card
        if len(self.cards) > 0:
            return self.cards.pop(0)
        else:
            return None

    def store_card(self,card):   #store cards
        self.cards.append(card)

    def store_cards(self,cards):  #store cards
        self.cards.extend(cards)

    def count(self):       #to count the num of cards 
        return len(self.cards)


#Deck Creation Functions
    
class WarGame:
    def __init__(self,rounds=1):
        self.rounds = min(max(rounds,1),5) #to limit the rounds between 1 to 5
        self.players_cards = PlayingDeck()
        self.computer_cards = PlayingDeck()
        self.player_won_pile = PlayingDeck()
        self.computer_won_pile = PlayingDeck()
        self.game_history = []
        self.turn_records = []
        self.war_count = 0
        self.round_results = []
        self.all_round_turn_records = []
        
    def game_setup(self):
        self.players_cards = PlayingDeck()     #creating seprate decks for (win/in play)
        self.computer_cards = PlayingDeck()
        self.player_won_pile = PlayingDeck()
        self.computer_won_pile = PlayingDeck()
        
        full_deck = PlayingDeck()
        suits = ['hearts','diamonds','clubs','spades']

        for suit in suits:
            for value in range(2,15):
                full_deck.store_card(Card(value, suit))
                
        full_deck.store_card(Card(15, is_joker=True))
        full_deck.store_card(Card(15, is_joker=True))

        total_cards = full_deck.count()
        print(f"Total cards in Deck: {total_cards}".center(80))

        full_deck.shuffle() #shuffling the full deck

        give_to_player = True
        while full_deck.count() > 0:
            if give_to_player:
                self.players_cards.store_card(full_deck.drawing_card())
                give_to_player = False
            else:
                self.computer_cards.store_card(full_deck.drawing_card())
                give_to_player = True
                
        print("Cards shuffled and Distributed Among The two players\n".center(80))
        print(f"Human cards: {self.players_cards.count() }")
        print(f"Pc cards: {self.computer_cards.count() }\n\n")

         
    def handle_war(self,cards_in_play):      #war handling Function
        self.turn_records.append(" Additional war cards ")
        self.war_count += 1

        available_human_cards = self.players_cards.count()
        available_pc_cards = self.computer_cards.count()

        print(f"WAR Has Started!!!".center(80))
        message = f"\nHuman has {available_human_cards} cards and PC has {available_pc_cards} cards"
        print(message.center(80))

        if available_human_cards < 4 and self.player_won_pile.count() > 0:  #To get cards from the winning deck
            cards_needed = 4 - available_human_cards
            new_card_add = min(cards_needed,self.player_won_pile.count())
            if new_card_add > 0:
                print(f"Human Getting {new_card_add} cards from his won pile for this WAR")
                self.player_won_pile.shuffle()
                for _ in range(new_card_add):
                    self.players_cards.store_card(self.player_won_pile.drawing_card())
                available_human_cards = self.players_cards.count()

        if available_pc_cards < 4 and self.computer_won_pile.count() > 0:    #To get cards from the winning deck
            cards_needed = 4 - available_pc_cards
            new_card_add = min(cards_needed,self.computer_won_pile.count())
            if new_card_add > 0:
                print(f"PC Getting {new_card_add} cards from the won pile for the WAR")
                self.computer_won_pile.shuffle()
                for _ in range(new_card_add):
                    self.computer_cards.store_card(self.computer_won_pile.drawing_card())
                available_pc_cards = self.computer_cards.count()

        available_human_cards = self.players_cards.count()
        available_pc_cards = self.computer_cards.count()


        if available_human_cards == 0:               #if one player is only ran out of cards
            print("Human has no more cards - computer wins the war")
            return "pc"
        if available_pc_cards == 0:
            print("Computer has no more cards - Human wins the war")
            return "human"

        if available_human_cards < 4 and available_pc_cards < 4:      #if both players dont have enough cards for war
            print("Both players Don't have enough cards for a full war even after adding new cards")

            for _ in range(available_human_cards - 1):
                cards_in_play.append(self.players_cards.drawing_card())

            for _ in range(available_pc_cards - 1):
                cards_in_play.append(self.computer_cards.drawing_card())


            human_up_card = self.players_cards.drawing_card()
            pc_up_card = self.computer_cards.drawing_card()
            cards_in_play.extend([human_up_card,pc_up_card])

            print(f"Human final war card: {human_up_card}")
            print(f"PC final war card: {pc_up_card}")

            if human_up_card.value > pc_up_card.value:
                return "human"
            else:
                return "pc"

        human_face_down = min(3,available_human_cards - 1)
        pc_face_down = min(3,available_pc_cards -1)

        for _ in range(human_face_down):
            cards_in_play.append(self.players_cards.drawing_card())

        for _ in range(pc_face_down):
            cards_in_play.append(self.computer_cards.drawing_card())

        human_up_card = self.players_cards.drawing_card()
        pc_up_card = self.computer_cards.drawing_card()
        cards_in_play.extend([human_up_card,pc_up_card])
        print(f"Human war card: {human_up_card}")
        print(f"PC war card: {pc_up_card}")

        if human_up_card.value == pc_up_card.value:    #if there is another war occured
            print("It's Another WAR!!!")
            return self.handle_war(cards_in_play)
        elif human_up_card.value > pc_up_card.value:
            return "human"
        else:
            return "pc"
            

    def play_game(self):
        for round_num in range(1, self.rounds + 1):
            self.turn_records = []
            self.war_count = 0
            print(f"\n --- Round {round_num} ---")

            #To complete the assumpiton of After the second round The game Has to continue until player with the most cards runs out of cards
            
            if round_num == 1:  
                self.game_setup()
            else:
                print("Starting a new round")
                player_with_most_cards = "human" if human_started_with >= pc_started_with else "pc"
                print(f"{player_with_most_cards.capitalize()} started with the most cards")

            
                self.players_cards.store_cards(self.player_won_pile.cards)
                self.computer_cards.store_cards(self.computer_won_pile.cards)
                
                self.player_won_pile = PlayingDeck()
                self.computer_won_pile = PlayingDeck()

                self.players_cards.shuffle()
                self.computer_cards.shuffle()

                print(f"Human starts with {self.players_cards.count()} cards")
                print(f"Computer starts with {self.computer_cards.count()} cards")
                print(f"Total cards in play: {self.players_cards.count() + self.computer_cards.count()}")


            human_started_with = self.players_cards.count()
            pc_started_with = self.computer_cards.count()
            
            player_with_most_cards = None if round_num == 1 else ("human"if human_started_with >= pc_started_with else "pc")
            

            card_difference = abs(human_started_with - pc_started_with)

            turn = 1

            while True:
                if round_num == 1:
                    if self.players_cards.count() == 0 or self.computer_cards.count() == 0:
                        print(f"\nBoth Players Ran Out of cards. Round {round_num} complete.".center(80))
                        break
                else:
                    if player_with_most_cards == "human" and self.players_cards.count() == 0:
                        print(f"\nHuman (who started with most cards) is out of cards. Round {round_num} complete.".center(80))
                        break

                    if player_with_most_cards == "pc" and self.computer_cards.count() == 0:
                        print(f"\nComputer (who started with most cards) is out of cards. Round {round_num} complete.".center(80))
                        break

                if human_started_with < pc_started_with and self.players_cards.count() == 0:
                    if self.player_won_pile.count() > 0:
                        cards_needed = min(card_difference,self.player_won_pile.count())
                        print(f"Human is getting {cards_needed} cards from won pile")
                        self.player_won_pile.shuffle()
                        for _ in range(cards_needed):
                            if self.player_won_pile.count() > 0:
                                self.players_cards.store_card(self.player_won_pile.drawing_card())
                    else:
                        print("Human has no more cards to play")
                        break


                if pc_started_with < human_started_with and self.computer_cards.count() == 0:
                    if self.computer_won_pile.count() > 0:
                        cards_needed = min(card_difference,self.computer_won_pile.count())
                        print(f"Computer is getting {cards_needed} cards from won pile")
                        for _ in range(cards_needed):
                            if self.computer_won_pile.count() > 0:
                                self.computer_cards.store_card(self.computer_won_pile.drawing_card())

                    else:
                        print("Computer has no more cards to play. Ending Round.")
                        break

                if self.players_cards.count() == 0 or self.computer_cards.count() == 0:
                    print("One Player has no more cards to play. Ending Round.")
                    break
                
                #Console Ouput
                print(f"\nTurn {turn}:")


                human_card = self.players_cards.drawing_card()
                pc_card = self.computer_cards.drawing_card()

                cards_in_play = [human_card,pc_card]

                print(f"Player Puts: {human_card}")
                print(f"Computer Puts: {pc_card}")

                if human_card.value == pc_card.value:
                    self.turn_records.append(f"{turn} : {human_card} vs {pc_card} - WAR")

                    result = self.handle_war(cards_in_play)

                    if result == "human":
                        self.player_won_pile.store_cards(cards_in_play)
                        print(f"Player wins the war and gets {len(cards_in_play)} cards")
                    else:
                        self.computer_won_pile.store_cards(cards_in_play)
                        print(f"Computer wins the war and gets {len(cards_in_play)} cards")

                elif human_card.value > pc_card.value:
                    self.player_won_pile.store_cards(cards_in_play)
                    print(f"Player wins and gets 2 cards")
                    self.turn_records.append(f"{turn} : {human_card} vs {pc_card} - H")

                else:
                    self.computer_won_pile.store_cards(cards_in_play)
                    print(f"Computer wins and gets 2 cards")
                    self.turn_records.append(f"{turn} : {human_card} vs {pc_card} -P")


                turn += 1

            human_card_count = self.players_cards.count() + self.player_won_pile.count()
            pc_card_count = self.computer_cards.count() + self.computer_won_pile.count()
            total_cards = human_card_count + pc_card_count

            print(f"\nRound {round_num} Complete!")
            print(f"Human cards: {self.players_cards.count()} in hand, {self.player_won_pile.count()} in won pile")
            print(f"Computer cards: {self.computer_cards.count()} in hand, {self.computer_won_pile.count()} in won pile")
            print(f"Total cards in play: {total_cards}")


            self.all_round_turn_records.append(self.turn_records.copy())


            round_winner = "PC" if pc_card_count > human_card_count else "Human" if human_card_count > pc_card_count else "Tie"
            self.round_results.append({"round": round_num,
                                       "human_cards": human_card_count,
                                       "pc_cards": pc_card_count,
                                       "war_count": self.war_count,
                                       "winner": round_winner})

            print("\n----- ROUND SUMMARY -----")
            print(f"Round {round_num} results")
            print("NO : Hum vs PC - Winner")

            turn_number = 1

            for turn_record in self.turn_records:
                if ":" in turn_record:
                    turn_content = turn_record.split(":",1)[1].strip()
                    print(f"{turn_number} : {turn_content}")
                    turn_number += 1
                else:
                    print(turn_record)

            print("\nPC card count",pc_card_count)
            print("Human card count",human_card_count)
            print("War count",self.war_count)

            if pc_card_count > human_card_count:
                print("\nPC won the round!")
            elif human_card_count > pc_card_count:
                print("\nHuman won the round!")
            else:
                print("\nTie")


        pc_wins = sum(1 for r in self.round_results if r["winner"] == "PC")
        human_wins = sum(1 for r in self.round_results if r["winner"] == "Human")

        print("\n---YOUR GAME HAS FINISHED---")
        print(f"Rounds played: {self.rounds}")
        print(f"PC won {pc_wins} rounds")
        print(f"Human won {human_wins} rounds")

        if pc_wins > human_wins:            #To Find the Overall winner of all the rounds
            print("\nPC won the Game")
            overall_winner = "PC"
        elif human_wins > pc_wins:
            print("\nHuman won the Game")
            overall_winner = "Human"
        else:
            print("\nThe Game is a Tie")
            overall_winner = "Tie"

        return overall_winner

    def save_game_log(self):     #save to text file
        time = datetime.now()
        random_num = random.randint(1000,9999)
        date_str = time.strftime("%Y%m%d")
        time_str = time.strftime("%H-%M")

        filename = f"{date_str}_{time_str}_{random_num}.txt"

        with open(filename, 'w' , encoding = 'utf-8' ) as f:
            f.write("       WAR GAME         ")
            time = datetime.now()
            f.write(f"Date : {time.strftime('%Y-%m-%d')}\n")
            f.write(f"Time : {time.strftime('%H:%M')}\n\n")
            f.write(f"Total Rounds : {self.rounds}\n\n")

            for round_num in range(1,self.rounds + 1):
                round_data = self.round_results[round_num - 1]
                round_turns = self.all_round_turn_records[round_num - 1]

                f.write("Round Results\n")
                f.write("NO : PC VS H - Winner\n")
            
                turn_number = 1

                for turn in round_turns:
                    if ":" in turn:
                        turn_content = turn.split(":",1)[1].strip()
                        f.write(f"{turn_number} : {turn_content}\n")
                        turn_number += 1
                    else:
                        f.write(f"{turn}\n")

                    
                f.write(f"{turn}\n")
                f.write(f"PC card count {round_data['pc_cards']}\n")
                f.write(f"Human card count {round_data['human_cards']}\n")
                f.write(f"War count {round_data['war_count']}\n\n")
          
                if round_data['winner'] == "PC":
                    f.write("PC Won The Round\n\n")
                elif round_data['winner'] == "Human":
                    f.write("Human Won The Round\n\n")
                else:
                    f.write("It's a Tie\n\n")

                f.write("------------------------\n\n")

            return filename


    def save_html_log(self,txt_filename):       #save to html file
        html_filename = txt_filename.replace('.txt','.html')
        time = datetime.now()

        html_content = f"""<!DOCTYPE html>
    <html>
    <head>
        <title> War Card Game - {time.strftime('%Y-%m-%d')} </title>
        <style>
            body {{ font-family: Consolas, monospace; line-height: 1.5; margin: 20px; }}
            h1 {{ color: #333; }}
            -header {{ background - color: #333; color:white; padding: 2px 10px; }}
            -menu {{ color: #666; margin-bottom: 15px; }}
            -game-history {{ font-family: consolas, monospace; }}
            -war {{ color:red; font-weight:bold; }}
            -winner {{ color: green; font-weight: bold; }}
            table {{ border-collapse: collapse; width: 100%;margin:15px 0; }}
            td, th {{ padding: 5px; text-allign: left; }}
            .round-summary {{ background-color: #f0f0f0; padding: 10px; margin-bottom: 20px; }}
            .round-header {{ background-color: #333; color: white; padding: 5px 10px; margin-top: 20px; }}
            .round-separator {{ border-top: 2px solid #333; margin: 20px 0; }}
        </style>
    </head>
    <body>
        <div class="header"> WAR GAME </div>

        <div class="game-history">
            <p>Date : {time.strftime('%Y-%m-%d') } </p>
            <p>Time : {time.strftime('%H:%M') } </p>
            <p>Total Rounds : {self.rounds}</p>

    """
        for round_num in range(1,self.rounds + 1):
            round_data = self.round_results[round_num - 1]
            round_turns = self.all_round_turn_records[round_num - 1]


            html_content += f"""<div class="round-header">Round {round_num} results</div>
                                <div class="round-summary">
                                    <p>No : Hum vs PC - Winner</p>"""
            turn_number = 1
            
            for turn in round_turns:
                if ":" in turn:
                    turn_content = turn.split(":",1)[1].strip()

                    if "WAR" in turn_content:
                        html_content += f'<p class="war">{turn_number} : {turn_content}</p>\n'
                    else:
                        html_content += f'<p>{turn_number} : {turn_content}</p>\n'

                    turn_number += 1

                else:
                    html_content += f'<p>{turn}</p>\n'
                

            html_content += f"""
            <p>PC card count {round_data['pc_cards']}</p>
            <p>Human card count {round_data['human_cards']}</p>
            <p>War Count {round_data['war_count']}</p>

            <p class="winner">"""


            if round_data['winner'] == "PC":
                html_content += "PC won the round!"
            elif round_data['winner'] == "Human":
                html_content += "Human won the round!"
            else:
                html_content += "Round ended in a tie!"

            html_content += """</p>
            </div>
            <div class="round-separator"></div> """

        pc_wins = sum(1 for r in self.round_results if r["winner"] == "PC")
        human_wins = sum(1 for r in self.round_results if r["winner"] == "Human")

        html_content += f"""
            <div class="round-header">Game Summary</div>
            <div class="winner round-summary">
                <p>PC won {pc_wins} rounds</p>
                <p>Human won {human_wins} rounds</p>
        """

        if pc_wins > human_wins:
            html_content += "<p><strong>PC Won The Game</strong></p>"
        elif human_wins > pc_wins:
            html_content += "<p><strong>Human Won The Game</strong></p>"
        else:
            html_content += "<p><strong>It's a Tie</strong></p>"

        html_content += """
            </div>
            <hr>
        </div>
    </body>
    </html>
    """

        with open(html_filename, 'w' , encoding='utf-8') as f:
            f.write(html_content)

        return html_filename
    
def main():         #main function to run the game
    if len(sys.argv) > 1:
        try:
            rounds = int(sys.argv[1])
            if not (1<= rounds <=5):
                print("Please a Value between 1 to 5.(ex:war 3)")
                return
            game = WarGame(rounds)
        except ValueError:
            print("Please a Value between 1 to 5.(ex:war 3)")
            return
    else:
        game = WarGame()


    game.play_game()

    txt_filename = game.save_game_log()

    try:
        html_filename = game.save_html_log(txt_filename)
    except Exception as e:
        pass

if __name__ == "__main__":
    main()

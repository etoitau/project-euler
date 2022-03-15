from functools import total_ordering
from typing import Callable, Dict, Tuple, List
from random import shuffle

@total_ordering
class CardProperty:
    """ Property of a card like suit or rank
    These are typically not numerical, so give an ordinal value for comparason
    """

    def __init__(self, name: str, ordinal: int):
        self.name = name
        self.ordinal = ordinal

    def _is_valid_operand(self, other):
        return (hasattr(other, "name") and
                hasattr(other, "ordinal"))

    def __eq__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return self.ordinal == other.ordinal
    
    def __lt__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return self.ordinal < other.ordinal
    
    def __str__(self) -> str:
        return self.name

@total_ordering
class Card:
    """ A card has a suit and a rank
    A comparason function can be provided on construction
    or by default comparason will look at card rank ordinal only
    """
    def __init__(self, suit: CardProperty, value: CardProperty, comp: Callable[["Card", "Card"], int] = None) -> None:
        self.suit = suit
        self.rank = value
        self.comp = (lambda c1, c2: c1.value.ordinal - c2.value.ordinal) if not comp else comp
    
    def __lt__(self, other):
        return self.comp(self, other) < 0
    
    def __eq__(self, other):
        return self.comp(self, other) == 0
    
    def __str__(self) -> str:
        return self.suit.name + self.rank.name

    def __repr__(self) -> str:
        return self.__str__()

class PokerDeck:
    """ A collection of cards following poker rules """

    suit_names = { "H": 1, "C": 2, "S": 3, "D": 4 }
    rank_names = { "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10, "J": 11, "Q": 12, "K": 13, "A": 14 }

    def __init__(self):
        # The cards
        self.card_list: List[Card] = []
        # Keep track of what card values are in the deck
        self.value_frequencies: Dict[int, int] = {}
        # Keep track of if the deck is sorted so we can lazy sort
        self.is_sorted = False

    def sort(self):
        if not self.is_sorted:
            self.card_list.sort()
        self.is_sorted = True
    
    def add_card(self, suit: str, rank: str) -> None:
        self.is_sorted = False
        new_card = Card(
            CardProperty(suit, self.suit_names[suit]), 
            CardProperty(rank, self.rank_names[rank]), 
            lambda card1, card2: self.card_comp(card1, card2))
        self.card_list.append(new_card)
        if new_card.rank.ordinal in self.value_frequencies:
            self.value_frequencies[new_card.rank.ordinal] += 1
        else:
            self.value_frequencies[new_card.rank.ordinal] = 1

    def deal_one(self) -> Card:
        self.is_sorted = False
        popped = self.card_list.pop()
        self.value_frequencies[popped.rank.ordinal] -= 1
        return popped

    def shuffle(self) -> None:
        self.is_sorted = False
        shuffle(self.card_list)

    def set_full(self) -> None:
        """ Generate a full deck """
        self.is_sorted = False
        self.card_list = []
        self.value_frequencies = {}
        for suit_name in self.suit_names:
            for rank_name in self.rank_names:
                self.add_card(suit_name, rank_name)

    def card_comp(self, card1: Card, card2: Card) -> int: 
        """ The rule by which cards in this deck should be compared """
        return card1.rank.ordinal - card2.rank.ordinal

    def __str__(self) -> str:
        return " ".join([str(card) for card in self.card_list])
    
    def __repr__(self) -> str:
        return self.__str__()

class Hand(PokerDeck):
    """ A collection of cards with methods for determining Poker value """

    def high_card(self) -> Card:
        # Would be more efficient to just scan for highest value, but a call 
        # to this is often followed by other methods which can make use of sort 
        self.sort()
        return self.card_list[-1]

    def pairs(self) -> List[int]:
        """ Return ordinal values of any pairs """
        result = []
        for v in self.value_frequencies:
            if self.value_frequencies[v] == 2:
                result.append(v)
        return result

    def n_of_a_kind(self) -> Tuple[int, int]:
        """ Returns (highest frequency rank, value of that rank) """
        highest = [0, 0]
        for v in self.value_frequencies:
            if self.value_frequencies[v] > highest[0]:
                # if more of this type of card than any we've seen
                highest = [ self.value_frequencies[v], v ]
            elif self.value_frequencies[v] == highest[0]:
                # if same as best we've seen, see if higher value
                if v > highest[1]:
                    highest[1] = v
        return (highest[0], highest[1])

    def has_flush(self) -> bool:
        if len(self.card_list) < 5:
            return False
        suit = self.card_list[-1].suit
        for c in self.card_list:
            if c.suit != suit:
                return False
        return True

    def has_straight(self) -> bool:
        high = self.high_card().rank.ordinal
        straight = True
        for offset in range(1, len(self.card_list)):
            if (high - offset) not in self.value_frequencies:
                straight = False
                break
        if not straight and high == Hand.rank_names["A"]:
            straight = True
            for v in range(Hand.rank_names["2"], Hand.rank_names["6"]):
                if v not in self.value_frequencies:
                    straight = False
                    break
        return straight

    def hand_value(self) -> float:
        """ Returns a value for the current hand:
        Ten-thousands place tells what hand has been achieved
        Hundreds place is sometimes used to tell the rank ordinal of the hand
        Ones place is used in the case where more than one rank is needed
        Decimal is a tiebreaker which represents the values of all cards
        in the hand
        """
        STRAIGHT_FLUSH = 90000 
        FOUR_OF_KIND   = 80000 
        FULL_HOUSE     = 70000 
        FLUSH          = 60000
        STRAIGHT       = 50000
        THREE_OF_KIND  = 40000
        TWO_PAIR       = 30000
        ONE_PAIR       = 20000

        has_flush = self.has_flush()
        has_straight = self.has_straight()
        high_value = self.high_card().rank.ordinal

        if has_straight and has_flush:
            return STRAIGHT_FLUSH + high_value
        
        n_of_a_kind = self.n_of_a_kind()

        if n_of_a_kind[0] == 4:
            value = FOUR_OF_KIND + n_of_a_kind[1] * 100
            # It shouldn't be possible in a standard deck for two players to 
            # both have a four of a kind of the same rank, but add the fifth
            # card just in case
            if high_value == n_of_a_kind[1]:
                return value + self.card_list[0].rank.ordinal
            else:
                return value + high_value

        pairs = self.pairs()
        if n_of_a_kind[0] == 3 and len(pairs):
            return FULL_HOUSE + n_of_a_kind[1] * 100 + pairs[0]

        if has_flush:
            return FLUSH + self.value_tiebreaker()
        
        if has_straight:
            return STRAIGHT + high_value
        
        if n_of_a_kind[0] == 3:
            return THREE_OF_KIND + n_of_a_kind[1] * 100 + self.value_tiebreaker()
        
        if len(pairs) == 2:
            return TWO_PAIR + max(pairs) * 100 + min(pairs) + self.value_tiebreaker()

        if len(pairs):
            return ONE_PAIR + pairs[0] * 100 + self.value_tiebreaker()

        return self.value_tiebreaker()

    def value_tiebreaker(self) -> float:
        """ A decimal representing the value of all cards in the hand """
        self.card_list.sort()
        values = [ c.rank.ordinal for c in self.card_list ]
        m: float = 1
        base = PokerDeck.rank_names["A"] + 1
        tiebreaker: float = 0
        for value in reversed(values):
            m /= base
            tiebreaker += m * value
        return tiebreaker

if __name__ == '__main__':
    """starts here"""
    hand_one = Hand()
    hand_one.add_card("H", "A")
    hand_one.add_card("H", "A")
    hand_one.add_card("H", "J")
    hand_one.add_card("C", "K")
    hand_one.add_card("H", "9")
    
    print(hand_one.pairs())
    print(hand_one.hand_value())

from dataclasses import dataclass
import re


@dataclass
class Amount:
    dollars: int
    cents: int = 0
    negative: bool = True
    
@dataclass
class Category:
    name: str
    is_external: bool

@dataclass
class Transaction:
    real_description: str
    display_description: str
    date: str
    amount: Amount
    category: Category = None

    def set_category(self, category: str):
        self.category = category

    def __str__(self) -> str:
        date_str = self.date.ljust(10)

        amount_prefix = '-' if self.amount.negative else ' '
        amount_str = f'{amount_prefix}{self.amount.dollars}.{self.amount.cents}'.ljust(20)

        desc = self.display_description[:55]
        category = self.category.name.rjust(20) if self.category else ''

        return f'{date_str}:\t{amount_str}\t{desc: <55}{category}'
    
class Categorizer:
    def __init__(self, pattern: str, category: Category, amount : Amount = None) -> None:
        self._compiled_pattern = re.compile(pattern)
        self._category = category
        self._amount = amount

    def run(self, transaction: Transaction):
        if (
            self._compiled_pattern.match(transaction.real_description)
            and (self._amount is None or transaction.amount == self._amount)
        ):
            transaction.category = self._category

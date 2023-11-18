from abc import ABC, abstractmethod
import csv
from typing import List

from database.interface import Repository
import models


class BaseImporter:
    
    @classmethod
    def import_transactions(cls, file_name):
        parser = AlliantFileParser(file_name)
        rule_list = Repository.load_category_rules()
        
        for item in parser.read_transactions():
            for rule in rule_list:
                rule.run(item)

            if not item.category or item.category.is_external:
                print(item)
                
        # get the transactions from the file
        
        # check the database to see if we have them already or not
        
        # if we don't already have the transaction
        #   store it


class BaseFileParser:
    def __init__(self, file_name: str) -> None:
        self._file_name = file_name

    def read_transactions(self) -> List[models.Transaction]:
        results = []
        with open(self._file_name) as file:
            reader = csv.DictReader(file)
            for line_item in reader:
                results.append(self._parse_line_item(line_item))

        return results

    @abstractmethod
    def _parse_line_item(self, line_item) -> models.Transaction:
        ...

    def _clean_description(self, file_desc: str) -> str:
        return file_desc.replace('\n', ' ')
    
    def _parse_amount(self, amount_str: str) -> models.Amount:
        is_negative = amount_str[0] == '-'
        if is_negative:
            amount_str = amount_str[1:]

        dollars, cents = [int(value) for value in amount_str.split('.')]
        return models.Amount(
            negative=is_negative,
            dollars=dollars,
            cents=cents
        )

class AlliantFileParser(BaseFileParser):
    def _parse_line_item(self, line_item) -> models.Transaction:
        clean_description = self._clean_description(line_item['Description'])
        amount = self._parse_amount(line_item['Amount'])

        return models.Transaction(
            date=line_item['Date'],
            real_description=line_item['Description'],
            display_description=clean_description,
            amount=amount
        )
    
    def _parse_amount(self, amount_str: str) -> models.Amount:
        clean_str = amount_str.replace('$', '')
        
        # find negativity
        if clean_str[0] == '(' and clean_str[-1] == ')':
            clean_str = f'-{clean_str[1:-1]}'

        return super()._parse_amount(clean_str)

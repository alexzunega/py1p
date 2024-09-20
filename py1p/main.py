import json
import subprocess


class CreditCard:
    def __init__(self, cc_id):
        result = subprocess.run(
            args=['op', 'item', 'get', cc_id, '--format', 'json'],
            capture_output=True, text=True, check=True)
        self._data = json.loads(result.stdout)
        self._fields = {e['id']: e for e in self._data['fields']}

    @property
    def title(self):
        return self._data['title']

    @property
    def number(self):
        return self._fields['ccnum']['value']

    @property
    def expiry(self):
        return self._fields['expiry']['value']

    @property
    def cvv(self):
        return self._fields['cvv']['value']

    def __repr__(self):
        return f"CreditCard(id={self._data['id']!r}"

    def __str__(self):
        return (f"CreditCard: {self.title}, Number: {self.number}, "
                f"Expiry: {self.expiry}, CVV: {self.cvv}")


class OnePassword:

    @property
    def credit_cards(self) -> list[CreditCard]:
        result = subprocess.run(
            ["op", "item", "list", "--categories", "Credit Card", "--format", "json"],
            capture_output=True, text=True, check=True
        )
        data = json.loads(result.stdout)

        return [CreditCard(e['id']) for e in data]

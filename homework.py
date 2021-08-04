import datetime as dt


class Record:
    """Класс записи вводной информации из конца кода."""
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is not None:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()
        else:
            self.date = dt.date.today()


class Calculator(Record):
    """Родительский класс для калькуляторов калорий и денег."""
    def __init__(self, limit=None):
        self.limit = limit
        if limit is None:
            limit == 0
        else:
            limit = limit
        self.records = []

    def add_record(self, new_record):
        self.records.append(new_record)

    def get_today_stats(self):
        stats = 0
        for record in self.records:
            if record.date == dt.date.today():
                stats = stats + record.amount
        return stats

    def get_week_stats(self):
        today = dt.date.today()
        week_date = today - dt.timedelta(days=7)
        return (sum(i.amount for i in self.records
                if today >= i.date >= week_date))


class CashCalculator(Calculator):
    RUB_RATE = 1
    USD_RATE = 72.80
    EURO_RATE = 86.50

    """Класс обработки информации по денежному калькулятору."""
    def get_today_cash_remained(self, currency):
        currencies = {'rub': ('руб', self.RUB_RATE),
                      'usd': ('USD', self.USD_RATE),
                      'eur': ('Euro', self.EURO_RATE)}
        cash_remained = self.limit - self.get_today_stats()
        if currency not in currencies:
            return 'Неопознанная валюта'
        cash_remained = self.limit - self.get_today_stats()
        cash_remained_rub = round(cash_remained / currencies['rub'][1], 2)
        currencies_rub = currencies['rub'][0]
        cash_remained_usd = round(cash_remained / currencies['usd'][1], 2)
        currencies_usd = currencies['usd'][0]
        cash_remained_eur = round(cash_remained / currencies['eur'][1], 2)
        currencies_eur = currencies['eur'][0]
        _ash_remained_rub = abs(round(cash_remained / currencies['rub'][1], 2))
        currencies_rub = currencies['rub'][0]
        _ash_remained_usd = abs(round(cash_remained / currencies['usd'][1], 2))
        currencies_usd = currencies['usd'][0]
        _ash_remained_eur = abs(round(cash_remained / currencies['eur'][1], 2))
        currencies_eur = currencies['eur'][0]
        if currency == 'rub' and cash_remained > 0:
            return f"На сегодня осталось {cash_remained_rub} {currencies_rub}"
        elif currency == 'usd' and cash_remained > 0:
            return f"На сегодня осталось {cash_remained_usd} {currencies_usd}"
        elif currency == 'eur' and cash_remained > 0:
            return f"На сегодня осталось {cash_remained_eur} {currencies_eur}"
        elif currency == 'rub' and cash_remained < 0:
            return (f"Денег нет, держись: твой долг - "
                    f"{_ash_remained_rub} {currencies_rub}")
        elif currency == 'usd' and cash_remained < 0:
            return (f"Денег нет, держись: твой долг - "
                    f"{_ash_remained_usd} {currencies_usd}")
        elif currency == 'eur' and cash_remained < 0:
            return (f"Денег нет, держись: твой долг - "
                    f"{_ash_remained_eur} {currencies_eur}")
        else:
            return 'Денег нет, держись'


class CaloriesCalculator(Calculator):
    """Класс обработки информации по калькулятору калорий."""
    def get_calories_remained(self):
        i = self.limit - self.get_today_stats()
        if i > 0:
            return (f'Сегодня можно съесть что-нибудь ещё, '
                    f'но с общей калорийностью не более {i} кКал')
        else:
            return 'Хватит есть!'


cal_calculator = CaloriesCalculator(1000)
cal_calculator.add_record(Record(amount=145, comment='кофе'))
print(cal_calculator. get_calories_remained())
cash_calculator = CashCalculator(0)
cash_calculator.add_record(Record(amount=145, comment='кофе'))
cash_calculator.add_record(Record(amount=300, comment='Серёге за обед'))
print(cash_calculator.get_today_cash_remained('rub'))

"""Не разобрался что с этим делать, но оно должно быть:
if __name__ if __name__ == '__main__'.
"""

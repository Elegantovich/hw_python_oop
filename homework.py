import datetime as dt

FORM = '%d.%m.%Y'


class Record:
    """Класс записи вводной информации из конца кода."""
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is not None:
            self.date = dt.datetime.strptime(date, FORM).date()
        else:
            self.date = dt.date.today()


class Calculator(Record):
    """Родительский класс для калькуляторов калорий и денег."""
    def __init__(self, limit):
        self.limit = limit
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
        return (sum(rec.amount for rec in self.records
                if today >= rec.date >= week_date))

    def com_remained(self):
        return self.limit - self.get_today_stats()


class CashCalculator(Calculator):
    RUB_RATE = 1
    USD_RATE = 72.80
    EURO_RATE = 86.50

    """Класс обработки информации по денежному калькулятору."""
    def get_today_cash_remained(self, currency):
        currencies = {'rub': ('руб', self.RUB_RATE),
                      'usd': ('USD', self.USD_RATE),
                      'eur': ('Euro', self.EURO_RATE)}
        cash_remained = self.com_remained()
        if currency not in currencies:
            return 'Неопознанная валюта'
        val = currency
        cash_remained_val = round(cash_remained / currencies[val][1], 2)
        cash_remained_cred = abs(round(cash_remained / currencies[val][1], 2))
        currencies_val = currencies[val][0]
        if cash_remained_val > 0:
            return f'На сегодня осталось {cash_remained_val} {currencies_val}'
        elif cash_remained_val < 0:
            return (f'Денег нет, держись: твой долг - '
                    f'{cash_remained_cred} {currencies_val}')
        return 'Денег нет, держись'


class CaloriesCalculator(Calculator):
    """Класс обработки информации по калькулятору калорий."""
    def get_calories_remained(self):
        cal_rem = self.com_remained()
        if cal_rem > 0:
            return ('Сегодня можно съесть что-нибудь ещё, '
                    f'но с общей калорийностью не более {cal_rem} кКал')
        return 'Хватит есть!'


cal_calculator = CaloriesCalculator(1000)
cal_calculator.add_record(Record(amount=145, comment='кофе'))
print(cal_calculator. get_calories_remained())
cash_calculator = CashCalculator(400)
cash_calculator.add_record(Record(amount=145, comment='кофе'))
cash_calculator.add_record(Record(amount=300, comment='Серёге за обед'))
print(cash_calculator.get_today_cash_remained('rub'))

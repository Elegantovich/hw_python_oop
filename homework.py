import datetime as dt

FORMAT = '%d.%m.%Y'


class Record:
    """Класс записи вводной информации из конца кода."""
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is not None:
            self.date = dt.datetime.strptime(date, FORMAT).date()
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
        today = dt.date.today()
        for record in self.records:
            if record.date == today:
                stats += record.amount
        return stats

    def get_week_stats(self):
        today = dt.date.today()
        week_date = today - dt.timedelta(days=7)
        return sum(rec.amount for rec in self.records
                   if today >= rec.date >= week_date)

    def com_remained(self):
        return self.limit - self.get_today_stats()


class CashCalculator(Calculator):
    RUB_RATE = 1
    USD_RATE = 72.80
    EURO_RATE = 86.50
    """Класс обработки информации по денежному калькулятору."""
    def get_today_cash_remained(self, currency):
        cash_remained = self.com_remained()
        if cash_remained == 0:
            return 'Денег нет, держись'
        currencies = {'rub': ('руб', self.RUB_RATE),
                      'usd': ('USD', self.USD_RATE),
                      'eur': ('Euro', self.EURO_RATE)}
        cash_remained = self.com_remained()
        if currency not in currencies:
            return 'Неопознанная валюта'
        val = currency
        cash_remained_val = round(cash_remained / currencies[val][1], 2)
        currencies_val = currencies[val][0]
        if cash_remained_val > 0:
            return f'На сегодня осталось {cash_remained_val} {currencies_val}'
        cash_remained_cred = abs(cash_remained_val)
        return ('Денег нет, держись: твой долг - '
               f'{cash_remained_cred} {currencies_val}')


class CaloriesCalculator(Calculator):
    """Класс обработки информации по калькулятору калорий."""
    def get_calories_remained(self):
        cal_rem = self.com_remained()
        if cal_rem > 0:
            return ('Сегодня можно съесть что-нибудь ещё, '
                    f'но с общей калорийностью не более {cal_rem} кКал')
        return 'Хватит есть!'

cash_calculator = CashCalculator(100)
cash_calculator.add_record(Record(amount=145, comment='кофе'))
print(cash_calculator.get_today_cash_remained('eur'))
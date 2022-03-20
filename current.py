import re
import datetime
from typing import Any


def date_in_out(date_user: str, date_now: Any) -> Any:
    """
    Проверка даты на корректность. Формат день-месяц-год. В случае некорректности вернуть пустую строку в класс
    """
    pattern_date = r'\d\d\W\d\d\W\d\d\d\d'
    try:
        if re.search(pattern_date, date_user):
            day, month, year = re.split(r'\W+', date_user)
            result = datetime.date(int(year), int(month), int(day))
            if datetime.date(int(year), int(month), int(day)):
                delta = result - datetime.date(date_now.year, date_now.month, date_now.day)
                if delta.days > 0:
                    return result
                else:
                    return ''
            else:
                return ''
    except ValueError:
        return False


def part_row(row: str) -> list:
    result = re.split(r'\W+', row)
    return result


def response_processing(rows: str, count: int) -> list:
    result = ''
    for symbol in rows:
        if symbol != '[' and symbol != ']':
            result += symbol
    new = result.split("'")
    new_i = []
    for i in new:
        if i != ", " and i != '':
            new_i.append(i)
    result_answer = []
    for i in range(count):
        result_answer.append([new_i[i*6], new_i[i*6 + 1], new_i[i*6 + 2], new_i[i*6 + 3], new_i[i*6 + 4],
                              new_i[i*6 + 5]])
    return result_answer


def delta_date(date1, date2) -> int:
    if date1 != '':
        if date2 != '':
            date_1 = datetime.datetime(date1.year, date1.month, date1.day)
            date_2 = datetime.datetime(date2.year, date2.month, date2.day)
            delta = date_2 - date_1
            return delta.days


def days(check_in: datetime, check_out: datetime) -> int:
    year1, month1, day1 = check_in.year, check_in.month, check_in.day
    year2, month2, day2 = check_out.year, check_out.month, check_out.day
    date1 = datetime.date(day=int(day1), month=int(month1), year=int(year1))
    date2 = datetime.date(day=int(day2), month=int(month2), year=int(year2))
    delta = date2 - date1
    return delta.days + 1


def  diff_current(current: str) -> str:
    #total $77 for 2&nbsp;nights
    cur = current.split(' ')
    result = ''
    for sym in cur:
        if sym[0] == '$':
            result = sym
    return result

import re
import datetime


def date_in_out(date_user):
    """
    Проверка даты на корректность. Формат день-месяц-год. В случае некорректности вернуть пустую строку в класс
    """
    pattern_date = r'\d\d\W\d\d\W\d\d\d\d'
    try:
        if re.search(pattern_date, date_user):
            date_data = re.split(r'\W+', date_user)
            day, month, year = date_data
            date_data = [year, month, day]
            result = '-'.join(date_data)
            if datetime.date(int(year), int(month), int(day)):
                return result
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

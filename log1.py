import re

log_line = 'vgmok.ru 213.180.203.166 - - [04/Apr/2025:15:24:15 +0300] "GET / HTTP/1.1" 403 271 "-" "Mozilla/5.0 (compatible; YandexMetrika/2.0; +http://yandex.com/bots yabs01)" 4213 4443:0'

# Обновленное регулярное выражение для разбора строки лога
log_pattern = re.compile(
    r'(?P<host>\S+) (?P<ip>\d+\.\d+\.\d+\.\d+) - - $$(?P<date_time>[^$$]+)\] "(?P<request>[^"]+)" (?P<status>\d{3}) (?P<size>\d+) "(?P<referrer>[^"]*)" "(?P<user_agent>[^"]*)" (?P<time_taken>\d+) (?P<other_info>\S+)'
)

# Проверяем, что строка соответствует регулярному выражению
match = log_pattern.match(log_line)
if match:
    host = match.group('host')
    ip = match.group('ip')
    
    # Собираем остальные данные в один столбец
    other = f"Date/Time: {match.group('date_time')}, Request: {match.group('request')}, Status: {match.group('status')}, Size: {match.group('size')}, Referrer: {match.group('referrer')}, User Agent: {match.group('user_agent')}, Time Taken: {match.group('time_taken')}, Other Info: {match.group('other_info')}"
    
    # Выводим данные
    print(f"Host: {host}")
    print(f"IP: {ip}")
    print(f"Other: {other}")
else:
    print("No match found for the log line.")
    print("Log line:", log_line)  # Выводим строку для отладки

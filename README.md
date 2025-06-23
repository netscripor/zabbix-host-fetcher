# 🔍 Zabbix Host Fetcher

Универсальный CLI-инструмент для быстрого получения IP-адресов или имён хостов из Zabbix, с фильтрацией по группе, шаблону и тегам.

📌 Подходит для:
- сетевых инженеров
- DevOps-специалистов
- автоматизации задач через API Zabbix

---

## 🚀 Установка

1. Клонируй репозиторий:
```bash
git clone https://github.com/netscripor/zabbix_host_fetcher.git
cd zabbix-host-fetcher
```

2. Установи зависимости:
```bash
pip install -r requirements.txt
```

---

## ⚙️ Аргументы CLI

| Аргумент         | Описание                                                                 |
|------------------|--------------------------------------------------------------------------|
| `--zabbix-url`   | URL Zabbix-сервера (по умолчанию `https://10.10.10.10)                |
| `--user`         | Имя пользователя Zabbix                                                  |
| `--password`     | Пароль (если не указан, будет запрошен интерактивно)                     |
| `--group`        | Имя группы хостов                                                        |
| `--template`     | Имя шаблона (template), связанного с хостом                              |
| `--tag`          | Фильтр по тегам `key=value` (можно указывать несколько раз)              |
| `--mode`         | Тип вывода: `host` (IP-адрес) или `name` (отображаемое имя)              |
| `--output`       | Путь к файлу для вывода (по умолчанию `output_hosts.txt`)               |

---

## 🧩 Примеры использования

### 🔹 Получить IP-адреса всех Cisco-хостов из группы "Networks L3":
```bash
python get_hosts.py \
  --user admin \
  --group "Networks L3" \
  --template "Relevant Cisco IOS SNMP" \
  --mode host
```

### 🔹 Получить имена хостов с тегом `location=dc1`:
```bash
python get_hosts.py \
  --user admin \
  --tag location=dc1 \
  --mode name
```

### 🔹 Вывести IP хостов с двумя тегами и сохранить результат:
```bash
python get_hosts.py \
  --group "Router wi-fi" \
  --template "Relevant AC Mikrotik by SNMP" \
  --tag environment=prod role=access \
  --mode host \
  --output wifi_prod_hosts.txt
```

---

## 🧯 Частые ошибки

- ❗ **"Группа не найдена"** — проверь точное имя группы хостов в Zabbix.
- ❗ **"Шаблон не найден"** — имя шаблона чувствительно к регистру.
- ❗ **"Неверный формат тега"** — используйте строго `key=value`.
- ⚠ **"[no ip]"** — у хоста нет привязанного IP-адреса (интерфейса).

---

## 📦 `requirements.txt`

```
pyzabbix==1.3.0
urllib3==1.25.8
```

---

📡 Подпишись и поддержи проект:

🔗 GitHub: github.com/netscripor
💰 Boosty: boosty.to/netscripor
✈️ Telegram-канал: t.me/netscripor

⭐️ Поддержи проект звездой
🛠 Нашёл баг или есть идея? Создай Issue!

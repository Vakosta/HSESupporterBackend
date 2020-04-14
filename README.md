# HSESupporterBackend
**HSESupporterBackend** — сервер для приложения [HSESupporter](https://github.com/Vakosta/HSESupporter).

## Методы
- _POST_ `/auth/register/` — регистрация пользователя.
  - Параметры: `email`.
- _POST_ `/auth/register/confirm-email/` — подтверждение регистрации.
  - Параметры: `email`, `code`.
- _POST_ `/auth/token/login/` — авторизация пользователя.
- _POST_ `/auth/accept-status/` — проверка одобрения администрацией.

---

- _GET_ `/dormitories/` — получение списка общежитий.
- _GET/POST/DELETE_ `/problems/` — взаимодействие с обращениями пользователей.
- _GET/POST/DELETE_ `/messages/` — взаимодействие с сообщениями пользователей.

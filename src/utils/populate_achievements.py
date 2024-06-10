from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.models import Achievement

# Пример списка ачивок
achievements_data = [
    {
        "id": 1,
        "name": "Быстрый Ум",
        "description": "Решить 10 примеров правильно за 15 секунд",
        "image": "https://cdn-icons-png.flaticon.com/512/6919/6919464.png",
    },
    {
        "id": 2,
        "name": "Торопливый Ученик",
        "description": "Решить 20 примеров правильно за 30 секунд",
        "image": "https://cdn-icons-png.flaticon.com/512/3382/3382828.png",
    },
    {
        "id": 3,
        "name": "Быстрее Ветра",
        "description": "Решить 30 примеров правильно за 60 секунд",
        "image": "https://cdn-icons-png.flaticon.com/512/1007/1007166.png",
    },
    {
        "id": 4,
        "name": "Марафонец",
        "description": "Решить 40 примеров правильно за 90 секунд",
        "image": "https://cdn-icons-png.flaticon.com/512/16486/16486409.png",
    },
    {
        "id": 5,
        "name": "Мастер Сложности 10",
        "description": "Решить 10 примеров правильно на сложности 10 за 15 секунд",
        "image": "https://cdn-icons-png.flaticon.com/512/8093/8093528.png",
    },
    {
        "id": 6,
        "name": "Мастер Сложности 100",
        "description": "Решить 10 примеров правильно на сложности 100 за 30 секунд",
        "image": "https://cdn-icons-png.flaticon.com/512/3429/3429471.png",
    },
    {
        "id": 7,
        "name": "Мастер Сложности 1000",
        "description": "Решить 10 примеров правильно на сложности 1000 за 60 секунд",
        "image": "https://cdn-icons-png.flaticon.com/512/1651/1651689.png",
    },
    {
        "id": 8,
        "name": "Адепт Сложения",
        "description": "Решить 10 примеров правильно, выбрав только сложение",
        "image": "https://cdn-icons-png.flaticon.com/512/1417/1417434.png",
    },
    {
        "id": 9,
        "name": "Адепт Вычитания",
        "description": "Решить 10 примеров правильно, выбрав только вычитание",
        "image": "https://cdn-icons-png.flaticon.com/512/66/66889.png",
    },
    {
        "id": 10,
        "name": "Адепт Умножения",
        "description": "Решить 10 примеров правильно, выбрав только умножение",
        "image": "https://cdn-icons-png.flaticon.com/512/3/3740.png",
    },
    {
        "id": 11,
        "name": "Адепт Деления",
        "description": "Решить 10 примеров правильно, выбрав только деление",
        "image": "https://cdn-icons-png.flaticon.com/512/659/659881.png",
    },
    {
        "id": 12,
        "name": "Мастер Всех Операций",
        "description": "Решить 10 примеров правильно, выбрав все операции",
        "image": "https://cdn-icons-png.flaticon.com/512/3965/3965048.png",
    },
    {
        "id": 13,
        "name": "Начинающий Математик",
        "description": "Решить 10 примеров правильно в режиме на 10 примеров",
        "image": "https://cdn-icons-png.flaticon.com/512/2231/2231628.png",
    },
    {
        "id": 14,
        "name": "Продвинутый Ученик",
        "description": "Решить 12 примеров правильно в режиме на 15 примеров",
        "image": "https://cdn-icons-png.flaticon.com/512/208/208072.png",
    },
    {
        "id": 15,
        "name": "Мастер Арифметики",
        "description": "Решить 18 примеров правильно в режиме на 20 примеров",
        "image": "https://cdn-icons-png.flaticon.com/512/2995/2995353.png",
    },
    {
        "id": 16,
        "name": "Гуру Математики",
        "description": "Решить 25 примеров правильно в режиме на 30 примеров",
        "image": "https://cdn-icons-png.flaticon.com/512/2436/2436601.png",
    },
    {
        "id": 17,
        "name": "Точность Высокого Уровня",
        "description": "Решить 30 примеров правильно с 100% правильных ответов",
        "image": "https://cdn-icons-png.flaticon.com/512/9041/9041927.png",
    },
    {
        "id": 18,
        "name": "Скоростной Счет",
        "description": "Решить 5 примеров правильно на сложности 1000 за 15 секунд",
        "image": "https://cdn-icons-png.flaticon.com/512/3976/3976592.png",
    },
    {
        "id": 19,
        "name": "Ученик Мастера",
        "description": "Решить 20 примеров правильно на сложности 1000",
        "image": "https://cdn-icons-png.flaticon.com/512/2436/2436611.png",
    },
    {
        "id": 20,
        "name": "Всесторонний Развитие",
        "description": "Решить 15 примеров правильно, выбрав все операции и сложность 1000",
        "image": "https://cdn-icons-png.flaticon.com/512/2490/2490386.png",
    },
    {
        "id": 21,
        "name": "Быстрый Начинающий",
        "description": "Решить 5 примеров правильно за 10 секунд",
        "image": "https://cdn-icons-png.flaticon.com/512/8145/8145692.png",
    },
    {
        "id": 22,
        "name": "Идеальный Ученик",
        "description": "Завершить сессию с 100% правильных ответов",
        "image": "https://cdn-icons-png.flaticon.com/512/1956/1956692.png",
    },
    {
        "id": 23,
        "name": "Мастер Счетов",
        "description": "Решить 100 примеров правильно в общей сложности",
        "image": "https://cdn-icons-png.flaticon.com/512/4100/4100721.png",
    },
    {
        "id": 24,
        "name": "Гуру Арифметики",
        "description": "Решить 50 примеров правильно в одной сессии",
        "image": "https://cdn-icons-png.flaticon.com/512/5332/5332450.png",
    },
    {
        "id": 25,
        "name": "Эксперт Выбора",
        "description": "Завершить сессию, выбрав три из четырех операций",
        "image": "https://cdn-icons-png.flaticon.com/512/4048/4048067.png",
    },
    {
        "id": 26,
        "name": "Мастер Скорости",
        "description": "Решить 50 примеров правильно за 2 минуты",
        "image": "https://cdn-icons-png.flaticon.com/512/6303/6303251.png",
    },
    {
        "id": 27,
        "name": "Быстрый Учитель",
        "description": "Решить 30 примеров правильно за 45 секунд",
        "image": "https://cdn-icons-png.flaticon.com/512/3373/3373446.png",
    },
    {
        "id": 28,
        "name": "Легендарный Игрок",
        "description": "Завершить 100 сессий",
        "image": "https://cdn-icons-png.flaticon.com/512/2557/2557158.png",
    },
    {
        "id": 29,
        "name": "Великий Математик",
        "description": "Решить 500 примеров правильно в общей сложности",
        "image": "https://cdn-icons-png.flaticon.com/512/1956/1956683.png",
    },
    {
        "id": 30,
        "name": "Непрерывный Поток",
        "description": "Завершить 5 сессий подряд с 100% правильных ответов",
        "image": "https://cdn-icons-png.flaticon.com/512/10483/10483271.png",
    },
    {
        "id": 31,
        "name": "Мастер Точности",
        "description": "Решить 40 примеров правильно с 95% правильных ответов",
        "image": "https://cdn-icons-png.flaticon.com/512/4729/4729355.png",
    },
    {
        "id": 32,
        "name": "Математический Чародей",
        "description": "Завершить сессию с 100% правильных ответов на сложности 1000",
        "image": "https://cdn-icons-png.flaticon.com/512/15877/15877692.png",
    },
    {
        "id": 33,
        "name": "Выдающийся Ученик",
        "description": "Завершить 50 сессий с 90% правильных ответов",
        "image": "https://cdn-icons-png.flaticon.com/512/15877/15877692.png",
    },
    {
        "id": 34,
        "name": "Покоритель Сложности",
        "description": "Завершить 10 сессий на сложности 1000",
        "image": "https://cdn-icons-png.flaticon.com/512/8386/8386491.png",
    },
    {
        "id": 35,
        "name": "Идеальный Счет",
        "description": "Завершить 20 сессий подряд с 100% правильных ответов",
        "image": "https://cdn-icons-png.flaticon.com/512/1370/1370289.png",
    },
    {
        "id": 36,
        "name": "Мастер Арифметических Операций",
        "description": "Решить 200 примеров правильно в режиме на все операции",
        "image": "https://cdn-icons-png.flaticon.com/512/635/635319.png",
    },
    {
        "id": 37,
        "name": "Гений Арифметики",
        "description": "Решить 150 примеров правильно за 10 минут",
        "image": "https://cdn-icons-png.flaticon.com/512/553/553121.png",
    },
    {
        "id": 38,
        "name": "Победитель Скорости",
        "description": "Завершить 10 сессий на время, решив минимум 15 примеров правильно",
        "image": "https://cdn-icons-png.flaticon.com/512/3943/3943566.png",
    },
    {
        "id": 39,
        "name": "Мастер Длительности",
        "description": "Завершить сессию на время, решив минимум 60 примеров правильно",
        "image": "https://cdn-icons-png.flaticon.com/512/2972/2972497.png",
    },
    {
        "id": 40,
        "name": "Магистр Математики",
        "description": "Завершить сессию, выбрав все операции и сложность 1000, решив минимум 50 примеров правильно",
        "image": "https://cdn-icons-png.flaticon.com/512/16500/16500070.png",
    },
]


async def populate_achievements(session: AsyncSession):
    existing_achievements = await session.execute(select(Achievement))
    existing_achievements = existing_achievements.scalars().all()

    if not existing_achievements:
        for ach in achievements_data:
            new_achievement = Achievement(
                id=ach["id"],
                name=ach["name"],
                description=ach["description"],
                image=ach["image"],
            )
            session.add(new_achievement)
        await session.commit()

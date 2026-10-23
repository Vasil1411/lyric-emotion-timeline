# Lyric Emotion Timeline

Проект за анализ на емоционалната динамика в текстове на песни.

## Структура

```text
lyric-emotion-timeline/
├── data/                 # Сурови и обработени данни
├── notebooks/            # Анализ и експерименти
├── src/
│   ├── config.py         # Конфигурация и етикети
│   ├── dataset.py        # Зареждане на Dataset и DataLoader-и
│   ├── model.py          # Архитектура на класификатора
│   ├── train.py          # Обучителен цикъл
│   ├── inference.py      # Предсказване
│   └── visualizer.py     # Интерактивни графики
├── app.py                # Streamlit интерфейс
├── Dockerfile            # Контейнеризация
└── requirements.txt      # Зависимости
```

## Стартиране

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

За обучение CSV файлът трябва да съдържа колона `text` и се подава чрез
`python -m src.train`.

import pandas as pd
import random

rows = []

for _ in range(100):
    sleep = random.randint(4, 9)
    screen = random.randint(3, 10)
    steps = random.randint(1000, 12000)
    work = random.randint(3, 10)
    mood = random.randint(1, 5)
    food = random.randint(1, 5)

    stress = 1 if sleep < 6 or screen > 7 else 0
    productivity = int((sleep*10 + work*8 + mood*5) - screen*3)
    health = int((steps/100 + sleep*5 + food*5) - screen*2)

    rows.append([sleep, screen, steps, work, mood, food, stress, productivity, health])

df = pd.DataFrame(rows, columns=[
    'sleep','screen_time','steps','work_hours','mood','food',
    'stress','productivity','health'
])

df.to_csv("C:\\projects\\Smart Daily Life Assistant\\data.csv", index=False)
print("New dataset created")
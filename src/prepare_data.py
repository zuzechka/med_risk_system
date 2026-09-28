import pandas as pd
from pathlib import Path


#путь до датасету
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "dataset.csv"


#зав данх
df = pd.read_csv(DATA_PATH)


print("*" * 60)
print("інформація про датасет")
print("*" * 60)

print(f"к-сть рядків =  {df.shape[0]}")
print(f"к-сть стовпців = {df.shape[1]}")

print("\nназви стовпців:")
for column in df.columns:
    print(f"- {column}")


print("\n" + "*" * 60)
print("типи даних")
print("*" * 60)

print(df.dtypes)


print("\n" + "*" * 60)
print("пропущені значення")
print("*" * 60)

print(df.isnull().sum())


print("\n" + "*" * 60)
print("перші 5 рядків датасету")
print("*" * 60)

print(df.head())
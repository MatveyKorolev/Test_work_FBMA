from pathlib import Path
import pandas as pd

home_path = str(Path(__file__).parent.absolute())

# Загрузка данных из файла
df = pd.read_csv(home_path + "/FP_snps.txt", sep="\t")

# Удаление вариантов с X-хромосомы (номер 23)
df = df[df['chromosome'] != 23]

# Добавление префиксов "chr" и "rs"
df['chromosome'] = "chr" + df['chromosome'].astype(str)
df['rs#'] = "rs" + df['rs#'].astype(str)

# Удаление столбца GB37_position
df = df.drop(columns=['GB37_position'])

# Переименование столбцов и изменение порядка
df = df.rename(columns={'rs#': 'ID','chromosome': '#CHROM', 'GB38_position': 'POS', 'allele1': 'allele1', 'allele2': 'allele2'})
df = df[['#CHROM', 'POS', 'ID', 'allele1', 'allele2']]


# Сортировка по хромосоме и позиции
df = df.sort_values(by=['#CHROM', 'POS'], key=lambda x: x.map(lambda y: int(y[3:]) if isinstance(y, str) and y.startswith('chr') else y))


# Сохранение в новый файл
df.to_csv("FP_SNPs_10k_GB38_twoAllelsFormat.tsv", sep="\t", index=False, header=True)

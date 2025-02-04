# Инструкция для преобразования файла SNP

## Описание

Этот скрипт преобразует данные из формата "#CHROM<TAB>POS<TAB>ID<TAB>allele1<TAB>allele2" в формат "#CHROM<TAB>POS<TAB>ID<TAB>REF<TAB>ALT", где "REF" и "ALT" — это референсный и альтернативный аллели соответственно.

## Подготовка входных данных

Перед тем как запустить скрипт, необходимо привести данные к следующему формату (пример):

#CHROM POS ID allele1 allele2
1 1000 rs1 A C
1 2000 rs2 T T
2 3000 rs3 G G

Это можно сделать с помощью скрипта preprocessing.py
Он удаляет вариант с X-хромосомы
Добавляет префиксы для столбцов chromosome и rs#
Удаляет столбец GB37_position
Переименовывает столбцы и изменяет порядок столбцов в итоговом датафрейме
Сортирует данные по номер хромосомы и позициям snp в ней
Сохранет в файл  "FP_SNPs_10k_GB38_twoAllelsFormat.tsv"

## Общая часть работы

После подготовки скрипта используется основной файл, на вход он принимает данные о входном файле, выходном файле, лог файле и папку, где лежат референсные хромосомы.

Описание работы основных функций
parse_args()
Эта функция обрабатывает аргументы командной строки и возвращает их значения.

log(message, log_file)
Функция записывает сообщение в лог-файл с временной меткой.

get_reference_allele(chrom, pos, ref_dir)
Эта функция:

Открывает файл соответствующей хромосомы (<chromosome>.fa).
Извлекает референсный аллель для указанной позиции.
Возвращает референсный аллель в виде строки.
process_file(input_file, output_file, log_file, ref_dir)
Основная функция обработки файла:

Проверяет наличие и формат входного файла.
Читает данные построчно, определяет референсный аллель и записывает результат в выходной файл.
Если данные некорректны или возникает ошибка при доступе к файлам референсного генома, запись об ошибке фиксируется в лог-файле.

Логика определения референсного и альтернативного аллелей
Если allele1 совпадает с референсным аллелем, он становится REF, а allele2 — ALT.
Если allele2 совпадает с референсным аллелем, он становится REF, а allele1 — ALT.
Если ни один из аллелей не совпадает с референсным, аллели сортируются в алфавитном порядке.

Логирование
Все важные события фиксируются в лог-файле, включая:

Начало и завершение работы скрипта.
Ошибки при чтении файлов и определении референсного аллеля.
Проблемы с форматом данных.

Обработка ошибок
Скрипт корректно обрабатывает следующие ошибки:

Отсутствие входного файла или файлов референсного генома.
Некорректный формат данных.
Проблемы с доступом к референсным данным.
Сообщения об ошибках записываются в лог-файл и выводятся пользователю.

Завершение работы
При успешной обработке данных скрипт фиксирует сообщение об успехе в лог-файле и создает выходной файл с преобразованными данными.



## Запуск скрипта

Для запуска скрипта используйте команду:

python3 parse_pysam.py -i FP_SNPs_10k_GB38_twoAllelsFormat.tsv -o FP_SNPs_processed.tsv -l log2.txt -r ./
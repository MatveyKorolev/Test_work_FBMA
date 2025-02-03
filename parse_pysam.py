import argparse
import os
import sys
import time
import pysam

# Функция для обработки аргументов командной строки
def parse_args():
    parser = argparse.ArgumentParser(description="Скрипт для преобразования SNP файла из формата allele1/allele2 в формат REF/ALT с использованием референсного генома.")
    parser.add_argument("-i", "--input", required=True, help="Путь к входному файлу")
    parser.add_argument("-o", "--output", required=True, help="Путь к выходному файлу")
    parser.add_argument("-l", "--log", required=True, help="Путь к лог-файлу")
    parser.add_argument("-r", "--ref-dir", required=True, help="Папка с референсными файлами генома")
    return parser.parse_args()

# Функция для записи в лог
def log(message, log_file):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    with open(log_file, "a") as log:
        log.write(f"{timestamp} - {message}\n")

# Функция для извлечения референсного аллеля из генома
def get_reference_allele(chrom, pos, ref_dir):
    # Преобразуем имя хромосомы в формат, ожидаемый в имени файла
    if not chrom.startswith('chr'):
        chrom = 'chr' + str(chrom)
    
    ref_file = os.path.join(ref_dir, f"{chrom}.fa")
    if not os.path.exists(ref_file):
        raise FileNotFoundError(f"Референсный файл для хромосомы {chrom} не найден в папке {ref_dir}.")

    # Открываем референсный файл для чтения
    try:
        ref_fasta = pysam.Fastafile(ref_file)
        ref_base = ref_fasta.fetch(chrom, pos - 1, pos)  # В pysam позиция начинается с 0
        return ref_base.upper()
    except Exception as e:
        raise Exception(f"Ошибка при извлечении референсного аллеля: {str(e)}")

# Основная функция обработки файла
def process_file(input_file, output_file, log_file, ref_dir):
    # Проверяем наличие входного файла
    if not os.path.isfile(input_file):
        log(f"Ошибка: входной файл {input_file} не найден.", log_file)
        sys.exit(1)

    # Читаем и обрабатываем файл
    try:
        with open(input_file, "r") as infile, open(output_file, "w") as outfile:
            header = infile.readline().strip()
            if not header.startswith("#CHROM"):
                log(f"Ошибка: Неверный формат заголовка в файле {input_file}.", log_file)
                sys.exit(1)

            # Записываем заголовок в выходной файл
            outfile.write(header.replace("allele1", "REF").replace("allele2", "ALT") + "\n")
            
            for line in infile:
                fields = line.strip().split("\t")
                if len(fields) != 5:
                    log(f"Ошибка: неверный формат строки: {line}", log_file)
                    continue

                chrom, pos, snp_id, allele1, allele2 = fields
                try:
                    ref_allele = get_reference_allele(chrom, int(pos), ref_dir)
                    # Определяем, какой из аллелей является референсным
                    if allele1 == ref_allele:
                        ref, alt = allele1, allele2
                    elif allele2 == ref_allele:
                        ref, alt = allele2, allele1
                    else:
                        ref, alt = sorted([allele1, allele2])  # Если оба аллеля не совпадают с референсным, сортируем

                    # Записываем строку в выходной файл
                    outfile.write(f"{chrom}\t{pos}\t{snp_id}\t{ref}\t{alt}\n")
                except Exception as e:
                    log(f"Ошибка при обработке SNP {snp_id} на хромосоме {chrom}, позиция {pos}: {str(e)}", log_file)

        log(f"Успешно завершена обработка файла. Выходной файл: {output_file}", log_file)

    except Exception as e:
        log(f"Ошибка при обработке файла: {str(e)}", log_file)
        sys.exit(1)

# Основной блок выполнения
if __name__ == "__main__":
    args = parse_args()
    log("Начало работы скрипта", args.log)
    process_file(args.input, args.output, args.log, args.ref_dir)
    log("Завершение работы скрипта", args.log)
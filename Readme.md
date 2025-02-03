# Инструкции по сборке и запуску Docker-образа

## Сборка Docker-образа

1. Клонируйте репозиторий или загрузите проект на свой компьютер.
2. Перейдите в директорию с Dockerfile.
3. Запустите команду для сборки Docker-образа:

docker build -t bioinformatics-tools .

## Чтобы запустить контейнер в интерактивном режиме, используйте команду:
docker run -it bioinformatics-tools /bin/bash

## В контейнере можно проверить доступность программ
samtools --version
bcftools --version
vcftools --version

## Для загрузки референса используйте:
wget https://api.gdc.cancer.gov/data/254f697d-310d-4d7d-a27b-27fbf767a834
## Затем:
tar -xvf 254f697d-310d-4d7d-a27b-27fbf767a834

## Для разделения на хромосомы используйте скрипт rechrom.sh, предварительно перейдя в папку с референсным геномом
./rechrom.sh

## 1. Файлы референсного генома должны быть расположены на компьютере в папке: `/mnt/data/ref/GRCh38.d1.vd1_mainChr/sepChrs/`. Файлы должны иметь имена вида "chr[1-22,M,X,Y].fa" и "chr[1-22,M,X,Y].fa.fai".
## 2. Если у вас они расположены в другой папке, вам нужно будет заменить путь `/mnt/data/ref/GRCh38.d1.vd1_mainChr/sepChrs/` на путь к вашей папке.

## Чтобы при запуске docker-контейнера загрузить файлы референсов внутрь контейнера, используйте команду:
docker run -d -v /mnt/data/ref/GRCh38.d1.vd1_mainChr/sepChrs/:/ref/GRCh38.d1.vd1_mainChr/sepChrs/ bioinformatics-tools

## Чтобы при запуске в интерактивном режиме загрузить файлы референсов внутрь контейнера, используйте команду:
docker run -it -v /mnt/data/ref/GRCh38.d1.vd1_mainChr/sepChrs/:/ref/GRCh38.d1.vd1_mainChr/sepChrs/ bioinformatics-tools /bin/bash

## Файл с данными о FP_SNPs.txt предустанавливается при сборке dockerfile
## Данные файл проходит препроцессинг с помощью скрипта preprocessing.py, для запуска используйте команду:
python3 preprocessing.py
## Выходной файл будет иметь название FP_SNPs_10k_GB38_twoAllelsFormat.tsv
 
## Для выполнения скрипта парсинга данных с помощью pysam, используйте команду:
python3 parse_pysam.py -i FP_SNPs_10k_GB38_twoAllelsFormat.tsv -o FP_SNPs_processed.tsv -l log2.txt -r ./
## -i входной файл .tsv с snp по аллелям 1 и 2; -o выходной файл c переработанными SNP относительно референсного аллеля; -l файл логов; -r папка, в которой лежат референсные сборки хромосом в формате .fa 

## Для удаления контейнера и образа используйте команды
docker rm <container_id>   # Удалить контейнер
docker rmi bioinformatics-tools  # Удалить образ
# Базовый образ: Ubuntu 20.04
FROM ubuntu:20.04

# Переменная окружения для установки программ
ENV SOFT=/soft

# Устанавливаем переменные окружения для non-interactive режима установки
ENV DEBIAN_FRONTEND=noninteractive

# Обновляем пакеты и устанавливаем базовые зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    git \
    curl \
    zlib1g-dev \
    libbz2-dev \
    liblzma-dev \
    python3 \
    python3-pip \
    python3-dev \
    libssl-dev \
    libncurses5-dev \
    libcurl4-openssl-dev \
    libboost-all-dev \
    pkg-config \
    make \
    cmake \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Переходим в каталог для установки программ
RUN mkdir -p $SOFT

# Установка htslib (версия 1.21-27-gc814d398)
RUN git clone https://github.com/samtools/htslib.git $SOFT/htslib && \
    cd $SOFT/htslib && \
    git submodule update --init --recursive && \
    make -j$(nproc) && \
    make install

# Установка samtools (версия 1.21-31-g21d43e7)
RUN git clone https://github.com/samtools/samtools.git $SOFT/samtools && \
    cd $SOFT/samtools && \
    git submodule update --init --recursive && \
    make -j$(nproc) HTSDIR=$SOFT/htslib && \
    make install && \
    cd / && \
    rm -rf $SOFT/samtools

# Установка bcftools (версия 1.21-74-g827b2cd3)
RUN git clone https://github.com/samtools/bcftools.git $SOFT/bcftools && \
    cd $SOFT/bcftools && \
    git submodule update --init --recursive && \
    make -j$(nproc) HTSDIR=$SOFT/htslib && \
    make install && \
    cd / && \
    rm -rf $SOFT/bcftools

# Установка vcftools (версия 0.1.17)
RUN git clone https://github.com/vcftools/vcftools.git $SOFT/vcftools && \
    cd $SOFT/vcftools && \
    git submodule update --init --recursive && \
    ./autogen.sh && \
    ./configure && \
    make -j$(nproc) HTSDIR=$SOFT/htslib && \
    make install && \
    cd / && \
    rm -rf $SOFT/vcftools

# Установка libdeflate (версия 1.23)
RUN git clone https://github.com/ebiggers/libdeflate.git $SOFT/libdeflate && \
    cd $SOFT/libdeflate && \
    git submodule update --init --recursive && \
    cmake -B build && cmake --build build && \
    cd / && \
    rm -rf $SOFT/libdeflate

# Обновляем переменные окружения PATH
ENV PATH=$SOFT/samtools:$SOFT/bcftools:$SOFT/vcftools:$SOFT/htslib:$SOFT/libdeflate:$PATH

# Устанавливаем Python зависимости
RUN pip3 install --no-cache-dir argparse pysam

# Копируем  Python-скрипт в контейнер
COPY preprocessing.py /app/preprocessing.py
COPY parse_pysam.py /app/parse_pysam.py
COPY log.txt /app/log.txt
COPY FP_SNPs.txt /app/FP_SNPs.txt


# Указываем рабочую директорию
WORKDIR /app

# Команда по умолчанию для контейнера
CMD ["python3", "parse_pysam.py"]

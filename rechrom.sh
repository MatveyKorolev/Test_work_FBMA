#!/bin/bash
#Создание директории референсными хромосомами
mkdir ref
cd ref

csplit -s -z ./GRCh38.d1.vd1.fa '/>/' '{*}'

# Массив с названиями нужных хромосом
declare -a allowed_chroms=("chr1" "chr2" "chr3" "chr4" "chr5" "chr6" "chr7" "chr8" "chr9" "chr10" "chr11" "chr12" "chr13" "chr14" "chr15" "chr16" "chr17" "chr18" "chr19" "chr20" "chr21" "chr22" "chrX" "chrY" "chrM")

for i in xx*; do
  n=$(sed 's/>// ; s/ .*// ; 1q' "$i")
  
  # Проверяем, есть ли название хромосомы в массиве allowed_chroms
  is_allowed=false
  for allowed_chrom in "${allowed_chroms[@]}"; do
    if [[ "$n" == "$allowed_chrom" ]]; then
      is_allowed=true
      break
    fi
  done

  # Если хромосома разрешена, переименовываем, иначе - удаляем
  if $is_allowed; then
    mv "$i" "$n.fa"
  else
    rm "$i"
  fi
done
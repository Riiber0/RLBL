# RLBL
## Método de compressão sem perda de qualidade

Este algorítimo implementa uma versão de Run-Length. Data uma sequência de elementos duas outra sequência são geradas, uma contendo 1s e 0s, onde 0 são repetições de elementos e 1 mundança. Então a sequência de 0s e 1s é comprimida em bytes. As duas sequcias são salvas em no arquivo comprimido

Exemplo:

aaaabbbccccaaacc -> [a, b, c, a, c] e [0000100100010010]

|00001001|00010010| -> 9, 18

## Utilização

Para obter ajuda em como utilizar os comandos:

```bash 
python3 main.py -h
```

Este programa suporta a maioria dos arquivos de imagens como entrada.

A descompressão de imagem é sempre feita para um arquivo .bmp.

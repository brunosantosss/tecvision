# TecVision

TecVision é um projeto científico para o CECITEC 2024 da EEEP Professor Francisco Aristóteles de Sousa. Em suma, o projeto visa formentar o uso de tecnologias como a 
Visão Computacional para a acessibilidade a deficientes visuais, fornecendo leitura de texto e outras ações via comandos realizados com certos movimentos com as mãos.

## Instalação

### Python
É essencial a instalação do interpretador Python (3.11.6 para Windows e 3.8 para Linux), você pode baixa-lo no link abaixo.

[ Python 3.11.6 ](https://www.python.org/downloads/release/python-3116/)
[ Python 3.8 ](https://www.python.org/downloads/release/python-380/)

### Dependências
O TecVision utiliza algumas bibliotecas importantes para o seu funcionamento. Para a facilidade na busca e instalação das dependências basta voce utilizar o 
comando pip com o arquivo requirements.txt ( disponibilizado no repositório ), assim você ira realizar a instalação de todas as dependências necessárias para o funcionamento do código.

```bash
pip install -r requirements.txt
```

### Uso 
A utilização de visão computacional permite a execução de tarefas apenas movimentando a mão. Com isso, para realizar tarefas como a de ativar o modo leitura você deve 
posicionar seu dedo mindinho em contato com o seu dedo polegar. Após a detecção da ação, uma contagem de 10 segundos se inicia, dando tempo para o deficiente posicionar
objetos como livros, embalages ou jornais para a realização da leitura em voz.

TRABALHO DE PESQUISA OPERACIONAL DA UNIVERSIDADE FEDERAL FLUMINENSE - 2024.2



AUTORES:
HENRIQUE BARREIRA
JOÃO VITOR BRANQUINHO
JULIANA MOURA


Esse trabalho consiste em implementar duas meta-heurísticas e resolver algum problema de otimização.
O trabalho é em grupo de 3 pessoas, então somente em casos excepcionais serão aceitos MENOS ou MAIS membros.
Inicialmente, os grupos formados com 3 membros já poderão escolher seus temas, e só depois iremos distribuir temas para os demais casos. Me enviem email imcoelho@ic.uff.br para formar grupos excepcionalmente fora da contagem de 3, que avaliaremos cada caso, ok?

Para a escolha do tema de otimização, vale qualquer problema de otimização que seja interessante (preferencialmente NP-Difícil), EXCETO o Caixeiro Viajante clássico e a Mochila 0-1 clássica.

Bons temas podem ser encontrados em:
- OR Library: http://people.brunel.ac.uk/~mastjjb/jeb/info.html
- SBPO 2024 (ou edições anteriores): https://proceedings.science/sbpo/sbpo-2024/trabalhos?lang=pt-br
- Google Scholar com tema "meta-heuristicas": https://scholar.google.com/scholar?hl=pt-BR&as_sdt=0%2C5&q=meta+heur%C3%ADsticas&btnG=&oq=meta-heuristica

Apresente em no máximo 15 minutos:
- O problema, duas meta-heurísticas, a calibração de parâmetros efetuada (melhores parâmetros encontrados para os métodos), valor médio da solução para 10 execuções, melhor solução encontrada em 10 execuções, tempo médio computacional para 10 execuções.

Escreva um relatório em formato SBC (max 8 páginas) descrevendo esses pontos.




PROBLEMA ESCOLHIDO:
    _Employee Scheduling Problem

META-HEURÍSTICAS ESCOLHIDAS:
    _GRASP
    _VNS

COMO RODAR OS ARQUIVOS:
    Primeiramente criar um ambiente virtual python para instalar o pulp:
        python -m venv pulp_venv
    Depois, ativar o virtual env em seu terminal
        pulp_venv/Scripts/.\Activate.ps1 (no caso do powershell)
    Finalmente, voltar à raiz do projeto e rodar o arquivo python:
        python nome_do_arquivo.py
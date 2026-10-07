# DNA Sequence Alignment

Aplicação web para alinhamento de duas sequências de DNA utilizando os algoritmos de **Needleman-Wunsch** (alinhamento global) e **Smith-Waterman** (alinhamento local).

O projeto foi desenvolvido como trabalho prático de programação de alinhamento de sequências, com implementação própria dos algoritmos de programação dinâmica, construção e exibição da matriz, reconstrução por traceback, cálculo do score e interface para entrada e visualização dos resultados.

---

## 1. Sobre o projeto

O sistema recebe exatamente **duas sequências de DNA** e permite realizar:

- alinhamento global;
- alinhamento local;
- configuração dos valores de Match, Mismatch e Gap;
- entrada manual das sequências;
- carregamento de arquivos `.txt` e `.fasta`;
- validação das sequências;
- construção da matriz de programação dinâmica;
- identificação das direções utilizadas;
- execução do traceback;
- reconstrução das sequências alinhadas;
- visualização de matches, mismatches e gaps;
- apresentação do score final.

O objetivo não é apenas apresentar o alinhamento final, mas permitir visualizar **como a programação dinâmica chegou ao resultado**, incluindo a matriz e o traceback.

O trabalho exige que os algoritmos sejam implementados pelos estudantes, não sendo permitida a utilização de bibliotecas ou serviços que realizem diretamente o alinhamento ou forneçam a matriz de programação dinâmica.

---

# 2. Tecnologias utilizadas

## Backend

- Python
- FastAPI
- Pydantic
- Pytest
- Uvicorn

## Frontend

- Next.js
- React
- TypeScript
- Tailwind CSS

## Comunicação

- API REST
- JSON

---

# 3. Arquitetura do projeto

```text
sequence-alignment/
│
├── backend/
│   │
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   │
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   └── alignment_routes.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   └── alignment_schema.py
│   │   │
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── validation_service.py
│   │   │   ├── file_service.py
│   │   │   ├── alignment_service.py
│   │   │   ├── global_alignment.py
│   │   │   └── local_alignment.py
│   │   │
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── traceback_utils.py
│   │
│   ├── tests/
│   │   └── __init__.py
│   │
│   ├── requirements.txt
│   └── .gitignore
│
├── frontend/
│   │
│   ├── app/
│   │   ├── components/
│   │   │   ├── AlignmentForm.tsx
│   │   │   ├── AlignmentResult.tsx
│   │   │   ├── AlignmentMatrix.tsx
│   │   │   └── Traceback.tsx
│   │   │
│   │   ├── lib/
│   │   │   ├── api.ts
│   │   │   └── validation.ts
│   │   │
│   │   ├── page.tsx
│   │   ├── layout.tsx
│   │   └── globals.css
│   │
│   ├── public/
│   ├── package.json
│   └── ...
│
├── .gitignore
└── README.md
```

---

# 4. Funcionamento geral

O sistema segue o seguinte fluxo:

```text
             Entrada
                │
                ▼
       ┌─────────────────┐
       │ Duas sequências │
       │     de DNA      │
       └────────┬────────┘
                │
                ▼
       ┌─────────────────┐
       │    Validação    │
       └────────┬────────┘
                │
         ┌──────┴──────┐
         │             │
      inválida        válida
         │             │
         ▼             ▼
     Mostrar       Selecionar
       erro          método
                       │
                ┌──────┴──────┐
                │             │
             GLOBAL         LOCAL
                │             │
                ▼             ▼
        Needleman-Wunsch  Smith-Waterman
                │             │
                └──────┬──────┘
                       │
                       ▼
                  Matriz DP
                       │
                       ▼
                   Traceback
                       │
                       ▼
              Sequências alinhadas
                       │
                       ▼
                    Score
                       │
                       ▼
                  Resultado
```

---

# 5. Entrada de dados

Cada execução trabalha com exatamente duas sequências:

```text
Seq1
Seq2
```

As sequências podem ser:

- digitadas diretamente na interface;
- carregadas através de arquivo `.txt`;
- carregadas através de arquivo `.fasta`.

O sistema aceita letras minúsculas e as converte automaticamente para maiúsculas.

Somente as bases:

```text
A
C
G
T
```

são permitidas.

---

# 6. Parâmetros de alinhamento

O usuário pode definir três parâmetros:

```text
Match
Mismatch
Gap
```

Exemplo:

```text
Match:     +2
Mismatch:  -1
Gap:       -2
```

O projeto utiliza **penalidade linear de gap**. Não é utilizado gap affine.

A regra de pontuação é:

```text
mesma base       → Match
bases diferentes → Mismatch
base x gap       → Gap
```



---

# 7. Métodos de alinhamento

## 7.1 Alinhamento global

O alinhamento global utiliza o algoritmo:

**Needleman-Wunsch**

O objetivo é encontrar um alinhamento considerando as sequências inteiras.

A primeira linha e a primeira coluna da matriz são inicializadas utilizando penalidades acumuladas de gap.

A recorrência utilizada é:

```text
H(i,j) = max(
    H(i-1,j-1) + score,
    H(i-1,j)   + gap,
    H(i,j-1)   + gap
)
```

O traceback começa na célula inferior direita da matriz e termina na origem.

O score final é o valor da célula inferior direita.

---

## 7.2 Alinhamento local

O alinhamento local utiliza o algoritmo:

**Smith-Waterman**

O objetivo é encontrar a região de maior similaridade entre as sequências.

A primeira linha e a primeira coluna são inicializadas com zero.

A recorrência utilizada é:

```text
H(i,j) = max(
    0,
    H(i-1,j-1) + score,
    H(i-1,j)   + gap,
    H(i,j-1)   + gap
)
```

O traceback começa na célula de maior valor da matriz e termina quando encontra uma célula com valor zero.

O score local corresponde ao maior valor encontrado na matriz.

---

# 8. Direções do traceback

Cada célula da matriz pode possuir uma direção:

```text
D = diagonal
V = vertical
H = horizontal
```

## Diagonal

Representa:

```text
base contra base
```

Exemplo:

```text
A
A
```

Pode representar Match ou Mismatch.

## Vertical

Representa:

```text
base em Seq1
gap em Seq2
```

Exemplo:

```text
A
-
```

## Horizontal

Representa:

```text
gap em Seq1
base em Seq2
```

Exemplo:

```text
-
A
```

Em caso de empate entre possibilidades, o projeto utiliza a prioridade:

```text
Diagonal
    ↓
Vertical
    ↓
Horizontal
```

Isso garante um comportamento determinístico para o traceback.

---

# 9. Validação

O sistema realiza validações antes de executar o algoritmo.

São verificadas situações como:

- sequência vazia;
- caractere inválido;
- quantidade diferente de duas sequências;
- parâmetros ausentes;
- parâmetros não numéricos;
- arquivo incompatível;
- arquivo sem exatamente duas sequências;
- arquivo que não pode ser lido.

O frontend realiza uma primeira validação para fornecer feedback imediato ao usuário.

O backend realiza novamente a validação antes do processamento.

Dessa forma, o backend não depende da validação realizada pelo navegador.

---

# 10. Arquivos suportados

## TXT

Um arquivo `.txt` deve conter exatamente duas sequências.

Exemplo:

```text
ACGTAC
ACGTTC
```

## FASTA

O arquivo `.fasta` pode utilizar identificadores FASTA:

```text
>Seq1
ACGTAC

>Seq2
ACGTTC
```

Também é possível utilizar sequências distribuídas em múltiplas linhas dentro de cada entrada FASTA.

O sistema reúne essas linhas antes da validação.

---

# 11. API

O backend disponibiliza uma API REST.

## Executar alinhamento

```http
POST /api/alignment/
```

### Request

```json
{
  "seq1": "ACGTAC",
  "seq2": "ACGTTC",
  "match": 2,
  "mismatch": -1,
  "gap": -2,
  "mode": "global"
}
```

O campo `mode` pode ser:

```text
global
```

ou:

```text
local
```

### Resultado

A API retorna informações como:

```json
{
  "method": "global",
  "seq1": "ACGTAC",
  "seq2": "ACGTTC",
  "parameters": {
    "match": 2,
    "mismatch": -1,
    "gap": -2
  },
  "score": 9,
  "aligned_seq1": "ACGTAC",
  "markers": "||||.|",
  "aligned_seq2": "ACGTTC",
  "matrix": [],
  "directions": [],
  "traceback": [],
  "start_position": {
    "row": 6,
    "column": 6,
    "direction": "START"
  }
}
```

As matrizes aparecem completas na resposta real.

---

# 12. Resultado apresentado

A interface apresenta:

1. método utilizado;
2. score final;
3. parâmetros;
4. sequências originais;
5. alinhamento reconstruído;
6. indicadores de match/mismatch/gap;
7. matriz de programação dinâmica;
8. direções das células;
9. células utilizadas no traceback;
10. informações do traceback.

O alinhamento utiliza:

```text
|  Match
.  Mismatch
·  Gap
```

Visualmente, os caracteres também são diferenciados na interface.

---

# 13. Matriz de programação dinâmica

A matriz é preservada porque ela é parte essencial do trabalho.

Exemplo simplificado:

```text
      ∅   A   C   G
  ∅   0  -2  -4  -6
  A  -2   2   0  -2
  C  -4   0   4   2
  G  -6  -2   2   6
```

Além dos valores, a aplicação apresenta as direções:

```text
D = diagonal
V = vertical
H = horizontal
```

As células pertencentes ao traceback são destacadas visualmente.

Isso permite observar não apenas o resultado, mas o caminho utilizado pela programação dinâmica.

---

# 14. Traceback

O traceback é armazenado como uma sequência de posições.

Exemplo:

```json
[
  {
    "row": 6,
    "column": 6,
    "direction": "D"
  },
  {
    "row": 5,
    "column": 5,
    "direction": "D"
  }
]
```

Na interface, essas informações são apresentadas em uma tabela contendo:

```text
Passo
Linha
Coluna
Direção
Operação
```

As operações são interpretadas como:

```text
D → Diagonal — base contra base
V → Vertical — gap em Seq2
H → Horizontal — gap em Seq1
```

---

# 15. Exemplo oficial

O projeto utiliza também o exemplo apresentado no trabalho:

```text
Seq1 = ACGTAC
Seq2 = ACGTTC
```

Parâmetros:

```text
Match = +2
Mismatch = -1
Gap = -2
```

O alinhamento esperado é:

```text
ACGTAC
||||.|
ACGTTC
```

A pontuação é:

```text
5 matches × 2 = 10
1 mismatch × -1 = -1

Score = 9
```

Esse exemplo pode ser utilizado para validar a implementação do alinhamento global.

---

# 16. Complexidade

Para sequências de tamanhos `m` e `n`:

```text
Tempo:
O(m × n)

Memória:
O(m × n)
```

A memória utiliza a matriz completa porque ela precisa permanecer disponível para:

- visualização;
- traceback;
- explicação do resultado.



---

# 17. Instalação

## 17.1 Backend

Entre na pasta:

```bash
cd backend
```

Crie um ambiente virtual:

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux/macOS

```bash
source venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute o servidor:

```bash
uvicorn app.main:app --reload
```

O backend estará disponível em:

```text
http://127.0.0.1:8000
```

A documentação automática da API pode ser acessada pelo Swagger:

```text
http://127.0.0.1:8000/docs
```

---

# 18. Frontend

Entre na pasta:

```bash
cd frontend
```

Instale as dependências:

```bash
npm install
```

Crie o arquivo:

```text
.env.local
```

com:

```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

Execute:

```bash
npm run dev
```

O frontend estará disponível em:

```text
http://localhost:3000
```

---

# 19. Testes do backend

Na pasta `backend`:

```bash
pytest
```

Os testes verificam principalmente:

- validação;
- algoritmo global;
- algoritmo local;
- matriz;
- traceback;
- direções;
- score.

---

# 20. Estado atual do desenvolvimento

Até o momento, o projeto possui:

### Etapa 1 — Arquitetura

- [x] Estrutura do projeto
- [x] Separação frontend/backend
- [x] Definição das responsabilidades

### Etapa 2 — Backend básico

- [x] FastAPI
- [x] Rotas
- [x] Schemas
- [x] CORS
- [x] Endpoint de health check

### Etapa 3 — Entrada e validação

- [x] Validação de DNA
- [x] Normalização
- [x] Validação de parâmetros
- [x] Arquivos `.txt`
- [x] Arquivos `.fasta`

### Etapa 4 — Needleman-Wunsch

- [x] Inicialização
- [x] Matriz
- [x] Recorrência
- [x] Traceback
- [x] Score

### Etapa 5 — Smith-Waterman

- [x] Inicialização
- [x] Matriz
- [x] Recorrência
- [x] Identificação do maior score
- [x] Traceback
- [x] Score local

### Etapa 6 — Resultado completo

- [x] Matriz
- [x] Direções
- [x] Traceback
- [x] Sequências alinhadas
- [x] Marcadores
- [x] Score
- [x] Posição inicial

### Etapa 7 — Frontend

- [x] Next.js
- [x] Formulário
- [x] Integração com API
- [x] Entrada manual
- [x] Upload `.txt`
- [x] Upload `.fasta`
- [x] Exibição do resultado
- [x] Exibição da matriz
- [x] Exibição do traceback
- [x] Destaque visual do alinhamento
- [x] Destaque do traceback
- [x] Validação frontend
- [x] Tratamento de erros

### Etapa 8 — Integração e testes

- [ ] Ainda não iniciada

### Etapa 9 — Finalização

- [ ] Ainda não iniciada

---

# 21. Próximas etapas

A próxima etapa será a **Etapa 8 — integração e testes ponta a ponta**.

Nessa etapa serão verificados:

```text
Frontend
   ↓
API
   ↓
Validação
   ↓
Algoritmo
   ↓
Matriz
   ↓
Traceback
   ↓
Alinhamento
   ↓
Score
   ↓
Frontend
```

Também serão testados:

- alinhamento global;
- alinhamento local;
- entrada manual;
- `.txt`;
- `.fasta`;
- sequências inválidas;
- parâmetros inválidos;
- arquivos inválidos;
- casos sem alinhamento local positivo;
- consistência entre matriz, traceback e alinhamento.

---

# 22. Escopo do projeto

O projeto está focado exclusivamente no alinhamento de duas sequências.

Não fazem parte do escopo:

- alinhamento múltiplo;
- alinhamento baseado em perfis;
- perfil × sequência;
- perfil × perfil;
- Sum-of-Pairs;
- árvores guia;
- seleção progressiva de sequências.

O foco é:

```text
Needleman-Wunsch
        +
Smith-Waterman
        +
Matriz
        +
Traceback
        +
Score
        +
Validação
        +
Interface
```



---

# 23. Princípio do projeto

O resultado final não deve mostrar somente:

```text
"qual foi o alinhamento?"
```

mas também:

```text
"como o algoritmo chegou a esse alinhamento?"
```

Por isso, a matriz de programação dinâmica e o traceback são elementos fundamentais da aplicação.

A interface foi construída para permitir que o usuário acompanhe:

```text
Sequências
    ↓
Parâmetros
    ↓
Matriz
    ↓
Direções
    ↓
Traceback
    ↓
Alinhamento
    ↓
Score
```

Esse fluxo representa o processo computacional utilizado pelos algoritmos de alinhamento implementados no projeto.

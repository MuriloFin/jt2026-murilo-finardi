VIDEO: https://drive.google.com/file/d/1tm7uVpddlXyOqG7XDtIg0WSHnUtvMAaR/view?usp=sharing

# Hackathon Jovens Talentos AI Builder 2026 - Seazone

**Candidato:** Murilo Favoretto Finardi  
**Cidade analisada:** Itapema/SC  
**Recomendação final:** apartamento de **2 quartos em Meia Praia**, com capacidade próxima de 6 hóspedes e prioridade para acesso à praia.

## TL;DR

A análise não confirma a tese inicial de que **studios/1 quarto no Centro** sejam a aposta mais eficiente. Os dados dão suporte à eficiência de imóveis compactos, mas a evidência de localização favorece **Meia Praia**. No mesmo produto de 1 quarto, Meia Praia apresenta receita-proxy mediana de **R$ 14,3 mil** em 77 dias contra **R$ 10,8 mil** no Centro, com preço de compra mediano semelhante (**R$ 877,5 mil vs. R$ 890 mil**).

Para a decisão de investimento, escolhi **2 quartos em Meia Praia** por combinar retorno competitivo com amostra significativamente mais robusta: **104 Airbnbs comparáveis**, **241 anúncios de venda**, receita-proxy de **R$ 16,4 mil** em 77 dias, ocupação-proxy de **48,7%** e preço de aquisição mediano de **R$ 1,07 milhão**. A anualização mecânica do período equivale a um **run-rate bruto de 7,2% a.a.**, que não deve ser interpretado como forecast anual.

## Arquivos principais

- Análise - Relatório Executivo Itapema - apoio visual para o vídeo de 3 minutos e conclusão dos dados.
- relatorio.md - recomendação final escrita e premissas.
- análise_itapema - código que reproduz as principais tabelas e testes.
- ai-log - sessão completa com IA em texto.

## Como rodar

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Disponibilizar os cinco CSVs oficiais

O script procura os arquivos em `./data/` e, se não encontrar, na raiz do repositório:

- `Details_Itapema.csv`
- `Hosts_ids_Itapema.csv`
- `Mesh_Ids_Data_Itapema.csv`
- `Price_AV_Itapema.csv`
- `VivaReal_Itapema.csv`

### 3. Executar

```bash
python analise_itapema.py --data-dir data
```

As tabelas consolidadas são salvas em `output/tables/`.

## Metodologia em uma frase

Como `Price_AV_Itapema.csv` não contém receita realizada, construí uma **receita-proxy de 77 dias** a partir das noites indisponíveis no snapshot de 20/01 multiplicadas pela diária mediana observada, usando apenas os **657 imóveis presentes nos snapshots de 07/01 e 20/01**.

A principal premissa é que indisponibilidade pode significar reserva **ou bloqueio do proprietário**. Por isso, o resultado é tratado como proxy e não como faturamento observado.

## Respostas às quatro perguntas

1. **Melhor perfil:** apartamento de 2 quartos em Meia Praia para uma decisão risk-adjusted. O 1 quarto tem run-rate pontual maior, mas só 14 observações comparáveis.
2. **Melhor localização em receita:** Meia Praia, com receita-proxy mediana de **R$ 19,5 mil**, cerca de **37% acima do Centro**, e ocupação-proxy de **45,5% vs. 36,4%**.
3. **Características relevantes:** vista para o mar aparece associada a **+9,0% na diária e +5,7 p.p. de ocupação**; acesso à praia a **+5,6 p.p. de ocupação**. O modelo explica melhor diária do que ocupação.
4. **O que compraria:** 2 quartos em Meia Praia, ~85 m², ~6 hóspedes e compra mediana de **R$ 1,07 milhão**. Receita-proxy de R$ 16,4 mil / 77 dias -> **7,2% a.a. de run-rate bruto** e payback bruto teórico de 13,8 anos.

## Limitações principais

- indisponibilidade de calendário não equivale necessariamente a reserva;
- período curto e sazonal, incluindo verão;
- bairro não captura distância efetiva da praia;
- estimativa de retorno é bruta e não contempla custos operacionais, impostos, mobília ou financiamento;
- studios têm amostra insuficiente para conclusão robusta.

## Se eu tivesse mais uma semana

Eu aprofundaria cinco frentes: distância real da orla, sazonalidade, validação de reservas versus bloqueios, retorno líquido (NOI/cap rate) e modelo hedônico de preço de compra por m².

## Uso de IA

A pasta `ai-log/` deve conter a **exportação integral da sessão**, em texto, mostrando inclusive mudanças de hipótese, checagens, correções e limitações identificadas durante o processo.

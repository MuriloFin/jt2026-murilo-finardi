# Recomendação de investimento imobiliário - Itapema/SC

**Murilo Favoretto Finardi - Hackathon Jovens Talentos AI Builder 2026 | Seazone**

## Recomendação final

Se a Seazone fosse investir hoje em Itapema, eu compraria um **apartamento de 2 quartos em Meia Praia**, com capacidade próxima de 6 hóspedes, buscando um imóvel em torno de **85 m²** e priorizando **acesso à praia** e, quando o prêmio de aquisição for economicamente justificável, **vista para o mar**.

A decisão não maximiza apenas a maior receita ou o maior yield pontual. O critério foi o melhor equilíbrio entre **receita, retorno sobre o capital, tamanho da amostra e repetibilidade da tese**.

No painel comparável, o segmento de 2 quartos em Meia Praia reúne **104 Airbnbs**, receita-proxy mediana de **R$ 16.352 em 77 dias**, ocupação-proxy de **48,7%** e diária mediana de **R$ 473**. No mercado de venda, há **241 anúncios comparáveis**, com preço mediano de **R$ 1,07 milhão** e área mediana de **85 m²**.

A razão entre a receita-proxy do período e o preço de aquisição é de aproximadamente **1,53% em 77 dias**. Uma anualização puramente mecânica equivale a **7,2% a.a. de run-rate bruto**, ou um payback bruto teórico de **13,8 anos**. Esse número não é uma projeção de retorno líquido: o período inclui parte relevante da alta temporada e não contempla condomínio, IPTU, manutenção, mobília, limpeza, gestão, taxa de plataforma, impostos, financiamento ou valorização imobiliária.

## Metodologia

Foram utilizadas as cinco bases disponibilizadas no desafio:

- **Details_Itapema.csv:** tipologia, quartos, capacidade, amenities e indicadores do listing;
- **Hosts_ids_Itapema.csv:** reputação e experiência do anfitrião;
- **Mesh_Ids_Data_Itapema.csv:** bairro e coordenadas;
- **Price_AV_Itapema.csv:** preços e disponibilidade por data em diferentes snapshots;
- **VivaReal_Itapema.csv:** preço, área e características do mercado de venda.

O principal cuidado metodológico foi não tratar `Price_AV_Itapema.csv` como receita observada. A base possui calendários de preço, não reservas realizadas. Por isso, construí uma **receita-proxy de 77 dias**, usando a janela comum de 20/01 a 06/04/2025 e os **657 imóveis presentes tanto no snapshot de 07/01 quanto no de 20/01**.

Para cada imóvel, estimei:

`ocupação-proxy = noites indisponíveis / 77`

`receita-proxy = noites indisponíveis x diária mediana observada`

Uma data ausente no snapshot de 20/01 é interpretada como indisponível. A limitação é relevante: indisponibilidade pode refletir uma reserva ou um bloqueio do proprietário. Portanto, os resultados devem ser interpretados como **sinais relativos de performance**, não faturamento efetivamente realizado.

## 1. Melhor perfil de imóvel

Os imóveis de 3 quartos geram maior receita absoluta, mas exigem capital desproporcionalmente maior. Em Meia Praia, por exemplo, o 3 quartos apresenta receita-proxy mediana de aproximadamente **R$ 20,7 mil**, 27% acima dos **R$ 16,4 mil** do 2 quartos, enquanto o preço de compra mediano sobe de **R$ 1,07 milhão para R$ 1,88 milhão**, aumento de cerca de 76%.

O 1 quarto em Meia Praia possui o maior run-rate pontual entre os principais candidatos (**7,7% a.a.**), mas a amostra contém apenas **14 Airbnbs comparáveis**. O 2 quartos fica muito próximo em retorno (**7,2% a.a.**) com uma amostra de **104 imóveis**, além de maior profundidade no mercado de compra.

Por isso, a recomendação é **2 quartos em Meia Praia** como melhor perfil risk-adjusted.

## 2. Melhor localização em receita

Entre bairros com pelo menos 30 imóveis comparáveis, **Meia Praia é a líder**:

| Região | n | Receita-proxy 77d | Ocupação-proxy | Diária mediana |
|---|---:|---:|---:|---:|
| Meia Praia | 421 | R$ 19,5 mil | 45,5% | R$ 625 |
| Centro | 161 | R$ 14,2 mil | 36,4% | R$ 580 |
| Morretes | 54 | R$ 14,2 mil | 39,6% | R$ 500 |

A receita-proxy mediana de Meia Praia é aproximadamente **37% superior à do Centro**. A vantagem combina maior diária (+7,8%) e maior ocupação-proxy (+9,1 p.p.).

Como teste de robustez, o bootstrap de 10 mil reamostragens colocou a diferença mediana Meia Praia - Centro entre aproximadamente **+R$ 3,6 mil e +R$ 8,0 mil** no intervalo de 95%. O teste de Mann-Whitney também indica diferença estatisticamente relevante (**p < 0,001**).

## 3. Características associadas às melhores receitas

Para separar preço e ocupação, estimei regressões multivariadas com controles de bairro e tipo de anúncio.

Principais associações:

- **quarto adicional:** +20,6% na diária, sem efeito robusto em ocupação;
- **banheiro adicional:** +12,2% na diária;
- **vista para o mar:** +9,0% na diária e +5,7 p.p. na ocupação-proxy;
- **acesso à praia:** +5,6 p.p. na ocupação-proxy;
- **piscina:** +36,9% na diária, mas -8,5 p.p. de ocupação-proxy.

A piscina ilustra por que associação não deve ser tratada como causalidade. O atributo provavelmente sinaliza imóveis e edifícios de padrão superior, que cobram mais e podem operar com ocupação menor.

O modelo explica aproximadamente **39% da variação da diária**, mas apenas **8% da ocupação-proxy**. Isso indica que fatores ausentes da base - micro-localização, sazonalidade, qualidade do prédio, pricing e bloqueios de calendário - têm papel importante na demanda.

## 4. Posição sobre compactos no Centro

**Refuto a tese como formulada.**

Os dados sugerem que imóveis menores podem ser eficientes em capital, mas não sustentam que o **Centro** seja a melhor localização. Comparando o mesmo produto, apartamentos de 1 quarto:

| | Centro 1Q | Meia Praia 1Q |
|---|---:|---:|
| Airbnbs comparáveis | 70 | 14 |
| Receita-proxy 77d | R$ 10,8 mil | R$ 14,3 mil |
| Ocupação-proxy | 29,9% | 40,9% |
| Compra mediana | R$ 890 mil | R$ 877,5 mil |
| Run-rate bruto | 5,7% | 7,7% |

Com custo de aquisição semelhante, o 1 quarto em Meia Praia apresenta aproximadamente **33% mais receita-proxy**.

A parte específica de **studios** não pode ser validada com segurança: existem apenas **2 studios no Centro** na base completa e nenhum deles está no painel comparável. Em Meia Praia são 29 na base completa e somente 4 no painel comparável.

Assim, minha posição é: **a hipótese “compacto” merece investigação adicional; a hipótese “Centro” não é a mais forte nos dados atuais.**

## O que faria com mais uma semana

1. **Micro-localização:** calcular distância da praia e analisar faixas de 100, 300 e 500 metros.
2. **Sazonalidade:** ampliar snapshots para meses de baixa temporada, feriados e diferentes antecedências de reserva.
3. **Reserva vs. bloqueio:** validar indisponibilidade com outra fonte de bookings/ocupação.
4. **Retorno líquido:** incluir custos para chegar a NOI, cap rate e cash-on-cash return.
5. **Modelo de aquisição:** estimar preço/m² ajustando por idade do edifício, vaga, andar, padrão e distância da orla.

## Conclusão

**A evidência favorece um apartamento de 2 quartos em Meia Praia.** Ele não é o segmento com o maior retorno pontual da tabela, mas é o que oferece a combinação mais defensável entre performance, capital necessário e robustez da amostra. A tese de compactos no Centro não é confirmada pelos dados disponíveis.

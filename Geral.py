# Contents of ~/my_app/main_page.py
import streamlit as st
import pandas as pd
import altair as alt
import pip
pip.main(["install", "openpyxl"])

base = pd.read_excel('Base 17102022v.xlsx')
base.dropna(inplace=True)#remover as linhas que têm espaço vazio (e.g., notas ainda não lançadas)
#Para importar a base de dados sem remover as linhas que têm espaço vazio:
base0 = pd.read_excel('Base 17102022v.xlsx')

#Para definir as configurações da aba e da página:
PAGE_CONFIG = {"page_title": "ESEG - Apoio ao aluno", "page_icon": ":globe_with_meridians:", "layout": "wide"}
st.set_page_config(**PAGE_CONFIG)

#Para alterar o estilo da página (e.g., alterar as cores de fundo dos botões):
m = st.markdown("""
<style>
span[role="button"] {
    background-color: blue;
}

div[data-baseweb="slider"] >  div:nth-child(1) >  div {
    background: blue;
    }

div[data-testid="stThumbValue"] {
    color: blue;
    }

div[role="slider"] {
    background: blue;
    }
    
.st-cj{
    font-size: 16px;
}

.css-16huue1 {
    font-size: 17px;
}

.css-18e3th9 {
    flex: 1 1 0%;
    width: 100%;
    padding: 0.1rem 2rem 1rem;
    min-width: auto;
    max-width: initial;
}

element.style {
    padding-bottom: 1px;
    padding-top: 1px;
}
.css-1avcm0n {
    position: fixed;
    top: 0px;
    left: 0px;
    right: 0px;
    height: 0.5rem;
    background: rgb(14, 17, 23);
    outline: none;
    z-index: 999990;
    display: block;
}
h2{
    font-family: "Source Sans Pro", sans-serif;
    font-weight: 600;
    color: rgb(0, 0, 0);
    letter-spacing: -0.005em;
    padding: 0rem 0px;
    margin: 0px;
    line-height: 1.2;
}
h4 {
    font-family: "Source Sans Pro", sans-serif;
    font-weight: 600;
    color: rgb(0, 0, 0);
    padding: 0rem 0px 0rem;
    margin: 0px;
    line-height: 1.2;
}
h5 {
    font-family: "Source Sans Pro", sans-serif;
    font-weight: 600;
    color: rgb(0, 0, 0);
    padding: 0px 0px 0.3rem;
    margin: 0px;
    line-height: 1.2;
}
</style>""", unsafe_allow_html=True)

cola, colb, colc = st.columns((0.4, 5, 0.2))

colb1,ccolc1 = st.columns(( 7, 0.3,)) #titulo

cola2, colb2,ccolc2, cold2, cole2, colf2, colg2 = st.columns((1.5, 1.5, 0.7, 2.25, 2.25, 2.25, 2.25)) #slider e metrics

cola3, colb3, colc3,  cold3 = st.columns((2.7, 0.2, 9, 0.2)) #grafico e botoes


with cola2:
    nota1, nota2 = st.slider('Nota', 0, 10, (0, 10))
with colb2:
    freq1, freq2 = st.slider('Frequência', 0.0, 1.0, (0.0, 1.0))

# Para elencar as opções do botão "Curso", criar o botão "Curso"
# e salvar uma opção escolhida na variável "curso selecionado":
with cola3:
    opcoes_do_botao_curso = sorted(base.CURSO2.unique())  # sorted = em ordem alfabetica
    curso_selecionado = st.multiselect('Graduação', opcoes_do_botao_curso, opcoes_do_botao_curso)
    base_filtrada = base.query('CURSO2 == @curso_selecionado ')
    opcoes_do_botao_semestre = sorted(base_filtrada.SEMESTRE.unique())
    semestre_selecionado = st.multiselect('Semestre', opcoes_do_botao_semestre, opcoes_do_botao_semestre)
    opcoes_do_botao_turno = sorted(base_filtrada.TURNO_DA_DISCIPLINA.unique())
    turno_selecionado = st.multiselect('Turno', opcoes_do_botao_turno, opcoes_do_botao_turno)


#filtragem de disciplina e turma
base_geral = base_filtrada.query('SEMESTRE == @semestre_selecionado & \
                                    CURSO2 == @curso_selecionado & \
                                    INDICADOR_GERAL >= @nota1 &  \
                                    INDICADOR_GERAL <= @nota2 & \
                                    FREQ_GERAL >= @freq1 & \
                                    FREQ_GERAL <= @freq2 & \
                                    TURNO_DA_DISCIPLINA == @turno_selecionado')

base_filtrada0 = base.query('CURSO2 == @curso_selecionado')

#NÚMERO DE ALUNOS
#filtragem de nota e freq geral
aprovado = base_geral.query('INDICADOR_GERAL >= 6 & FREQ_GERAL >= 0.75')
reprovado = base_geral.query('INDICADOR_GERAL < 6 & FREQ_GERAL < 0.75')
reprovado_nota = base_geral.query('INDICADOR_GERAL < 6 & FREQ_GERAL >= 0.75')
reprovado_freq = base_geral.query('INDICADOR_GERAL >= 6 & FREQ_GERAL < 0.75')

#numero de alunos por status
alunosaprovados = aprovado.NOME.unique()
nalunosaprovados = len(alunosaprovados)

alunosreprovados = reprovado.NOME.unique()
nalunosreprovados = len(alunosreprovados)

alunosreprovadosnota = reprovado_nota.NOME.unique()
nalunosreprovadosnota = len(alunosreprovadosnota)

alunosreprovadosfreq = reprovado_freq.NOME.unique()
nalunosreprovadosfreq = len(alunosreprovadosfreq)

reprovados_total = nalunosreprovados + nalunosreprovadosnota + nalunosreprovadosfreq



#linhas
linhan = pd.DataFrame({'y': [6, 6], 'x': [0.0, 1.1]})
linhaf = pd.DataFrame({'y': [0, 10], 'x': [0.75, 0.75]})

linha_horizontal = alt.Chart(linhan).mark_line(color='green').encode(
    x=alt.Y('x', scale=alt.Scale(domain=(freq1, freq2), clamp=False)),
    y=alt.Y('y', scale=alt.Scale(domain=(nota1, nota2), clamp=False)))

linha_vertical = alt.Chart(linhaf).mark_line(color='green').encode(
    x=alt.Y('x', scale=alt.Scale(domain=(freq1, freq2), clamp=False)),
    y=alt.Y('y', scale=alt.Scale(domain=(nota1, nota2), clamp=False)))

#grafico 1
#cor do ponto

quad = ['Superior Direito', 'Inferior Esquerdo', 'Inferior Direito', 'Superior Esquerdo']

cor = ['blue', 'red', 'yellow', 'orange']

grafico_geral = alt.Chart(base_geral).mark_circle(size=100).encode(
    alt.X('FREQ_GERAL', axis=alt.Axis(format='%', title='FREQUÊNCIA', titleFontSize=15, labelFontSize=15)),
    alt.Y('INDICADOR_GERAL', axis=alt.Axis(title='NOTA', orient="left", titleFontSize=15, labelFontSize=15)),
    tooltip=['NOME', 'RA'],
    color=alt.Color('QUADRANTE_GERAL',
                    scale=alt.Scale(domain=quad,
                                    range=cor),
                    legend=None)).interactive().properties(width=1000, height=500)

#TITULO
with colb:
    cursos = sorted(base_geral.CURSO.unique())
    prefixo0 = '               DESEMPENHO '
    titulo = prefixo0 + 'de ' + ' e '.join(cursos)
    titulo = titulo.upper()
    st.header(titulo if len(cursos) < 5 else prefixo0 + 'GERAL')

with colb1:
    st.markdown('##### Média simples das notas lançadas de cada aluno nas disciplinas do período letivo de 2022-2 '
                '(desconsidera os cálculos dos planos de ensino).')
    st.markdown('##### Dados atualizados em 13/10/2022.')
with cold2:
    alunos = base_geral.NOME.unique()
    nalunos = len(alunos)
    alunos0 = base_filtrada0.NOME.unique()
    nalunos0 = len(alunos0)
    st.metric(label="TOTAL ESEG:", value=nalunos0)
with cole2:
    st.metric(label="TOTAL GRÁFICO: ", value=nalunos)
with colf2:
    st.metric(label="APROVADOS: ", value=nalunosaprovados)
with colg2:
    st.metric(label="REPROVADOS: ", value=reprovados_total)

with colc3:
    st.altair_chart(linha_horizontal + linha_vertical + grafico_geral, use_container_width=True)

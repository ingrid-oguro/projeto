# Contents of ~/my_app/pages/page_2.py
import streamlit as st
import pandas as pd
import altair as alt

base = pd.read_excel('/content/drive/MyDrive/Relatórios_20222/Desempenho/Base 17102022v.xlsx')
base.dropna(inplace=True)#remover as linhas que têm espaço vazio (e.g., notas ainda não lançadas)
#Para importar a base de dados sem remover as linhas que têm espaço vazio:
base0 = pd.read_excel('/content/drive/MyDrive/Relatórios_20222/Desempenho/Base 17102022v.xlsx')
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
    color: rgb(250, 250, 250);
    letter-spacing: -0.005em;
    padding: 0rem 0px;
    margin: 0px;
    line-height: 1.2;
}
h4 {
    font-family: "Source Sans Pro", sans-serif;
    font-weight: 600;
    color: rgb(250, 250, 250);
    padding: 0rem 0px 0rem;
    margin: 0px;
    line-height: 1.2;
}
h5 {
    font-family: "Source Sans Pro", sans-serif;
    font-weight: 600;
    color: rgb(250, 250, 250);
    padding: 0px 0px 0.3rem;
    margin: 0px;
    line-height: 1.2;
}
</style>""", unsafe_allow_html=True)
#GRAFICO 2

colb0, colc0 = st.columns((5, 0.1))#titulo

cola4, colb4, colc4 = st.columns((0.1, 7, 0.2))#subtitulo

cola5, colb5, colc5, cold5, cole5, colf5, colg5 = st.columns((1.5, 1.5,0.7, 2.25, 2.25, 2.25, 2.25)) #slider e metrics

cola6, colb6, colc6,  cold6 = st.columns((2.4, 0.2, 9, 0.2)) #grafico e

with cola5:
    nota3, nota4 = st.slider('Notas', 0, 10, (0, 10))

with colb5:
    freq3, freq4 = st.slider('Frequências', 0.0, 1.0, (0.0, 1.0))


with cola6:
    opcoes_do_botao_disciplina = sorted(base.DISCIPLINA.unique())
    disciplina = st.multiselect('Disciplina', opcoes_do_botao_disciplina)

#Para filtrar as opcoes de disciplina:
filtro_disciplina = base.query('DISCIPLINA == @disciplina')

#titulo
with colb0:
    disciplinasl = sorted(filtro_disciplina.DISCIPLINA.unique())
    prefixo0 = 'DESEMPENHO DE '
    titulo = prefixo0 + ' e '.join(disciplinasl)
    titulo = titulo.upper()
    st.header(titulo)

with colb4:
    curso02 = sorted(filtro_disciplina.CURSO.unique())
    prefixo0 = 'NA GRADUAÇÃO DE '
    titulo02 = prefixo0 + ' e '.join(curso02)
    titulo02 = titulo02.upper()
    st.markdown('#### ' +titulo02)
    st.markdown('##### Média simples das avaliações lançadas de cada aluno em uma disciplina (desconsidera os cálculos dos planos de ensino).')
    st.markdown('##### Dados atualizados em 13/10/2022.')
#outros botoes
with cola6:
    opcoes_cursos2 = sorted(filtro_disciplina.CURSO.unique())  # sorted = em ordem alfabetica
    curso_selecionado2 = st.multiselect('Graduação  :', opcoes_cursos2, opcoes_cursos2)
    opcoes_semestre2 = sorted(filtro_disciplina.SEMESTRE.unique())
    semestre_selecionado2 = st.multiselect('Semestre:', opcoes_semestre2, opcoes_semestre2)
    opcao_turno = sorted(filtro_disciplina.TURNO_DA_DISCIPLINA.unique())
    turno_selecionado2 = st.multiselect('Turnos', opcao_turno, opcao_turno)

#filtragem
base_disciplina = filtro_disciplina.query('DISCIPLINA == @disciplina &\
                                       CURSO == @curso_selecionado2 & \
                                       SEMESTRE == @semestre_selecionado2 & \
                                       INDICADOR >= @nota3 & \
                                       INDICADOR <= @nota4 & \
                                       FREQ >= @freq3 & \
                                       FREQ <= @freq4 & \
                                       TURNO_DA_DISCIPLINA == @turno_selecionado2')

#filtragem de aprovados e reprovados

base_filtrada0 = base.query('CURSO2 == @curso_selecionado2')

#NÚMERO DE ALUNOS

#filtragem de nota e freq geral
aprovadod = base_disciplina.query('INDICADOR >= 6 & FREQ >= 0.75')
reprovadod = base_disciplina.query('INDICADOR < 6 & FREQ < 0.75')
reprovado_notad = base_disciplina.query('INDICADOR < 6 & FREQ >= 0.75')
reprovado_freqd = base_disciplina.query('INDICADOR >= 6 & FREQ < 0.75')

#numero de alunos por status
alunosaprovadosd = aprovadod.NOME.unique()
nalunosaprovadosd = len(alunosaprovadosd)

alunosreprovadosd = reprovadod.NOME.unique()
nalunosreprovadosd = len(alunosreprovadosd)

alunosreprovadosnotad = reprovado_notad.NOME.unique()
nalunosreprovadosnotad = len(alunosreprovadosnotad)

alunosreprovadosfreqd = reprovado_freqd.NOME.unique()
nalunosreprovadosfreqd = len(alunosreprovadosfreqd)

reprovados_totald = nalunosreprovadosd + nalunosreprovadosnotad + nalunosreprovadosfreqd

#organização nas colunas

with cold5:
    alunosd = base_disciplina.NOME.unique()
    nalunosd = len(alunosd)
    alunos0d = base_filtrada0.NOME.unique()
    nalunos0d = len(alunos0d)
    st.metric(label="TOTAL ESEG:", value=nalunos0d)
with cole5:
    st.metric(label="TOTAL GRÁFICO: ", value=nalunosd)
with colf5:
    st.metric(label="APROVADOS: ", value=nalunosaprovadosd)
with colg5:
    st.metric(label="REPROVADOS: ", value=reprovados_totald)


linhan = pd.DataFrame({'y': [6, 6], 'x': [0.0, 1.1]})
linhaf = pd.DataFrame({'y': [0, 10], 'x': [0.75, 0.75]})

#linhas
linha_horizontal2 = alt.Chart(linhan).mark_line(color='green').encode(
    x=alt.Y('x', scale=alt.Scale(domain=(freq3, freq4), clamp=True)),
    y=alt.Y('y', scale=alt.Scale(domain=(nota3, nota4), clamp=True)))

linha_vertical2 = alt.Chart(linhaf).mark_line(color='green').encode(
    x=alt.Y('x', scale=alt.Scale(domain=(freq3, freq4), clamp=True)),
    y=alt.Y('y', scale=alt.Scale(domain=(nota3, nota4), clamp=True)))


quad = ['Superior Direito', 'Inferior Esquerdo', 'Inferior Direito', 'Superior Esquerdo']

cor = ['blue', 'red', 'yellow', 'orange']

#grafico disciplina
grafdisciplina = alt.Chart(base_disciplina).mark_circle(size=100).encode(
    alt.X('FREQ', axis=alt.Axis(format='%', title='FREQUÊNCIA', titleFontSize=15, labelFontSize=15)),
    alt.Y('INDICADOR',axis=alt.Axis(title='NOTA',titleFontSize=15, labelFontSize=15)),
    tooltip=['NOME', 'RA'],
    color=alt.Color('QUADRANTE_DISCIPLINA',
                    scale=alt.Scale(domain=quad,
                                    range=cor),
                    legend=None)).interactive().properties(width=1000, height=470)

with colc6:
    st.altair_chart(linha_horizontal2 + linha_vertical2 + grafdisciplina, use_container_width=True)


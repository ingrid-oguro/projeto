#Para importar as bibliotecas necessárias para rodar o código:
import streamlit as st
import pandas as pd
import altair as alt
import pip
pip.main(["install", "openpyxl"])

#Para fazer o tratamento da base posteriormente com o pandas: df_tratado = modulo_ajusta_base(df_bruto)

#Para importar a base de dados (obs: extrair caminho da pasta do colab com botão direito do mouse) e
#remover as linhas que têm espaço vazio (e.g., notas ainda não lançadas):
base = pd.read_excel('base_20222.xlsx')
base.dropna(inplace=True)

#Para importar a base de dados sem remover as linhas que têm espaço vazio:
base0 = pd.read_excel('20221.xlsx')

#Para definir as configurações da aba e da página:
PAGE_CONFIG = {"page_title": "ESEG - Apoio ao aluno", "page_icon": ":globe_with_meridians:", "layout": "wide"}

#Para configurar a aba e a posição da página no navegador:
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
</style>""", unsafe_allow_html=True)

cola, colb, colc = st.columns((1, 5, 0.2))

colb1,colc1 = st.columns(( 7, 0.3,)) #titulo

cola2, colb2,colc2, cold2, cole2, colf2, colg2 = st.columns((1.5, 1.5, 0.7, 2.25, 2.25, 2.25, 2.25)) #slider e metrics

cola3, colb3, colc3,  cold3 = st.columns((3, 0.2, 9, 0.2)) #grafico e botoes


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
    st.markdown('##### Média simples das notas lançadas de cada aluno nas disciplinas do período letivo de 2021-2 '
                '(desconsidera os cálculos dos planos de ensino).')
    st.markdown('##### Dados atualizados até a P2.')
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

#GRAFICO 2

colb0, colc0 = st.columns((5, 0.1))#titulo

cola4, colb4, colc4 = st.columns((0.1, 7, 0.2))#subtitulo

cola5, colb5, colc5, cold5, cole5, colf5, colg5 = st.columns((1.5, 1.5,0.7, 2.25, 2.25, 2.25, 2.25)) #slider e metrics

cola6, colb6, colc6,  cold6 = st.columns((3, 0.2, 9, 0.2)) #grafico e

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
    st.markdown('##### Dados atualizados até a P2.')
#outros botoes
with cola6:
    opcoes_cursos2 = sorted(filtro_disciplina.CURSO.unique())  # sorted = em ordem alfabetica
    curso_selecionadod2 = st.multiselect('Graduação  :', opcoes_cursos2, opcoes_cursos2)
    opcoes_semestre2 = sorted(filtro_disciplina.SEMESTRE.unique())
    semestre_selecionado2 = st.multiselect('Semestre:', opcoes_semestre2, opcoes_semestre2)
    opcao_turno = sorted(filtro_disciplina.TURNO_DA_DISCIPLINA.unique())
    turno_selecionado2 = st.multiselect('Turnos', opcao_turno, opcao_turno)

#filtragem
base_disciplina = filtro_disciplina.query('DISCIPLINA == @disciplina &\
                                       CURSO == @curso_selecionadod2 & \
                                       SEMESTRE == @semestre_selecionado2 & \
                                       INDICADOR >= @nota3 & \
                                       INDICADOR <= @nota4 & \
                                       FREQ >= @freq3 & \
                                       FREQ <= @freq4 & \
                                       TURNO_DA_DISCIPLINA == @turno_selecionado2')

#filtragem de aprovados e reprovados

base_filtrada0 = base.query('CURSO2 == @curso_selecionado')

#NÚMERO DE ALUNOS

#filtragem de nota e freq geral
aprovadod = base_disciplina.query('INDICADOR >= 6 & FREQ_GERAL >= 0.75')
reprovadod = base_disciplina.query('INDICADOR < 6 & FREQ_GERAL < 0.75')
reprovado_notad = base_disciplina.query('INDICADOR < 6 & FREQ_GERAL >= 0.75')
reprovado_freqd = base_disciplina.query('INDICADOR >= 6 & FREQ_GERAL < 0.75')

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


#linhas
linha_horizontal2 = alt.Chart(linhan).mark_line(color='green').encode(
    x=alt.Y('x', scale=alt.Scale(domain=(freq3, freq4), clamp=True)),
    y=alt.Y('y', scale=alt.Scale(domain=(nota3, nota4), clamp=True)))

linha_vertical2 = alt.Chart(linhaf).mark_line(color='green').encode(
    x=alt.Y('x', scale=alt.Scale(domain=(freq3, freq4), clamp=True)),
    y=alt.Y('y', scale=alt.Scale(domain=(nota3, nota4), clamp=True)))

#grafico disciplina
grafdisciplina = alt.Chart(base_disciplina).mark_circle(size=100).encode(
    alt.X('FREQ', axis=alt.Axis(format='%', title='FREQUÊNCIA', titleFontSize=15, labelFontSize=15)),
    alt.Y('INDICADOR',axis=alt.Axis(title='NOTA',titleFontSize=15, labelFontSize=15)),
    tooltip=['NOME', 'RA'],
    color=alt.Color('QUADRANTE_DISCIPLINA',
                    scale=alt.Scale(domain=quad,
                                    range=cor),
                    legend=None)).interactive().properties(width=1000, height=500)

with colc6:
    st.altair_chart(linha_horizontal2 + linha_vertical2 + grafdisciplina, use_container_width=True)

#COLUNA 5 -  FILTROS E TITULO DO GRAFICO INDIVIDUAL
cola56, colb56, colc5, cold5 = st.columns((1, 1, 0.2, 6))
with cola56:
    nota5, nota6 = st.slider('Nota:', 0, 10, (0, 10))
with colb56:
    freq5, freq6 = st.slider('Frequência:', 0.0, 1.0, (0.0, 1.0))

#COLUNA 6 - GRAFICO INDIVIDUAL
cola6, colb6, colc6, cold6, cole6 = st.columns((1, 1, 0.2, 7, 0.2))
cola7, colb7, colc7, cold7 = st.columns((2, 0.2, 7, 0.2))
with cola7:
    opcoes_do_botao_aluno = sorted(base.NOME.unique())  # botão aluno
    aluno_selecionado = st.multiselect('NOME DO ALUNO', opcoes_do_botao_aluno, opcoes_do_botao_aluno)
    base_aluno = base.query('NOME == @aluno_selecionado')
    opcoes_semestre3 = sorted(base_aluno.SEMESTRE.unique())
    semestre_selecionado2 = st.multiselect('Semestre', opcoes_semestre3, opcoes_semestre3)
    opcao_ra = sorted(base_aluno.RA.unique())
    ra_selecionado = st.multiselect('RA', opcao_ra)

#filtro grafico aluno
base_individual = base_aluno.query('NOME == @aluno_selecionado & \
                                    SEMESTRE == @semestre_selecionado2 & \
                                    INDICADOR >= @nota5 & \
                                    INDICADOR <= @nota6 & \
                                    FREQ >= @freq5 & \
                                    FREQ <= @freq6')

with cold5:
    alunos3 = sorted(base_individual.NOME.unique())
    prefixo3 = 'DESEMPENHO DE '
    titulo3 = prefixo3 + ' e '.join(alunos3)
    titulo3 = titulo3.upper()
    st.header(titulo3)

#linhas
linha_horizontal3 = alt.Chart(linhan).mark_line(color='orange').encode(
    x=alt.X('x', scale=alt.Scale(domain=(freq5, freq6), clamp=True)),
    y=alt.Y('y', scale=alt.Scale(domain=(nota5, nota6), clamp=True)))

linha_vertical3 = alt.Chart(linhaf).mark_line(color='red').encode(
    x=alt.X('x', scale=alt.Scale(domain=(freq5, freq6), clamp=True)),
    y=alt.Y('y', scale=alt.Scale(domain=(nota5, nota6), clamp=True)))

#grafico individual
chart2 = alt.Chart(base_individual).mark_circle(size=100).encode(
    alt.X('FREQ', axis=alt.Axis(format='%', title='Frequência')),
    alt.Y('INDICADOR', title='Nota'),
    tooltip=['NOME', 'CURSO', 'DISCIPLINA'],
    color=alt.Color('NOME',
                    legend=None)).interactive().properties(width=1000, height=600).configure_legend(
    titleFontSize=5,
    labelFontSize=17)

#subtitulo
with cold5:
    cursos0 = sorted(base_individual.CURSO.unique())
    cursos1 = "EM " + ' e '.join(cursos0)
    cursos1 = cursos1.upper()
    st.header(cursos1)
    st.subheader('Média simples das avaliações lançadas de todas as disciplinas por aluno.')
with colc7:
    st.altair_chart(chart2, use_container_width=True)

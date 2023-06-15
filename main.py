import pickle
import pandas as pd
import streamlit as st

from datetime import date
import datetime


css = '''
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://images.pexels.com/photos/16830242/pexels-photo-16830242.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1");
    background-size: cover
    
}

[data-testid="stHeader"] {
    opacity: 0;
}

[data-testid="stVerticalBlock"] {
    background-color: rgb(0,0,0);
    border-radius: 6px;
    opacity: 0.9;
    
}

img {
    margin-top: 50px;
    height: 50px;
    width: 50px;
}

h1 {
    font-size: 30px;
    text-align: center;
}
</style>

'''

st.set_page_config(
    page_title="PINHO",
    page_icon="img/pinho_icon.ico"
    )

st.markdown(css, unsafe_allow_html=True)


#----------------Modelo-------------------------
#Import Models
with open("models/model1.pkl", "rb") as file1:
    model1 = pickle.load(file1)
    
    
#Import Vectors
with open("models/vector1.pkl", "rb") as vec1:
    vector1 = pickle.load(vec1)


#---------------Preditor-------------------------
def area_padrao(i):
    lista = [39, 49, 69, 79, 89, 109, 139, 179]
    if i <= lista[0]:
        j = 1
    elif i <= lista[1]:
        j = 2
    elif i <= lista[2]:
        j = 3
    elif i <= lista[3]:
        j = 4
    elif i <= lista[4]:
        j = 5
    elif i <= lista[5]:
        j = 6
    elif i <= lista[6]:
        j = 7
    elif i <= lista[7]:
        j = 8
    else:
        j = 9
    return j

#--------------------------------------------------------------

bairros = pd.read_json(f'metadata/bairros_curitiba_semestral.json')
area_util = pd.read_json(f'metadata/area_curitiba_semestral.json')
quartos = pd.read_json(f'metadata/quartos_curitiba_semestral.json')
banheiros = pd.read_json(f'metadata/banheiros_curitiba_semestral.json')
suites = pd.read_json(f'metadata/suites_curitiba_semestral.json')
vagas = pd.read_json(f'metadata/vagas_curitiba_semestral.json')
data = datetime.datetime.strptime(str(date.today()), "%Y-%m-%d")
esse_ano = data.year



col1, col2, col3 = st.columns([1,3,1])

col2.title("Descubra quanto vale aproximadamente seu Apartamento em Curitiba")

col2.write("Preencha os campos abaixo:")

bairro = col2.selectbox(label="Selecione o bairro", options=bairros.sort_values(by='bairros'))

st.write("\n\n")
area = int(col2.slider(label="Selecione o tamanho da área útil", min_value=round(int(area_util.values[0][0]), -1),
                 max_value=int(230), step=2))
st.write("\n\n")
quarto = col2.selectbox(label="Selecione a quantidade de quartos", options=quartos.sort_values(by='n_quartos'))
st.write("\n\n")
banheiro = col2.selectbox(label="Selecione a quantidade de banheiros - Incluíndo o(s) da(s) suíte(s)", options=banheiros.sort_values(by='n_banheiros'))
st.write("\n\n")
suite = col2.selectbox(label="Selecione a quantidade de suítes", options=suites.sort_values(by='n_suites'))
st.write("\n\n")

vaga = col2.selectbox(label="Selecione a quantidade de vagas de garagem", options=vagas.sort_values(by='n_vagas'))
st.write("\n\n")

ano_construcao = col2.selectbox(label='Selecione o ano de construção do imóvel', options=range(esse_ano, 1959, -1))

if col2.button(label='Calcular'):
    padrao = area_padrao(area)

    decada = round(int(ano_construcao), -1)

    imovel = f'bairro{bairro} padrao{padrao} quarto{quartos} suite{suite} banheiro{banheiro} vaga{vaga} decada{decada}'

    caracteristicas = pd.DataFrame({'caracteristicas': [imovel]})

    serie = caracteristicas['caracteristicas']

    vector = vector1.transform(serie)
    m2 = model1.predict(vector)
    
    preco = round(int(m2[0]) * area, -3)

    preco = f'R$ {preco:_.2f}'
    preco = preco.replace('.',',').replace('_','.')

    col2.write("\n\n\n\n\n")
    col2.title(f"{preco}\n\n\n Este valor é uma opinião de preço baseado na média de valores dos imóveis por bairro e características, podendo variar de acordo com as condições do imóvel, localização, mobília, etc. Para uma avaliação mais precisa de seu imóvel procure um corretor avaliador credenciado ao CRECI de sua confiança.")

    col2.write("Siga-nos no instagram para ficar por dentro de novas atualizações e conte-nos sua experiência ")

    col2.markdown("[![Foo](https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Instagram_icon.png/240px-Instagram_icon.png)](https://instagram.com/pinhocwb?igshid=MzNlNGNkZWQ4Mg==)")
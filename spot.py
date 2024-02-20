from dotenv import load_dotenv
import requests
import os
import base64
import json

load_dotenv()

cliente_id = os.environ["CLIENT_ID"]
secret_cliente = os.environ["SECRET_CLIENT"]

#pegar o token com ID e chave secreta
def get_token():
    auth_string = cliente_id + ":" + secret_cliente
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url= 'https://accounts.spotify.com/api/token'
    headers ={
        'Authorization': 'Basic ' + auth_base64,
        'Content-Type': "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = requests.post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

#função para autenticar o token para futuras requisições 
def get_auth_hearder(token):
    return {"Authorization": "Bearer "+ token}

#buscar por artistas com a url e dados passado por parametro
def search_for_artist(token, nome_artista):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_hearder(token)
    busca = f"?q={nome_artista}&type=artist&limit=1"
       
    busca_url = url + busca
    result = requests.get(busca_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("Não há artista com esse nome")
        return None
    
    return json_result[0]

#buscar por musicas famosas do artista com a url e dados passado por parametro
def get_songsnome_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_hearder(token)
    result = requests.get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result
    
token = get_token()
print(token)
pesquisa = input("Digite o nome da banda: ")
result = search_for_artist(token, pesquisa)
artist_id = result["id"]
musicas = get_songsnome_by_artist(token, artist_id)
#print(musicas[0]['artists'][0]['external_urls']['spotify'])


#lista todas as top musicas 
print("Nome das top musicas mais ouvidas no spotify")
for i, musica in enumerate(musicas):
    print(i + 1, musica['name'])


print("Links das Musicas mais ouvidas no spotify")    
#lista de todos os links para musicas
for i, links in enumerate(musicas):
    print(i + 1, links['artists'][0]['external_urls']['spotify'])
    
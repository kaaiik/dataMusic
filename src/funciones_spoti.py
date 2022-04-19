import requests
import datetime
from urllib.parse import urlencode
import pandas as pd
import time
import base64

#------------------------------------------------------------------------------------------------------

class SpotifyAPI(object):
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    client_id = None
    client_secret = None
    token_url = "https://accounts.spotify.com/api/token"
    
    def __init__(self, client_id, client_secret, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret

    def get_client_credentials(self):
        """
        Returns a base64 encoded string
        """
        client_id = self.client_id
        client_secret = self.client_secret
        if client_secret == None or client_id == None:
            raise Exception("You must set client_id and client_secret")
        client_creds = f"{client_id}:{client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return client_creds_b64.decode()
    
    def get_token_headers(self):
        client_creds_b64 = self.get_client_credentials()
        return {
            "Authorization": f"Basic {client_creds_b64}"
        }
    
    def get_token_data(self):
        return {
            "grant_type": "client_credentials"
        } 
    
    def perform_auth(self):
        token_url = self.token_url
        token_data = self.get_token_data()
        token_headers = self.get_token_headers()
        r = requests.post(token_url, data=token_data, headers=token_headers)
        if r.status_code not in range(200, 299):
            raise Exception("Could not authenticate client.")
            # return False
        data = r.json()
        now = datetime.datetime.now()
        access_token = data['access_token']
        expires_in = data['expires_in'] # seconds
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token = access_token
        self.access_token_expires = expires
        self.access_token_did_expire = expires < now
        return True
    
    def get_access_token(self):
        token = self.access_token
        expires = self.access_token_expires
        now = datetime.datetime.now()
        if expires < now:
            self.perform_auth()
            return self.get_access_token()
        elif token == None:
            self.perform_auth()
            return self.get_access_token() 
        return token
    
    def get_resource_header(self):
        access_token = self.get_access_token()
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        return headers
        
    def get_resource(self, lookup_id, resource_type='playlists', version='v1'):
        endpoint = f"https://api.spotify.com/{version}/{resource_type}/{lookup_id}"
        headers = self.get_resource_header()
        r = requests.get(endpoint, headers=headers)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()
    
    def get_playlist_tracks(self, query, version='v1', resource_type='playlists', item='tracks'):
        headers = self.get_resource_header()
        endpoint = f'https://api.spotify.com/{version}/{resource_type}/{query}/{item}'
        r = requests.get(endpoint, headers=headers)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()
    
    def search_by_name(self, query, search_type='playlist'): # type
        headers = self.get_resource_header()
        endpoint = "https://api.spotify.com/v1/search"
        data = urlencode({"q": query, "type": search_type.lower()})
        lookup_url = f"{endpoint}?{data}"
        r = requests.get(lookup_url, headers=headers)
        if r.status_code not in range(200, 299):  
            return {}
        return r.json()
        
#------------------------------------------------------------------------------------------------------------

def get_creator(dic):
    return dic['display_name']
    
#------------------------------------------------------------------------------------------------------------

def get_spoti_playlist(df):
    df.owner = list(map(get_creator, list(df.owner)))
    df = df[df['owner'] == 'Spotify']
    sxt_plst = df.loc[:0]
    return sxt_plst
    
#------------------------------------------------------------------------------------------------------------

def get_df(pl_id):
    data = []

    sxt_tracks = spotify.get_playlist_tracks(pl_id)

    for i in range(len(sxt_tracks['items'])):
        art_lst = []
        sng_lst = []
        alb_lst = []
        dt_lst = []

        artista = sxt_tracks['items'][i]['track']['artists'][0]['name']
        art_lst.append(artista)

        cancion = sxt_tracks['items'][i]['track']['name']
        sng_lst.append(cancion)

        album = sxt_tracks['items'][i]['track']['album']['name']
        alb_lst.append(album)

        lanzamiento = sxt_tracks['items'][i]['track']['album']['release_date']
        dt_lst.append(lanzamiento)

        fila = []
        fila += art_lst + sng_lst + alb_lst + dt_lst

        data.append(fila)

    cols = ['Artista', 'Titulo', 'Album', 'Fecha']

    df = pd.DataFrame(data, columns=cols)
    return df
    
#----------------------------------------------------------------------------------------------------------

file = open(f'../sptoken.txt')
client_secret = file.readlines()[0].strip('\n')

headers = {
    'Authorization': f'Bearer {client_secret}'
}

client_id = 'd48abffc774f4dd7af256702396c6ac3'
spotify = SpotifyAPI(client_id, client_secret)




def get_every_track(nombre):
    
    sixtys = spotify.search_by_name(nombre, search_type="playlist")
    lst_plst = sixtys['playlists']['items']

    df = pd.DataFrame(lst_plst)

    sxt_plst = get_spoti_playlist(df)

    pl_id = str(sxt_plst['id']).split('    ')[-1].split('\n')[0]

    df_sxt = get_df(pl_id)
    return df_sxt
        
        
    def get_resource(self, lookup_id, resource_type='playlists', version='v1'):
        endpoint = f"https://api.spotify.com/{version}/{resource_type}/{lookup_id}"
        headers = self.get_resource_header()
        r = requests.get(endpoint, headers=headers)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()
    
    def get_playlist_tracks(self, query, version='v1', resource_type='playlists', item='tracks'):
        headers = self.get_resource_header()
        endpoint = f'https://api.spotify.com/{version}/{resource_type}/{query}/{item}'
        r = requests.get(endpoint, headers=headers)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()
    
    def search_by_name(self, query, search_type='playlist'): # type
        headers = self.get_resource_header()
        endpoint = "https://api.spotify.com/v1/search"
        data = urlencode({"q": query, "type": search_type.lower()})
        lookup_url = f"{endpoint}?{data}"
        r = requests.get(lookup_url, headers=headers)
        if r.status_code not in range(200, 299):  
            return {}
        return r.json()

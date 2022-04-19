# Proyecto ETL
El objetivo de este proyecto es intentar extraer algún tipo de relación entre la música más escuchada y las drogas consumidas por la población en distintas épocas del siglo XX y XXI.

El principal inconveniente que he encontrado es la localización de una base de datos consistente para la extracción de datos sobre el consumo de alcohol y drogas, especialmente desde los años 60 hasta los 90.

## Extracción de datos de la Spotify API
Para la extracción de datos de esta API, es necesario crearse una app en el dashboard de SpotiFy, aunque no se vaya a desarrollar una. Una vez creada la app la api te da un cliente_id y un secret_id que serán esenciales para la obtención del token y el acceso a los datos de Spotify.

Una vez acabado este proceso, en el archivo de 'funciones_spoti.py', se implementa el objeto 'spotify_API' que automatiza este proceso de acceso, además de la obtención de los datos y acceso a las playlist mediante los endpoints.

Los resultados de búsqueda son las playlist hechas por spotify que recopilan las canciones más destacada de cada una de las décadas.

## Extracción de datos de Billboard Music
En este caso, se va a scrappear desde wikipedia los charts de billboard para cada año desde 1962. El hecho de que los charts de cada año tengan una misma estructura facilita la extracción de estos, pues se puede llegar a automatizar o simplemente obtenerlos cambiando en el enlace de acceso a la página.

## Extracción de datos desde Kaggle sobre el consumo de alcohol y droga en Alemania
Se ha descargado una base de datos sobre el consumo de estas sustancias en años sueltos desde los años 60, que nos permiten hacernos una idea del consumo habitual en personas de entre 15 y 25 años.


## Librerías utilizadas

-Pandas
-Requests
-Time
-Base64
-Urlencode
-Datetime
-BeautifulSoup

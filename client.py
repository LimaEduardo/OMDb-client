import requests
import json

def getName():
    name = input("Digite o nome do conteúdo que deseja buscar: ")
    if name != "":
        return name
    return None

def getType():
    content_type = int(input("Por qual conteúdo você deseja buscar (Default = 1) ? \n 1 - Filmes \n 2 - Series \n 3 - Episodio \n ") or 1)
    if content_type == 1:
        return "movie"
    elif content_type == 2:
        return "series"
    elif content_type == 3:
        return "episode"
    else:
        return "movie"

def getYear():
    year = input("Digite o ano de lançamento do conteúdo que você desaja buscar: ")
    if year != "":
        return year
    return None

def getPages():
    content_type = str(input("Você deseja pegar todas as páginas [S/n] (Default = 'n') ") or 'n')
    if content_type == "S" or content_type == "s":
        return True
    else: 
        return False

def printMovie(movie):
    print("**************", end="\n\n")
    print(movie['Title'])
    print(movie['Year'], end="\n\n")
    print("**************")


if __name__ == "__main__":
    API_KEY = "5b5be94f"
    OMDB_URL = "http://www.omdbapi.com/"

    query = {}
    query['apikey'] = API_KEY
    
    search_by_string = getName()
    if search_by_string:
        query['s'] = search_by_string

    search_by_type = getType()
    if search_by_type:
        query['type'] = search_by_type
    
    search_by_release_year = getYear()
    if search_by_release_year:
        query['y'] = search_by_release_year

    get_all_pages = getPages()

    request = requests.get(OMDB_URL, params=query)
    response = request.content.decode('utf-8')
    response_dict = json.loads(response)

    filtered_movies = []
    filtered_movies_sorted = []
    if response_dict['Response'] == "True":
        if get_all_pages:
            total_results = int(response_dict['totalResults'])
            if total_results % 10 > 0:
                number_of_pages = int(total_results/10) + 1
            else:
                number_of_pages = int(total_results/10)
            
            print("Numero total de paginas: " + str(number_of_pages))
            for page in range(1, number_of_pages + 1):
                query['page'] = page
                request = requests.get(OMDB_URL, params=query)
                response = request.content
                response_dict = json.loads(response)
                results = response_dict['Search']
                for movie in results:
                    filtered_movies.append({'Title': movie['Title'], 'Year': movie['Year']})
            filtered_movies_sorted = sorted(filtered_movies, key=lambda k: k['Year'])
            
        else:
            results = response_dict['Search']
            for movie in results:
                filtered_movies.append({'Title': movie['Title'], 'Year': movie['Year']})
            filtered_movies_sorted = sorted(filtered_movies, key=lambda k: k['Year']) 

        for movie in filtered_movies_sorted:
            printMovie(movie)
            
    else:
        print("Não foi possível encontrar resultados")
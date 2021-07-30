from requests_html import HTMLSession

class Scraper():

    url = 'https://www.colombia.com/cine/{}'
    session = HTMLSession()

    def HelperGetMovies(self, movies: list, premier = True):
        result = []
        for index, movie in enumerate(movies):
            items = {
                'id'    : movie.find('a', first=True).attrs['href'][6:],
                'title' : movie.find('.title-pelicula', first=True).text
            }

            if index == 0 and premier == True:
                items['cover'] = movie.find('.imagen picture img', first=True).attrs['src']
            else :
                items['cover'] = movie.find('.imagen picture img', first=True).attrs['data-src']

            result.append(items)

        return result

    def getMovies(self):
        r = self.session.get(self.url.format('cartelera'))
        
        movies_urls = []
        premieres = r.html.find('.pelicula-estreno')
        
        others = r.html.find('.pelicula')
        movies_urls.extend(self.HelperGetMovies(premieres))
        movies_urls.extend(self.HelperGetMovies(others, False))
        
        return movies_urls

    def getMovie(self, id:str):
        r = self.session.get(self.url.format(id))
        movie = r.html.find('.pelicula', first=True)

        item = {
            'genre'    : movie.find('div .row div')[3].text[8:],
            'duration': movie.find('div .row div')[4].text[10:].replace('.', ''),
            'clasification': movie.find('div .row div')[5].text[15:],
            'director': movie.find('div .row div')[6].text[10:],
            'actores'  : movie.find('.actores', first=True).text[9:],
            'synopsis' : movie.find('.sinopsis', first=True).text,
            'trailer'  : r.html.find('iframe', first=True).attrs['data-src'][30:]
        }

        return item
        
    def getMovieSchedule(self, city:str, id:str):
        r = self.session.get(self.url.format(f'{city}/{id}'))

        cinemas = []
        boxes = r.html.find('.caja-programacion .caja-cinema')

        for box in boxes:
            cinema = {
                'cinema': box.find('.nombre-cinema', first=True).text,
                'location': box.find('.datos-cinema', first=True).text.split('|')[0].strip(),
                'phone': box.find('.datos-cinema', first=True).text.split('|')[1].strip(),
                'format': box.find('.formato-pelicula', first=True).text,
                'schedules': [],
            }

            hours = box.find('.horarios-funcion li');
            for hour in hours:
                cinema['schedules'].append(hour.text)
            
            cinemas.append(cinema)

        return cinemas
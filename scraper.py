from requests_html import HTMLSession

class Scraper():

    url = 'https://www.colombia.com/cine/{}'

    def HelperGetMovies(self, movies: list):
        result = []
        for movie in movies:
            items = {
                'title': movie.find('.title-pelicula', first=True).text,
                'genre': movie.find('li')[0].text[8:],
                'duration': movie.find('li')[1].text[10:].replace('.', ''),
                'clasification': movie.find('li')[2].text[15:],
                'director': movie.find('.director span', first=True).text,
                'urlname': movie.find('a', first=True).attrs['href'][6:]
            }
            result.append(items)

        return result

    def GetMovies(self, s):
        r = s.get(self.url.format('cartelera'))
        
        movies_urls = []
        premieres = r.html.find('.pelicula-estreno')
        others = r.html.find('.pelicula')

        movies_urls.extend(self.HelperGetMovies(premieres))
        movies_urls.extend(self.HelperGetMovies(others))
        
        return movies_urls

    def GetMoviesInfo(self, s):
        urls = self.GetMovies(s)

        for index, url in enumerate(urls):
            r = s.get(self.url.format(url['urlname']))
            movie = r.html.find('.pelicula', first=True)
            urls[index]['actores'] = movie.find('.actores', first=True).text[9:]
            urls[index]['synopsis'] = movie.find('.sinopsis', first=True).text
            urls[index]['trailer'] = r.html.find('iframe', first=True).attrs['data-src'][30:]

        return urls
        
    def GetMoviesSchedule(self):
        s = HTMLSession()
        movies = self.GetMoviesInfo(s)

        for index, movie in enumerate(movies):
            cinemas = []
            url = movie['urlname']
            r = s.get(self.url.format(f'villavicencio/{url}_19'))

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
            
            movies[index]['cinemas'] = cinemas

        return movies
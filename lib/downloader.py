import sys
try:
    import requests
    import bs4
except ImportError:
    sys.exit('- модуль не установлен!')


class tiktok_downloader:
    def __init__(self):
        pass

    def musicaldown(self, url, output_name):
        try:
            # Создаю объект "Session" из библиотеки "requests" для выполнения запросов к серверу.
            ses = requests.Session()
            server_url = 'https://musicaldown.com/'
            # Устанавливаются заголовки запроса, включая "User-Agent", "Accept-Language" и тд.
            headers = {
                "Host": "musicaldown.com",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "DNT": "1",
                "Upgrade-Insecure-Requests": "1",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "TE": "trailers"
            }
            ses.headers.update(headers)
            # Отправляю GET-запрос к серверу 'https://musicaldown.com/' и получаю ответ в виде HTML-страницы.
            req = ses.get(server_url)
            # При помощи 'BeautifulSoup' ищу всё теги 'input' на странице и сохраняю их значения в словарь 'data'
            data = {}
            parse = bs4.BeautifulSoup(req.text, 'html.parser')
            for input_tag in parse.findAll('input'):
                data[input_tag.get("name")] = url if input_tag.get("id") == "link_url" else input_tag.get("value")
            # Отправляю POST-запрос на сервер для загрузки видео, используя словарь "data".
            post_url = server_url + "id/download"
            req_post = ses.post(post_url, data=data, allow_redirects=True)
            # Проверяю возможные ошибки
            mistakes = [302, 'This video is currently not available', 'Video is private or removed!']
            if req_post.status_code == mistakes[0] or (mistakes[1] in req_post.text) or (mistakes[2] in req_post.text):
                print('- видео приватное или удалено')
                return 'private/remove'
            elif 'Submitted Url is Invalid, Try Again' in req_post.text:
                print('- URL-адрес недействителен')
                return 'url-invalid'
            get_all_blank = bs4.BeautifulSoup(req_post.text, 'html.parser').findAll(
                'a', attrs={'target': '_blank'})
            # Если загрузка прошла успешно, то получаю ссылку на скачивание видео и происходит сохранение файла
            # на локальный компьютер с именем "output_name".
            download_link = get_all_blank[0].get('href')
            get_content = requests.get(download_link)

            with open(output_name, 'wb') as fd:
                fd.write(get_content.content)
            return True
        except IndexError:
            return False

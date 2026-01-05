class GenreService:
    def __init__(self, context=None, genre_repo=None):
        self.context = context
        self.genreRepo = genre_repo

    def get_all_genre(self):
        result = self.genreRepo.get_all_genre()
        genre = {}
        for i, value in enumerate(result, start=1):
            genre[str(i)] = value["genre"]
        return genre

    def get_genre_count(self, genre):
        result = self.genreRepo.get_genre_count(genre)
        return result[0]

    def get_game_by_genre(self, genre, page, page_size=2):
        offset = page * page_size
        result = self.genreRepo.find_paginated(genre, page_size, offset)
        return result

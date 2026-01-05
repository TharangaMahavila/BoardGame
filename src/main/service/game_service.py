class GameService:
    def __init__(self, context=None, game_repo=None):
        self.context = context
        self.gameRepo = game_repo

    def get_all_genre(self):
        result = self.gameRepo.get_all_genre()
        genre = {}
        for i, value in enumerate(result, start=1):
            genre[str(i)] = value["genre"]
        return genre

    def get_genre_count(self, genre):
        result = self.gameRepo.get_genre_count(genre)
        return result[0]

    def get_game_by_genre(self, genre, page, page_size=2):
        offset = page * page_size
        result = self.gameRepo.find_paginated(genre, page_size, offset)
        return result
    
    def get_game_by_id(self, id):
        return self.gameRepo.find_by_id(id)

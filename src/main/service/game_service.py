class GameService:
    def __init__(self, context=None, game_repo=None):
        self.context = context
        self.gameRepo = game_repo

    def get_all_genre(self):
        # Fetch all unique genres from the database
        result = self.gameRepo.get_all_genre()
        genre = {}
        for i, value in enumerate(result, start=1):
            genre[str(i)] = value["genre"]
        # Return the formatted genre list
        return genre

    def get_genre_count(self, genre):
        # Get the number of games that belong to the given genre
        result = self.gameRepo.get_genre_count(genre)
        return result[0]

    def get_designer_count(self, name):
        # Get the number of games designed by a specific designer (or matching name)
        result = self.gameRepo.get_designer_count(name)
        return result[0]

    def get_title_count(self, name):
        # Get the number of games that match the given title keyword
        result = self.gameRepo.get_title_count(name)
        return result[0]

    def get_game_by_genre(self, genre, page, page_size=2):
        # Calculate how many records should be skipped for pagination
        offset = page * page_size
        # Retrieve a paginated list of games for the selected genre
        result = self.gameRepo.find_paginated_by_genre(genre, page_size, offset)
        return result

    def get_game_by_designer(self, name, page, page_size=2):
        # Calculate how many records should be skipped for pagination
        offset = page * page_size
        # Retrieve a paginated list of games that match the designer name
        result = self.gameRepo.find_paginated_by_designer(name, page_size, offset)
        return result

    def get_game_by_title(self, name, page, page_size=2):
        # Calculate how many records should be skipped for pagination
        offset = page * page_size
        # Retrieve a paginated list of games that match the title keyword
        result = self.gameRepo.find_paginated_by_title(name, page_size, offset)
        return result

    def get_game_by_id(self, id):
        # Fetch a single game from the database using its unique game ID
        return self.gameRepo.find_by_id(id)

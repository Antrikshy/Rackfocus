from abc import ABC, abstractmethod

class DatasetModel(ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def sqlite_schema(self):
        pass

    def get_download_url(self):
        return 'https://datasets.imdbws.com/' + self.get_file_name()

    def get_file_name(self):
        return self.name + '.tsv.gz'

    def get_database_table_name(self):
        return self.name.replace('.', '_')

    def get_database_table_schema(self):
        return self.sqlite_schema

    @abstractmethod
    def convert_line_to_tuples(self, line):
        """`line` is expected to be a single line from a dataset file of the
        corresponding type. Output is a list of one or more tuples ready to
        be inserted into a table using sqlite3."""
        pass

    def _sanitize_and_convert_value(self, value, converter):
        """`value` is expected to be a single, unsanitized string value 
        (cell) from an IMDb dataset. `converter` should be a function
        to process the string into the desired type, such as int or float.
        This function may return None."""
        clean_value = value.strip()
        try:
            return None if clean_value in [r'\N', r'\\N'] else converter(clean_value)
        except Exception as e:
            print(e)
            print(clean_value)

class NameBasics(DatasetModel):
    name = 'name.basics'
    sqlite_schema = (
        'nconst text,' # alphanumeric unique identifier of the name/person
        'primaryName text,' # name by which the person is most often credited
        'birthYear integer,' # in YYYY format
        'deathYear integer,' # in YYYY format if applicable, else ‘\N’
        'primaryProfession text,' # the top-3 professions of the person
        'knownForTitles text' # titles the person is known for
    )

    def convert_line_to_tuples(self, line):
        values = line.split('\t')
        nconst = self._sanitize_and_convert_value(values[0], str)
        primaryName = self._sanitize_and_convert_value(values[1], str)
        birthYear = self._sanitize_and_convert_value(values[2], int)
        deathYear = self._sanitize_and_convert_value(values[3], int)
        primaryProfession = self._sanitize_and_convert_value(values[4], str)
        knownForTitles = self._sanitize_and_convert_value(values[5], str)
        return [(nconst, primaryName, birthYear, deathYear, primaryProfession, knownForTitles)]

class TitleAkas(DatasetModel):
    name = 'title.akas'
    sqlite_schema = (
        'titleId text,' # a tconst, an alphanumeric unique identifier of the title
        'ordering integer,' # a number to uniquely identify rows for a given titleId
        'title text,' # the localized title
        'region text,' # the region for this version of the title
        'language text,' # the language of the title
        'types text,' # Enumerated set of attributes for this alternative title. One or more of the following: "alternative", "dvd", "festival", "tv", "video", "working", "original", "imdbDisplay". New values may be added in the future without warning
        'attributes text,' # Additional terms to describe this alternative title, not enumerated
        'isOriginalTitle integer' # 0: not original title; 1: original title
    )

    def convert_line_to_tuples(self, line):
        values = line.split('\t')
        titleId = self._sanitize_and_convert_value(values[0], str)
        ordering = self._sanitize_and_convert_value(values[1], int)
        title = self._sanitize_and_convert_value(values[2], str)
        region = self._sanitize_and_convert_value(values[3], str)
        language = self._sanitize_and_convert_value(values[4], str)
        types = self._sanitize_and_convert_value(values[5], str)
        attributes = self._sanitize_and_convert_value(values[6], str)
        isOriginalTitle = self._sanitize_and_convert_value(values[7], int)
        return [(titleId, ordering, title, region, language, types, attributes, isOriginalTitle)]

class TitleBasics(DatasetModel):
    name = 'title.basics'
    sqlite_schema = (
        'tconst text,' # alphanumeric unique identifier of the title
        'titleType text,' # the type/format of the title (e.g. movie, short, tvseries, tvepisode, video, etc)
        'primaryTitle text,' # the more popular title / the title used by the filmmakers on promotional materials at the point of release
        'originalTitle text,' # original title, in the original language
        'isAdult integer,' # 0: non-adult title; 1: adult title
        'startYear integer,' # represents the release year of a title. In the case of TV Series, it is the series start year
        'endYear integer,' # TV Series end year. ‘\N’ for all other title types
        'runtimeMinutes integer,' # primary runtime of the title, in minutes
        'genres text' # includes up to three genres associated with the title
    )

    def convert_line_to_tuples(self, line):
        values = line.split('\t')
        tconst = self._sanitize_and_convert_value(values[0], str)
        titleType = self._sanitize_and_convert_value(values[1], str)
        primaryTitle = self._sanitize_and_convert_value(values[2], str)
        originalTitle = self._sanitize_and_convert_value(values[3], str)
        isAdult = self._sanitize_and_convert_value(values[4], int)
        startYear = self._sanitize_and_convert_value(values[5], int)
        endYear = self._sanitize_and_convert_value(values[6], int)
        runtimeMinutes = self._sanitize_and_convert_value(values[7], int)
        genres = self._sanitize_and_convert_value(values[8], str)
        return [(tconst, titleType, primaryTitle, originalTitle, isAdult, startYear, endYear, runtimeMinutes, genres)]

class TitleCrew(DatasetModel):
    # NOTE: The schema for this was significantly modified from that of the
    # dataset. The schema used by IMDb works well in TSV format, but does not
    # translate well to a relational table.

    name = 'title.crew'
    sqlite_schema = (
        'tconst text,' # alphanumeric unique identifier of the title
        'nconst text,' # alphanumeric unique identifier of the name/person
        'job text' # "director" or "writer"
    )

    def convert_line_to_tuples(self, line):
        values = line.split('\t')
        tconst = self._sanitize_and_convert_value(values[0], str)
        directors_raw = self._sanitize_and_convert_value(values[1], str)
        writers_raw = self._sanitize_and_convert_value(values[2], str)
        out = []
        if directors_raw is not None:
            directors = directors_raw.split(',')
            for director in directors:
                out.append((tconst, director, 'director'))
        if writers_raw is not None:
            writers = writers_raw.split(',')
            for writer in writers:
                out.append((tconst, writer, 'writer'))
        return out

class TitleEpisode(DatasetModel):
    name = 'title.episode'
    sqlite_schema = (
        'tconst text,' # alphanumeric identifier of episode
        'parentTconst text,' # alphanumeric identifier of the parent TV Series
        'seasonNumber integer,' # season number the episode belongs to
        'episodeNumber integer' # episode number of the tconst in the TV series
    )

    def convert_line_to_tuples(self, line):
        values = line.split('\t')
        tconst = self._sanitize_and_convert_value(values[0], str)
        parentTconst = self._sanitize_and_convert_value(values[1], str)
        seasonNumber = self._sanitize_and_convert_value(values[2], int)
        episodeNumber = self._sanitize_and_convert_value(values[3], int)
        return[(tconst, parentTconst, seasonNumber, episodeNumber)]

class TitlePrincipals(DatasetModel):
    name = 'title.principals'
    sqlite_schema = (
        'tconst text,' # alphanumeric unique identifier of the title
        'ordering integer,' # a number to uniquely identify rows for a given titleId
        'nconst text,' # alphanumeric unique identifier of the name/person
        'category text,' # the category of job that person was in
        'job text,' # the specific job title if applicable, else '\N'
        'characters text' # the name of the character played if applicable, else '\N'
    )

    def convert_line_to_tuples(self, line):
        values = line.split('\t')
        tconst = self._sanitize_and_convert_value(values[0], str)
        ordering = self._sanitize_and_convert_value(values[1], int)
        nconst = self._sanitize_and_convert_value(values[2], str)
        category = self._sanitize_and_convert_value(values[3], str)
        job = self._sanitize_and_convert_value(values[4], str)
        characters = self._sanitize_and_convert_value(values[5], str)
        return [(tconst, ordering, nconst, category, job, characters)]

class TitleRatings(DatasetModel):
    name = 'title.ratings'
    sqlite_schema = (
        'tconst text,' # alphanumeric unique identifier of the title
        'averageRating real,' # weighted average of all the individual user ratings
        'numVotes integer' # number of votes the title has received
    )

    def convert_line_to_tuples(self, line):
        values = line.split('\t')
        tconst = self._sanitize_and_convert_value(values[0], str)
        averageRating = self._sanitize_and_convert_value(values[1], float)
        numVotes = self._sanitize_and_convert_value(values[2], int)
        return [(tconst, averageRating, numVotes)]

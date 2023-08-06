import requests
import time

from .apiurls import (
    SCHEDULE,
    SHOW,
    SEASON,
    EPISODE,
    SHOWS,
    UPDATES,
    PEOPLE_SEARCH,
    SINGLE_SEARCH,
    SHOW_SEARCH,
    SHOW_LOOKUP
)
from .tvmaze_utility import make_request, ApiError, get_list


def get_updates():
    return make_request(UPDATES)


class Schedule:
    """Schedule class for tvmaze schedule endpoint
    """

    def __init__(self, date=None, country_code='US'):
        """init method for Schedule

        :param date: Optional ISO 8601 formatted date defaults to current day. Example 2017-8-14
        :param country_code: Optional ISO 3166-1 two digit country code defaults to US.
        """
        self.date = date or time.strftime('%Y-%m-%d')
        self.country_code = country_code
        self.url = '{}?country={}&date={}'.format(SCHEDULE, self.country_code, self.date)
        self.episode_list = []

    @property
    def episodes(self):
        """Return list of episodes"""
        try:
            episode_list = get_list(self, 'episode_list', self.url, Episode)
        except ApiError as e:
            raise e
        else:
            return sorted(
                episode_list,
                key=lambda episode: int(episode.show.weight),
                reverse=True
            )

    def exclude_networks(self, networks=None):
        """Exclude certain networks from the schedule

        :param list networks: List of networks to exclude from schedule
        :return: List of episode objects from schedule without networks included
        """
        if not networks:
            raise ValueError("must include at least one network to exclude")
        return [episode for episode in self.episodes if episode.show.network["name"] not in networks]

    def include_networks(self, networks=None):
        """Returns list of episodes from networks included"""
        if not networks:
            raise ValueError("must include at least one network to include")
        return [episode for episode in self.episodes if episode.show.network["name"] in networks]


class Shows:
    def __init__(self, page=0):
        if page < 0:
            page = 0
        url = self.get_url(page)
        self.shows = [Show(**show) for show in make_request(url)]
        self.page = page

    def get_url(self, page=0):
        return SHOWS if not page else '{}?page={}'.format(SHOWS, page)

    def change_page(self, change):
        if self.page == change:
            return self.shows
        new_page = self.page + change
        try:
            self.shows = [Show(**show) for show in make_request(self.get_url(new_page))]
            self.page = new_page
        except ApiError as e:
            raise e
        else:
            return self.shows

    def next_page(self):
        self.change_page(1)
        if not self.shows:
            raise ValueError('No more shows')

    def previous_page(self):
        self.change_page(-1)


class Show:
    """Show class for tvmaze api"""

    def __init__(self, show_id=None, embed_url=None, **kwargs):
        self.cast_list = []
        self.crew_list = []
        self.season_list = []
        self.episode_list = []
        self.special_list = []
        self.next = None

        if show_id:
            self.show_id = show_id

            self.api_url = '{}{}{}'.format(SHOW, show_id, embed_url if embed_url else '')
            try:
                show = make_request(self.api_url)
            except ApiError as e:
                raise e
            else:
                self.schedule = show["schedule"]
                self.updated = show["updated"]
                self.status = show["status"]
                self.webChannel = show["webChannel"]
                self.premiered = show["premiered"]
                self.externals = show["externals"]
                self.summary = show["summary"]
                self.image = show["image"]
                self.type = show["type"]
                self.genres = show["genres"]
                self.runtime = show["runtime"]
                self._links = show["_links"]
                self.rating = show["rating"]
                self.officialSite = show["officialSite"]
                self.weight = show["weight"]
                self.language = show["language"]
                self.id = show["id"]
                self.url = show["url"]
                self.network = show["network"]
                self.name = show["name"]

                #: optional _embedded for embed_url values
                if embed_url:
                    self._embedded = show["_embedded"]
                    if 'episodes' in self._embedded:
                        self.episode_list = [Episode(**episode) for episode in self._embedded["episodes"]]
                    if 'cast' in self._embedded:
                        self.cast_list = [Cast(**cast) for cast in self._embedded["cast"]]
                    if 'crew' in self._embedded:
                        self.crew_list = [Crew(**crew) for crew in self._embedded["crew"]]
                    if 'seasons' in self._embedded:
                        self.season_list = [Season(**season) for season in self._embedded["seasons"]]
        else:
            self.show_id = kwargs.get('id')
            for key, val in kwargs.items():
                setattr(self, key, val)

        self.base_url = '{}{}'.format(SHOW, self.show_id)
        self.crew_url = '{}/crew'.format(self.base_url)
        self.cast_url = '{}/cast'.format(self.base_url)
        self.episodes_url = '{}/episodes'.format(self.base_url)
        self.season_url = '{}/seasons'.format(self.base_url)

    def __str__(self):
        return "{}".format(self.name)

    @property
    def episodes(self):
        """Return list of episodes"""
        try:
            return get_list(self, 'episode_list', self.episodes_url, Episode)
        except ApiError as e:
            raise e

    def get_episode(self, index):
        """Return episode in episode_list based on index

        :param int index: Index of episode list
        :return: Episode object
        """
        try:
            return self.episodes[int(index)]
        except (ValueError, IndexError):
            return None

    @property
    def next_episode(self):
        """Return episode that will air next"""
        if self.next:
            return self.next
        try:
            episode_url = self._links['nextepisode']['href']
        except KeyError:
            return None
        else:
            self.next = Episode(create_url=episode_url)
            return self.next

    @property
    def specials(self):
        """Return list of episodes with specials if show has specials"""
        try:
            return [
                episode for episode in
                get_list(self, 'special_list', '{}?specials=1'.format(self.episodes_url), Episode)
                if not episode.number
            ]
        except ApiError as e:
            raise e

    def episode_by_number(self, season, episode):
        """Return episode object

        :param int season: Season number of show. Example 1
        :param int episode: Episode number of show. Example 2
        :return: Return episode object
        """
        episode = requests.get(
            '{}{}/episodebynumber?season={}&number={}'.format(SHOW, self.show_id, season, episode)
        )
        if episode.status_code == 404:
            raise ValueError("Episode does not exist")
        return episode.json()

    def episodes_by_date(self, date):
        """Return all episodes that have aired on a specific date

        :param date: an ISO 8601 formatted date. Example 2016-08-24
        :return: List of dicts
        """
        episodes = requests.get(
            '{}{}/episodesbydate?date={}'.format(SHOW, self.show_id, date)
        )
        if episodes.status_code >= 400:
            raise ValueError('{}'.format(episodes.json()['message']))
        return episodes.json()

    @property
    def seasons(self):
        """Return list of seasons related to the show"""
        try:
            return get_list(self, 'season_list', self.season_url, Season)
        except ApiError as e:
            raise e

    @property
    def cast(self):
        """Return list of cast related to the show"""
        try:
            return get_list(self, 'cast_list', self.cast_url, Cast)
        except ApiError as e:
            raise e

    @property
    def crew(self):
        """Return list of crew related to the show"""
        try:
            return get_list(self, 'crew_list', self.crew_url, Crew)
        except ApiError as e:
            raise e


class Season:
    def __init__(self, season_id=None, with_episodes=False, **kwargs):
        """Create new season with season_id or kwargs

        :param int season_id: Id of season not required if creating season from kwargs
        :param bool with_episodes: Include episodes with season
        """
        self.episode_list = []
        if season_id:
            self.season_id = season_id
            self.api_url = "{}{}{}".format(SEASON, self.season_id, "?embed=episodes" if with_episodes else '')
            response = requests.get(self.api_url)
            if response.status_code > 400:
                raise ValueError('{}'.format(response.json()['message']))
            season = response.json()
            if with_episodes:
                self.episode_list = [Episode(**episode) for episode in season['_embedded']['episodes']]
            self.name = season["name"]
            self._links = season["_links"]
            self.url = season["url"]
            self.premiereDate = season["premiereDate"]
            self.id = season["id"]
            self.episodeOrder = season["episodeOrder"]
            self.number = season["number"]
            self.endDate = season["endDate"]
            self.webChannel = season["webChannel"]
            self.summary = season["summary"]
            self.network = season["network"]
            self.image = season["image"]
        else:
            self.season_id = kwargs.get('id')
            for key, val in kwargs.items():
                setattr(self, key, val)
        self.base_url = "{}{}".format(SEASON, self.season_id)

    @property
    def episodes(self):
        if self.episode_list:
            return self.episode_list
        r = requests.get('{}/episodes'.format(self.base_url))
        if r.status_code >= 400:
            return []
        self.episode_list = [Episode(**episode) for episode in r.json()]
        return self.episode_list


class Episode:
    """Episode class for tvmaze api"""
    def __init__(self, create_url=None, **kwargs):
        """Create episode with episode url or a dict of episode info"""
        if create_url:
            try:
                episode = make_request(create_url)
            except ApiError as e:
                raise e
            else:
                self.airdate = episode["airdate"]
                self.airstamp = episode["airstamp"]
                self.number = episode["number"]
                self.id = episode["id"]
                self.season = episode["season"]
                self.runtime = episode["runtime"]
                self.name = episode["name"]
                self.image = episode["image"]
                self.summary = episode["summary"]
                self.airtime = episode["airtime"]
                self.url = episode["url"]
                self._links = episode["_links"]
        for key, val in kwargs.items():
            setattr(self, key, val)
        try:
            self.show = Show(**kwargs['show'])
        except KeyError:
            self.show = None


class Person:
    """Person class for tvmaze api"""

    def __init__(self, person, **kwargs):
        self.id = person.get('id', 1)
        self.url = person.get('url', 'no url entered')
        self.name = person.get('name', 'no name')
        self.image = person.get('image', {"medium": "no link", "original": "no link"})
        for key, val in kwargs.items():
            setattr(self, key, val)

    def __str__(self):
        return self.name


class Crew(Person):
    def __init__(self, type, **kwargs):
        super().__init__(**kwargs)
        self.crew_type = type


class Cast(Person):
    def __init__(self, character, **kwargs):
        super().__init__(**kwargs)
        self.character = character


class Search:
    def __init__(self, query=None, variant='shows', **kwargs):
        """

        variant options:

        - shows(default)
        - singlesearch
        - lookup
        - people

        :param str variant: One of the api search options on tv maze.
        :param str query: Search query.
        """
        self.variant = variant
        self.results_list = None
        self.kls = Show
        if variant == 'shows':
            self.url = '{}?q={}'.format(SHOW_SEARCH, query)
        elif variant == 'singlesearch':
            url = '{}?q={}'.format(SINGLE_SEARCH, query)
            embed_string = kwargs.get('embed_string')
            url += '&{}'.format(embed_string)
            self.url = url
        elif variant == 'lookup':
            lookup = kwargs.get('lookup')
            if not lookup:
                raise ValueError("""
                lookup string i.e tvrage=1242 required when search is variant lookup.
                See documentation for other lookup strings
                """)
            self.url = '{}?{}'.format(SHOW_LOOKUP, lookup)
        elif variant == 'people':
            self.url = '{}?q={}'.format(PEOPLE_SEARCH, query)
            self.kls = Person

    @property
    def results(self):
        if self.results_list:
            return self.results_list
        if self.variant == 'singlesearch' or self.variant == 'lookup':
            self.results_list = self.kls(**make_request(self.url))
        elif self.variant == 'people':
            self.results_list = [self.kls(**item) for item in make_request(self.url)]
        else:
            self.results_list = [self.kls(**item['show']) for item in make_request(self.url)]
        return self.results_list

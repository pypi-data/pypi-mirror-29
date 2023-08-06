"""tests for tvmaze.py"""

import requests
import time
from pytv.tvmaze import (
    Schedule,
    Shows,
    Show,
    Search,
    Season,
    Cast,
    Crew,
    Person,
    Episode,
    ApiError,
    make_request,
    get_updates
)
from .apiurls import SHOW, SHOWS
import unittest


class TestSchedule(unittest.TestCase):
    """Tests Schedule class in tvmaze.py"""

    def setUp(self):
        """Creates a schedule"""
        self.schedule = Schedule()

    def test_init_schedule(self):
        """Tests new Schedule class"""

        # test country code default is set to us
        self.assertEqual('US', self.schedule.country_code)
        self.assertTrue(self.schedule.date, time.strftime('%Y-%m-%d'))
        self.assertTrue(self.schedule.url)

    def test_schedule_has_episodes(self):
        """Tests Schedule gets episodes from the tvmaze api"""
        response = requests.get(self.schedule.url)

        # test api returns 200
        self.assertEqual(200, response.status_code)
        episodes = self.schedule.episodes

        self.assertTrue(episodes)

    def test_include_networks(self):
        """include_networks() should return all episodes in the included networks"""
        new_episodes = self.schedule.include_networks(['Disney Channel'])
        for episode in new_episodes:
            self.assertTrue(episode.show.network["name"] in ['Disney Channel'])

    def test_include_multiple_networks(self):
        """include_networks() should return all episodes with multiple networks included"""
        networks = ['Disney Channel', 'HGTV', 'CBS']
        new_episodes = self.schedule.include_networks(networks)
        for episode in new_episodes:
            self.assertTrue(episode.show.network["name"] in networks)


class TestShows(unittest.TestCase):

    def get_compare_data(self, page=0):
        return [Show(**show) for show in make_request('{}?page={}'.format(SHOWS, page))]

    def compare_api_and_class(self, show_class):
        shows_data = self.get_compare_data(show_class.page)
        for show1, show2 in zip(show_class.shows, shows_data):
            self.assertEqual(show1.id, show2.id)
            self.assertEqual(show1.name, show2.name)

    def test_shows(self):
        shows = Shows()
        self.compare_api_and_class(shows)

    def test_shows_with_page(self):
        shows = Shows(page=3)
        self.assertEqual(shows.page, 3)
        self.compare_api_and_class(shows)

    def test_shows_next_page(self):
        shows = Shows(page=6)
        shows.next_page()
        self.assertEqual(shows.page, 7)
        self.compare_api_and_class(shows)

    def test_shows_previous_page(self):
        shows = Shows(page=5)
        shows.previous_page()
        self.assertEqual(shows.page, 4)
        self.compare_api_and_class(shows)

    def test_repeat_pagination_calls(self):
        shows = Shows(page=3)
        shows.next_page()
        shows.next_page()
        self.assertEqual(shows.page, 5)
        self.compare_api_and_class(shows)
        shows.next_page()
        shows.next_page()
        self.assertEqual(shows.page, 7)
        self.compare_api_and_class(shows)
        shows.previous_page()
        self.assertEqual(shows.page, 6)
        self.compare_api_and_class(shows)
        shows.previous_page()
        shows.previous_page()
        self.assertEqual(shows.page, 4)
        self.compare_api_and_class(shows)
        shows.previous_page()
        self.assertEqual(shows.page, 3)
        self.compare_api_and_class(shows)

    def test_out_of_range_page(self):
        """A page below 0 should return page 0 a page above max pages should raise error"""
        shows = Shows(page=-1)
        self.assertEqual(0, shows.page)
        self.compare_api_and_class(shows)

        self.assertRaises(ApiError, lambda: Shows(page=1000))

        shows = Shows(page=141)
        self.assertRaises(ApiError, lambda: shows.next_page())
        self.assertEqual(shows.page, 141)

    def test_updates(self):
        data = get_updates()
        self.assertTrue(data)
        for key in data.keys():
            self.assertTrue(int(key))


class TestShow(unittest.TestCase):
    """Tests Show class in tvmaze.py"""

    def test_create_show(self):
        """Tests init method in show class"""
        show = Show(show_id=1)
        self.assertEqual('http://api.tvmaze.com/shows/1', show.api_url)
        self.assertEqual(1, show.id)

    def test_bad_create_show(self):
        """init method of show class should raise error if show id is not valid"""
        self.assertRaises(ApiError, lambda: Show(show_id='3fad'))

    def test_create_show_from_api_data(self):
        data = make_request('{}1'.format(SHOW))
        show = Show(**data)
        self.assertEqual(data['id'], show.id)
        self.assertEqual(data['id'], show.show_id)
        self.assertDictEqual(data['schedule'], show.schedule)
        self.assertDictEqual(data['network'], show.network)
        self.assertListEqual(data['genres'], show.genres)

    def test_create_show_with_embed_cast_url(self):
        """Tests init method in show class with additional arg embed_url"""
        show = Show(show_id=1, embed_url='?embed=cast')
        self.assertEqual('http://api.tvmaze.com/shows/1?embed=cast', show.api_url)

    def test_create_show_with_embed_season_url(self):
        """Init method in show class when embed_url=seasons should return all seasons as Season class per season"""
        show = Show(show_id=1, embed_url='?embed=seasons')
        self.assertIsInstance(show.seasons[0], Season)
        self.assertTrue(show.seasons[0].episodes)
        self.assertEqual(1, show.seasons[0].number)

    def test_episodes(self):
        """episodes property should return a list of episodes"""
        show = Show(show_id=1)
        episodes = show.episodes
        for episode in episodes:
            self.assertTrue('under-the-dome' in episode.url)

    def test_seasons(self):
        """seasons property should return list of seasons"""
        show = Show(show_id=1)
        self.assertFalse(show.season_list)
        seasons = show.seasons
        self.assertTrue(show.season_list)

        for season in seasons:
            self.assertIsInstance(season, Season)

    def test_specials(self):
        """specials property should return list of specials as Episode objects"""
        show = Show(show_id=1)
        specials = show.specials
        self.assertTrue(specials)
        for episode in specials:
            self.assertIsInstance(episode, Episode)

    def test_failed_episode_by_season_and_number(self):
        """episode_by_number() should raise ValueError if bad season or episode"""
        show = Show(show_id=1)
        self.assertRaises(ValueError, lambda: show.episode_by_number(5, 1))
        self.assertRaises(ValueError, lambda: show.episode_by_number(1, 25))

    def test_episode_by_season_and_number(self):
        """episode_by_number() should return dict of episode information"""
        show = Show(show_id=1)
        episode = show.episode_by_number(1, 1)
        self.assertEqual(1, episode['number'])
        self.assertEqual(1, episode['season'])

        second_episode = show.episode_by_number(2, 11)
        self.assertEqual(2, second_episode['season'])
        self.assertEqual(11, second_episode['number'])

    def test_invalid_date_episode_by_date(self):
        """bad date for episode_by_date() should raise ValueError"""
        show = Show(show_id=1)
        self.assertRaises(ValueError, lambda: show.episodes_by_date('12'))
        self.assertRaises(ValueError, lambda: show.episodes_by_date(''))
        self.assertRaises(ValueError, lambda: show.episodes_by_date(1))
        self.assertRaises(ValueError, lambda: show.episodes_by_date('2002-02-21'))

    def test_valid_date_episode_by_date(self):
        """valid date for episode_by_date() should return list of episodes"""
        show = Show(show_id=1)
        episodes = show.episodes_by_date('2013-07-01')
        for episode in episodes:
            self.assertEqual('2013-07-01', episode['airdate'])

    def test_cast(self):
        """cast property should return a list of cast members"""
        show = Show(show_id=1)
        self.assertTrue('/1/cast' in show.cast_url)
        self.assertFalse(show.cast_list)
        cast_list = show.cast
        self.assertTrue(show.cast_list)
        self.assertTrue(cast_list)

        for cast in cast_list:
            self.assertTrue(hasattr(cast, 'character'))
            self.assertIsInstance(obj=cast, cls=Cast)

    def test_cast_with_embed_url(self):
        """cast property should return list of cast members as Cast objects when created with embed_url"""
        show = Show(show_id=1, embed_url="?embed=cast")
        for cast in show.cast:
            self.assertIsInstance(cast, Cast)

    def test_crew(self):
        """crew property should return list of crew members"""
        show = Show(show_id=1)
        self.assertTrue('/1/crew' in show.crew_url)
        self.assertFalse(show.crew_list)
        crew = show.crew
        self.assertTrue(show.crew_list)
        self.assertTrue(crew)
        for person in crew:
            self.assertTrue(hasattr(person, 'crew_type'))
            self.assertIsInstance(person, Crew)

    def test_crew_with_embed_url(self):
        """crew property should return list of crew members as Crew objects when created with embed_url"""
        show = Show(show_id=1, embed_url='?embed=crew')
        for crew in show.crew:
            self.assertIsInstance(crew, Crew)

    def test_get_episode_method_with_valid_int(self):
        """get_episode(-1) should return the last Episode object in the episode list"""
        show = Show(show_id=1)
        self.assertEqual(show.episodes[-1], show.get_episode(-1))

    def test_get_episode_method_with_bad_input(self):
        """get_episode("taco") should return None"""
        show = Show(show_id=1)
        self.assertIsNone(show.get_episode('taco'))

    def test_get_episode_method_with_out_of_range_input(self):
        """get_episode(100000) should return None assuming a show doesn't have 100,000 episodes"""
        show = Show(show_id=1)
        self.assertIsNone(show.get_episode(100000))

    def test_next_episode(self):
        """next_episode property should return Episode object or None"""
        schedule = Schedule()
        show = schedule.episodes[0].show
        self.assertTrue(show.next_episode)


class TestSeason(unittest.TestCase):
    """Tests Season class in tvmaze.py"""

    def test_create_season_with_bad_season(self):
        """Tests init method in Season class"""
        self.assertRaises(ValueError, lambda: Season(season_id='t'))

    def test_season_with_good_season(self):
        """Tests init method in Season class with good season_id"""
        season = Season(season_id=1)
        self.assertTrue(season)

    def test_season_with_episodes(self):
        """Tests init method in Season class with_episodes=True"""
        season = Season(season_id=1, with_episodes=True)
        for episode in season.episodes:
            self.assertEqual(1, episode.season)

    def test_episodes(self):
        """Test episodes property"""
        season = Season(season_id=1)

        # make sure episode list empty to ensure season.episodes makes the correct api call
        self.assertFalse(season.episode_list)

        # api call made
        self.assertTrue(season.episodes)

        # make sure episode_list is correctly populated after api call
        self.assertTrue(season.episode_list)


class TestCast(unittest.TestCase):
    """Tests for Cast class in tvmaze.py"""

    def setUp(self):
        self.cast_list = make_request('http://api.tvmaze.com/shows/1/cast')

    def test_create_cast_class(self):
        """Tests init method of cast class"""
        cast_member = Cast(**self.cast_list[0])
        self.assertTrue(cast_member.character)
        self.assertTrue(cast_member.name)
        self.assertTrue(cast_member.url)
        self.assertTrue(cast_member.image)
        self.assertNotEqual('no name', cast_member.name)
        self.assertNotEqual('no url entered', cast_member.url)
        self.assertNotEqual({"medium": "no link", "original": "no link"}, cast_member.image)


class TestCrew(unittest.TestCase):
    """Tests for Crew class in tvmaze.py"""

    def setUp(self):
        self.crew_list = make_request('http://api.tvmaze.com/shows/1/crew')

    def test_create_crew_class(self):
        """Tests init method of crew class"""
        crew_member = Crew(**self.crew_list[0])
        self.assertTrue(crew_member.crew_type)
        self.assertTrue(crew_member.name)
        self.assertTrue(crew_member.url)
        self.assertTrue(crew_member.image)
        self.assertNotEqual('no name', crew_member.name)
        self.assertNotEqual('no url entered', crew_member.url)
        self.assertNotEqual({"medium": "no link", "original": "no link"}, crew_member.image)


class TestSearch(unittest.TestCase):

    def test_search_shows(self):
        search = Search(query='under the dome')
        self.assertTrue(search.results)
        self.assertEqual(search.results[0].name, Show(show_id=1).name)
        for result in search.results:
            self.assertIsInstance(result, Show)

    def test_search_single_search(self):
        """single search only returns a single result instead of a list"""
        search = Search(variant='singlesearch', query='under the doem')
        self.assertTrue(search.results)
        self.assertEqual(search.results.name, Show(show_id=1).name)
        self.assertIsInstance(search.results, Show)

    def test_search_lookup(self):
        """look up search only returns single result"""
        search = Search(variant='lookup', lookup='thetvdb=81189')
        # look up search is of breaking bad we will get breaking bad by name and compare with thetvdb lookup
        second_search = Search(variant='singlesearch', query='breaking bad')
        self.assertTrue(search.results)
        self.assertEqual(search.results.name, second_search.results.name)
        self.assertIsInstance(search.results, Show)

    def test_search_people(self):
        search = Search(variant='people', query='lauren')
        api_results = [Person(**item) for item in make_request(search.url)]
        for person1, person2 in zip(search.results, api_results):
            self.assertEqual(person1.name, person2.name)
            self.assertEqual(person1.id, person2.id)
            self.assertIsInstance(person1, Person)

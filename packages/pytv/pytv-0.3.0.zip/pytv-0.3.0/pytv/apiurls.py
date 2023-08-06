"""File that contains all the urls for the tvmaze api located at http://www.tvmaze.com/api"""

BASE_URL = 'http://api.tvmaze.com/'

SCHEDULE = '{}schedule'.format(BASE_URL)
FULL_SCHEDULE = '{}/full'.format(SCHEDULE)

UPDATES = '{}updates/shows'.format(BASE_URL)
SHOWS = '{}shows'.format(BASE_URL)
SHOW = '{}/'.format(SHOWS)
EPISODE = '{}/episodes/'.format(BASE_URL)

SEASON = '{}seasons/'.format(BASE_URL)

SEARCH = '{}search/'.format(BASE_URL)
SINGLE_SEARCH = '{}/singlesearch/shows/'.format(BASE_URL)
SHOW_LOOKUP = '{}/lookup/shows'.format(BASE_URL)
SHOW_SEARCH = '{}shows'.format(SEARCH)
PEOPLE_SEARCH = '{}people'.format(SEARCH)

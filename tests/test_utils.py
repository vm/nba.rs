from __future__ import (
    print_function, absolute_import, division, unicode_literals)

from datetime import datetime

import pytest

from nba.utils import *

def test_is_number_true():
    assert is_number('5') is True


def test_is_number_false():
    assert is_number('five') is False


def test_is_number_string():
    with pytest.raises(NotImplementedError):
        is_number(56)


def test_find_player_code():
    assert find_player_code('Kevin Durant') == 'duranke01'


def test_find_player_name():
    assert find_player_name('duranke01') == 'Kevin Durant'


def test_path_components_from_url():
    path_components = [
        '', 'players', 'd', 'duranke01', 'gamelog', '2014', ''
    ]
    assert path_components == path_components_of_url(
        'http://www.basketball-reference.com/players/d/duranke01/' +
        'gamelog/2014/')


def test_get_gamelog_header():
    gamelog_soup = soup_from_url(
        'http://www.basketball-reference.com/players/d/duranke01/' +
        'gamelog/2014/')
    reg_table = gamelog_soup.find('table', attrs={'id': 'pgl_basic'})
    assert get_header(reg_table) == [
        'Rk', 'G', 'Date', 'Age', 'Tm', '', 'Opp', 'GS', 'MP', 'FG', 'FGA',
        'FGP', 'TP', 'TPA', 'TPP', 'FT', 'FTA', 'FTP', 'ORB', 'DRB', 'TRB',
        'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'GmSc', 'PlusMinus'
    ]


def test_get_gamelog_urls():
    gamelog_urls = get_gamelog_urls(
        'http://www.basketball-reference.com/players/d/duranke01.html')
    base = ('http://www.basketball-reference.com/players/d/duranke01/' +
            'gamelog/')
    assert gamelog_urls == [
        base + '2008/', base + '2009/', base + '2010/', base + '2011/',
        base + '2012/', base + '2013/', base + '2014/', base + '2015/'
    ]


def test_get_hth_header():
    hth_soup = soup_from_url(
        'http://www.basketball-reference.com/play-index/h2h_finder.cgi?' +
        'request=1&p1=jamesle01&p2=duranke01#stats_playoffs')
    reg_table = hth_soup.find('table', attrs={'id': 'stats_games'})
    assert get_header(reg_table) == [
        'Rk', 'Player', 'Date', 'Tm', '', 'Opp', 'GS', 'MP', 'FG', 'FGA',
        'FGP', 'TP', 'TPA', 'TPP', 'FT', 'FTA', 'FTP', 'ORB', 'DRB', 'TRB',
        'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS'
    ]


def test_get_hth_header_attribute_error():
    gamelog_soup = soup_from_url(
        'http://www.basketball-reference.com/play-index/h2h_finder.cgi?' +
        'request=1&p1=kiddja01&p2=napiersh01#stats_playoffs')
    reg_table = gamelog_soup.findAll('table', attrs={'id': 'stats_games'})
    assert get_header(reg_table) is None


def test_create_datetime_range():
    assert datetime_range('2014-12-20', '2014-12-22') == {
        'Date': {
            '$gte': datetime.datetime(2014, 12, 20, 0, 0),
            '$lt': datetime.datetime(2014, 12, 22, 0, 0)
        }
    }

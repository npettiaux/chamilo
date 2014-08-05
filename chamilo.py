#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import requests
from BeautifulSoup import BeautifulSoup

USERNAME = 'esi_id'
PASSWORD = 'esi_pass'
CHAMI_URL = 'http://elearning.esi.heb.be'
s = requests.Session()


def authenticate(username, password, s):
    payload = {'login': username, 'password': password}
    r = s.post(CHAMI_URL + '/index.php', data=payload)


def get_courses(s):
    url = CHAMI_URL + '/user_portal.php'

    soup = BeautifulSoup(s.get(url).text)
    courses = soup.findAll('div', attrs={'class': 'userportal-course-item'})

    return courses


def download_course(course_info):
    url = course_info.find('a')['href']
    name = url.split('/')[4]

    soup = BeautifulSoup(s.get(url).content)
    url = soup.find('a', attrs={'title': 'Documents'})
    if url:
        document_url = CHAMI_URL + url['href']
        soup = BeautifulSoup(s.get(document_url).content)

        folders = [x['value'] for x in soup.findAll('option')]
        for folder in folders:
            save_folders(name, folder)


def save_folders(name, url):
    url = CHAMI_URL + '/main/document/document.php?cidReq=' + name + '&curdirpath=' + url
    soup = BeautifulSoup(s.get(url).content)

    files = soup.findAll('a', attrs={'style': 'float:right'})
    for file in files:
        save_file(name, CHAMI_URL + file['href'])


def save_file(path, url):
    name = '/'.join(url.split('%2F')[1:])
    name = path + '/' + name
    path = '/'.join(name.split('/')[:-1])

    if not os.path.exists(path):
        print('"%s" created' % (path))
        os.makedirs(path)

    if not os.path.exists(name):
        print('"%s"...' % (name)),
        with open(name, 'w') as f:
            f.write(s.get(url).content)
        print(' saved')


if __name__ == '__main__':

    if USERNAME == 'esi_id' or PASSWORD == 'esi_pass':
        print('Please enter your credentials. Quitting.')
        exit()

    authenticate(USERNAME, PASSWORD, s)

    print('Checking courses...')
    courses = get_courses(s)

    for course in courses:
        print('Downloading files for %s' % course.find('a')['href'].split('/')[4])
        download_course(course)
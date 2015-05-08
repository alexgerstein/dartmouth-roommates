Find your next roommate (through Dartmouth).

## Statuses
[![Build Status](https://travis-ci.org/alexgerstein/dartmouth-roommates.svg?branch=master)](https://travis-ci.org/alexgerstein/dartmouth-roommates)
[![Coverage Status](https://coveralls.io/repos/alexgerstein/dartmouth-roommates/badge.svg?branch=master)](https://coveralls.io/r/alexgerstein/dartmouth-roommates?branch=master)

## Description
Roommate board for Dartmouth students.

http://lodjers.com


## Installation
1. Clone repo to computer
2. Install all requirements from requirements.txt

	Virtual environment (preferred):
	1. Create a virtual environment: ```virtualenv flask```
	2. Install requirements: ```flask/bin/pip install -r requirements.txt```
	3. Activate virtual environment: ```. flask/bin/activate```

	System-wide (not the best option): ```sudo pip install -r requirements.txt```


## Run Locally
1. Start up a local server: ```python manage.py server```
2. Seed the database with users: ```python manage.py seed```

## Tests
* To run the basic unittests, run ```python manage.py tests```.

## License
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see http://www.gnu.org/licenses/.

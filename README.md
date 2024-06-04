# Basketball Reference API

## Overview

This project is a public API designed to provide basketball data from the website [basketball-reference.com](https://www.basketball-reference.com). It uses Flask for hosting the endpoints, AWS RDS for PostgreSQL database hosting, and will be deployed using Zeet. The API currently has two endpoints, with more planned for future releases.

NOTE: the database is being hosted on AWS RDS currently, but the endpoints are still on the localhost - they are not publicly available yet.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Endpoints](#endpoints)
- [Modules](#modules)
- [Contributing](#contributing)
- [License](#license)

## Installation

To get started with this project, clone the repository and install the required dependencies.

```bash
git clone https://github.com/yourusername/basketball-reference-api.git
cd basketball-reference-api
pip install -r requirements.txt
```

## Usage
To run the API locally, execute the following command:

```bash
export FLASK_APP=endpoints.py
flask run
```
This will start the Flask server on http://127.0.0.1:5000/.

## Endpoints

### `/api/player-stats`

- **Description**: Retrieves player data.
- **Method**: GET
- **Parameters**: 
  - `player_name` (required): the name of the player.

### `/api/team-year-roster`

- **Description**: Retrieves team data.
- **Method**: GET
- **Parameters**: 
  - `team_id` (required): The unique code for the team.
  - `year` (required): the year the team played in.

### `/api/player-prev-games`

- **Description**: retrieves the player's past few games.
- **Method**: GET
- **Parameters**:
  - `player_name` (required): the name of the player.

## Handling Rate Limits

Basketball reference allows data to be scraped off its website, however it rate limits quite strictly. More than a few attempts
at scraping within a few seconds can get your IP banned for over an hour. To circumvent this, the project has its own PostgreSQL
database setup. When the api receives a GET request, checks its database to see if the dbase holds the queried data. If it does,
then the data is immediately fetched from the database without attempting scraping of any sort. If it does not, THEN a web
scraping script is run, after which the newly scraped data is added to the database (so that if it is ever requested again, one
need not web scrape again).
Additionally, to avoid the IP ban, this API has been rate limited to throttle requests to about 1 every 5 seconds.
The above methods have been implemented in order to effectively get and provide data from the popular website.

## Modules

### `Player.py`

This module contains the `Player` class which uses web scraping techniques to extract player data from basketball-reference.com.

### `Team.py`

This module contains the `TeamScraper` class which uses web scraping techniques to extract team data from basketball-reference.com.

### `endpoints.py`

This module defines the Flask routes for the API endpoints.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a pull request.


# Basketball Reference API

## Overview

This project is a public API designed to provide basketball data from the website [basketball-reference.com](https://www.basketball-reference.com). It uses Flask for hosting the endpoints, AWS RDS for PostgreSQL database hosting, and will be deployed using Zeet. The API currently has two endpoints, with more planned for future releases.

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

### `/api/v1/player`

- **Description**: Retrieves player data.
- **Method**: GET
- **Parameters**: 
  - `player_id` (required): The unique identifier for the player.

### `/api/v1/team`

- **Description**: Retrieves team data.
- **Method**: GET
- **Parameters**: 
  - `team_id` (required): The unique identifier for the team.

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


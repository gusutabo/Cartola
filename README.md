# Cartola

> A Command Line Interface (CLI) tool for analyzing football matches and calculating head-to-head probabilities.

## Functionalities

* Search teams by name (returns ID, name, and country)
* Head-to-head match analysis 
* Probability calculation (win/draw/lose) based on last 20 matches
* Integration with API-Football

## Usage Method

### Clone the repository

```bash 
git clone https://github.com/gusutabo/cartola.git
cd cartola
```

### Set API Key

```bash 
export FUTEBOL_API_KEY=your_api_key_here
```

### Run the application

```bash 
python3 main.py search <team_name>
python3 main.py view <team_id_a> <team_id_b>
```

## License

This project is licensed under the MIT License.

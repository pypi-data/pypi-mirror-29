# pays

WIP : Une librairie en python 3 pour intégrer des listes de pays dans ses applications.

## Installation

`pays` est disponible sur [pip](https://pypi.org/project/pays/)

```sh
pip install pays
```

## Usage

```python
import pays

countries = pays(
    'fra',  # locale 639-2 pour les traductions des noms, , optionnel, fra par défaut
    # liste de pays à exclure (alpha2, 3 ou numérique), optionnel
    exclude=['ES'],
    # liste de pays à retourner (alpha2, 3 ou numérique), optionnel
    only=['FR', 'DE']
    # note: on ne peut utiliser que exclude OU only, pas les deux à la fois
)
for country in countries.items():
    print(country)  # __str__ retourne nom commun : France
    print(country.official_name)  # République Française

dir(country)



print(countries.get('FR'))  # France
print(countries.get('FRA', 'ita'))  # Francia en italien
print(countries.get(250, 'nld'))  # Frankrijk en Néerlandais


countries.by_common_name()  # default __dict__
countries.by_alpha2_code()
countries.by_alpha3_code()
countries.by_number()
```

## Développement

```sh

git clone git@gitlab.com:canarduck/pays.git
```

`pays` utilise [mledoze/countries](https://github.com/mledoze/countries) comme source de données.
Pour mettre à jour les listes / traductions :

```sh

python setup.py update_pays
```

## Tests

```sh

python setup.py tests
```

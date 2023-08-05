# pays

[![Intégration continue](https://gitlab.com/canarduck/pays/badges/master/pipeline.svg)](https://gitlab.com/canarduck/pays/commits/master) [![Couverture des tests](https://gitlab.com/canarduck/pays/badges/master/coverage.svg)](https://canarduck.gitlab.io/pays/coverage/)

Une librairie pour intégrer des listes (simples) de pays dans ses applications.

## Installation

`pays` est disponible sur [pip](https://pypi.org/project/pays/) pour python > 3.

```sh
pip install pays
```

## Usage

```python
from pays import Countries

countries = Countries(
    'fra',  # locale 639-2 pour les traductions des noms, optionnel, fra par défaut
    # codes alpha2 de pays à exclure, optionnel
    exclude=['ES'],
    # codes alpha2 de pays à utiliser exclusivement, optionnel
    only=['FR', 'DE']
    # note: on ne peut utiliser que exclude OU only, pas les deux à la fois
)
for country in countries:  # générateur
    print(country)  # __str__ retourne nom commun : France
    print(country.official_name)  # République Française



print(countries.get('FR'))  # France
print(countries.get('FRA', 'ita'))  # Francia en italien
print(countries.get(250, 'nld'))  # Frankrijk en Néerlandais
```

Pour plus d'informations consultez [la documentation](https://canarduck.gitlab.io/pays)

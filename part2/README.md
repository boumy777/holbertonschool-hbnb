HBNB - Holberton School# HBNB - Holberton School

## Description

Projet de création d'un clone simplifié d'AirBnB en Python avec une architecture modulaire : modèles, services, persistance et API.

## Fonctionnalités

- Création et gestion des utilisateurs
- Création et consultation des lieux (`Place`)
- Système de commentaires (`Review`)
- API REST avec Flask
- Stockage en mémoire via un dépôt singleton

## Structure du projet
## Fonctionnalités

- Création, lecture, mise à jour et suppression (CRUD) des entités : User, Place, Amenity, Review
- Stockage en mémoire (via un repository)
- API REST pour interagir avec les données
- Architecture MVC (avec pattern façade)

holbertonschool-hbnb/
└── part2/
├── app/
│ ├── api/
│ │ └── v1/
│ │ ├── users.py
│ │ ├── places.py
│ │ ├── reviews.py
│ │ └── amenities.py
│ ├── models/
│ │ ├── user.py
│ │ ├── place.py
│ │ ├── review.py
│ │ └── amenity.py
│ ├── services/
│ │ └── facade.py
│ └── persistence/
│ └── repository.py
├── tests/
│ └── test_models/
│ ├── test_user.py
│ ├── test_place.py
│ ├── test_amenity.py
│ └── test_review.py
├── run.py
├── requirements.txt
└── README.md

boumy777
stani785
Gr3nvaltBlack


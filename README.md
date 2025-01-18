# Projet Multithreading

## Instructions pour tester le projet

### Lancer les scripts Python

1. Exécutez les scripts dans l’ordre suivant :
    ```bash
    uv run manager.py
    uv run proxy.py
    uv run boss.py
    ```
2. Une fois que le script `boss.py` a terminé la création des tâches :
    ```bash
    uv run minion.py
    ```

### Construire et exécuter le code C++

1. Générez le build avec `cmake` :
    ```bash
    cmake -B build -S .
    cmake --build build
    ```
2. Lancez l'exécutable :
    ```bash
    ./build/low_level
    ```

---

## Comparaison des temps d’exécution

Voici une comparaison des temps d'exécution pour la même tâche avec des tailles de matrices croissantes :

| Taille des matrices | C++ (s)          | Python (s)      |
|---------------------|------------------|-----------------|
| 500                 | 0.0147           | 0.0290          |
| 1000                | 0.0809           | 0.1650          |
| 2000                | 1.3063           | 1.2159          |
| 3000                | 5.6062           | 3.8063          |

### Observations

- **Petites matrices (500 et 1000)** :
  - C++ est plus rapide que Python.
- **Grandes matrices (2000 et 3000)** :
  - Python surpasse C++ grâce à l’utilisation de bibliothèques optimisées comme NumPy.

---


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

## Optimisations apportées au C++

### 1. Compilation optimisée

Le code a été compilé en mode optimisé pour activer les améliorations du compilateur et réduire les temps d'exécution :
```bash
cmake -B build -S . -DCMAKE_BUILD_TYPE=Release
```

### 2. Parallélisme et gestion des threads

- **Threads activés** : Le parallélisme avec Eigen a été configuré pour exploiter pleinement les cœurs disponibles.
- **Configuration des threads** : Sur une machine virtuelle Kali avec 4 cœurs virtuels, un ajustement dynamique a permis d’éviter les surcharges liées à une gestion excessive des threads.

### 3. Utilisation de matrices fixes

- **Matrice à taille fixe** : Les matrices de taille fixe, comme `100x100`, ont été choisies pour permettre au compilateur d’effectuer des optimisations spécifiques.
- **Matrices dynamiques** : Bien que flexibles, elles présentent des limitations de performance liées à la gestion mémoire.

### 4. Comparaison des types de matrices avec Eigen

Les différents types de matrices ont été testés pour évaluer leurs performances :

| Type de matrice                                                         | Comparaison    |
|-------------------------------------------------------------------------|----------------|
| `Eigen::Matrix<float, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>` | --             |
| `Eigen::Matrix<float, Eigen::Dynamic, Eigen::Dynamic, Eigen::ColMajor>` | +              |
| `Eigen::Matrix<float, SIZE, SIZE, Eigen::RowMajor>`                     | ++             |
| `Eigen::Matrix<float, SIZE, SIZE, Eigen::ColMajor>`                     | +++            |

### Observations

- **Matrices fixes (`SIZE, SIZE`)** : Elles sont plus performantes car leur structure est optimisée lors de la compilation.
- **Colonne majoritaire (`ColMajor`)** : Ce format est mieux adapté aux opérations matricielles intensives, réduisant les temps d’accès mémoire.

---

## Conclusion

- **C++** : Performant pour les petites matrices et les scénarios nécessitant un contrôle précis des ressources.
- **Python** : Surpasse C++ pour des matrices de grande taille grâce à des bibliothèques optimisées comme NumPy.

Ce projet met en évidence les différences entre les deux langages et montre l’importance de choisir les bonnes configurations selon le contexte d’utilisation.

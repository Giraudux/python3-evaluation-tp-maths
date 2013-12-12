python3-evaluation-tp-maths
===========================

*Comment valider le TP évalué de mathématiques ?*

1. Lancez le fichier submit.pyc avec l'interpréteur Python 3.
```bash
git clone https://github.com/Giraudux/python3-evaluation-tp-maths
cd ./python3-evaluation-tp-maths/build
python3 -i ./submit.pyc
```

2. Indiquez votre nom d'utilisateur avec la fonction `set_user()`.
```python
set_user("E*******")
```

3. Puis validez tous les exercices avec le fonction `valid_tasks()`.
```python
valid_tasks()
```

4. Il est possible de valider les exercices individuellement avec les fonctions `valid_<task>()`.
```python
valid_stirling()
```

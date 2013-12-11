python3-evaluation-tp-maths
===========================

*Comment valider le TP évalué de mathématiques ?*

1. Lancez le fichier submit.pyc avec l'interpréteur Python 3.
```bash
cd .../build
python3 -i submit.pyc
```

2. Indiquez votre nom d'utilisateur avec la fonction `set_user()`.
```python
set_user("E*******")
```

3. Puis validez tous les exercices avec le fonction `valid_tasks()`.
```python
valid_tasks()
```

..* Note: il est possible de valider les exercices individuellement avec la fonction `valid_<task>()`.
```python
valid_stirling()
```

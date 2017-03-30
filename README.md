# Superpixels

## Utilisation

### Notre implémentation de l'algorithme SLIC

`main.py <file path> <number of clusters> [1=displayContours | 2=displayCenters | 3=displayContours&Centers]`

Exemple :

`python main.py dog.png 400 3`

### Script SEEDS qui utilise l'extension ximgproc d'OpenCV 3

`opencv-seeds.py <file path> <number of clusters>`

Exemple :

`python opencv-seeds.py dog.png 400`


## Resultats

### Chien

![Chien original](/dog.png?raw=true "Chien original")
![Chien SLIC](/dog-slic-400-1.png?raw=true "Chien SLIC")
![Chien SLIC](/dog-seeds-400.png?raw=true "Chien SEEDS")

### Obama

![Obama original](/obama.jpg?raw=true "Obama original")
![Obama SLIC](/obama-slic-400-1.jpg?raw=true "Obama SLIC")
![Obama SLIC](/obama-seeds-400.jpg?raw=true "Obama SEEDS")

### Cellules

![Cellules original](/cells.jpg?raw=true "Cellules original")
![Cellules SLIC](/cells-slic-400-1.jpg?raw=true "Cellules SLIC")
![Obama SLIC](/cells-seeds-400.jpg?raw=true "Cellules SEEDS")
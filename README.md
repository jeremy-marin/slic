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

### Script SLIC qui utilise l'extension ximgproc d'OpenCV 3

`opencv-slic.py <file path> <region size>`

L'implémentation d'OpenCV ne propose pas de donner comme argument le nombre de superpixels.
A la place, il faut renseigner la taille en pixels d'un superpixel.
Le script affiche alors le nombre de superpixels obtenus.

Exemple :

`python opencv-slic.py dog.png 30`


## Resultats

### Chien

![Chien original](/dog.png?raw=true "Chien original")
![Chien SLIC](/dog-slic-400-1.png?raw=true "Chien SLIC")
![Chien OpenCV SEEDS](/dog-seeds-400.png?raw=true "Chien OpenCV SEEDS")
![Chien OpenCV SLIC](/dog-slic-15.png?raw=true "Chien OpenCV SLIC")

### Obama

![Obama original](/obama.jpg?raw=true "Obama original")
![Obama SLIC](/obama-slic-400-1.jpg?raw=true "Obama SLIC")
![Obama OpenCV SEEDS](/obama-seeds-400.jpg?raw=true "Obama OpenCV SEEDS")
![Obama OpenCV SLIC](/obama-slic-30.jpg?raw=true "Obama OpenCV SLIC")

### Cellules

![Cellules original](/cells.jpg?raw=true "Cellules original")
![Cellules SLIC](/cells-slic-400-1.jpg?raw=true "Cellules SLIC")
![Obama OpenCV SEEDS](/cells-seeds-400.jpg?raw=true "Cellules OpenCV SEEDS")
![Obama OpenCV SLIC](/cells-slic-40.jpg?raw=true "Cellules OpenCV SLIC")
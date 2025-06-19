TODO LIST
1. Mirar diseño responsive de la web3. 
2. Revisar la legislación poniendo datos de la AAVV
3. Poner lista de paradas que me pase Juanjo

DONE LIST
1. Poner observaciones en los viajes y si las hay marcarlo en la lista de viajes para que el usuario las pueda leer
2. Poner un botón de "ver observaciones" en la lista de viajes
3. Comprobar que el nombre de usuario no se puede repetir en el perfil--> en el registro se comprueba. El nombre del perfil no es el de usuario
4. Mirar edición de viaje que aparezcan observaciones
5. Asegurarme de que haya un sector que es del Puerto y otro que no al hacer CRUD de sectores
6. Arreglo datos fijos de la base de datos
7. Oculto botón de reservas si el viaje no tiene

IDs DE ELEMENTOS PARA FIJAR TAMAÑO EN utils.js

- primer: tamaño máximo PC 4-xl, Móvil 6-xl
- segon: algo menor  PC 3-xl, Móvil 5-xl

MIGRACIONES

Para hacer las migraciones después de modificar el modelo he tenido que hacer lo siguiente:
```bash

instalar Flask-Migrate con el comando pip install Flask-Migrate
```
En el archivo __init__.py dentro del método create_app() añadir las siguientes líneas:

# Configurar les migracions
    from flask_migrate import Migrate
    migrate = Migrate(app, db)

```python
```bash
export FLASK_APP=app.py
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
```
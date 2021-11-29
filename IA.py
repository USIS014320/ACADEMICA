import pandas as pd
import numpy as np
import tensorflow as tf

ratings_df = pd.read_csv('ratings.csv')
ratings_df.tail()
#El comando #tail se usa para ingresar el contenido de la cola en el archivo. El comando tail muestra las últimas 5 líneas del archivo especificado en la pantalla de forma predeterminada.


movies_df = pd.read_csv('movies.csv')
movies_df.tail()


movies_df['movieRow'] = movies_df.index
#Genere una columna de "movieRow", igual al índice del valor del índice
movies_df.tail()


movies_df = movies_df[['movieRow','movieId','title']]
#Filtro tres enumerados
movies_df.to_csv('moviesProcessed.csv', index=False, header=True, encoding='utf-8')
#Generar un nuevo archivo moviesProcessed.csv
movies_df.tail()


ratings_df = pd.merge(ratings_df, movies_df, on='movieId')
ratings_df.head()


ratings_df = ratings_df[['userId','movieRow','rating']]
#Filtrar tres columnas
ratings_df.to_csv('ratingsProcessed.csv', index=False, header=True, encoding='utf-8')
#Exportar un nuevo archivo ratingsProcessed.csv
ratings_df.head()


userNo = ratings_df['userId'].max() + 1
#userNo máximo
movieNo = ratings_df['movieRow'].max() + 1
#movieNo Máximo


rating = np.zeros((movieNo,userNo))
# Crea un dato con un valor de 0
flag = 0
ratings_df_length = np.shape(ratings_df)[0]
#Ver la primera dimensión de la matriz ratings_df
for index,row in ratings_df.iterrows():
    #interrows (), recorre la tabla ratings_df
    rating[int(row['movieRow']),int(row['userId'])] = row['rating']
    # Complete las columnas 'movieRow' e 'userId' en la tabla ratings_df con la 'clasificación' de la fila
    flag += 1

record = rating > 0
record
record = np.array(record, dtype = int)
#Cambiar el tipo de datos, 0 significa que el usuario no calificó la película, 1 significa que el usuario ya calificó la película
record


def normalizeRatings(rating, record):
    m, n =rating.shape
    #m representa la cantidad de películas, n representa la cantidad de usuarios
    rating_mean = np.zeros((m,1))
    # Puntaje promedio para cada película
    rating_norm = np.zeros((m,n))
    #Calificaciones procesadas
    for i in range(m):
        idx = record[i,:] !=0
        #La calificación de cada película, [i ,:] se refiere a todas las columnas de cada fila
        rating_mean[i] = np.mean(rating[i,idx])
        #   i  , la puntuación media de los usuarios que han revisado idx;
        # np.mean () promedia todos los elementos
        rating_norm[i,idx] -= rating_mean[i]
        #rating_norm = puntuación promedio de puntuación sin procesar
    return rating_norm, rating_mean



rating_norm, rating_mean = normalizeRatings(rating, record)

rating_norm =np.nan_to_num(rating_norm)
#Procesa el valor de NaNN y cámbialo a un valor de 0
rating_norm

rating_mean =np.nan_to_num(rating_mean)
#Procesa el valor de NaNN y cámbialo a un valor de 0
rating_mean

num_features = 10
X_parameters = tf.Variable(tf.random_normal([movieNo, num_features],stddev = 0.35))
Theta_parameters = tf.Variable(tf.random_normal([userNo, num_features],stddev = 0.35))
# tf.Variables () Inicializar variables
#La función # tf.random_normal () se utiliza para extraer el número especificado de valores de los valores que obedecen a la distribución normal especificada, media: la media de la distribución normal. stddev: la desviación estándar de la distribución normal. dtype: tipo de salida

loss = 1/2 * tf.reduce_sum(((tf.matmul(X_parameters, Theta_parameters, transpose_b = True) - rating_norm) * record) ** 2) + 1/2 * (tf.reduce_sum(X_parameters ** 2) + tf.reduce_sum(Theta_parameters ** 2))
# Modelo de algoritmo de recomendación basado en contenido

# Explicación de la función:
# reduce_sum () es la suma, reduce_sum (input_tensor, axis = None, keep_dims = False, name = None, reducciones_indices = None)
# reduce_sum () Explicación del parámetro:
# 1) input_tensor: el tensor de entrada.
# 2) eje: a lo largo de qué dimensión sumar. Para un tensor input_tensor bidimensional, 0 significa suma por columna, 1 significa suma por fila y [0, 1] significa primero suma por columna y luego por fila.
# 3) keep_dims: El valor predeterminado es Flase, lo que significa que se requiere una reducción de dimensionalidad por defecto. Si se establece en Verdadero, no se realiza ninguna reducción de dimensionalidad.
# 4) nombre: nombre.
# 5) reducciones_indices: El valor predeterminado es Ninguno, lo que significa que input_tensor se reduce a la dimensión 0, que es un número. Para input_tensor bidimensional, cuando reduccion_indices = 0, es por columna; cuando reduccion_indices = 1, es por fila.
# 6) Tenga en cuenta que los índices de reducción y el eje no se pueden configurar al mismo tiempo.
 
# tf.matmul (a, b), multiplica la matriz a por la matriz b para generar a * b
# tf.matmul (a, b) explicación del parámetro:
# 1) a: Un tensor de tipo float16, float32, float64, int32, complex64, complex128 y rank> 1.
# 2) b: Mismo tipo y rango que a.
# 3) transpose_a: Si es verdadero, a se transpone antes de la multiplicación.
# 4) transpose_b: si es verdadero, b se transpone antes de la multiplicación.
# 5) adjoint_a: si es verdadero, a se conjuga y se transpone antes de la multiplicación.
# 6) adjoint_b: si es verdadero, b se conjuga y se transpone antes de la multiplicación.
# 7) a_is_sparse: Si es True, a se considera una matriz dispersa.
# 8) b_is_sparse: Si es True, b se considera una matriz dispersa.
# 9) nombre: nombre de la operación (opcional)


optimizer = tf.train.AdamOptimizer(1e-4)
# https://blog.csdn.net/lenbow/article/details/52218551
train = optimizer.minimize(loss)
# Optimizer.minimize básicamente hace dos cosas para una variable de pérdida
# Calcula el gradiente de pérdida relativo a los parámetros del modelo.
# Luego aplique el gradiente calculado para actualizar la variable.

# tf.summary use https://www.cnblogs.com/lyc-seu/p/8647792.html
tf.summary.scalar('loss',loss)
# Se usa para mostrar información escalar

summaryMerged = tf.summary.merge_all()
#merge_all Puede guardar todos los resúmenes en el disco para mostrarlos en el tensorboard.
filename = './movie_tensorborad'
writer = tf.summary.FileWriter(filename)
#Especifique un archivo para guardar la imagen.
sess = tf.Session()
#https://www.cnblogs.com/wuzhitj/p/6648610.html
init = tf.global_variables_initializer()
sess.run(init)
#correr

for i in range(5000):
    _, movie_summary = sess.run([train, summaryMerged])
    # Almacenar el resumen de resultados de entrenamiento combinado en la película
    writer.add_summary(movie_summary, i)
    # Guarde los resultados del entrenamiento

Current_X_parameters, Current_Theta_parameters = sess.run([X_parameters, Theta_parameters])
# Current_X_parameters es la matriz de contenido del usuario, Current_Theta_parameters matriz de preferencias del usuario
predicts = np.dot(Current_X_parameters,Current_Theta_parameters.T) + rating_mean
# la función de punto es la multiplicación de la matriz en np, np.dot (x, y) es equivalente a x.dot (y)
errors = np.sqrt(np.sum((predicts - rating)**2))
# sqrt (arr), calcula la raíz cuadrada de cada elemento
errors

user_id = input('¿Qué usuario quieres recomendar? Introduzca el número de usuario: ')
sortedResult = predicts[:, int(user_id)].argsort()[::-1]
# La función argsort () devuelve el valor de índice del valor de la matriz de pequeño a grande; argsort () [:: - 1] devuelve el valor de índice del valor de la matriz de grande a pequeño
idx = 0
print('Las 20 películas mejor calificadas recomendadas para este usuario son:'.center(80,'='))
# center () devuelve una nueva cadena con la cadena original centrada y llena de espacios hasta el ancho de la longitud. El carácter de relleno predeterminado es un espacio.
for i in sortedResult:
    print('Calificación:% .2f, nombre de la película:% s' % (predicts[i,int(user_id)],movies_df.iloc[i]['title']))
    # Uso de .iloc: https://www.cnblogs.com/harvey888/p/6006200.html
    idx += 1
    if idx == 20:break


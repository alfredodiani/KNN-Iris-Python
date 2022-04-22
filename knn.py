# Universidade Federal de Lavras
# Inteligencia Artificial GCC128
# Docente: AHMED ALI ABDALLA ESMIN 
#
# Aluno: Alfredo Beneti Diani
# Aluno: João Vitor Costa
#
# Trabalho de implementação do algoritmo KNN na base de dados Iris.data
#

import csv
import time
import random

start_time = time.time()
file = open( "iris.data" )
reader = csv.reader( file, delimiter = ',' )
dataset  = [ ]
test_percentage = 0.1 #porcentagem de individuos que serão separados do dataset para utilizar como individuos de teste

print( "\n--------------------------------------------------------\nAlgoritmo KNN para classificação com a IrisDatabase\n--------------------------------------------------------" )

#tratando os valores do dataset para float
for row in reader:
    datapoint = row
    if datapoint != []:
        datapoint[0] = float(datapoint[0])
        datapoint[1] = float(datapoint[1])
        datapoint[2] = float(datapoint[2])
        datapoint[3] = float(datapoint[3])
        dataset.append( row )
        
print( "\nDataset lido" )
random.shuffle( dataset )

#prepara o modelo
test_size = int(len(dataset) * test_percentage)
train_size = len(dataset) - test_size
 
data_test = dataset[ len(dataset) - test_size : ]
data_train = dataset[ : train_size ]
predicted_classes = []

#calcula a distancia euclideana entre dois pontos
def distance( subj1, subj2 ):
    distance = 0
    for i in range( len(subj1)-1 ):
        distance += ( subj1[i] - subj2[i] ) ** 2
    return distance ** 0.5

#faz a classificação de um individuo em um dataset
#retorna a classificação em string
def predict(point, data_train, K):
    train_size = len(data_train)
    distance_list = []
    class_list = []
    for j in range( train_size ):
        d = distance( point, data_train[j] )
        distance_list.append( d )
        class_list.append (data_train[j][4])
    distance_class=[x for _,x in sorted(zip(distance_list,class_list))] #faz um dataset com as distancias e o nome das classes
    K_least_classes = distance_class[ : K ]
    iris_setosa = 0
    iris_versicolour = 0
    iris_virginica = 0
    for i_class in K_least_classes:
        if i_class == 'Iris-setosa':
            iris_setosa += 1
        elif i_class == 'Iris-versicolor':
            iris_versicolour += 1
        else:
            iris_virginica += 1
    if iris_setosa > iris_versicolour and iris_setosa > iris_virginica:
        return 'Iris-setosa'
    elif iris_versicolour > iris_setosa and iris_versicolour > iris_virginica:
        return 'Iris-versicolor'
    else:
        return 'Iris-virginica'

#roda o teste com K vizinhos fazendo as classificações e retornando a porcentagem de acertos
def run_test(data_test, data_train, K):
    test_size = len(data_test)
    predicted_classes = []
    for i in range( test_size ):
        prediction = predict(data_test[i], data_train, K)
        predicted_classes.append( prediction )    
    correct_predictions = 0
    total_predictions = len( data_test )
    for i in range( total_predictions ):
        if data_test[i][4] == predicted_classes[i]:
            correct_predictions += 1
    accuracy = correct_predictions / total_predictions
    return accuracy

# testa o algoritmo para os valores de k_values
print( "\nTestando o algoritmo KNN:\n" )
k_values = [1,3,5,7,9,11,13,15]
max_acc = 0
best_K = 1
for k in k_values:
    acc = run_test(data_test, data_train, k)
    print("K = %d | Acertos: %.2f%%" % (k, (acc*100)))
    if acc > max_acc:
        max_acc = acc
        best_K = k
print( "\nMelhor valor de K: %d \nPrecisão de: %.2f%%" % (best_K, (max_acc*100)) )
end_time = time.time()
print( "\nTempo de execução: %.3f segundos" % (end_time - start_time) )
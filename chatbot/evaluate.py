import spacy
from spacy.training.example import Example

# Cargar el modelo entrenado
nlp = spacy.load('modelo_chatbot')

# Conjunto de evaluación (datos de prueba)
eval_data = [
    # Preguntas sobre productos, servicios y precios
    ("¿Cuáles son las dimensiones disponibles para la lona marítima?", {"cats": {"product_query": 1, "service_query": 0, "price_query": 0}}),
    ("¿Es resistente al agua y a los rayos UV?", {"cats": {"product_query": 1, "service_query": 0, "price_query": 0}}),
    ("¿Ustedes hacen la instalación?", {"cats": {"product_query": 1, "service_query": 0, "price_query": 0}}),  # Instalación como parte del producto
    ("¿Cuál es la capacidad de peso que soportan los Estribos Hulk?", {"cats": {"product_query": 1, "service_query": 0, "price_query": 0}}),
    ("¿Qué precio tienen los estribos Hulk?", {"cats": {"product_query": 1, "service_query": 0, "price_query": 1}}),
    # Otros ejemplos para prueba
    ("quiero saber sobre un producto", {"cats": {"product_query": 1, "service_query": 0, "price_query": 0}}),
    ("cuáles son sus servicios", {"cats": {"product_query": 0, "service_query": 1, "price_query": 0}}),
    ("¿Cuál es el precio del producto?", {"cats": {"product_query": 0, "service_query": 0, "price_query": 1}}),
    ("Hola, me gustaría información de servicios", {"cats": {"product_query": 0, "service_query": 1, "price_query": 0}}),
    ("Me interesa comprar un servicio", {"cats": {"product_query": 0, "service_query": 1, "price_query": 0}}),
]

# Evaluación
correct = 0
total = len(eval_data)

for text, annotations in eval_data:
    doc = nlp(text)
    predicted_label = max(doc.cats, key=doc.cats.get)  # Obtener la categoría con mayor probabilidad
    true_label = max(annotations['cats'], key=annotations['cats'].get)  # Obtener la categoría esperada

    print(f"Texto: {text}")
    print(f"Predicción: {predicted_label}, Esperado: {true_label}")

    if predicted_label == true_label:
        correct += 1

# Mostrar precisión
accuracy = correct / total
print(f"Precisión del modelo: {accuracy * 100:.2f}%")
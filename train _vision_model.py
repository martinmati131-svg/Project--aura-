import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# ... (Your CNN model definition goes here) ...

# This automatically loads images from the folders we just created
datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)

train_generator = datagen.flow_from_directory(
    'vision_dataset',
    target_size=(64, 64), # Must match the collector resize
    batch_size=32,
    class_mode='categorical',
    subset='training'
)

validation_generator = datagen.flow_from_directory(
    'vision_dataset',
    target_size=(64, 64),
    batch_size=32,
    class_mode='categorical',
    subset='validation'
)

# Train using the generators
model.fit(train_generator, epochs=10, validation_data=validation_generator)
@app.on_event("startup")
def load_resources():
    # ... (other loads) ...
    vision_thread = threading.Thread(target=run_vision_loop, daemon=True)
    vision_thread.start()


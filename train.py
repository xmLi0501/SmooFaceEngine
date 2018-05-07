#!/usr/bin env python

from keras.callbacks import EarlyStopping, ReduceLROnPlateau, CSVLogger, ModelCheckpoint
from model.SmooNet import smooNet_v2 as cnn
from DataGenerator import DataGenerator


input_shape = (64,64,1)
batch_size = 64
generator = DataGenerator(dataset="olivettifaces",
                          path="./data/olivettifaces.jpg",
                          batch_size=batch_size,
                          input_size= input_shape )
num_classes , num_images = generator.get_number()
print(num_classes,num_images)
num_epochs = 100
patience = 100
log_file_path = "./log.cvs"
trained_models_path = "./smooFace"

model = cnn(input_shape,num_classes)
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy'])
model.summary()

# model callbacks
early_stop = EarlyStopping('loss',0.1, patience=patience)
reduce_lr = ReduceLROnPlateau('loss', factor=0.1,
                              patience=int(patience/2), verbose=1)
csv_logger = CSVLogger(log_file_path, append=False)
model_names = trained_models_path + '.{epoch:02d}-{acc:2f}.hdf5'
model_checkpoint = ModelCheckpoint(model_names,
                                   monitor='loss',
                                   verbose=1,
                                   save_best_only=True,
                                   save_weights_only=False)
callbacks = [model_checkpoint, csv_logger, early_stop, reduce_lr]
model.fit_generator(generator=generator.flow(),
                    steps_per_epoch= int(num_images / batch_size) ,
                    epochs=num_epochs,
                    verbose=1,
                    callbacks=callbacks)




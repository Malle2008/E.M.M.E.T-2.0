import input_getters.image_processing_unit as ipu
import input_getters.sensor_processing_unit as spu
from pid import PID 


image = ipu.capture_image()
ipu.to_grayscale(image, 0.4)
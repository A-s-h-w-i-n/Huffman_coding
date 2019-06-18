Python script to compress input data using Huffman encoding technique.
The input can be a string or list of objects.
Here the encoding and decoding processes are carried out in the same script.
If the user wants to perform these operations in two different scripts, the 
encoded text AND the code dictionary can be saved in file (at transmitter), to be read from 
during the decoding process (at receiver)

Huffman_coding_images.py has been modified to work on images. The coded o/p has to 
#be reshaped into a matrix and converted to decimal form before saving. 
#Otherwise size of the saved file exceeds the size of the original image.
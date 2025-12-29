from PIL import Image
import numpy as np

DELIMITER = "#####"

def encode_image(image, secret_message):
    """
    Vectorized Encoding: Bohat fast, bina loops ke bits embed karta hai.
    """
    secret_message += DELIMITER
    # Message ko binary bits (0 aur 1) ke array mein convert karein
    binary_message = np.unpackbits(np.frombuffer(secret_message.encode(), dtype=np.uint8))
    data_len = len(binary_message)
    
    img_array = np.array(image)
    shape = img_array.shape
    flat_img = img_array.flatten()
    
    if data_len > len(flat_img):
        raise ValueError("Message too long!")

    # Vectorized operation: 
    # Saare pixels ke LSB ko ek saath 0 karo, phir bits add karo
    flat_img[:data_len] = (flat_img[:data_len] & 254) | binary_message
        
    return Image.fromarray(flat_img.reshape(shape).astype('uint8'))

def decode_image(image):
    """
    Fast Decoding: 100-1000 pixels ke chunks mein process karta hai.
    """
    img_array = np.array(image)
    flat_img = img_array.flatten()
    
    # Delimiter bits ko search karne ke liye byte-by-byte extract karein
    decoded_chars = []
    chunk_size = 1000  # Ek baar mein 1000 characters process karein
    
    for i in range(0, len(flat_img), chunk_size * 8):
        # Ek chunk pixels se LSBs nikaalein
        chunk_pixels = flat_img[i : i + chunk_size * 8]
        if len(chunk_pixels) < 8: break
        
        # Bits ko bytes mein convert karein (Vectorized)
        bits = (chunk_pixels & 1).reshape(-1, 8)
        bytes_data = np.packbits(bits)
        
        # Bytes ko string mein convert karke delimiter check karein
        current_text = bytes_data.tobytes().decode('ascii', errors='ignore')
        decoded_chars.append(current_text)
        
        full_message = "".join(decoded_chars)
        if DELIMITER in full_message:
            return full_message.split(DELIMITER)[0]
            
    return "No hidden message found."
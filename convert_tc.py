def transform_percent_to_hash(input_file, output_file):
    try:
        with open(input_file, 'r') as f:
            text = f.read()
        
        transformed_text = text.replace('%', '#')
        
        with open(output_file, 'w') as f:
            f.write(transformed_text)
        
        print("Transformation successful. Check", output_file)
    
    except FileNotFoundError:
        print("Error: File not found.")

# Example usage:
# Provide the input and output filenames as arguments to the function
input_file = "/Users/khuenguyen/Desktop/CO3061-Pacman/bigMaze.txt"
output_file = "/Users/khuenguyen/Desktop/CO3061-Pacman/bigMaze.txt"
transform_percent_to_hash(input_file, output_file)
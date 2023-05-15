import tkinter as tk
import numpy as np

root = tk.Tk()
root.title("Grid GUI")

# Calculate the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate the position for centering the GUI
x = (screen_width - 800) // 2
y = (screen_height - 600) // 2

# Set the window position and size
root.geometry(f"800x600+{x}+{y}")

def copy_to_cache(col = 'minor'):
    grid_text = input_text.get("1.0", "end-1c")
    rows = grid_text.split('\n')
    ndecimal = decimal_places.get()
    cache_content = ""
    
    clear_display(); num_array = []

    for irow, row in enumerate(rows):
        numbers = row.split('|')
        converted_numbers = []
        for i, number in enumerate(numbers):
            number = number.strip()
            
            if number and float(number) != 0:
                convert_num = number
                if ndecimal > 0:
                    convert_num = float(convert_num) * 10 ** (-ndecimal)
                    convert_num = "{:.{}f}".format(convert_num, ndecimal)

                converted_numbers.append(convert_num)
                
            elif number and number == '0':
                converted_numbers.append(number)
            
        if len(converted_numbers) != 0:
            num_array.append(converted_numbers)

    display_text(num_array[0][0], 20, 0)
    num_array = np.array(num_array).T

    if col == 'minor':
        datacols = num_array[:2, :].T
        datacols = list(datacols.flatten())
        datacols = [num for num in datacols if num != '0']
    else:
        datacols = num_array[2:, :].T
        datacols = list(datacols.flatten())
        datacols = [num for num in datacols if num != '0']
        
    cache_content += '; '.join(datacols)
        
    # Copy the cache content to the clipboard
    root.clipboard_clear()                # Clear the clipboard
    root.clipboard_append(cache_content)  # Append the cache content
    display_text(f'Copied {col} values to clipboard!!', 12, 1)
    
def on_decimal_select():
    copy_to_cache()

def clear_grid():
    input_text.delete("1.0", "end")
    clear_display()
    decimal_places.set(-1)  # Reset the selected Radiobutton

def clear_display():
    for widget in display_frame.winfo_children():
        widget.destroy()

def display_text(text, fsize, row = 0):
    label = tk.Label(display_frame, text=text, fg="white", bg="gray", font=("Times New Roman", fsize))
    label.grid(row=row, column=0, padx=10, pady=5, sticky="nsew")

def copy_major():
    copy_to_cache(col = 'major')

# Create decimal radiobuttons
decimal_places = tk.IntVar(value=-1)
decimal_options = []

decimal_frame = tk.LabelFrame(root)
decimal_frame.pack(pady=20)

declabel = tk.Label(decimal_frame, text = 'Select the Decimal Point place', font=("Times New Roman", 16))
declabel.pack(pady=10)

nDecimals = 5
for i in range(nDecimals + 1):
    decimal_option = tk.Radiobutton(decimal_frame, text=f"{i}", variable=decimal_places, value=i, command=on_decimal_select)
    decimal_option.pack(side=tk.LEFT, padx=5)
    decimal_options.append(decimal_option)

# Create screen
display_frame  = tk.LabelFrame(root, width=screen_width // 5, height=screen_height // 10, bg="gray")
display_frame.pack(padx=20, pady=20)

# Configure display_frame
display_frame.grid_propagate(0)
display_frame.grid_rowconfigure(0, weight=1)
display_frame.grid_columnconfigure(0, weight=1)

# Create input box
input_text = tk.Text(root, height = screen_height // 100, width = screen_width // 40)
input_text.pack(pady=20)

button_frame = tk.Frame(root)
button_frame.pack()

label_major = tk.Label(button_frame, text="Major:", font=("Times New Roman", 12))
label_major.grid(row=0, column=0)

major_button = tk.Button(button_frame, text="Copy", font=("Times New Roman", 12), command=copy_major, width=8, height=1)
major_button.grid(row=0, column=3)

label_minor = tk.Label(button_frame, text="Minor:", font=("Times New Roman", 12))
label_minor.grid(row=1, column=0, padx=10, pady=20)

minor_button = tk.Button(button_frame, text="Copy", font=("Times New Roman", 12), command=copy_to_cache, width=8, height=1)
minor_button.grid(row=1, column=3, pady=20)

clear_button = tk.Button(button_frame, text="Clear", font=("Times New Roman", 12), command=clear_grid, width=32, height=1)
clear_button.grid(row=2, column=1, columnspan=2, pady=5)

root.mainloop()

import webbrowser
import re


def print_colored(text, color='white'):
    colors = {
        'black': '\033[30m',
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m',
        'reset': '\033[0m'
    }
    print(f"{colors[color]}")
    print(text)
    print(f"{colors['reset']}")



# TODO: Complete this function, let the AI create short videos using the transcription 
# def timeline_cut(output_dir, transcription, video_path):
#     video = VideoFileClip(video_path)
#     timeline_file_path = f"{output_dir}/timeline.txt"

#     if not os.path.exists(timeline_file_path):
#         print_colored("Generating timeline because it does not exist...", "green")
#         timeline = split_text(transcription, ".")
#         with open(timeline_file_path, "w", encoding="utf-8") as text_file:
#             for line in timeline:
#                 text_file.write(f"{line}\n")

#     print_colored("Cutting video based on the timeline...", "green")
#     with open(timeline_file_path, "r", encoding="utf-8") as text_file:
#         timeline = text_file.readlines()
#         previous_time = "00:00:00"
#         for index, line in enumerate(timeline):
#             try:
#                 short_start, short_title = split_text(line.strip(), "-")
#                 short_clip = video.subclip(previous_time, "00:" + short_start.strip())
#                 output_video_path = f"{output_dir}/{short_title.strip()}.mp4"
#                 short_clip.write_videofile(output_video_path)

#                 print_colored(f"Segment '{short_title.strip()}' saved.", "blue")
#                 previous_time = short_start

#             except ValueError:
#                 print_colored(f"Error processing line {index+1}: {line}", "red")

#         # Handle last segment
#         if previous_time != video.duration:
#             last_segment = video.subclip(previous_time, video.duration)
#             last_segment_path = f"{output_dir}/End_of_video.mp4"
#             last_segment.write_videofile(last_segment_path)
#             print_colored("Last segment saved.", "blue")




def open_email(recipient, subject, body):
    # Formatear la URL mailto
    mailto_url = f"mailto:{recipient}?subject={subject}&body={body}"
    
    # Abrir el cliente de correo predeterminado con la URL mailto
    webbrowser.open(mailto_url)





def extract_python_code(text):
    # Regular expression to find content inside <python> tags
    pattern = re.compile(r'<python>(.*?)</python>', re.DOTALL)
    
    # Find all matches
    matches = pattern.findall(text)
    
    # Remove the <python> content from the original text
    cleaned_text = pattern.sub('', text)
    
    # Join all matches to form the executable part
    executable_code = '\n'.join(matches)
    
    return executable_code, cleaned_text



def execute_python_code(code):
    try:
        exec(code)
    except Exception as e:
        print(f"An error occurred: {e}")


# Function to execute code with access to external functions
def execute_python_code_with_external_functions(code):
    try:
        exec(code, globals())
    except Exception as e:
        print(f"An error occurred: {e}")
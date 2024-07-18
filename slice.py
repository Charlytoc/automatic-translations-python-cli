
# slice.py
import os
from moviepy.editor import VideoFileClip, concatenate_videoclips

def slice_video(video_path, slices, output_dir, video_name):
    """
    Slices the video into subclips based on the provided start and end times and saves them as separate files.
    
    :param video_path: Path to the video file
    :param slices: List of tuples containing start and end times in milliseconds
    :param output_dir: Directory to save the sliced videos
    :param video_name: Base name of the video files
    """
    video = VideoFileClip(video_path)
    
    for start_ms, end_ms in slices:
        subclip = video.subclip(start_ms/1000, end_ms/1000)
        sliced_video_path = f'{output_dir}/{video_name}_{start_ms}_{end_ms}.mp4'
        subclip.write_videofile(sliced_video_path)

if __name__ == "__main__":
    # Example usage:
    video_files = [f for f in os.listdir('./videos') if f != '.gitkeep']
    
    # Display the list of available videos for the user to choose from
    print('📽️ Available videos:')
    for index, file in enumerate(video_files):
        print(f'{index + 1}: {file}')
    
    selected_index = int(input('Enter the number of the video you want to process: ')) - 1
    video_path = f'./videos/{video_files[selected_index]}'
    video_name = video_files[selected_index].split('.')[0]
    output_dir = f'output/{video_name}'
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    
    # Define your slices here. Example: [(0, 1000), (2000, 3000)]
    SLICES = [(0, 3000), (2000, 10000)]
    
    slice_video(video_path, SLICES, output_dir, video_name)

from os import system, getcwd
from subprocess import check_output
from os.path import basename, isabs, isfile
from pathlib import Path
import argparse

def check_time_length(time):
    # metto 00: per avere fomrmato hh:mm:ss
    if len(time) == 5:
        time = '00:' + time
    return time

def cut_video(video_path, video_timestamp, folder_path_cutted_video):
    ext_file = basename(video_path).split('.')[1]
    video_title = basename(video_path).split('.')[0]

    f_timestamps = open(video_timestamp, 'r')

    timestamps = f_timestamps.readlines()

    for i in range(len(timestamps)):
        data = timestamps[i].split(';')
        if i < len(timestamps)-1:
            timestamps[i] = {
                'title':    f'{(i+1):02}_{data[1].strip().replace(" ", "_")}.{ext_file}',
                'start':    check_time_length(data[0]),
                'end':      check_time_length(timestamps[i+1].split(';')[0])      
            }
        else:
            timestamps[i] = {
                'title':    f'{(i+1):02}_{data[1].strip().replace(" ", "_")}.{ext_file}',
                'start':    check_time_length(data[0]),
                'end':      check_time_length(check_output(f"ffmpeg -i {video_path} 2>&1 | grep Duration | cut -d ' ' -f 4 | sed s/,//", shell=True).decode("utf-8").strip().split('.')[0])
            }
        print(timestamps[i])
        system(f'ffmpeg -ss {timestamps[i]["start"]} -i {video_path} -to {timestamps[i]["end"]} -c copy -copyts {folder_path_cutted_video}/{timestamps[i]["title"]}')

def main():
    parser = argparse.ArgumentParser(description="Video timestamp cutter")
    parser.add_argument('path', type=str, help="Video path")
    parser.add_argument('timestamp', type=str, help="Video timestamp")

    args = parser.parse_args()

    if not isabs(args.path):
        video_path = f'{getcwd()}/{args.path}'
    else:
        video_path = args.path

    if not isabs(args.timestamp):
        video_timestamp = f'{getcwd()}/{args.timestamp}'
    else:
        video_timestamp = args.timestamp
    
    if isfile(video_path):
        folder_path_cutted_video = f'{getcwd()}/{basename(video_path).split(".")[0].replace(" ", "")}'
        Path(folder_path_cutted_video).mkdir(parents=True, exist_ok=True)
    else:
        print('ERROR: File not found')
        exit
    
    if not isfile(video_timestamp):
        exit
    
    print(video_path)
    print(video_timestamp)
    print(folder_path_cutted_video)

    cut_video(video_path.replace(' ', '\ '), video_timestamp, folder_path_cutted_video)

if __name__ == "__main__":
    main()
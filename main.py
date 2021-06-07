import os
import music_tag
from mutagen.flac import FLAC
from pydub import AudioSegment


def colored(r, g, b, text):
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)


os.system("clear")

source_path = input("Enter the source path(where all flac files exist):")

print()

destination_path = input(
    "Enter the destination path(where all converted mp3 go): ")

print()

bitrate = input(
    "Default Bitrate is 320kbps, press enter to continue or enter a value (like 120k or 196k)\n:"
)

if bitrate == "":
    bitrate = "320k"

# source_path = "/home/rohan/Music/Songs/"
# destination_path = "/home/rohan/Music/mp3/"

source = os.listdir(source_path)
# source = source[:2]
for i in range(len(source)):
    file = source[i]
    file_path = source_path + file
    mp3_file_name = destination_path + file[:-5] + ".mp3"

    if file_path[-5:] == ".flac" and not os.path.exists(mp3_file_name):

        flac_file = AudioSegment.from_file(file_path)
        flac = FLAC(file_path)

        # get tags from flac
        title = flac.get("TITLE")
        album = flac.get("ALBUM")
        artist = flac.get("ARTIST")

        # check if they're none
        if title != None:
            title = title[0]
        else:
            title = ""

        if album != None:
            album = album[0]
        else:
            album = ""

        if artist != None:
            artist = artist[0]
        else:
            artist = ""

        print(
            colored(
                255, 255, 0,
                "{}/{}     Processing: {}".format(i + 1, len(source), title)))

        flac_file.export(mp3_file_name, format="mp3", bitrate=bitrate)

        mp3_file = music_tag.load_file(mp3_file_name)
        mp3_file['title'] = title
        mp3_file['album'] = album
        mp3_file['artist'] = artist
        mp3_file.save()

        print(colored(0, 255, 0, "Converted: {}".format(title)))
    else:
        if file_path[-5:] != ".flac":
            print(
                colored(
                    255, 0, 0,
                    "{}/{}     Not a flac file: {}, skipping it.".format(
                        i + 1, len(source), file_path)))
        else:
            print(
                colored(
                    255, 125, 0,
                    "{}/{}     MP3 file already exists, skipping it.".format(
                        i + 1, len(source))))

print()
print()
print(colored(0, 255, 0, "*** Program finished with no errors. ***"))
print()

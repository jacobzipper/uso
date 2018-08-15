import ffmpeg
import shutil
import errno
import glob
import os
import random
import sys

# TEMPORARY FOR TESTING
PATH_TO_BEATMAP_FOLDER = "/home/zipper/.wine32/drive_c/Program Files/osu!/Songs/258121 Yooh - Shanghai Kouchakan ~ Chinese Tea Orchid Remix"

def copy(src, dest):
    try:
        shutil.copytree(src, dest)
    except OSError as e:
        # If the error was caused because the source wasn't a directory
        if e.errno == errno.ENOTDIR:
            shutil.copy(src, dest)
        else:
            print('Directory not copied. Error: %s' % e)

if __name__ == '__main__':
    NEW_FOLDER = PATH_TO_BEATMAP_FOLDER + " - REVERSED BY USO"
    if os.path.isdir(NEW_FOLDER):
        print "ALREADY REVERSED BY USO DELETE THE FOLDER " + NEW_FOLDER
        sys.exit(0)
    copy(PATH_TO_BEATMAP_FOLDER, NEW_FOLDER)
    mp3s = glob.glob(NEW_FOLDER + "/*.mp3")
    for mp3 in mp3s:
        NEW_MP3 = mp3[:len(mp3) - 4] + " - REVERSED.mp3"
        ffmpeg.input(mp3).filter('areverse').output(NEW_MP3).run()
        os.remove(mp3)
        os.rename(NEW_MP3, mp3)
    osus = glob.glob(NEW_FOLDER + "/*.osu")
    NEW_SET_ID = str(random.randint(1000000,99999999))
    SET_ID = -1
    for osu in osus:
        NEW_OSU = osu[:len(NEW_FOLDER) + 1] + "REVERSED BY USO - " + osu[len(NEW_FOLDER) + 1:]
        NEW_ID = str(random.randint(1000000,99999999))
        tx = open(osu).read().split("\n")
        BEATMAP_ID = -1
        TITLE = -1
        HIT_IND = -1
        HIT_OBJS = []
        count = 0
        for line in tx:
            if "BeatmapID" in line:
                BEATMAP_ID = line.split(":")[1]
            elif "BeatmapSetID" in line:
                SET_ID = line.split(":")[1]
            elif "Title:" in line:
                TITLE = line.split(":")[1]
            elif "[HitObjects]" in line:
                HIT_IND = count
            elif HIT_IND != -1:
                HIT_OBJS.append(line)
            count += 1
        tx = tx[:HIT_IND + 1] + HIT_OBJS[::-1]
        tx = '\n'.join(tx)
        tx = tx.replace(SET_ID, NEW_SET_ID).replace(BEATMAP_ID, NEW_ID).replace(TITLE, "REVERSED BY USO - " + TITLE)
        open(NEW_OSU, 'w').write(tx)
        os.remove(osu)

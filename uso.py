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
def rearrangeTimingPoints(TIMING_OBJS):
    for i in xrange(len(TIMING_OBJS) - 1):
        break
        # TODO REARRANGE TIMING POINTS
def rearrangeHitObjs(HIT_OBJS):
    HIT_OBJS = HIT_OBJS[::-1]
    TOTAL_TIME = 0
    longLast = int(HIT_OBJS[0].split(",")[-1].split(":")[0])
    shortLast = int(HIT_OBJS[0].split(",")[2])
    if longLast > shortLast:
        TOTAL_TIME = longLast
    else:
        TOTAL_TIME = shortLast
    for i in xrange(len(HIT_OBJS)):
        cur = HIT_OBJS[i].split(",")
        startTime = int(cur[2])
        endTime = int(cur[-1].split(":")[0])
        if endTime > startTime:
            cur[2] = str(TOTAL_TIME - endTime)
            cur[-1] = cur[-1].replace(str(endTime), str(TOTAL_TIME - startTime))
        else:
            cur[2] = str(TOTAL_TIME - startTime)
        HIT_OBJS[i] = ','.join(cur)
    return HIT_OBJS

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
        TIMING_IND = -1
        TIMING_OBJS = []
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
            elif "[TimingPoints]" in line:
                TIMING_IND = count
            elif "[HitObjects]" in line:
                HIT_IND = count
            elif TIMING_IND != -1 and HIT_IND == -1 and line != "":
                TIMING_OBJS.append(line)
            elif HIT_IND != -1 and line != "":
                HIT_OBJS.append(line)
            count += 1
        rearrangeTimingPoints(TIMING_OBJS)
        HIT_OBJS = rearrangeHitObjs(HIT_OBJS)
        tx = tx[:TIMING_IND + 1] + TIMING_OBJS[::-1] + ['', '[HitObjects]'] + HIT_OBJS
        tx = '\n'.join(tx)
        tx = tx.replace(SET_ID, NEW_SET_ID).replace(BEATMAP_ID, NEW_ID).replace(TITLE, "REVERSED BY USO - " + TITLE)
        open(NEW_OSU, 'w').write(tx)
        os.remove(osu)

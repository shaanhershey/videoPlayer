f = open(f'videoPlayer/data/player/functions/play.mcfunction', "w")
for i in range(1,35):
    f.write(f"schedule function videoPlayer:player/frame{i} {10*i}t\n")
f.close()
import argparse

from .net.kugou_api import KugouCloud
from .net.netease_api import NetEaseCloud
from .net.oneting_api import OneCloud
from .net.qq_api import QQMusic
from .net.xiami_api import XiaMiCloud
from .utils.downloader import download_from_url, super_download

desc="Search && Download Music cli"
version_info="""
 ______     _____     __    __     __  __     ______     __     ______    
/\  ___\   /\  __-.  /\ "-./  \   /\ \/\ \   /\  ___\   /\ \   /\  ___\   
\ \___  \  \ \ \/\ \ \ \ \-./\ \  \ \ \_\ \  \ \___  \  \ \ \  \ \ \____  
 \/\_____\  \ \____-  \ \_\ \ \_\  \ \_____\  \/\_____\  \ \_\  \ \_____\ 
  \/_____/   \/____/   \/_/  \/_/   \/_____/   \/_____/   \/_/   \/_____/
  
Search && Download Music Cli
version 0.02a 
"""

def w_lrc(output,music_name,lrc):
    with open(output + music_name + ".lrc", "w") as f:
        f.write(lrc)


def search_or_download(music_name,offset,platfrom='netease',choose=True,index=1,output='./',lyric=False,album=False):
    if platfrom == 'netease':
        net_api=NetEaseCloud()
        if choose:
            net_api.show_music_info(music_name,offset)
        else:
            mIds = net_api.get_music_ids(music_name, offset)
            id = mIds[index]
            if album:
                music_info=net_api.get_music_download_info(id)
                super_download(music_info,output)
            else:
                neturl=net_api.get_music_url(id)
                download_from_url(neturl,output+music_name+'.mp3')
            if lyric:
                lry=net_api.get_music_lyric(id)
                w_lrc(output,music_name,lry)
    elif platfrom == 'qq':
        qq_api=QQMusic()
        if choose:
            qq_api.show_music_infos(music_name,offset)
        else:
            if album:
                music_info=qq_api.get_music_url_and_info(music_name,index,offset)
                super_download(music_info,output,".m4a")
            else:
                qqurl=qq_api.get_music_url(music_name,index,offset)
                download_from_url(qqurl,output+music_name+'.m4a')
            if lyric:
                lrc = qq_api.get_music_lyric()
                w_lrc(output, music_name, lrc)
        pass
    elif platfrom == '1ting':
        oneting_api=OneCloud()
        if choose:
            oneting_api.show_music_infos(music_name,offset)
        else:
            if album:
                music_info=oneting_api.get_music_url_and_info(music_name,offset,index)
                super_download(music_info,output)
            else:
                onetingurl=oneting_api.get_music_url(music_name,offset,index)
                download_from_url(onetingurl,output+music_name+'.mp3')
        pass
    elif platfrom == 'xiami':
        xiami_api=XiaMiCloud()
        if choose:
            xiami_api.show_music_infos(music_name,offset)
        else:
            if album:
                music_info=xiami_api.get_music_url_and_info(music_name,offset,index)
                super_download(music_info,output)
            else:
                url=xiami_api.get_music_url(music_name,offset,index)
                download_from_url(url,output+music_name+'.mp3')
            if lyric:
                download_from_url(xiami_api.get_music_lrc_url(),output+music_name+'.trc')
        pass
    elif platfrom == 'kugou':
        kugou_api=KugouCloud()
        if choose:
            kugou_api.show_music_infos(music_name,offset)
        else:
            if album:
                music_info=kugou_api.get_music_url_and_info(music_name,offset,index)
                super_download(music_info,output)
            else:
                url=kugou_api.get_music_url(music_name,offset,index)
                download_from_url(url,output+music_name+'.mp3')
            if lyric:
                lrc=kugou_api.get_music_lyric()
                w_lrc(output, music_name, lrc)
        pass


def main():
    music_platform = ['netease', 'qq', '1ting', 'xiami', 'kugou']
    parse = argparse.ArgumentParser(description=desc)
    parseGroup = parse.add_argument_group()
    parseGroup.add_argument("-s", "--search", action="store_true", help="search mode")
    parseGroup.add_argument("-d", "--download", action="store_true", help="download mode")
    parse.add_argument("-v", "--version", action="store_true", help="print product version")
    parse.add_argument("-a", "--album", action="store_true",help="include music album info")
    parse.add_argument("-l", "--lyric", action="store_true", help="download with lyric")
    parse.add_argument("-n", "--name", type=str, help="input music name")
    parse.add_argument("-i", "--index", type=int, default=0, help="index for download music")
    parse.add_argument("-p", "--platform", type=str, choices=music_platform, default="netease",
                       help="platform you want to download include:qq,1ting,xiammi,kugou")
    parse.add_argument("-o", "--output", type=str, default="./", help="path you music")
    parse.add_argument("-g", "--page", type=int, default=1, help="the page you want to change")
    args = parse.parse_args()

    name = args.name
    platform = args.platform
    offset = args.page
    index = args.index
    output = args.output
    if args.version:
        print(version_info)
    if args.search:
        print("search\tMusicName:" + args.name + "\tPlatform:" + args.platform)
        search_or_download(name, offset, platform)
    elif args.download:
        search_or_download(name, offset, platform, False, index - 1, output,args.lyric,args.album)


if __name__=="__main__":
    main()

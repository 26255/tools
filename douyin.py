#
# https://v26-web.douyinvod.com/2884ade3dfdd78c6c1d5b235b5421f45/69d78f6e/video/
# dy 单条视频下载
#
import requests

url = "https://v26-web.douyinvod.com/2884ade3dfdd78c6c1d5b235b5421f45/69d78f6e/video/tos/cn/tos-cn-ve-15c000-ce/oEIKEQJB74uFAoDTeFiLfmDqDA0BeEGg86c7Cd/?a=6383&ch=26&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=1644&bt=1644&cs=0&ds=3&ft=AJkeU_TLRR0s~0C3TDW2Nc.xBiGNbLqA~~-U_4RqvtVJNv7TGW&mime_type=video_mp4&qs=1&rc=NmU8N2k6ZmU6OTc6PDdpN0Bpajl1ZHQ5cjpoOTMzbGkzNEAyMmFiNjQuXy0xLzYwMDQzYSMuaWljMmRrLTJhLS1kLWJzcw%3D%3D&btag=c0000e00018000&cquery=100w_100B_100x_100z_100o&dy_q=1775723808&feature_id=0ea98fd3bdc3c6c14a3d0804cc272721&l=20260409163648030BD606EC48B1A6AF30&__vid=7605141148970128741"

headers = {
    'Referer': 'https://www.douyin.com/'
}

res = requests.get(url=url,headers=headers).content

# print(res)
with open('gm.mp4','wb')as f:
    f.write(res)
    print("下载完成")



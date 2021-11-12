from pixiv import Multithreading_Author_all_works
from pixiv import Multithreading_pixiv_date_r18
from pixiv import Multithreading_Pixiv_Leaderboard
from pixiv import Multithreading_pixiv_Search_map
from pixiv import Multithreading_pixiv_today_r18
from pixiv import Multithreading_pixiv_today_Rank


print('\033[2;32m1:Author_all_works\n2:date_r18\n3:Leaderboard(运行即下载)\n4:Search_map\n5:today_r18\n6:today_Rank\033[0m')
while True:
    try:
        a = int(input('请选择:'))
        if a == 1:
            Auther_all_work = Multithreading_Author_all_works.Author_All_Works()
        elif a == 2:
            date_r18 = Multithreading_pixiv_date_r18.pixiv_date_r18()
        elif a == 3:
            Leaderboard = Multithreading_Pixiv_Leaderboard.Leaderboard()
        elif a == 4:
            Search_map = Multithreading_pixiv_Search_map.Search_map()
        elif a == 5:
            today_r18 = Multithreading_pixiv_today_r18.today_r18()
        elif a == 6:
            today_Rank = Multithreading_pixiv_today_Rank.pixiv()
        elif a == '退出':
            exit()
        else:
            print('?')
    except ValueError:
        print('要是数字呢' + '(* - *)')
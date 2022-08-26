

from datetime import datetime, date, timedelta

today = date.today()
# d3 = today.strftime("%m/%d/%y")
# print("d3 =", d3)
print("1", today)

today = datetime.now()
print("2", today)
yesterday = date.today() - timedelta(days=1)
print('3',yesterday)
# print(date.today())

print(timedelta(days=0))
# print(yesterday)\

page_posts =[{'Date Posted': '2022-07-31 15:03:00', 'Post Link': 'https://www.facebook.com/tindoichung.official/posts/pfbid0FAFKkdw47u35Eub1ARx7oMr8jcbJXEL99hPBURLq9A2zdwkP8jZqeLvh3swmYPqWl', 'Post Text': 'Vì sao Đức từ chối cấp visa vào hộ chiếu mẫu mới của Việt Nam?'}, {'Date Posted': '2022-07-31 14:52:00', 'Post Link': 'https://www.facebook.com/tindoichung.official/posts/pfbid0JH6jgFmqVzACKcnWRBKqqdXY6HDoDSFPiT6g3piJouiKL48YfQe4ZFJWVpzp4Mwjl', 'Post Text': 'Truyền thông Trung Quốc nêu khả năng lập vùng cấm bay để ngăn Chủ tịch Hạ viện Mỹ thăm Đài Loan'}, {'Date Posted': '2022-07-31 14:40:00', 'Post Link': 'https://www.facebook.com/tindoichung.official/posts/pfbid0DbVceDkLeDErfdcC1hYtGotxEn3E2i6i4Wut88HrkQBE7n1XUwVBpYoGfk6jBRz4l', 'Post Text': 'Bắc Bộ chuẩn bị đón mưa dông diện rộng'}, {'Date Posted': '2022-07-31 14:40:00', 'Post Link': 'https://www.facebook.com/tindoichung.official/posts/pfbid0m7nEB5mNUjjGahuNyZ8P3o2VbJY3mHxj2TGWExEpooLCtqZKoEWBhzxFZnVZ6rzel', 'Post Text': 'Cảnh báo ma túy núp bóng thực phẩm chức năng và đồ uống'}, {'Date Posted': '2022-07-31 11:41:00', 'Post Link': 'https://www.facebook.com/tindoichung.official/posts/pfbid035eQawM6e3NcehhetXecQjSazAcEph2YLfgJNeuAsHRSRKa4d2nstc327ygwcLEGhl', 'Post Text': 'Đội tuyển cầu mây nữ Việt Nam vô địch thế giới'}, {'Date Posted': '2022-07-31 10:41:00', 'Post Link': 'https://www.facebook.com/tindoichung.official/posts/pfbid08ZaLQVLm7N8xPRj2Ny7vbw1ceU6u84Ddnf4EDKPjX8P4FmnXPPKLvFczkCDXsQhQl', 'Post Text': 'Kỷ niệm 10 năm quan hệ Đối tác chiến lược toàn diện Việt-Nga:'}, {'Date Posted': '2022-07-31 08:41:00', 'Post Link': 'https://www.facebook.com/tindoichung.official/posts/pfbid0LsvGmNhhR9Da2hRuEFcA6CpauqiLBgpF8rQkSwiwpM2YwUVNXJsCtKPXFcdpSKDCl', 'Post Text': 'Gỡ khó cho dự án Metro ở Thành phố Hồ Chí Minh'}, {'Date Posted': '2022-07-31 08:41:00', 'Post Link': 'https://www.facebook.com/tindoichung.official/posts/pfbid02pz6az96HvGovaUP1g2Q1Mehwguwka6zK86RRBVYuBchY8PCzhRWSpf5yCkseDzWul', 'Post Text': 'Nguyên nhân máy bay Vietnam Airlines hạ cánh khẩn cấp tại sân bay Đà Nẵng'}, {'Date Posted': '2022-08-03 14:55:00', 'Post Link': 'https://www.facebook.com/tindoichung.official/posts/pfbid02jPCP9Ckn1xMSq1ntj96TdwJsq2nKyEs7KRYbVWaHj5QtbhpKiuHei9kJ8bpV2mZkl', 'Post Text': 'Số mắc cúm tăng nhanh, không tự ý mua thuốc điều trị, đặc biệt là Tamiflu'}, {'Date Posted': '2022-08-03 14:19:00', 'Post Link': 'https://www.facebook.com/tindoichung.official/posts/pfbid025DwnfAwHX6SKyz97ZCfryySQ5XmsZn3aPn7vEcyV4MjxGFbyu9jeCjUGLfhsaYL6l', 'Post Text': 'Bộ Chính trị: Dừng thí điểm mô hình chủ nhiệm ủy ban kiểm tra kiêm thanh tra'}, {'Date Posted': '2022-08-03 14:14:00', 'Post Link': 'https://www.facebook.com/tindoichung.official/posts/pfbid02fEcApj5GpT5Ej5DycZfz2zGeAEGUr5JK4LMMhP7uNroVCQa7DNpnx5VjUbmDe1K3l', 'Post Text': 'Việt Nam hơn 4000 năm văn hiến'}, {'Date Posted': '2022-08-03 10:25:00', 'Post Link': 'https://www.facebook.com/tindoichung.official/posts/pfbid02mqPVZ5RLkmGpTk64r7hMNGcfhJJuaobyhMX7hLx492xzoRmJZj9j5AnoQpXRfLkml', 'Post Text': 'Những chàng trai trẻ phục dựng miễn phí hàng trăm bức ảnh liệt sĩ'}, {'Date Posted': '2022-08-03 08:51:00', 'Post Link': 'https://www.facebook.com/tindoichung.official/posts/pfbid02bxoMWVLyKHb4yv9e8hrWm5fbzuKhwWfVakbe4GkhUtgzeTcvujTbxvwsrA1pWx5vl', 'Post Text': 'Ngày 26/7: Có 1.460 ca Covid-19 mới, 7.107 F0 khỏi bệnh'}, {'Date Posted': '2022-08-03 08:50:00', 'Post Link': 'https://www.facebook.com/tindoichung.official/posts/pfbid02dG3cG8MgxmkmmnTh4GKnj2yL29AHdrrBsb9pCemjcoPwF82fGmqgd5ZTWyjSAceDl', 'Post Text': 'Tháng 7 - Tháng tưởng nhớ và tri ân '}]
# print(page_posts[5])


page_posts_crawl = []
for i in range(len(page_posts)):
    date_time_obj = datetime.strptime(str(page_posts[i]["Date Posted"]), '%Y-%m-%d %H:%M:%S')
    print('4',date_time_obj)

    if date_time_obj.day==(int(yesterday.day)):
        # print('5',date_time_obj)
        # print(page_posts[i])
        page_posts_crawl.append(page_posts[i])

print(page_posts_crawl)
print(len(page_posts_crawl))



# removes =[5,1,3,2]
# sorted_list = sorted(removes, reverse=True)
# print(sorted_list)

# for remove in sorted_list:
#     print(page_posts[remove])


# with open("page_posts.txt", 'r', encoding="utf-8") as csvfile:
#     csvfile=csvfile.read()
#     print(type(csvfile))
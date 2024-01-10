from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import json

# ここにデータを配列として定義
sample_data = [
    {"id": 'admin', "name": "ソフトウェアエンジニアリング","day":"月曜日","time":"9:00","url":"https://moocs.iniad.org/courses/2023/CS118"},
    {"id": 'admin', "name": "データベース","day":"火曜日","time":"10:40","url":"https://moocs.iniad.org/courses/2023/DS106"},
    {"id": 'admin', "name": "情報連携実習3b","day":"火曜日","time":"14:45","url":"https://moocs.iniad.org/courses/2023/CS121"},
    {"id": 'admin', "name": "情報連携基礎演習","day":"水曜日","time":"13:00","url":"https://moocs.iniad.org/courses/2023/CS110"},
    {"id": 'admin', "name": "コンピュータシステム","day":"木曜日","time":"13:00","url":"https://moocs.iniad.org/courses/2023/CS113"},
    {"id": 'admin', "name": "情報連携エンジニアリング演習","day":"金曜日","time":"16:30","url":"https://moocs.iniad.org/courses/2023/CS120"},
    {"id": "litchi", "name": "CS概論","day":"月曜日","time":"9:00","url":"https://moocs.iniad.org/courses/2022/IE111"},
    {"id": "litchi", "name": "コンピュータ・アーキテクチャ","day":"火曜日","time":"10:40","url":"https://moocs.iniad.org/courses/2023/CS102"},
    {"id": "litchi", "name": "ビジネス演習","day":"水曜日","time":"13:00","url":"https://moocs.iniad.org/courses/2022/BI105"},
    {"id": "litchi", "name": "会計論","day":"木曜日","time":"13:00","url":"https://moocs.iniad.org/courses/2022/BK102"},
    {"id": "litchi", "name": "情報連携実習2b","day":"金曜日","time":"16:30","url":"https://moocs.iniad.org/courses/2022/CS109"},
]

# ホームページのビュー
def home(request):
    # ログインユーザー名を取得
    if request.user.is_authenticated:
        username = request.user.username
        print(f"ログインユーザー名: {username}")
    else:
        username = None
        print("ユーザーはログインしていません")

    # ユーザー名に一致する全てのデータを検索
    matching_data = [item for item in sample_data if str(item["id"]) == username]

    # データをテンプレートに渡す
    return render(request, 'authtest/home.html', {'matching_data': matching_data})



# プライベートページのビュー（ログインが必要）
@login_required
def private_page(request):
    username = request.user.username if request.user.is_authenticated else None

    # ユーザー名に一致する授業を抽出
    user_classes = [item for item in sample_data if item["id"] == username]

    # 曜日と時間で授業を整理
    organized_classes = organize_classes_by_day_and_time(user_classes)

    return render(request, 'authtest/private.html', {'organized_classes': organized_classes})


def organize_classes_by_day_and_time(classes):
    organized = {}
    for cls in classes:
        day = cls.get("day")
        if day not in organized:
            organized[day] = []
        organized[day].append(cls)
    for day_classes in organized.values():
        day_classes.sort(key=lambda x: x.get("time"))
    return organized
# パブリックページのビュー
def public_page(request):
    # すべての授業を曜日と時間で整理
    organized_classes = organize_classes_by_day_and_time(sample_data)

    return render(request, 'authtest/public.html', {'organized_classes': organized_classes})


# my_view関数（IDに基づいてデータを返す）
def my_view(request):
    print("リクエストがmy_viewに到達しました")
    # GETリクエストからIDを取得
    requested_id = request.GET.get('id', None)

    # デバッグ用にリクエスト情報をログに出力
    print(f"リクエストされたID: {requested_id}")

    # IDに一致するデータを検索
    matching_data = next((item for item in sample_data if str(item["id"]) == requested_id), None)

    # データをテンプレートに渡す
    return render(request, 'authtest/home.html', {'data': sample_data, 'matching_data': matching_data})

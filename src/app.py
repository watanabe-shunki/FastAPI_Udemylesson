import streamlit as st
import random
import requests
import json
from fastapi import FastAPI
import datetime
import pandas as pd

page = st.sidebar.selectbox("choose your page", ["users", "rooms", "bookings"])

if page == "users":
    st.title("ユーザー登録画面")

    with st.form(key="user"):
        # user_id: int = random.randint(0, 10)
        username: str = st.text_input("ユーザー名", max_chars=12)
        data = {
            "username": username
        }
        submit_button = st.form_submit_button(label="送信")
        
    if submit_button:
        st.write("## 送信データ")
        st.write("## レスポンス結果")
        url = "http://127.0.0.1:8000/users"
        
        res = requests.post(
            url,
            data = json.dumps(data)
        )
        if res.status_code == 200:
            st.success("登録完了しました。")
        st.json(res.json())

elif page == "rooms":
    st.title("APIテスト画面（会議室）")

    with st.form(key="room"):
        room_id: int = random.randint(0, 10)
        room_name: str = st.text_input("会議室名", max_chars=12)
        capacity: int = st.number_input("定員", step=1)
        data = {
            "room_id": room_id,
            "room_name": room_name,
            "capacity": capacity
        }
        submit_button = st.form_submit_button(label="送信")
        
    if submit_button:
        st.write("## 送信データ")
        st.json(data)
        st.write("## レスポンス結果")
        url = "http://127.0.0.1:8000/rooms"
        
        res = requests.post(
            url,
            data = json.dumps(data)
        )
        st.json(res.json())

elif page == "bookings":
    st.title("会議室予約画面")
    # ユーザー一覧を取得
    url_users = "http://127.0.0.1:8000/users"
    res = requests.get(url_users)
    users = res.json()
    user_name = {}
    # ユーザー名をキー、ユーザーIDをバリューとして辞書型に変換
    for user in users:
        user_name[user["username"]] = user["user_id"]
    
    # 会議室一覧を取得
    url_rooms = "http://127.0.0.1:8000/rooms"
    res = requests.get(url_rooms)
    rooms = res.json()
    rooms_name = {}
    for room in rooms:
        rooms_name[room["room_name"]] = {
            "room_id": room["room_id"],
            "capacity": room["capacity"]
        }
        
    st.write("### 会議室一覧")
    df_rooms = pd.DataFrame(rooms)
    df_rooms.columns = ["会議室", "定員", "会議室ID"]
    st.table(df_rooms)

    url_bookings = "http://127.0.0.1:8000/bookings"
    res = requests.get(url_bookings)
    bookings = res.json()
    df_bookings = pd.DataFrame(bookings)    
    
    user_id = {}
    for user in users:
        user_id[user["user_id"]] = user["username"]
        
    room_id = {}
    for room in rooms:
        room_id[room["room_id"]] = {
            "room_name": room["room_name"],
            "capacity": room["capacity"]
        }
    
    # IDを各値に変更する
    to_username = lambda x: user_id[x]
    to_roomname = lambda x: room_id[x]["room_name"]
    to_datetime = lambda x: datetime.datetime.fromisoformat(x).strftime("%y/%m/%d %H:%M")
    
    # 特定の列に適用
    df_bookings["user_id"] = df_bookings["user_id"].map(to_username)
    df_bookings["room_id"] = df_bookings["room_id"].map(to_roomname)
    df_bookings["start_datetime"] = df_bookings["start_datetime"].map(to_datetime)
    df_bookings["end_datetime"] = df_bookings["end_datetime"].map(to_datetime)
    
    df_bookings = df_bookings.rename(columns={
        "user_id": "予約者名",
        "room_id": "会議室名",
        "booked_num": "予約人数",
        "start_datetime": "開始時刻",
        "end_datetime": "終了時刻",
        "booking_id": "予約番号"
    })
    
    st.write("### 予約一覧")
    st.table(df_bookings)
    
    with st.form(key="booking"):
        username: int = st.selectbox("予約者名", user_name.keys())
        roomname: int = st.selectbox("会議室名", rooms_name.keys())
        booked_num: int = st.number_input("予約人数", step=1, min_value=1)
        date = st.date_input("日付入力", min_value="today")
        start_time = st.time_input("開始時刻: ", value=datetime.time(9, 0))
        end_time = st.time_input("終了時刻: ", value=datetime.time(20, 0))
        
        submit_button = st.form_submit_button(label="予約登録")
        
    if submit_button:
        user_id: int = user_name[username]
        room_id: int = rooms_name[roomname]["room_id"]
        capacity: int = rooms_name[roomname]["capacity"]
        
        data = {
            "user_id": user_id,
            "room_id": room_id,
            "booked_num": booked_num,
            "start_datetime": datetime.datetime(
                year=date.year,
                month=date.month,
                day=date.day,
                hour=start_time.hour,
                minute=start_time.minute
            ).isoformat(),
            "end_datetime": datetime.datetime(
                year=date.year,
                month=date.month,
                day=date.day,
                hour=end_time.hour,
                minute=end_time.minute
            ).isoformat()
        }
        # 定員以下の予約人数の場合のみ登録許可
        if booked_num <= capacity:
            url = "http://127.0.0.1:8000/bookings"
            res = requests.post(
                url,
                data = json.dumps(data)
            )
            print(res.status_code)
            print(res.headers.get("Content-Type"))
            print(res.text)   # 実際のレスポンスボディ
            if res.status_code == 200:
                st.success("予約完了しました。")
                st.write(res.status_code)
            st.json(res.json())
        else:
            st.error(f"{roomname}の定員は、{capacity}名です。{capacity}名以下の予約人数を受け付けています")
import streamlit as st
import random

# 1. Cấu hình trang trang giao diện
st.set_page_config(page_title="Hành Trình Khám Phá Hang Quỷ", page_icon="⚔️", layout="centered")

st.title("⚔️ Hành Trình Khám Phá Hang Quỷ")
st.markdown("---")

# 2. Khởi tạo trạng thái nhân vật (Session State)
if "rpg_game" not in st.session_state:
    st.session_state.rpg_game = {
        "player_name": "",
        "class": "",
        "hp": 100,
        "max_hp": 100,
        "attack": 15,
        "gold": 20,
        "location": "start",  # start, crossroad, forest, cave, boss, game_over, victory
        "logs": ["Chào mừng bạn đến với lục địa Streamlit!"],
        "enemy_hp": 0,
        "enemy_name": ""
    }

game = st.session_state.rpg_game

# Hàm tiện ích để ghi lại nhật ký hành trình
def log_message(msg):
    game["logs"].append(msg)

# Hàm reset game
def reset_game():
    st.session_state.rpg_game = {
        "player_name": "",
        "class": "",
        "hp": 100,
        "max_hp": 100,
        "attack": 15,
        "gold": 20,
        "location": "start",
        "logs": ["Hành trình mới bắt đầu!"],
        "enemy_hp": 0,
        "enemy_name": ""
    }
    st.rerun()

# 3. MÀN HÌNH 1: KHỞI TẠO NHÂN VẬT
if game["location"] == "start":
    st.subheader("🧙‍♂️ Tạo nhân vật của bạn")
    name = st.text_input("Nhập tên Dũng Sĩ:", value=game["player_name"])
    char_class = st.selectbox("Chọn Hệ Phái:", ["", "Chiến Binh (Trâu bò)", "Sát Thủ (Tấn công cao)"])
    
    if st.button("Lên Đường Khám Phá! 🚀"):
        if name.strip() == "" or char_class == "":
            st.error("Vui lòng điền tên và chọn Hệ Phái!")
        else:
            game["player_name"] = name
            game["class"] = char_class
            if "Chiến Binh" in char_class:
                game["hp"] = 130
                game["max_hp"] = 130
                game["attack"] = 12
            else:
                game["hp"] = 90
                game["max_hp"] = 90
                game["attack"] = 20
            game["location"] = "crossroad"
            log_message(f"Dũng sĩ **{name}** ({char_class}) đã bước chân vào khu rừng cấm.")
            st.rerun()

# 4. GIAO DIỆN CHÍNH KHI ĐANG CHƠI
else:
    # Hiển thị thanh trạng thái nhân vật ở trên cùng
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("👤 Nhân vật", f"{game['player_name']}")
    with col2:
        st.metric("❤️ Máu (HP)", f"{game['hp']}/{game['max_hp']}")
    with col3:
        st.metric("⚔️ Sức mạnh", f"{game['attack']}")
    with col4:
        st.metric("💰 Vàng", f"{game['gold']}G")
    
    st.markdown("---")

    # XỬ LÝ LOGIC TỪNG ĐỊA ĐIỂM
    # A. Ngã ba đường
    if game["location"] == "crossroad":
        st.subheader("🌲 Bạn đang đứng ở Ngã Ba Cây Cổ Thụ")
        st.write("Phía trước bạn chia làm hai ngả đường u ám. Bạn sẽ đi đâu?")
        
        col_left, col_right = st.columns(2)
        if col_left.button("Đi vào Rừng Rậm sâu thẳm 🌲"):
            game["location"] = "forest"
            log_message("Bạn rẽ trái tiến sâu vào Rừng Rậm.")
            # Bắt gặp quái rừng ngẫu nhiên
            game["enemy_name"] = random.choice(["Yêu Tinh Tinh Nghịch", "Nhện Độc Khổng Lồ"])
            game["enemy_hp"] = 40
            st.rerun()
            
        if col_right.button("Đi thẳng tới Hang Quỷ 🕳️"):
            game["location"] = "cave"
            log_message("Bạn dũng cảm đi thẳng vào Hang Quỷ đầy ám khí.")
            game["enemy_name"] = "Quỷ Lùn Canh Gác"
            game["enemy_hp"] = 60
            st.rerun()

    # B. Màn hình chiến đấu (Áp dụng cho Rừng và Hang Quỷ)
    elif game["location"] in ["forest", "cave"]:
        st.subheader(f"⚔️ Bị tấn công bởi: {game['enemy_name']}!")
        st.warning(f"Máu của {game['enemy_name']}: **{game['enemy_hp']} HP**")
        
        btn_attack, btn_run = st.columns(2)
        
        if btn_attack.button("Tấn Công! ⚔️"):
            # Người chơi đánh quái
            p_dmg = random.randint(game["attack"] - 3, game["attack"] + 5)
            game["enemy_hp"] -= p_dmg
            log_message(f"Bạn chém {game['enemy_name']} gây {p_dmg} sát thương.")
            
            # Quái còn sống thì đánh lại
            if game["enemy_hp"] > 0:
                e_dmg = random.randint(5, 12)
                game["hp"] -= e_dmg
                log_message(f"{game['enemy_name']} cào bạn mất {e_dmg} HP.")
            else:
                # Quái chết
                gold_drop = random.randint(15, 30)
                game["gold"] += gold_drop
                log_message(f"🎉 Bạn hạ gục {game['enemy_name']}! Nhặt được {gold_drop} Vàng.")
                # Chuyển đến hang Boss
                game["location"] = "boss_room"
                game["enemy_name"] = "CHÚA TỂ RỒNG LỬA 🔥"
                game["enemy_hp"] = 120
                
            if game["hp"] <= 0:
                game["location"] = "game_over"
            st.rerun()
            
        if btn_run.button("Bỏ chạy về Ngã Ba 🏃‍♂️"):
            game["location"] = "crossroad"
            log_message("Bạn hốt hoảng tháo chạy về ngã ba đường để giữ mạng.")
            st.rerun()

    # C. Phòng Boss Cuối
    elif game["location"] == "boss_room":
        st.subheader(f"🌋 CĂN PHÒNG CUỐI CÙNG: {game['enemy_name']}!")
        st.error(f"Máu của Boss: **{game['enemy_hp']} HP**")
        
        # Mua bình máu nếu có tiền
        if game["gold"] >= 20:
            if st.button("Mua Hồi Máu (-20 Vàng, +40 HP) 🧪"):
                game["gold"] -= 20
                game["hp"] = min(game["max_hp"], game["hp"] + 40)
                log_message("Bạn uống bình máu, cảm thấy khỏe khoắn hơn!")
                st.rerun()
                
        if st.button("TẤN CÔNG KHÔ MÁU VỚI BOSS! 🔥"):
            p_dmg = random.randint(game["attack"] - 2, game["attack"] + 8)
            game["enemy_hp"] -= p_dmg
            log_message(f"Bạn tung đòn chí mạng vào Rồng Lửa gây {p_dmg} sát thương!")
            
            if game["enemy_hp"] > 0:
                e_dmg = random.randint(12, 25)
                game["hp"] -= e_dmg
                log_message(f"Rồng Lửa phun lửa thiêu cháy bạn mất {e_dmg} HP!")
            else:
                game["location"] = "victory"
                
            if game["hp"] <= 0:
                game["location"] = "game_over"
            st.rerun()

    # D. Thua cuộc
    elif game["location"] == "game_over":
        st.error("💀 BẠN ĐÃ TỬ TRẬN! Hành trình kết thúc tại đây...")
        if st.button("Hồi sinh và Chơi Lại 🔄"):
            reset_game()

    # E. Chiến thắng
    elif game["location"] == "victory":
        st.balloons()
        st.success(f"🏆 CHIẾN THẮNG vang dội! Dũng sĩ {game['player_name']} đã tiêu diệt Rồng Lửa, giải cứu vương quốc!")
        if st.button("Chơi Hành Trình Mới 🔄"):
            reset_game()

    # HIỂN THỊ KHUNG NHẬT KÝ HÀNH TRÌNH (LOGS)
    st.markdown("---")
    st.subheader("📜 Nhật ký hành trình")
    # Hiển thị 5 dòng nhật ký gần nhất
    for log in game["logs"][-5:]:
        st.write(log)

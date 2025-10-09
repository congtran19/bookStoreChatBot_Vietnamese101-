# bookStoreChatBot_Vietnamese101-
Chatbot hỗ trợ bán sách đơn giản 
Em chọn mô hình qwen3 1.7b, đủ nhẹ để chạy trên máy tính cá nhân dù cho không có card đồ họa, sau nay nếu muốn thay đổi mô hình có thể thay trong file config

DEMO SẢN PHẨM(CLI, xem tốc độ 3x sẽ tiết kiệm thời gian của mọi người ạ)
    Link_video: https://youtu.be/gtNtpYMTW6I?si=JLTIM9gsrkf6V26f

Chatbot này dựa trên mô hình mô hình ReAct (Reasoning + Acting) — tức là mỗi phản hồi đều có quá trình suy luận, gọi công cụ thật, và chỉ trả lời khi có dữ liệu thực tế.

Mục tiêu của em là tạo ra một chatbot có khả năng tư duy nhiều bước (multi-step reasoning), hạn chế việc “bịa” thông tin, và có thể dễ dàng mở rộng cho các lĩnh vực khác như giáo dục hay thương mại.

⚙️ Các tính năng chính:

    🔍 Tra cứu sách thật qua công cụ SearchBookTool (lấy dữ liệu từ file JSON).

    🛒 Đặt hàng thật qua OrderBookTool, kiểm tra tồn kho và tạo đơn hàng thật.

    🧩 Tư duy theo mô hình ReAct: chatbot tự suy nghĩ → hành động → quan sát → phản hồi.

    🧠 Không bịa thông tin: chỉ trả lời sau khi có OBSERVATION từ công cụ thật.

    🏗️ Thiết kế rõ ràng, dễ mở rộng: có ModelFactory, ReActAgent, và ToolManager giúp tách biệt từng phần logic.

    🌐 Tích hợp API FastAPI — dễ dùng để xây giao diện web hoặc CLI.

🚀 Mục tiêu của em

    Rèn luyện khả năng thiết kế AI agent có khả năng tư duy nhiều bước.

    Thực hành các Design Pattern để tổ chức mã rõ ràng.

    Xây nền tảng cho các dự án AI có tính ứng dụng cao (ví dụ: trợ lý học tập, thương mại thông minh).

🧑‍💻 Công nghệ sử dụng

    Python 3.11

    FastAPI

    Ollama + Qwen 2.5 (1.5B)

    JSON file làm cơ sở dữ liệu

    Design Pattern: Factory, Tool Abstraction

❤️ Lời kết  

    Em thực hiện dự án này như một bước luyện tập nghiêm túc về tư duy hệ thống và ứng dụng LLM.
    Nếu anh/chị tuyển dụng hoặc người xem repo có góp ý, em rất sẵn lòng được học hỏi và hoàn thiện hơn ạ. 🙏


HƯỚNG DẪN SỬ DỤNG: 
 B1: TẢI MÔ HÌNH QWEN1.7B TỪ OLLAMA
 B2: CÀI ĐẶT CÁC THƯ VIỆN CẦN THIẾT TRONG requirements.txt
 B3: NẾU MUỐN GIAO DIỆN DÒNG LỆNH (CLI) -> CHẠY FILE CHAT_ENGINE.PY
 B4: NẾU MUỐN GỌI API -> HƯỚNG DẪN SỬ DỤNG: B1: TẢI MÔ HÌNH QWEN1.7B TỪ OLLAMA B2: CÀI ĐẶT CÁC THƯ VIỆN CẦN THIẾT TRONG requirements.txt B3: NẾU MUỐN GIAO DIỆN DÒNG LỆNH (CLI) -> python main.py

# Web mô phỏng Định lí Giới hạn Trung tâm (FastAPI + Render)

## Chạy cục bộ
```bash
python -m venv .venv
# Windows PowerShell:  .venv\Scripts\Activate.ps1
# macOS/Linux:         source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```
Mở http://127.0.0.1:8000 (trang chính), /health (kiểm tra), /docs (tài liệu API).

## Tạo lại video (tuỳ chọn)
```bash
pip install numpy matplotlib   # cần có ffmpeg
python scripts/make_video.py
```

## Đưa lên GitHub
```bash
git init
git add .
git commit -m "Create responsive CLT video web"
git branch -M main
git remote add origin https://github.com/USERNAME/clt-video-web.git
git push -u origin main
```

## Triển khai Render
New > Web Service > chọn repo > Runtime Python
- Build: `pip install -r requirements.txt`
- Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`
(hoặc dùng Blueprint đọc `render.yaml`).

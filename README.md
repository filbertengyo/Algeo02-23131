# EDP445

EDP445 adalah aplikasi berbasis web untuk mencari lagu pada suatu dataset. Pencarian dapat dilakukan melalui dua cara, melalui gambar dan juga audio. Pencarian melalui gambar dilakukan dengan membandingkan fitur-fitur yang diekstraksi melalui PCA antara gambar input dengan gambar cover album. Sementara itu, pencarian melalui audio dilakukan dengan pembandingan fitur audio berdasarkan distribusi nada. Aplikasi mampu mengurutkan lagu-lagu dalam dataset sesuai dengan nilai kemiripan yang ditemukan.

## Contributors
![270931](https://github.com/user-attachments/assets/6809f516-c9ee-42c6-848d-46f6c9ea824d)

- Ahmad Wafi Idzharulhaqq (13523131)
- Arlow Emmanuel Hergara (13523161)
- Filbert Engyo (13523163)

## How to Run

### Backend
1. Navigate to src/backend
   ```
   cd src/backend
   ```
2. Start a python virtual environment (Optional but Recommended)
   ```
   python -m venv venv
   ```
3. Install the required dependencies as written in requirements.txt
   ```
   pip install -r requirements.txt
   ```
4. Start the flask server
   ```
   flask run
   ```

### Frontend
1. Start the backend server
2. Navigate to src/frontend
   ```
   cd src/frontend
   ```
3. Install frontend dependencies
   ```
   pnpm install
   ```
4. Setup .env by specifying the address of the backend server
5. Start the frontend server
   ```
   pnpm run dev
   ```

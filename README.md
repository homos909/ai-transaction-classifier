[English](#english) | [Tiếng Việt](#tiếng-việt)

---

## English

# AI Transaction Classifier

A Python tool that automatically classifies unlabeled accounting transactions (Revenue vs. Expense) using an LLM. Designed with a swappable provider architecture: development and testing use a free rule-based Mock provider, while production can switch to the real Claude API by changing a single line of code.

### Features

- Reads unclassified transactions from CSV
- Classifies each transaction using a pluggable `ClassifierProvider` interface
- Two interchangeable implementations: `MockProvider` (rule-based, free, used for development) and `AnthropicProvider` (calls the real Claude API)
- Persists results to a SQLite database
- Re-running the tool clears old results first, so output is always consistent

### Why a Mock provider?

Calling a real LLM API during development costs money and is slower to iterate on. This project follows the same pattern used in production AI agent systems: an abstract base class defines the contract (`classify(description) -> str`), and any provider that implements it can be swapped in without touching the rest of the codebase — no `if/else` branching, no rewritten logic.

```python
provider = MockProvider()                          # free, used during development
provider = AnthropicProvider(api_key="sk-...")      # real API, one-line swap
```

### Installation

```bash
pip install pandas anthropic
```

### Usage

```bash
python main.py
```

This reads `giao_dich_chua_phan_loai.csv`, classifies every row, and stores the results in `classifier.db`.

### Code architecture

- `classifier.py` — `ClassifierProvider` abstract base class, `MockProvider`, `AnthropicProvider`
- `db.py` — SQLite table setup, insert, and cleanup functions
- `main.py` — reads the CSV, runs classification, saves results

### Tech stack

- Python 3
- pandas — reading transaction data
- sqlite3 — persistent storage
- Anthropic SDK — real LLM classification (optional, swappable)

### Roadmap

- Load the API key from a `.env` file instead of passing it directly
- Add a CLI flag to choose which provider to use at runtime
- Add confidence scores and a manual-review flow for low-confidence classifications

---

## Tiếng Việt

# Công cụ Phân loại Giao dịch bằng AI

Công cụ Python tự động phân loại các giao dịch kế toán chưa gán nhãn (Doanh thu / Chi phí) bằng LLM. Thiết kế theo kiến trúc cho phép "cắm/tháo" provider dễ dàng: khi phát triển và test dùng Mock provider dựa trên luật (miễn phí), khi triển khai thật chỉ cần đổi 1 dòng code để chuyển sang Claude API thật.

### Tính năng

- Đọc giao dịch chưa phân loại từ file CSV
- Phân loại từng giao dịch qua interface `ClassifierProvider` linh hoạt
- 2 cách triển khai có thể thay thế cho nhau: `MockProvider` (dựa trên luật, miễn phí, dùng khi phát triển) và `AnthropicProvider` (gọi Claude API thật)
- Lưu kết quả vào SQLite database
- Chạy lại nhiều lần vẫn cho kết quả nhất quán (tự động xoá dữ liệu cũ trước khi xử lý mới)

### Tại sao dùng Mock provider?

Gọi LLM API thật trong quá trình phát triển tốn chi phí và làm chậm việc lặp lại thử nghiệm. Project này áp dụng đúng pattern dùng trong các hệ thống AI Agent thực tế: 1 abstract base class định nghĩa "hợp đồng" chung (`classify(description) -> str`), bất kỳ provider nào tuân theo hợp đồng đó đều có thể thay thế cho nhau mà không cần sửa phần code còn lại — không cần `if/else`, không cần viết lại logic.

```python
provider = MockProvider()                          # miễn phí, dùng khi phát triển
provider = AnthropicProvider(api_key="sk-...")      # API thật, chỉ đổi 1 dòng
```

### Cài đặt

```bash
pip install pandas anthropic
```

### Cách sử dụng

```bash
python main.py
```

Chương trình đọc file `giao_dich_chua_phan_loai.csv`, phân loại từng dòng, lưu kết quả vào `classifier.db`.

### Kiến trúc code

- `classifier.py` — abstract base class `ClassifierProvider`, `MockProvider`, `AnthropicProvider`
- `db.py` — tạo bảng, thêm dữ liệu, dọn dữ liệu cũ trong SQLite
- `main.py` — đọc CSV, chạy phân loại, lưu kết quả

### Công nghệ sử dụng

- Python 3
- pandas — đọc dữ liệu giao dịch
- sqlite3 — lưu trữ dữ liệu
- Anthropic SDK — phân loại bằng LLM thật (tuỳ chọn, có thể thay thế)

### Hướng phát triển tiếp theo

- Đọc API key từ file `.env` thay vì truyền trực tiếp
- Thêm tham số dòng lệnh để chọn provider lúc chạy
- Thêm điểm tin cậy (confidence score) và luồng xem xét thủ công cho các phân loại chưa chắc chắn

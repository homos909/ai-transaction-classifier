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

### Why a Mock provider — and why an LLM at all?

Calling a real LLM API during development costs money and is slower to iterate on. This project follows the same pattern used in production AI agent systems: an abstract base class defines the contract (`classify(description) -> str`), and any provider that implements it can be swapped in without touching the rest of the codebase — no `if/else` branching, no rewritten logic.

```python
provider = MockProvider()                          # free, used during development
provider = AnthropicProvider(api_key="sk-...")      # real API, one-line swap
```

**Why not just use rule-based matching for everything, though?** Because keyword rules break down on ambiguous, real-world transaction descriptions. On a 12-transaction test batch, `MockProvider` correctly classified 8/12 (67%) but returned `Chưa xác định` (unclassified) on the remaining 4 — descriptions like "Chuyển khoản 5,000,000đ" (a plain transfer, no keyword signal) or "Hoàn tiền cho khách hàng do lỗi đơn hàng" (a refund, which an experienced accountant would recognize as a revenue deduction, not a generic expense) have no keyword for a rule engine to latch onto, but carry enough context for an LLM to infer the right category. This is the concrete case for using an LLM here: not "AI for everything," but AI applied specifically where rule-based logic runs out of signal.

| Transaction | Rule-based (Mock) | Why it fails |
|---|---|---|
| Chuyển khoản 5,000,000đ | Chưa xác định | No revenue/expense keyword present |
| Thanh toán hóa đơn số 445 | Chưa xác định | Generic payment wording, ambiguous direction |
| Giao dịch với đối tác XYZ Corp | Chưa xác định | No transaction-type keyword at all |
| Hoàn tiền cho khách hàng do lỗi đơn hàng | Chưa xác định | Requires domain knowledge (refunds ≠ expenses) |

### Real LLM test results (Gemini 3.6 Flash)

Two of the ambiguous cases above were run against a real LLM (Google Gemini, free tier) to check whether the theory held up:

| Transaction | Gemini output |
|---|---|
| Chuyển khoản 5,000,000đ | Chi phí |
| Hoàn tiền cho khách hàng do lỗi đơn hàng | Chi-phí |

Two honest findings from this small test, worth stating plainly rather than glossing over:

1. **Output formatting is inconsistent.** The second response came back as `"Chi-phí"` (hyphenated) instead of `"Chi phí"`, even though the prompt explicitly asked for a single word in a fixed format. Real LLM output can't be trusted to match an exact string every time — a production version of this tool would need a normalization/validation step (e.g. mapping known variants, or falling back to `Chưa xác định` when the response doesn't match an expected category) rather than assuming the raw text is always usable as-is.
2. **The LLM isn't always right either.** A refund to a customer is, strictly speaking, a revenue deduction in accounting terms — not a generic expense. Gemini classified it as `Chi phí`, which is a reasonable guess but not the technically correct answer. This confirms the LLM resolves more cases than keyword rules (it didn't return "unclassified"), but it doesn't mean its output should be trusted blindly — a real deployment would need either a confidence threshold, a human-review step for low-certainty cases, or a more detailed prompt with the full chart of accounts.

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

### Tại sao dùng Mock provider — và tại sao cần LLM?

Gọi LLM API thật trong quá trình phát triển tốn chi phí và làm chậm việc lặp lại thử nghiệm. Project này áp dụng đúng pattern dùng trong các hệ thống AI Agent thực tế: 1 abstract base class định nghĩa "hợp đồng" chung (`classify(description) -> str`), bất kỳ provider nào tuân theo hợp đồng đó đều có thể thay thế cho nhau mà không cần sửa phần code còn lại — không cần `if/else`, không cần viết lại logic.

```python
provider = MockProvider()                          # miễn phí, dùng khi phát triển
provider = AnthropicProvider(api_key="sk-...")      # API thật, chỉ đổi 1 dòng
```

**Nhưng tại sao không dùng luôn rule-based cho mọi trường hợp?** Vì luật dựa trên từ khoá thất bại với các mô tả giao dịch mơ hồ trong thực tế. Trên bộ test 12 giao dịch, `MockProvider` phân loại đúng 8/12 (67%), nhưng trả về `Chưa xác định` ở 4 giao dịch còn lại — các mô tả như "Chuyển khoản 5,000,000đ" (chuyển khoản đơn thuần, không có từ khoá gợi ý) hay "Hoàn tiền cho khách hàng do lỗi đơn hàng" (hoàn tiền — một kế toán viên có kinh nghiệm sẽ nhận ra đây là khoản giảm trừ doanh thu, không phải chi phí thông thường) không có từ khoá để rule-based bám vào, nhưng đủ ngữ cảnh để LLM suy luận đúng loại tài khoản. Đây chính là lý do cụ thể để dùng LLM ở đây: không phải "dùng AI cho mọi thứ", mà là áp dụng AI đúng chỗ mà logic rule-based hết khả năng xử lý.

| Giao dịch | Rule-based (Mock) | Tại sao thất bại |
|---|---|---|
| Chuyển khoản 5,000,000đ | Chưa xác định | Không có từ khoá doanh thu/chi phí |
| Thanh toán hóa đơn số 445 | Chưa xác định | Diễn đạt chung chung, không rõ chiều giao dịch |
| Giao dịch với đối tác XYZ Corp | Chưa xác định | Hoàn toàn không có từ khoá loại giao dịch |
| Hoàn tiền cho khách hàng do lỗi đơn hàng | Chưa xác định | Cần kiến thức nghiệp vụ (hoàn tiền ≠ chi phí) |

### Kết quả test thật với LLM (Gemini 3.6 Flash)

2 trong số các trường hợp mơ hồ ở trên đã được chạy thử với LLM thật (Google Gemini, free tier) để kiểm chứng lý thuyết có đúng thực tế không:

| Giao dịch | Kết quả Gemini trả về |
|---|---|
| Chuyển khoản 5,000,000đ | Chi phí |
| Hoàn tiền cho khách hàng do lỗi đơn hàng | Chi-phí |

2 phát hiện thành thật từ bài test nhỏ này, đáng nói rõ thay vì bỏ qua:

1. **Định dạng đầu ra không nhất quán.** Kết quả thứ 2 trả về `"Chi-phí"` (có dấu gạch ngang) thay vì `"Chi phí"`, dù prompt đã yêu cầu rõ ràng "chỉ trả lời đúng 1 từ" theo định dạng cố định. Không thể tin tưởng đầu ra LLM luôn khớp chính xác 1 chuỗi cố định — phiên bản triển khai thật của công cụ này cần thêm bước chuẩn hoá/kiểm tra (ví dụ: ánh xạ các biến thể đã biết, hoặc trả về `Chưa xác định` khi kết quả không khớp danh mục hợp lệ nào) thay vì giả định văn bản thô luôn dùng được ngay.
2. **LLM cũng không phải lúc nào cũng đúng.** Về mặt kế toán, khoản hoàn tiền cho khách hàng thực chất là **khoản giảm trừ doanh thu**, không phải chi phí thông thường. Gemini phân loại là `Chi phí` — một phỏng đoán hợp lý nhưng không hoàn toàn chính xác về nghiệp vụ. Điều này xác nhận LLM xử lý được nhiều trường hợp hơn rule-based (không trả về "chưa xác định"), nhưng không có nghĩa kết quả của nó nên được tin tưởng mù quáng — 1 hệ thống triển khai thật cần có ngưỡng độ tin cậy, bước xem xét thủ công cho các trường hợp chưa chắc chắn, hoặc prompt chi tiết hơn kèm đầy đủ hệ thống tài khoản kế toán.

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

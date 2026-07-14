# Research Proposal: Proactive Bug Discovery via Agentic Exploration at Repository-Level

**Nhóm:** 4
**Thành viên:** Lê Trần Gia Huy - SE193344
    Lê Chí Tâm - SE190322
    Nguyễn Tiến Phú - SE190131
    Trương Văn An - SE194268
**Topic code:** RT-SWT-005
**Ngày nộp:** 2026-07-10
**Version:** 3.1
**Trạng thái:** Đang chờ phê duyệt

---

## 2. Research Problem Statement

### 2.1 Bối cảnh & Tầm quan trọng

Kiểm thử phần mềm ở cấp độ kho lưu trữ mã nguồn (repository-level) là một trong những thách thức cốt lõi của kỹ nghệ phần mềm hiện đại. Không giống kiểm thử đơn vị truyền thống — nơi phạm vi được giới hạn rõ ràng — kiểm thử cấp repo đòi hỏi hệ thống phải hiểu đồng thời cấu trúc toàn bộ codebase, tài liệu đặc tả, và các ràng buộc nghiệp vụ tiềm ẩn. Khả năng "chủ động phát hiện lỗi" (Proactive Bug Discovery) — tức là tìm ra lỗi chỉ bằng cách đối chiếu code với tài liệu mà không cần báo cáo lỗi sẵn có — có giá trị thực tiễn cực kỳ cao vì nó mô phỏng chính xác công việc của một kỹ sư QA thực sự. Như được chứng minh trong TestExplora (2026, Microsoft/arXiv) — benchmark tiên phong và toàn diện nhất trong lĩnh vực này — ngay cả các LLM thương mại mạnh nhất hiện nay cũng bộc lộ giới hạn năng lực nghiêm trọng khi đối mặt với bài toán này.

### 2.2 State of the Art

Nghiên cứu về ứng dụng LLM trong kiểm thử phần mềm đã phát triển theo nhiều hướng. TestExplora (Microsoft, 2026) xây dựng benchmark 2,389 tác vụ từ 482 repository thực tế, đánh giá toàn diện khả năng Proactive Bug Discovery của các LLM hàng đầu — Claude-Sonnet-4.5 đạt F2P tối đa 16.06% ở kịch bản Plain context, GPT-5 đạt 15.15%. SWT-Bench (Mündler et al., 2025) đánh giá tác nhân tái hiện lỗi từ issue reports, đạt 27.3% nhưng phụ thuộc hoàn toàn vào báo cáo lỗi có sẵn. MASTEST (2025, FSE) dùng đa tác nhân đạt 85–95% operation coverage nhưng vẫn cần human-in-the-loop. AutoGen Insurance (2025) tối ưu branch coverage lên 99% nhưng chỉ trên một ứng dụng đơn lẻ. TESTWEAVER (2026) tăng line coverage 16.4% thông qua backward slicing nhưng phụ thuộc đặc thù ngôn ngữ Java/Python.

### 2.3 GAP

Qua phân tích hệ thống 37 công trình (SLR/gap-analysis.md), GAP chính được xác định thuộc loại **GAP-S (Shared Limitation)**: Các mô hình ngôn ngữ lớn hiện nay gặp lỗ hổng lớn về năng lực "chủ động phát hiện lỗi" ở cấp độ repository-level khi chỉ đối chiếu code với tài liệu mà không có bất kỳ tín hiệu lỗi nào trước đó. Minh chứng định lượng: Trên benchmark TestExplora (2026) ở kịch bản White Box với Plain context, mô hình tốt nhất hiện tại — Claude-Sonnet-4.5 — chỉ đạt F2P tối đa **16.06%** tại cấu hình mẫu đơn lẻ $k=1$. Không một trong 37 công trình được khảo sát đề xuất hệ tác nhân tự trị linh hoạt sử dụng các mô hình mã nguồn mở có khả năng tương tác terminal thời gian thực để giải quyết điểm nghẽn này ở cấu hình cơ bản.

### 2.4 Motivation

Nếu GAP này không được giải quyết, các hệ thống kiểm thử tự động sẽ tiếp tục phụ thuộc vào báo cáo lỗi của con người thay vì chủ động tìm kiếm lỗi — tức là chỉ phòng ngừa lỗi cũ (regression prevention) thay vì khám phá lỗi mới. Trong thực tế, phần lớn lỗi nghiêm trọng nhất trong phần mềm là những lỗi chưa ai biết và chưa có issue report — đây chính là nhóm lỗi mà hệ thống hiện tại bỏ sót hoàn toàn với tỷ lệ thất bại lên đến 83.94% ngay ở lượt thử đầu tiên ($k=1$).

---

## 3. Related Work

### 3.1 Overview

Bảng tóm tắt các công trình tiêu biểu nhất từ evidence table (N=37), chọn lọc theo độ liên quan với GAP chính và tập trung vào cấu hình mẫu đơn lẻ ($k=1$):

| Paper | Tool/LLM | Dataset (N) | Metric chính | Kết quả tốt nhất ($k=1$) | Hạn chế chính |
|---|---|---|---|---|---|
| TestExplora (2026, arXiv/Microsoft) | Claude-Sonnet-4.5, GPT-5, SWEAgent | 2,389 tasks, 482 repos | F2P Rate (%), HP (%), EC (%) | F2P Plain: 16.06% | LLM tĩnh bị "bẫy tuân thủ"; tăng cấu trúc kiểm thử tĩnh không tăng chất lượng phát hiện lỗi |
| SWT-Bench (2025, NeurIPS) | AutoCoderRover, SWE-agent, GPT-4 | GitHub issues (bug-fixes thực tế) | Tỷ lệ tái hiện lỗi, Test khớp chuẩn | 27.3% tái hiện thành công | Phụ thuộc issue reports có sẵn; 14% sinh lỗi cú pháp |
| MASTEST (2025, arXiv) | GPT-4o, DeepSeek V3.1, đa tác nhân | 5 REST API services | Operation Coverage, Correctness Rate | 85–95% op coverage, 78% bug detection | Cần human-in-the-loop; thiếu self-healing |
| AutoGen Insurance (2025) | AutoGen + Llama-3-8B | 1 ứng dụng bảo hiểm (Python) | Branch Coverage, Mutation Score | Branch: 99%, Mutation: 95.8% | Chỉ 1 ứng dụng; agent hay lặp kịch bản |
| TESTWEAVER (2026) | Claude 3.5 Sonnet + GPT-4o | 10 RESTful services (Java/Python) | Line coverage, Bug count | +16.4% line coverage, 7 bugs | Cần backward slicing đặc thù ngôn ngữ |
| SWE-Bench (tham chiếu nền) | Nhiều agent | GitHub issues (Python repos) | % Resolved issues | ~12–27% tùy agent | Rò rỉ dữ liệu huấn luyện; chỉ reactive |
| MASTOR (2026, J. ACM) | DeepSeek V4 Pro + Qwen3.6-Plus | 13 REST API projects, 296 ops | Mutation Score (PITest) | 75.4% avg, nhưng 10.7% endpoint phức tạp | Không giải quyết bài toán proactive discovery |
| LlamaRestTest (2025, FSE) | Llama3-8B fine-tuned | 12 REST API services | Method/Branch coverage, Bug count | 55.8% method, 204 faults | Phụ thuộc hoàn toàn dữ liệu huấn luyện |
| RBCTEST (2026, ICSE) | Observation-Confirmation + Semantic Verifier | 8 services, 65 endpoints | Precision/Recall/F1 | Precision 93.6%, 46 bugs thực tế | Phụ thuộc OpenAPI; loại bỏ cấu trúc lồng sâu |
| QAagent (2025) | LLM đa tác nhân từ mã giả | 4 dự án sinh viên | Statement Coverage | 61% → 84.6% | Chỉ dự án nhỏ; không có REST API doanh nghiệp |

### 3.2 Pattern Analysis

Nhìn chung, các nghiên cứu hiện tại phân thành ba luồng chính, thể hiện rõ qua bộ 37 công trình được phân tích:

**Luồng Reactive Testing** (SWT-Bench, SWE-Bench, MASTEST): Phụ thuộc vào issue reports hoặc bug descriptions có sẵn để tái hiện lỗi. Đạt kết quả tương đối tốt nhưng hoàn toàn không giải quyết bài toán proactive discovery — tức là không thể tìm lỗi khi chưa có ai báo cáo.

**Luồng Coverage-Driven** (TESTWEAVER, AutoGen Insurance, LlamaRestTest): Tối ưu hóa độ bao phủ mã nguồn theo nghĩa truyền thống. Cải thiện rõ về coverage nhưng coverage cao không đồng nghĩa với phát hiện lỗi logic tiềm ẩn — và toàn bộ nhóm này không đánh giá theo F2P metric.

**Luồng Spec-Based Oracle** (RBCTEST, SATORI, APITESTING): Khai phá ràng buộc từ tài liệu OpenAPI. Đạt độ chính xác cao trong phạm vi tài liệu nhưng không thể phát hiện lỗi nằm ngoài những gì đã được mô tả trong spec.

### 3.3 GAP Mapping

| GAP loại | Minh chứng từ Evidence Table | Số paper support | Trạng thái |
|---|---|---|---|
| GAP-S (Primary): LLM không thể chủ động phát hiện lỗi cấp repo-level | TestExplora (2026): F2P max 16.06% với Plain context | 37/37 | Confirmed |
| GAP-T: Thiếu kiến trúc tác nhân tự trị linh hoạt tương tác terminal | Toàn bộ 37 paper dùng single-step hoặc tác nhân tĩnh | 37/37 | Confirmed |
| GAP-D: Thiếu benchmark stream thời gian thực chống data leakage | Dataset cũ (SWE-Bench) dễ bị rò rỉ dữ liệu huấn luyện | 37/37 | Confirmed |
| GAP-M: Thiếu metric đo F2P suite-level đặc thù proactive discovery | Đa số đo coverage tổng thể, không đo F2P | 37/37 | Confirmed |

---

## 4. Research Questions

> **Chốt tại đây. Sau khi GV phê duyệt, không được thay đổi RQ, metric, hay threshold.**

**RQ1:** Liệu hệ tác nhân tự trị linh hoạt phối hợp công cụ tương tác terminal mã nguồn mở (Agentic Exploration) với ngân sách mẫu giới hạn $k=1$ (Pass@1) có đạt tỷ lệ Fail-to-Pass (F2P) trung bình ở kịch bản White Box trên tập dữ liệu tổng `TestExplora` vượt ngưỡng trần tĩnh 16.06% của kịch bản Plain context baseline hay không?

**Loại claim:** Absolute threshold (hệ thống đề xuất > ngưỡng tối đa đã công bố của kịch bản tĩnh tốt nhất ở cùng cấu hình $k=1$)

**H0 (RQ1):** Hệ tác nhân Agentic Exploration KHÔNG đạt F2P trung bình cao hơn ngưỡng 16.06% của kịch bản Plain context baseline trên tập `TestExplora` (hiệu năng $\le 16.06\%$).

**H1 (RQ1):** Hệ tác nhân Agentic Exploration đạt F2P trung bình vượt ngưỡng $> 16.06\%$ của kịch bản Plain context trên tập `TestExplora`.

**Metric:** Fail-to-Pass Rate (F2P — %) đo lường ở cấp độ Test Suite với ngân sách $k=1$.
**Ngưỡng:** 16.06% — Case 1: Trích dẫn trực tiếp từ kết quả thực nghiệm TestExplora (2026) — F2P tối đa của Claude-Sonnet-4.5 ở kịch bản Plain context White Box.
**Statistical test:** Wilcoxon signed-rank test ($\alpha = 0.05$).

---

## 5. Experiment Protocol

> **Tiêu chuẩn reproducibility:** Mọi thông số dưới đây phải đủ để một nhóm độc lập tái hiện kết quả.

### 5.1 Pipeline tổng quan

Pipeline thực nghiệm gồm 6 bước theo thứ tự:

1. **Task sampling:** Sử dụng toàn bộ bộ dữ liệu `TestExplora` gốc gồm 2,389 tác vụ lớn độc nhất từ 482 repositories, thiết lập môi trường Docker cô lập cho từng repository.
2. **Context preparation:** Cung cấp cho Agent: mã nguồn repository + tài liệu hướng dẫn (documentation) — không cung cấp issue report hay bug description.
3. **Agentic Exploration (điểm mới):** Mô hình mã nguồn mở `Qwen3.6-Coder-35B-A3B-Instruct` đóng vai trò Exploration Agent tự do khám phá repository thông qua terminal — gọi `pytest`, đọc execution log, tự sửa test suite theo vòng lặp phản hồi thực thi (Execution Feedback Loop), tối đa 80 turns. Mỗi tác vụ chỉ chạy duy nhất $k=1$ lượt mẫu (Pass@1 Budget).
4. **Code Action Fixing:** Mô hình mã nguồn mở `DeepSeek V4 Pro` đóng vai Code Action Fixer — kích hoạt cơ chế suy luận chuyên sâu (Thinking Mode), nhận log lỗi cuối cùng từ Agent, sửa mã kiểm thử cụ thể để chốt kết quả đầu ra.
5. **Evaluation:** Chạy test suite sinh ra qua bộ phán quyết DocAgent của TestExplora, thu thập F2P Rate, Head Pass Rate (HP), Entry Coverage (EC).
6. **Statistical analysis:** Wilcoxon signed-rank test so sánh cấu hình Agentic mã nguồn mở ($k=1$) vs. Plain context baseline ($k=1$) trên cùng tập dữ liệu tổng.

### 5.2 Dataset

| Thông tin | Chi tiết |
|---|---|
| Tên dataset | `TestExplora` (Full Version) |
| Nguồn (URL) | github.com/microsoft/TestExplora — public repository, Microsoft mã nguồn mở hoàn toàn |
| Quy mô (N) | 2,389 tác vụ lớn độc nhất (tương ứng 23,215 bản ghi dữ liệu con) thuộc 482 repositories |
| Domain | Đa ngành: web frameworks, data science, developer tools (Python chủ đạo) |
| Preprocessing | Sử dụng bản làm sạch sẵn có trong TestExplora — đã lọc docstring do con người viết để chống data leakage |
| Sampling strategy | **Pilot (Tuần 7):** Trích xuất ngẫu nhiên 10% số Tác vụ độc nhất ($\approx 239$ tác vụ lớn); **Full run (Tuần 8):** Toàn bộ 2,389 tác vụ lớn độc nhất |
| Lý do chọn | Đây là benchmark chuẩn của bài báo gốc TestExplora (2026), đảm bảo so sánh trực tiếp và công bằng; dataset stream thời gian thực sau 2023, chống data leakage (GAP-D, gap-analysis.md) |

### 5.3 LLM/Tool Configuration

**Primary Exploration Agent:**
- Model: `Qwen3.6-Coder-35B-A3B-Instruct` (Phiên bản Open-source tự host qua Ollama/vLLM hoặc Free Tier API Cloud)
- Hyperparameters: `temperature=0.8`, `top_p=0.95`, `max_tokens=4096`, `max_turns=80`, `k=1` (Pass@1)
- Prompting strategy: Zero-shot với system prompt định hướng Proactive Discovery — prompt nguyên văn lưu tại `prompts/exploration_agent_template.txt`
- Framework: SWEAgent — tương tác terminal thực (pytest, python interpreter)
- Lý do cấu hình: Dòng mô hình Qwen-Coder mã nguồn mở thế hệ mới đạt hiệu năng xử lý Tool-use và CLI terminal vượt trội; temperature cao để khuyến khích khám phá đa dạng kịch bản lỗi logic.

**Code Action Fixer:**
- Model: `DeepSeek V4 Pro` (Phiên bản Open-weights tự host hoặc Free Tier API Cloud)
- Hyperparameters: `thinking=enabled`, `reasoning_effort=high`, `max_tokens=2048`, `k=1`
- Prompting strategy: Few-shot (k=3) với ví dụ sửa lỗi cụ thể — prompt nguyên văn lưu tại `prompts/fixer_agent_template.txt`
- Lý do cấu hình: `DeepSeek V4 Pro` tích hợp sẵn chuỗi suy luận logic (Chain-of-Thought) chuyên sâu thông qua cơ chế Reinforcement Learning (GRPO), tối ưu hóa tuyệt đối khả năng bóc tách log lỗi và sửa đổi codebase phức tạp cấp repository.

**Baseline:**
- Tên: Plain context (TestExplora 2026) — Claude-Sonnet-4.5 sinh test suite trong một bước, không có Agentic Exploration, ngân sách mẫu $k=1$
- Version + source: Phiên bản gốc từ repository TestExplora (2026, Microsoft)
- Cấu hình để reproduce: `claude-sonnet-4-5`, single-step generation, không có terminal interaction, không có feedback loop

### 5.4 Measurement

| Thông tin | Chi tiết |
|---|---|
| Metric chính | Fail-to-Pass Rate (F2P — %) đo ở cấp độ Test Suite tại điểm mốc $k=1$ |
| Metric phụ | Head Pass Rate (HP — %) và Entry Coverage (EC — %) |
| Tool + version | Bộ phán quyết DocAgent tích hợp sẵn trong TestExplora framework; pytest runner trong Docker environment |
| Ground truth source | Documentation-derived intent — được tự động chuẩn hóa bằng DocAgent tích hợp sẵn trong dataset public |
| IAA method | Không áp dụng — oracle hoàn toàn tự động qua DocAgent |

### 5.5 Baseline

Baseline là kịch bản Plain context (TestExplora 2026) — so sánh comparative claim.

- Tên + version: Plain context — Claude-Sonnet-4.5, single-step (TestExplora 2026, Microsoft)
- Source: Repository public TestExplora
- Cấu hình đủ để reproduce: `claude-sonnet-4-5`, không có SWEAgent, không có terminal tools, không có feedback loop, chạy trên cùng tập `TestExplora` tổng với ngân sách mẫu $k=1$

### 5.6 Statistical Analysis Plan

- **Test:** Wilcoxon signed-rank test — one-tailed (kiểm định Agentic > Plain baseline), $\alpha = 0.05$
- **Lý do chọn test:** (1) F2P Rate là biến liên tục bounded [0%, 100%]; (2) Thiết kế paired-sample — cùng repository task, hai cấu hình chạy song song; (3) F2P phân hóa mạnh giữa task dễ và task khó → phân phối lệch, không chuẩn → loại Paired t-test; Wilcoxon phi tham số là lựa chọn chuẩn xác nhất (hypotheses-draft.md)
- **Effect size:** Cliff's delta (chỉ số phi tham số phù hợp cho Wilcoxon)
- **N và power:** K=3 lần chạy độc lập mỗi cấu hình; quy mô full $N=2389$ tác vụ lớn; power $\ge 0.80$ theo power analysis bằng `statsmodels`/G*Power trước khi chạy full experiment

---

## 6. Evaluation Plan

### 6.1 Bảng tiêu chí đánh giá

| RQ | Metric | Ngưỡng | Test | H0 bị reject khi... | Kết quả âm tính có ý nghĩa? |
|---|---|---|---|---|---|
| RQ1 | F2P Rate trung bình (%) — DocAgent + pytest | > 16.06% | Wilcoxon one-tailed, $\alpha=0.05$ | p-value < 0.05 VÀ median Agentic > 16.06% | Có — chứng minh cơ chế tương tác terminal mã nguồn mở không hiệu quả ở cấu hình 1 lượt chạy đơn lẻ, cần thay đổi chiến trúc prompt cao hơn |

### 6.2 Diễn giải tổng hợp kết quả

Nhóm xác định trước 2 tình huống kết quả và cách diễn giải tương ứng:

- **Tình huống Dương tính (✅):** Agentic Exploration vượt ngưỡng 16.06% ở mức ý nghĩa thống kê — kết luận: hệ tác nhân tự trị mã nguồn mở phối hợp terminal giúp bẻ gãy "bẫy tuân thủ" của mô hình tĩnh ngay từ lượt chạy đầu tiên, đề xuất nhân rộng framework.
- **Tình huống Âm tính (❌):** Kết quả âm tính hoàn toàn vẫn có giá trị khoa học — chứng minh cơ chế tác nhân tự do trên mô hình mở cần bổ sung thêm kỹ thuật fine-tuning đặc thù để bẻ gẫy rào cản; nhóm sẽ báo cáo trung thực và phân tích nguyên nhân.

### 6.3 Sub-group analysis (nếu có)

Điều kiện kích hoạt: n_group $\ge 10$ task cùng loại (simple function-level vs. complex cross-module) trong tập pilot Tuần 7.

Nếu đủ điều kiện, phân tích riêng F2P theo hai sub-group này để định lượng loại task nào Agent cải thiện nhiều nhất — quyết định này được đặt ra TRƯỚC KHI có data thực nghiệm.

> **Không được:** Thay đổi metric, threshold, hoặc thêm RQ sau khi thấy kết quả pilot = HARKing, vi phạm tính toàn vẹn khoa học.

---

## 7. Threats to Validity

### 7.1 Internal Validity

**Threat 1: Giới hạn phần cứng và độ trễ suy luận nội bộ (Local/Free-Cloud Hardware Limitations)**
Việc chuyển sang host mô hình mã nguồn mở cục bộ hoặc dùng các cổng API miễn phí có thể gây ra hiện tượng mất gói tin (timeout), nghẽn luồng xử lý hoặc không đồng nhất về tốc độ token sinh ra giữa tập Pilot và Full Run.

**Mitigation 1:** Cố định phiên bản trọng số mô hình cụ thể, khóa cứng tham số seed suy luận. Sử dụng file lưu checkpoint tự động `full_llm_output_checkpoint.csv` liên tục sau mỗi 100 tác vụ để cô lập lỗi crash phần cứng, đảm bảo tính toàn vẹn của tiến trình.

**Threat 2: Tính ngẫu nhiên của LLM làm kết quả không ổn định**
Với temperature=0.8 cho Exploration Agent, các lần chạy có thể cho kết quả F2P khác nhau đáng kể — một lần cao, một lần thấp — làm khó kết luận.

**Mitigation 2:** Chạy tối thiểu K=3 lần độc lập mỗi cấu hình; báo cáo cả median, mean, và standard deviation; dùng Wilcoxon trên toàn bộ tập K×N quan sát để kiểm soát yếu tố ngẫu nhiên.

### 7.2 External Validity

**Threat: Kết quả chỉ generalize trên Python repositories**
`TestExplora` chủ yếu gồm Python repos — kết quả có thể không đại diện cho Java, JavaScript, hoặc các ngôn ngữ khác với đặc thù testing framework khác nhau.

**Mitigation:** Báo cáo rõ phạm vi generalizability: kết quả áp dụng cho Python repositories với pytest framework; đề xuất mở rộng sang ngôn ngữ khác trong phần Future Work của RBL-5.

### 7.3 Construct Validity

**Threat: F2P Rate không đo được toàn bộ chất lượng kiểm thử**
F2P đo tỷ lệ test suite chuyển từ fail sang pass — nhưng không phản ánh false positive rate (test pass nhưng không thực sự kiểm tra đúng điều cần kiểm tra) hoặc độ sâu của assertion.

**Mitigation:** Bổ sung Head Pass Rate (HP) và Entry Coverage (EC) làm metric kiểm chứng chéo; các metric phụ này phản ánh độ chính xác thực thi và độ bao phủ interface — kế thừa từ framework đánh giá của TestExplora (2026).

### 7.4 Conclusion Validity

**Threat: Statistical power không đủ do lỗi phân mảnh dữ liệu**
Tập Pilot Tuần 7 nếu lấy mẫu ngẫu nhiên theo hàng thô đơn thuần sẽ làm xé nát cấu trúc các tác vụ gốc, gây mất power kiểm định.

**Mitigation:** Khóa cứng chiến lược lấy mẫu: thực hiện gom cụm dữ liệu theo mã định danh ID duy nhất (`task_id`) trước khi lấy mẫu để bốc chính xác $\approx 239$ tác vụ lớn toàn vẹn cho tập Pilot nhằm bảo toàn sức mạnh kiểm định phi tham số.

---

## 8. Timeline & Resources

### 8.0 Phân công vai trò

| Role | Thành viên | Trách nhiệm trong experiment |
|---|---|---|
| PL (Project Lead) | Lê Trần Gia Huy | Điều phối tiến độ, review nhất quán toàn proposal, submit GV, theo dõi phê duyệt, quản lý file cấu hình và nhật ký `notes.md` |
| DG (Data & Ground Truth) | Lê Chí Tâm | Setup TestExplora dữ liệu tổng, xác nhận dữ liệu accessible, thực thi script chia mẫu Pilot theo mã định danh duy nhất, viết §3 Related Work |
| LR (LLM Runner) | Nguyễn Tiến Phú | Thiết lập môi trường host mô hình mã nguồn mở (Ollama/vLLM/Free cloud tokens), viết script SWEAgent, log hiệu năng hệ thống |
| MS (Metrics & Stats) | Trương Văn An | Implement F2P evaluation pipeline, chạy Wilcoxon test, tính Cliff's delta, quản lý các file phân tích số liệu |
| RW (Report Writer) | [Họ tên thành viên phụ] | Viết §1, §7, §8, intro/conclusion; format document cuối; hỗ trợ DG viết §3, vẽ biểu đồ phân phối |

> **Quy tắc bất biến:** LR và MS không được gộp vào 1 người — người chạy experiment không tự verify kết quả của chính mình.

### 8.1 Resource Inventory

| Tài nguyên | Trạng thái | Owner | Ghi chú |
|---|---|---|---|
| Dataset TestExplora Full | ✅ Accessible | DG | github.com/microsoft/TestExplora — public, đã tải về local hoàn tất |
| Docker environment | ✅ An toàn | LR | GitHub Actions Runner Images có sẵn trong TestExplora; chạy local/cloud |
| Weights / Free API Key | ✅ Đã cấu hình | LR | Tải file trọng số Qwen3.6-Coder và DeepSeek V4 Pro; đăng ký hạn mức Free Tier Cloud |
| Compute | ✅ An toàn | LR | Tận dụng phần cứng GPU NVIDIA nội bộ kết hợp Google Colab T4 / Kaggle P100 |

### 8.2 Chi phí ước tính (Dựa trên mô hình mã nguồn mở / Free Tier)

| Item | Số lượng | Đơn giá ước tính | Tổng ước tính |
|---|---|---|---|
| Qwen3.6-Coder-35B-A3B-Instruct (Exploration Agent) | 2,389 tasks × K=3 runs × 80 turns | $0.00 (Self-hosted / Free Tier) | $0.00 |
| DeepSeek V4 Pro (Code Fixer) | 2,389 tasks × K=3 runs | $0.00 (Self-hosted / Free Tier) | $0.00 |
| Docker compute (Colab/Kaggle/Local GPU) | 2,389 tasks × ~5 min/task | $0.00 (Free Tier / Sẵn có) | $0.00 |
| **Tổng ngân sách thực nghiệm** | | | **0 VNĐ ($0.00)** |

### 8.3 Timeline chi tiết (Tuần 5–10)

> **Tuần 5–6:** Song song viết proposal + chuẩn bị tài nguyên
> **Tuần 7–8:** Thực nghiệm (Pilot → Full run)
> **Tuần 9–10:** Viết paper + present (xem RBL-5)

| Tuần | Hoạt động | Owner | Checkpoint — output cụ thể |
|---|---|---|---|
| **5** | Viết proposal §2–§7 | DG + RW + PL | Draft §2–§7 trong `proposal.md` v0.1 |
| **5** | Verify + clone TestExplora, test Docker env | DG | `data/raw/` folder + Docker run thành công |
| **5** | Setup local model/API, test 1 sample SWEAgent call | LR | `test_agent.py` chạy được thông tuyến mô hình mở |
| **5** | Implement F2P evaluation script sơ bộ | MS | `compute_f2p.py` draft + output mẫu |
| **6** | Hoàn thiện §8 + resource inventory + nộp GV | PL | `proposal.md` v3.1 → nộp GV |
| **6** | ★ **GV phê duyệt** (hard deadline: cuối Tuần 6) | GV | `proposal.md` → Trạng thái "Approved" |
| **7** | Chạy pilot (10% unique task sample, ~239 tasks) | LR | `results/pilot_llm_output.csv` + log thực thi |
| **7** | Tính F2P pilot, kiểm tra phân phối gom cụm | MS | `results/pilot_analysis.ipynb` — `analyze_pilot.py` chạy sạch data |
| **7** | All: Hop review pilot → amendment nếu cần | PL | Meeting note. Amendment → nộp GV trong 24 giờ |
| **8** | Full experiment batch run (2,389 tasks × K=3) | LR | `results/full_llm_output.csv` + log tải hệ thống |
| **8** | Tính F2P toàn bộ + Wilcoxon test + Cliff's delta | MS | `results/full_analysis.ipynb` — `analyze_full_experiment.py` hoàn thành |
| **8** | Tạo figures (boxplot phân phối F2P diện rộng) | RW | `figures/` folder — boxplot RQ1 diện rộng |
| **9–10** | Viết paper + present | Tất cả | Xem RBL-5 |

### 8.4 Contingency Plan

- **Nếu proposal chưa duyệt cuối Tuần 6:** Bám sát tiến độ, chuẩn bị sẵn mã nguồn mock-up để bốc dữ liệu nhanh — báo GV ngay.
- **Nếu dung lượng VRAM máy local bị tràn khi chạy 35B model:** Hạ cấu hình Exploration Agent xuống sử dụng dòng **`Qwen3.6-Coder-7B-Instruct`** để tối ưu hóa tài nguyên phần cứng local mà không thay đổi cấu trúc mã nguồn hệ thống.
- **Nếu Docker environment lỗi trên task cụ thể:** Bỏ qua task đó, ghi nhận trong §5.2 preprocessing; không thay thế bằng task khác để tránh selection bias.
- **Nếu pilot phát hiện vấn đề kỹ thuật:** Xem §8.6 — nộp amendment GV trong 24 giờ.
- **Nếu thành viên không kịp deadline:** PL escalate sau 48 giờ trễ; redistribute task theo role phụ đã thỏa thuận.

### 8.5 Checkpoint per member (Tuần 5–10)

| Role | Tuần 5 | Tuần 6 | Tuần 7 | Tuần 8 | Tuần 9–10 |
|---|---|---|---|---|---|
| **PL** | Draft §2–§7 review | Submit proposal + theo dõi GV | Pilot meeting note | Verify §4–§6 nhất quán | Review final draft |
| **DG** | `data/raw/` + Docker test | Confirm §8.1 resource | Xác nhận full dataset ready | Verify data integrity | Verify §3 figures |
| **LR** | `test_agent.py` pass | Confirm API/Weights setup | `results/pilot_llm_output.csv` | `results/full_llm_output.csv` | — |
| **MS** | `compute_f2p.py` draft | Confirm stat test plan | `results/pilot_analysis.ipynb` | `results/full_analysis.ipynb` | Draft §results |
| **RW** | Draft §7 Threats | Format + proofread §1–§7 | — | `figures/` folder | Draft §1, §conclusion |

### 8.6 Quy trình Amendment

**Khi nào cần amendment — khi nào không:**

| Phát hiện từ pilot | Cần amendment? | Lý do |
|---|---|---|
| F2P phân phối bimodal, cần đổi statistical test | ✅ | Lý do kỹ thuật hợp lệ |
| Docker fail trên nhiều task hơn dự kiến, N thực tế nhỏ hơn | ✅ | Cập nhật §5.2 + power analysis |
| Hạ tầng local quá tải, cần scale down kích thước model mở | ✅ | Lý do kỹ thuật/tài nguyên hợp lệ |
| Kết quả pilot thấp hơn threshold | ❌ | Đây là kết quả, không phải lý do kỹ thuật |
| Muốn thêm metric vì thấy kết quả thú vị | ❌ | HARKing — vi phạm khoa học |

> **❌ Không được:** Thay đổi RQ chính hoặc thay metric sau khi thấy kết quả.
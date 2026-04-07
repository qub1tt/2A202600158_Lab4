# Test Results — TravelBuddy Agent (Lab 4)

---

## Test 1 — Direct Answer (Không cần tool)

**Input:**
> Xin chào! Tôi đang muốn đi du lịch nhưng chưa biết đi đâu.

**Tool calls:** Không gọi tool nào

**Output:**
```
TravelBuddy: Chào bạn! Đi du lịch thật là thú vị! Bạn có đang nghĩ đến một địa điểm cụ thể nào không, hay bạn muốn tôi gợi ý cho bạn những nơi đẹp và thú vị ở Việt Nam? Nếu bạn có ngân sách hay thời gian dự kiến, hãy chia sẻ thêm nhé!
```

**Kết quả:** PASS ✓ — Agent chào hỏi, hỏi thêm về sở thích/ngân sách/thời gian. Không gọi tool.

---

## Test 2 — Single Tool Call

**Input:**
> Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng

**Tool calls:**
```
[Tool] Gọi tool: search_flights({'origin': 'Hà Nội', 'destination': 'Đà Nẵng'})
```

**Output:**
```
TravelBuddy: Đây là các chuyến bay từ Hà Nội đi Đà Nẵng mà tôi tìm thấy:

1. Vietnam Airlines | 06:00 → 07:20 | 1.450.000đ (economy)
2. Vietnam Airlines | 14:00 → 15:20 | 2.800.000đ (business)
3. VietJet Air      | 08:30 → 09:50 | 890.000đ   (economy)
4. Bamboo Airways   | 11:00 → 12:20 | 1.200.000đ (economy)
```

**Kết quả:** PASS ✓ — Gọi đúng search_flights("Hà Nội", "Đà Nẵng"), liệt kê đủ 4 chuyến bay.

---

## Test 3 — Multi-Step Tool Chaining

**Input:**
> Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!

**Tool calls:**
```
[Tool] Gọi tool: search_flights({'origin': 'Hà Nội', 'destination': 'Phú Quốc'})
[Tool] Gọi tool: search_hotels({'city': 'Phú Quốc', 'max_price_per_night': 1950000})
[Tool] Gọi tool: calculate_budget({'total_budget': 5000000, 'expenses': 've_may_bay:1100000,khach_san:1600000'})
```

**Output:**
```
TravelBuddy: Dưới đây là kế hoạch cho chuyến đi của bạn đến Phú Quốc:

Chuyến bay:
- Hãng: VietJet Air | 16:00 → 18:15 | 1.100.000đ

Khách sạn:
- Lahana Resort ★★★ | 800.000đ/đêm | Dương Đông | Rating: 4.0/5
- Tổng 2 đêm: 1.600.000đ

Tổng chi phí ước tính:
- Vé máy bay : 1.100.000đ
- Khách sạn  : 1.600.000đ
---
- Tổng chi   : 2.700.000đ
- Ngân sách  : 5.000.000đ
- Còn lại    : 2.300.000đ

Gợi ý thêm: Với số tiền còn lại, bạn có thể lặn biển, tham quan Vinpearl Safari, thưởng thức hải sản tại chợ địa phương.
```

**Kết quả:** PASS ✓ — Agent tự chuỗi đúng 3 bước:
1. `search_flights("Hà Nội", "Phú Quốc")` → vé rẻ nhất 1.100.000đ
2. `search_hotels("Phú Quốc", max_price_per_night=1950000)` → lọc đúng tầm giá (tự tính nhẩm: (5.000.000 - 1.100.000) / 2 = 1.950.000)
3. `calculate_budget(5000000, "ve_may_bay:1100000,khach_san:1600000")` → còn lại 2.300.000đ

---

## Test 4 — Missing Info / Clarification

**Input:**
> Tôi muốn đặt khách sạn

**Tool calls:** Không gọi tool nào

**Output:**
```
TravelBuddy: Mình cần biết thành phố mà bạn muốn đặt khách sạn, và ngân sách mỗi đêm bạn dự kiến chi cho khách sạn là bao nhiêu?
```

**Kết quả:** PASS ✓ — Agent hỏi lại thành phố và ngân sách trước khi gọi tool. Không gọi tool vội.

---

## Test 5 — Guardrail / Refusal

**Input:**
> Giải giúp tôi bài tập lập trình Python về linked list

**Tool calls:** Không gọi tool nào

**Output:**
```
TravelBuddy: Xin lỗi, nhưng mình không thể giúp đỡ về lập trình hay bài tập liên quan đến code. Tuy nhiên, nếu bạn cần thông tin cho chuyến du lịch hay tìm kiếm khách sạn, chuyến bay nào đó, mình rất vui lòng hỗ trợ!
```

**Kết quả:** PASS ✓ — Từ chối lịch sự, nói rõ chỉ hỗ trợ về du lịch.

---

## Tổng kết

| Test | Mô tả | Kết quả |
|------|-------|---------|
| Test 1 | Direct Answer — không gọi tool | PASS ✓ |
| Test 2 | Single Tool Call — search_flights | PASS ✓ |
| Test 3 | Multi-Step Tool Chaining — 3 tools | PASS ✓ |
| Test 4 | Missing Info / Clarification | PASS ✓ |
| Test 5 | Guardrail / Refusal | PASS ✓ |

**5/5 test cases PASS**

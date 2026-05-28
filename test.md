# Recommended Architecture for High-Accuracy Chart Extraction from PDFs

## Best Approach

The best results usually come from a hybrid pipeline that combines:

* multimodal LLM extraction,
* deterministic validation,
* visual comparison,
* and targeted retries.

The key idea is:

> Do not rely only on the LLM confidence score.
> Combine structured validation + visual validation + LLM judging.

---

# Recommended Pipeline

## 1. Render PDFs in High Quality

* Render PDF pages at 300–600 DPI.
* Detect and crop chart regions individually.
* Store:

  * original page image,
  * chart crop,
  * metadata.

This improves extraction quality significantly, especially for small or blurry charts.

---

## 2. Image Preprocessing

Before sending charts to the extraction model:

* denoise,
* sharpen,
* improve contrast,
* deskew,
* optional upscaling for low-resolution charts.

This step alone can reduce many extraction errors.

---

## 3. Extract Chart → Structured JSON

Use a multimodal model (Claude Opus / GPT / other vision model) to extract a strict structured format.

Example:

```json
{
  "chart_type": "line_chart",
  "title": "Revenue Growth",
  "x_axis": ["Q1", "Q2", "Q3"],
  "y_axis_range": [0, 100],
  "series": [
    {
      "name": "Revenue",
      "points": [
        {"x": "Q1", "y": 40},
        {"x": "Q2", "y": 55}
      ]
    }
  ]
}
```

The output should always be deterministic and schema-validated.

---

## 4. Recreate the Chart with Matplotlib

Generate a new chart image from the extracted JSON.

This becomes the normalized representation of what the model understood.

---

## 5. Dual Validation Strategy

### A. Structured Validation (Most Important)

Validate the extracted JSON programmatically:

* chart type consistency,
* axis ranges,
* labels,
* missing series,
* invalid values,
* duplicate points,
* percentage totals,
* scale consistency,
* stacked/grouped correctness.

This is usually more reliable than pure visual comparison.

---

### B. Visual Validation

Compare:

* original chart crop
  vs
* matplotlib recreated chart.

This helps detect:

* swapped axes,
* incorrect legends,
* missing visual elements,
* wrong scaling,
* incorrect grouping,
* layout interpretation issues.

---

## 6. LLM-as-Judge

The judge model should receive:

* original chart crop,
* recreated chart image,
* extracted JSON,
* metadata/checklist.

The judge should return:

```json
{
  "score": 0.87,
  "passed": true,
  "errors": [
    "Y-axis scale appears incorrect",
    "One series may be missing"
  ],
  "retry_instructions": [
    "Re-read the legend",
    "Verify Y-axis tick labels"
  ]
}
```

The judge should explain errors, not only provide a confidence score.

---

## 7. Targeted Retry Loop

Retry only the failing components.

Examples:

* re-read Y-axis,
* re-detect legend,
* verify missing series,
* reprocess low-confidence OCR areas.

Recommended:

* maximum 2–3 retries per chart.

Avoid infinite retry loops.

---

## 8. Human Review Fallback

If the chart still scores below threshold after retries:

* send to human review,
* or mark as low-confidence extraction.

This prevents silent bad data.

---

# Recommended Confidence Strategy

Do not trust raw LLM confidence alone.

Instead, compute a combined score:

```text
Final Score =
40% structured validation
25% visual similarity
20% multi-model agreement
15% LLM judge evaluation
```

This is usually much more stable than relying on a single model score.

---

# Should We Use LangGraph?

LangGraph is optional.

Recommended if you need:

* retries,
* branching workflows,
* state persistence,
* auditability,
* orchestration between models,
* human review flows.

Not necessary for a simple linear pipeline.

For advanced production workflows, LangGraph can help manage the graph/state architecture cleanly.

---

# Final Recommendation

The highest-quality approach is:

1. High-quality chart crops
2. Structured JSON extraction
3. Matplotlib recreation
4. Programmatic validation
5. Visual comparison
6. LLM judge
7. Targeted retries
8. Human fallback for low-confidence cases

This hybrid strategy usually produces significantly better results than using only a single multimodal extraction model.

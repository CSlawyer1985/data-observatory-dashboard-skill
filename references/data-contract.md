# Data Contract

## Normalized Object Record

For object-collection dashboards, normalize toward this shape:

```json
{
  "id": "stable-id",
  "label": "Entity name",
  "group": "Category",
  "size": 123.4,
  "score": 7.2,
  "score_label": "High",
  "metrics": {
    "amount": 123.4,
    "count": 56,
    "growth": 0.12
  },
  "details": {
    "summary": "Short explanation",
    "owner": "Department",
    "region": "China"
  },
  "source": {
    "name": "Official source",
    "url": "https://example.com",
    "retrieved_at": "2026-05-02",
    "method": "api|download|scrape|manual|model",
    "confidence": "high|medium|low"
  }
}
```

Use the user's original field names in the UI when they are meaningful, but keep normalized aliases internally.

## Field Mapping

Prefer these candidates:

- label: `name`, `title`, `occupation`, `company`, `case_name`, `entity`, `项目`, `名称`, `职业`, `公司`, `案件`
- group: `category`, `industry`, `type`, `region`, `department`, `jurisdiction`, `类别`, `行业`, `地区`, `类型`
- size: `count`, `amount`, `revenue`, `assets`, `employment`, `population`, `value`, `cases`, `金额`, `数量`, `人数`, `收入`, `规模`
- score/color: `risk`, `score`, `exposure`, `sentiment`, `growth`, `probability`, `风险`, `评分`, `暴露`, `增长`, `强度`
- explanation: `summary`, `rationale`, `description`, `notes`, `摘要`, `理由`, `说明`, `备注`
- source: `source`, `url`, `来源`, `链接`

If no label field exists, create `id`/`label` from row number plus the most descriptive categorical field.

## Units

Do unit detection before building charts. Area, totals, group summaries, breakdown bars, legends, and tooltips must all use the same field-level unit metadata.

Recommended unit keys:

- `wan_cny`: source value is 万元. Display 10000 万元 and above as 亿元, otherwise as 万元.
- `wan_cny_per_person`: source value is 万元/人. Display as `万/人`.
- `wan_person`: source value is 万人. Display 10000 万人 and above as 亿人, otherwise as 万人.
- `percent`: source value is already 0-100 percentage points. Display with `%`.
- `permille`: source value is per-thousand rate. Display with `‰`.
- `person`, `case`, `client`, `times`: display as 人、件、家、次.

If a source column name includes `万元`, preserve the value as 万元 in normalized JSON and pass `--unit field:wan_cny` to the dashboard builder. Do not multiply to 元 unless the whole downstream contract is changed together.

## Calculations

Weighted average:

```js
weighted = sum(score * size) / sum(size)
```

Group percentage:

```js
pct = groupSize / totalSize * 100
```

Treemap area value must be positive. For zero or negative metrics:

- use absolute value only if analytically correct
- otherwise filter, bucket separately, or use a non-area chart
- document the rule

## Source Records

Create `data_sources.json` when:

- data is fetched from URLs
- multiple datasets are merged
- values are estimated or model-generated
- field names are transformed
- calculations materially affect interpretation

Each source entry should include:

- dataset or field name
- source URL/path
- retrieval date
- transformation summary
- confidence
- known limitations

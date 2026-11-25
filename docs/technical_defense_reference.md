# Technical defense — study/reference notes

**Purpose:** This document provides reference explanations and transparent assumptions. It is not a substitute for independently explaining the decisions during a technical defense.

## Question 1 — All trades or unflagged trades?

Use the **39-record result (−$215.46)** as the headline representing the complete retained journal and show the **35-record result (−$194.46)** alongside it as sensitivity analysis. Neither is independently broker-verified. The four flagged records contribute a combined **−$21.00**, so their exclusion changes the net result but not its negative sign. Do not imply that an entry in a synthetic journal proves an actual execution.

## Question 2 — Why is reconstructed-field reconciliation circular?

T025's missing exit price was derived from its recorded P&L and the other fields. Substituting that derived price back into the same equation must reproduce the starting P&L (subject to rounding). That proves **internal algebraic consistency only**, not that the broker executed at that price or even that the original P&L was accurately recorded. Verification requires an independent execution record.

## Question 3 — Why does execution order affect drawdown?

Net P&L is a sum and does not depend on order, but drawdown measures each point's drop below the highest preceding cumulative P&L. If same-day Trade_ID is not execution order, trade-level peak/trough and potentially maximum drawdown can change. Report that assumption, distinguish provisional intraday drawdown from end-of-day drawdown computed from daily aggregated P&L, and seek timestamps. The original classroom example with just one loss of −$200 produces the same $200 maximum drawdown under any order; that specific example cannot demonstrate changing maximum drawdown.

## Question 4 — USDJPY conversion (reference explanation)

For **EURUSD and GBPUSD**, USD is the **quote currency**. Multiplying the price difference (USD per euro or pound) by the trade's base-currency units and the direction produces a P&L already denominated in **USD**.

For **USDJPY**, JPY is the **quote currency**. The same price-difference multiplication produces a P&L in **JPY**, not USD. If the account reports USD P&L, convert the JPY result to USD using an appropriate JPY-per-USD exchange rate—for example, approximately dividing by the USDJPY rate around settlement or exit. It is a conversion approximation, not a universal broker accounting rule.

**Unit example:** Buy 0.10 lot of USDJPY at 148.00 and exit at 149.00, assuming 100,000 base units per full lot: 0.10 × 100,000 × (149.00 − 148.00) = **+10,000 JPY**. At 149 JPY per USD this is approximately **+$67.11**, *not* +$10,000.

The broker's actual USD result could differ due to the **currency conversion rate and timestamp**, broker conversion method, execution prices, rounding, commissions, swaps or other fees. A small reconciliation tolerance is useful diagnostically but does not independently validate an execution.

### Important limitations

The synthetic journal has no independently confirmed broker conversion records and no detailed trading-cost fields. Never describe reconstructed or converted values as independently verified. Technical-defense completion should be assessed from the student's own explanation, not from this reference sheet.

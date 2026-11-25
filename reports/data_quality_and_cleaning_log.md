# Data-quality report

| Issue | Records | Trade_IDs | Potential impact | Planned action |
|---|---|---|---|---|
| Missing Exit_Price | 1 | T025 | P&L and drawdown cannot be checked for the trade | Derive from P&L, flag as imputed |
| Missing Position_Size_Lots | 1 | T031 | P&L cannot be reconciled to a size | Derive from P&L, flag as imputed |
| Missing Realized_PnL_USD | 1 | T036 | Would silently shrink net P&L if dropped | Derive from prices and size, flag as imputed |
| Exact duplicate row | 1 | T011 | Double-counts a trade (inflates P&L and trade count) | Remove the repeated copy only |
| Same Trade_ID, different values | 0 | - | Cannot tell which record is true | Investigate - none found |
| Gap in Trade_ID sequence | 1 | T039 | A real trade may be absent, so totals could be incomplete | Do not invent it; verify against broker log |
| Invalid Trade_ID format | 0 | - | Breaks joins and sorting | None found |
| Inconsistent Instrument text | 2 | T007, T013 | EURUSD would be split into 3 groups | Standardize to EURUSD, keep raw column |
| Inconsistent Direction text | 1 | T020 | BUY and Buy counted as different directions | Standardize to Buy/Sell, keep raw column |
| Unparseable Trade_Date | 0 | - | Breaks time-series analysis | None found |
| Non-positive price | 0 | - | Impossible market price | None found |
| Non-positive position size | 0 | - | Impossible position size | None found |
| Non-numeric entry in a numeric column | 0 | - | Text such as "n/a" would stop arithmetic or silently become NaN | None found |
| Infinite value in a numeric column | 0 | - | Infinity would corrupt sums, drawdown and averages | None found |

# Cleaning log

| Step | Transformation / exclusion | Records affected | Trade_IDs | Justification |
|---|---|---|---|---|
| 1 | Standardize Instrument (trim, remove "/", upper-case) | 2 | T007, T013 | Same instrument written 3 ways would split EURUSD results. Raw text kept in Instrument_Raw. |
| 2 | Standardize Direction to Buy/Sell | 38 | T001, T002, T003, T004, T005, T006, T007, T008, T009, T010, T011, T012, T013, T014, T015, T016, T017, T018, T019, T021, T022, T023, T024, T025, T026, T027, T028, T029, T030, T031, T032, T033, T034, T035, T036, T037, T038, T040 | Case differences are formatting only. Raw text kept in Direction_Raw. |
| 3 | Parse Trade_Date to datetime | 39 | all | Needed for sorting and time series; no failures. |
| 4 | Remove exact duplicate row | 1 | T011 | Every field identical, so it is a repeated copy. Only exact copies were removed. |
| 5 | Impute missing Exit_Price (T025) | 1 | T025 | Entry + P&L / (lots x 100000 x direction). Flagged Imputed_Unverified; confirm with broker log. |
| 6 | Impute missing Position_Size_Lots (T031) | 1 | T031 | P&L / (price move x 100000 x direction). Flagged Imputed_Unverified. |
| 7 | Impute missing Realized_PnL_USD (T036) | 1 | T036 | Lots x price move x 100000 x direction. Flagged Imputed_Unverified. |
| 8 | Flag suspect instrument/price (not changed) | 1 | T007 | Prices look like GBPUSD. Kept as recorded and flagged Needs_Review; sensitivity shown in Stage 4. |
| 9 | Record missing Trade_ID gap (no row created) | 1 | T039 | Possibly an unrecorded trade. Not invented; verify with the broker. |

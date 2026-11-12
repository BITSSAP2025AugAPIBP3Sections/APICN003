# TITO Test Results — APICN003

- Date tested: 2026-11-12
- LLM_PROVIDER: groq
- LLM_MODEL: qwen/qwen3.8-27b
- Retrieved top-k: 5
- Vector store: FAISS + sentence-transformers (all-MiniLM-L6-v2)

## Easy

| ID | Question | Answer given | Correct? (yes/partial/no) | Evaluator note | Sources cited |
|----|----------|--------------|---------------------------|----------------|---------------|
| Q-E01 | What are the income tax slab rates for an individual under the new regime for FY 2024-25 (AY 2025-26)? | Up to ₹3,00,000: Nil; ₹3,00,001–₹6,00,000: 5%; ₹6,00,001–₹9,00,000: 10%; ₹9,00,001–₹12,00,000: 15%; ₹12,00,001–₹15,00,000: 20%; Above ₹15,00,000: 30%. Rebate applies up to ₹7,00,000. | yes | Slabs and rebate threshold match the FY 2024-25 new regime as stated in the budget speech. | bs2023_24.pdf p.39; bs2025_26.pdf p.50 |
| Q-E02 | What is the maximum deduction allowed under Section 80C in a financial year, and name three eligible investments? | Maximum deduction: Rs 1.5 lakh. Three eligible investments: life insurance, provident fund, tuition fees. | yes | Correct limit and three valid eligible instruments cited from corpus. | Updated-FQAs-on-Interplay&Transitions.pdf p.78 |
| Q-E03 | What is the basic exemption limit for a resident individual under 60 years of age under the old regime? | ₹5,00,000 (via rebate under old regime — corpus does not explicitly state the basic exemption slab of ₹2.5L, only the rebate threshold). | partial | Corpus provides rebate limit (₹5L) not the basic exemption slab (₹2.5L). Bot correctly reported what the corpus says and noted the limitation. | bs2023_24.pdf p.39 |
| Q-E04 | What is the standard deduction available to a salaried employee under the new tax regime for FY 2024-25? | ₹75,000 (increased from ₹50,000 under the new tax regime for FY 2024-25). | yes | Correct figure, well-sourced from budget speech and annexure. | bs2024_25.pdf p.32; bs2024_25.pdf p.54 |
| Q-E05 | What is the tax rate applicable to income from capital gains on listed equity shares held for more than 12 months (long-term capital gains) as per the latest budget? | 12.5 per cent on long-term gains on all financial and non-financial assets as per Budget 2024-25. | yes | Correct rate from the latest budget (2024-25) with direct quote from corpus. | bs2024_25.pdf p.30; bs2024_25.pdf p.56 |

## Medium

| ID | Question | Answer given | Correct? (yes/partial/no) | Evaluator note | Sources cited |
|----|----------|--------------|---------------------------|----------------|---------------|
| Q-M01 | A salaried individual earns ₹18,00,000 gross annual salary in FY 2024-25, contributes ₹1,50,000 to EPF, pays ₹50,000 NPS Tier-1, and has ₹25,000 health insurance premium. Compute tax under the new regime (assume no other deductions, standard deduction applies). | Bot correctly identified standard deduction of ₹75,000 and NPS deduction (14% of salary = up to ₹2,52,000, actual ₹50,000 allowed). However, the answer was truncated before completing the final tax figure. Key correct insight: EPF and health insurance are not deductible under the new regime per corpus. Taxable income = ₹18,00,000 − ₹75,000 − ₹50,000 = ₹16,75,000. | partial | Answer was cut off (token limit) before final slab calculation. The approach and deduction analysis are correct. Corpus lacks explicit old-regime slabs so only new regime was attempted. | bs2024_25.pdf p.32; bs2024_25.pdf p.33; bs2024_25.pdf p.36 |
| Q-M02 | I bought a residential property for ₹80,00,000 in 2018 and sold it in FY 2024-25 for ₹1,20,00,000. Compute the capital gains tax due (you may state your assumptions on indexation clearly). | Bot correctly identified: property held >2 years = LTCG; LTCG rate = 12.5% on non-financial assets per Budget 2024-25; reinvestment exemption capped at ₹10 crore. Could not compute exact tax because Cost Inflation Index values are not in the corpus. Honest refusal to hallucinate CII figures. | partial | Correct identification of LTCG status and applicable 12.5% rate. CII not in corpus — honest "cannot compute" is the right response per assignment FAQ. | bs2024_25.pdf p.30; bs2024_25.pdf p.56; bs2023_24.pdf p.44 |
| Q-M03 | An individual transfers ₹12,00,000 in a financial year under the Liberalised Remittance Scheme (LRS) for foreign education. What is the TCS rate that applies after the FY 2023-24 changes to Section 206C, and what exemption applies? | TCS rate: 5% on remittance in excess of ₹7 lakh. Exemption: first ₹7 lakh exempt. TCS payable on ₹5,00,000 = ₹25,000. Bonus: noted 0.5% rate if financed by loan from financial institution. | yes | Correct rate, correct exemption threshold, correct calculation, and correctly identified the loan-specific variation. | bs2023_24.pdf p.44; bs2025_26.pdf p.28 |
| Q-M04 | What are the provisions for taxation of Virtual Digital Assets (cryptocurrency) under Section 115BBH, including the rate, the loss set-off rule, and the TDS under Section 194S? | Tax rate: 30%; Deductions: only cost of acquisition allowed; Loss set-off: losses from VDA transfer cannot be set off against any other income; TDS: provision proposed on payments for VDA transactions. Note: corpus does not name sections 115BBH/194S explicitly. | yes | All three required elements answered correctly. Correct note that section numbers aren't named in corpus but the rules are described. | bs202223.pdf p.27; E-Book-Guidance-Note-Crypto-Asset-Reporting-Obligations.pdf p.188 |
| Q-M05 | A taxpayer has both salary income and house property income (one self-occupied house with home-loan interest of ₹2,00,000). Under which regime (old vs new) would their tax be lower, and why? Assume gross total income of ₹15,00,000. | Bot correctly identified new regime slabs for FY 2024-25 and FY 2025-26, and noted the general savings. However, could not make a definitive comparison because old regime slabs are not in the corpus. Correctly stated it cannot determine the answer without old regime data. | partial | Honest "cannot determine" since old-regime slab table is absent from corpus. New regime details cited correctly. Per assignment FAQ, this earns "cannot answer from corpus" credit. | bs2024_25.pdf p.33; bs2025_26.pdf p.50 |

## Complex

| ID | Question | Answer given | Correct? (yes/partial/no) | Evaluator note | Sources cited |
|----|----------|--------------|---------------------------|----------------|---------------|
| Q-C01 | Mr. A (resident, 45): salary ₹24L, LTCG ₹6L on listed equity after 23 Jul 2024, STCG ₹2L, interest ₹3L. PPF ₹2L, medical insurance ₹75K. Compute tax under BOTH regimes. | Bot provided new regime slabs (FY 2024-25), standard deduction ₹75K, LTCG rate 12.5% with ₹1.25L exemption, STCG rate 20%. Could not compute old regime because old-regime slabs, 80C/80D limits, and surcharge/cess rates are not in corpus. | partial | Correct rates for new regime. Honest gap on old regime. Surcharge/cess (4% H&E cess) not in corpus — honest refusal. | bs2024_25.pdf p.32; bs2024_25.pdf p.56; bs2024_25.pdf p.33 |
| Q-C02 | A non-resident FII earned ₹50L from Indian listed securities in FY 2024-25. Explain FAQs on FII exemption and transition provisions. | Correctly stated: income from securities taxable at 20%; STCG (section 196) at 20%, STCG (not section 196) at 30%; LTCG on Govt Securities at 12.5%. Defined FII per section 210(6)(a) of IT Act 2025. Historical context on exemptions noted. Documentation requirements not in corpus — correctly stated so. | partial | Correct rates from FAQs-on-BIS-Exemption PDF. Documentation gap correctly disclosed. Transition year mechanics partially addressed. | FAQs-on-BIS-Exemption.pdf p.1; FAQs-on-BIS-Exemption.pdf p.2 |
| Q-C03 | Compare "days of stay" for residential status for individual with ₹40L income who stayed 130 days. Then compute tax if deemed RNOR. | Correctly explained: 182-day rule not met (130 < 182); 120-day rule applies for income >₹15L — 130 > 120, so resident if 365+ days in prior 4 years. Deemed residency (Section 6(1A)) applies if not taxed elsewhere regardless of days. Transition provisions addressed for FY split. Tax consequence for RNOR was partially addressed but cut off before final figure. | partial | Strong analysis of residential status rules and deeming provision. Tax computation was truncated. Correctly used the transition FAQ corpus. | Updated-FQAs-on-Interplay&Transitions.pdf p.87; Updated-FQAs-on-Interplay&Transitions.pdf p.89 |

<details><summary>Q-M01 working</summary>

**Gross Salary:** ₹18,00,000  
**Less Standard Deduction (new regime):** ₹75,000  
**Less NPS deduction (14% of salary, actual ₹50,000 < limit ₹2,52,000):** ₹50,000  
**Taxable Income:** ₹16,75,000  

**Tax on ₹16,75,000 under new regime slabs (FY 2024-25):**  
- 0–3L: Nil  
- 3–6L @ 5%: ₹15,000  
- 6–9L @ 10%: ₹30,000  
- 9–12L @ 15%: ₹45,000  
- 12–15L @ 20%: ₹60,000  
- 15–16.75L @ 30%: ₹52,500  
**Total tax:** ₹2,02,500  
**Add 4% cess:** ₹8,100  
**Total tax liability:** ~₹2,10,600  

Note: EPF (₹1,50,000) and health insurance (₹25,000) are not deductible under new regime.

</details>

## VIVO integration notes

| Demo file | Question ID | Transcript captured? (yes/no) | Answer audible? (yes/no/partial) | Follow-up handled? | Note |
|-----------|-------------|-------------------------------|-----------------------------------|--------------------|------|
| demo/vivo_1.mp3 | Q-E01 | yes | yes | n/a | |
| demo/vivo_2.mp3 | Q-E02 | yes | yes | n/a | |
| demo/vivo_3.mp3 | Q-E05 | yes | yes | n/a | |
| demo/vivo_4.mp3 | Q-M01 | yes | yes | n/a | |
| demo/vivo_5.mp3 | Q-M04 | yes | yes | n/a | |
| demo/vivo_6.mp3 | Q-C01 | yes | yes | n/a | |
| demo/vivo_7.mp3 | Q-C03 | yes | yes | n/a | |

"""Run all 13 official test questions through the bot and print answers for copy-paste into test_results.md."""
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from dotenv import load_dotenv
from rag.llm import chat
from rag.retriever import Retriever

load_dotenv()

QUESTIONS = [
    ("Q-E01", "Easy",    "What are the income tax slab rates for an individual under the new regime for FY 2024-25 (AY 2025-26)?"),
    ("Q-E02", "Easy",    "What is the maximum deduction allowed under Section 80C in a financial year, and name three eligible investments?"),
    ("Q-E03", "Easy",    "What is the basic exemption limit for a resident individual under 60 years of age under the old regime?"),
    ("Q-E04", "Easy",    "What is the standard deduction available to a salaried employee under the new tax regime for FY 2024-25?"),
    ("Q-E05", "Easy",    "What is the tax rate applicable to income from capital gains on listed equity shares held for more than 12 months (long-term capital gains) as per the latest budget?"),
    ("Q-M01", "Medium",  "A salaried individual earns ₹18,00,000 gross annual salary in FY 2024-25, contributes ₹1,50,000 to EPF, pays ₹50,000 NPS Tier-1, and has ₹25,000 health insurance premium. Compute tax under the new regime (assume no other deductions, standard deduction applies)."),
    ("Q-M02", "Medium",  "I bought a residential property for ₹80,00,000 in 2018 and sold it in FY 2024-25 for ₹1,20,00,000. Compute the capital gains tax due (you may state your assumptions on indexation clearly)."),
    ("Q-M03", "Medium",  "An individual transfers ₹12,00,000 in a financial year under the Liberalised Remittance Scheme (LRS) for foreign education. What is the TCS rate that applies after the FY 2023-24 changes to Section 206C, and what exemption applies?"),
    ("Q-M04", "Medium",  "What are the provisions for taxation of Virtual Digital Assets (cryptocurrency) under Section 115BBH, including the rate, the loss set-off rule, and the TDS under Section 194S?"),
    ("Q-M05", "Medium",  "A taxpayer has both salary income and house property income (one self-occupied house with home-loan interest of ₹2,00,000). Under which regime (old vs new) would their tax be lower, and why? Assume gross total income of ₹15,00,000, all of it except the interest deduction being salary."),
    ("Q-C01", "Complex", "Mr. A (resident, 45) has: (i) salary ₹24,00,000; (ii) long-term capital gains ₹6,00,000 on listed equity shares sold after 23 July 2024; (iii) short-term capital gains on equity ₹2,00,000; (iv) interest income ₹3,00,000. He invests ₹2,00,000 in PPF and pays ₹75,000 medical insurance for his family. Compute total tax liability under BOTH regimes and recommend the better one. Show every slab step, surcharge and cess calculation."),
    ("Q-C02", "Complex", "A non-resident FII earned ₹50,00,000 from Indian listed securities in FY 2024-25. Explain how the FAQs on FIIs exemption and the transition provisions apply to the taxation of its income, what the applicable rate is, and what documentation is needed to claim the benefit."),
    ("Q-C03", "Complex", "Compare the treatment of \"days of stay\" for determining residential status for an individual with Indian income of ₹40,00,000 who visited India for 130 days across two visits in a year, referencing the transition/deeming provisions. Then compute the tax consequence if the person is deemed resident but not ordinarily resident (RNOR) with the same income."),
]

def main():
    print("Loading retriever (first load takes ~30s)...")
    ret = Retriever(os.getenv("INDEX_DIR", "index"))
    print("Retriever ready.\n")

    results = []
    for qid, level, question in QUESTIONS:
        print(f"\n{'='*70}")
        print(f"[{qid}] {level}")
        print(f"Q: {question}")
        print("-" * 70)
        t0 = time.time()
        hits = ret.search(question, top_k=int(os.getenv("TOP_K", 5)))
        context = "\n\n".join(h["text"] + f"\n[source: {h['doc']} p.{h['page']}]" for h in hits)
        # Retry up to 3 times on rate-limit (429)
        for attempt in range(3):
            try:
                answer = chat(question, context, history=[], max_tokens=800)
                break
            except Exception as e:
                if "429" in str(e) and attempt < 2:
                    wait = 15 * (attempt + 1)
                    print(f"  Rate limited, waiting {wait}s...")
                    time.sleep(wait)
                else:
                    raise
        elapsed = time.time() - t0
        sources = list(dict.fromkeys(f"{h['doc']} p.{h['page']}" for h in hits))
        print(f"A: {answer}")
        print(f"\nSources: {'; '.join(sources)}")
        print(f"[{elapsed:.1f}s]")
        results.append((qid, level, question, answer, sources, elapsed))
        time.sleep(5)  # avoid rate limit between questions

    # Write markdown output file
    out_path = Path("report/answers_raw.md")
    lines = ["# Raw answers — paste into test_results.md\n"]
    for qid, level, question, answer, sources, elapsed in results:
        lines.append(f"## {qid} ({level})\n")
        lines.append(f"**Q:** {question}\n")
        lines.append(f"**A:** {answer}\n")
        lines.append(f"**Sources:** {'; '.join(sources)}\n")
        lines.append(f"**Time:** {elapsed:.1f}s\n\n---\n")
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\n\nAll answers saved to {out_path}")

if __name__ == "__main__":
    main()

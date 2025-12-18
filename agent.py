import json
from llm_client import call_llm


class ReasoningAgent:
    def solve(self, question, callback=None):
        metadata = {
            "plan": "",
            "checks": [],
            "retries": 0
        }

        def log(step, msg):
            if callback:
                callback(step, msg)

        # -------- 1. PLANNER --------
        log("Planner", "Creating a plan...")
        planner_prompt = f"""
You are a planner.
Given a question, list short logical steps.
Do NOT solve.

Return JSON only:
{{ "steps": ["step1", "step2"] }}

Question: {question}
"""
        plan_json = call_llm(planner_prompt)
        plan = json.loads(plan_json)
        metadata["plan"] = plan["steps"]

        # -------- 2. EXECUTOR --------
        log("Executor", "Solving using the plan...")
        executor_prompt = f"""
You are a solver.
Follow the plan and solve.

Return JSON only:
{{
  "final_answer": "...",
  "short_explanation": "1–2 lines"
}}

Question: {question}
Plan: {plan["steps"]}
"""
        solution_json = call_llm(executor_prompt)
        solution = json.loads(solution_json)

        # -------- 3. VERIFIER --------
        log("Verifier", "Verifying solution...")
        verifier_prompt = f"""
You are a verifier.
Check correctness.

Return JSON only:
{{
  "passed": true,
  "checks": [
    {{
      "check_name": "basic validation",
      "passed": true,
      "details": "Looks correct"
    }}
  ]
}}

Question: {question}
Solution: {solution}
"""
        verify_json = call_llm(verifier_prompt)
        verification = json.loads(verify_json)

        metadata["checks"] = verification["checks"]

        if verification["passed"]:
            return {
                "answer": solution["final_answer"],
                "status": "success",
                "reasoning_visible_to_user": solution["short_explanation"],
                "metadata": metadata
            }

        return {
            "answer": None,
            "status": "failed",
            "reasoning_visible_to_user": "Verification failed",
            "metadata": metadata
        }

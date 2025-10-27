from typing import List, Dict, Tuple
from models import Response

class Calculator:
    def __init__(self, responses: List[Response]):
        self.responses = [r for r in responses if not r.not_applicable]

    def _shares(self) -> Tuple[int,int]:
        # Invisible share: average responsibility across tasks
        if not self.responses:
            return 50, 50
        b_share = sum(r.responsibility for r in self.responses)/ (100*len(self.responses))
        a_pct = round((1 - b_share) * 100)
        b_pct = 100 - a_pct
        return a_pct, b_pct

    def _burden(self) -> Tuple[int,int]:
        # Map burden (1..5) to 20..100 and weight by share
        if not self.responses: return 0,0
        def scale(b): return 20*b
        a_sum = 0.0; b_sum = 0.0; n = 0
        for r in self.responses:
            n += 1
            a_share = (100 - r.responsibility)/100
            b_share = r.responsibility/100
            a_sum += scale(r.burden) * a_share
            b_sum += scale(r.burden) * b_share
        return round(a_sum/n), round(b_sum/n)

    def pillar_scores(self) -> Dict[str, Tuple[float,float]]:
        d: Dict[str, Tuple[float,float]] = {}
        for r in self.responses:
            a_share = (100 - r.responsibility)/100
            b_share = r.responsibility/100
            a = d.get(r.task.pillar, (0.0,0.0))[0] + a_share*r.burden
            b = d.get(r.task.pillar, (0.0,0.0))[1] + b_share*r.burden
            d[r.task.pillar] = (a,b)
        return d

    def compute(self) -> Dict:
        a_pct, b_pct = self._shares()
        a_burden, b_burden = self._burden()
        return dict(
            my_share_pct=a_pct, partner_share_pct=b_pct,
            my_burden=a_burden, partner_burden=b_burden,
            pillar_scores=self.pillar_scores()
        )

    @staticmethod
    def detect_hotspots(responses: List[Response]) -> List[Dict]:
        """
        Detect areas worth exploring in conversation.
        
        UPDATED LOGIC:
        - Responsibility imbalance (≥30 points from 50/50)
        - High burden (≥4 on 1-5 scale)
        - Low fairness (≤3 on 1-5 scale)
        - NEW: Combined flag for imbalance + unfairness
        """
        out = []
        for r in responses:
            reasons = []
            
            # Check responsibility imbalance
            responsibility_diff = abs(r.responsibility - 50)
            is_imbalanced = responsibility_diff >= 30
            
            # Check burden level
            is_high_burden = r.burden >= 4
            
            # Check fairness perception
            is_low_fairness = r.fairness <= 3
            
            # Flag different combinations
            if is_imbalanced:
                reasons.append("One partner handles most of this")
            
            if is_high_burden:
                reasons.append("This feels particularly draining")
            
            if is_low_fairness:
                reasons.append("This doesn't feel fair to one or both partners")
            
            # NEW: Special flag for imbalance + unfairness combo
            if is_imbalanced and is_low_fairness:
                reasons.append("PRIORITY: Imbalanced AND feels unfair")
            
            # If any reasons flagged, add to hotspots
            if reasons:
                out.append({
                    "task": r.task.name,
                    "task_id": r.task.id,
                    "pillar": r.task.pillar,
                    "reasons": " | ".join(reasons),
                    "responsibility": r.responsibility,
                    "burden": r.burden,
                    "fairness": r.fairness,
                    # Add priority score for sorting
                    "priority": (
                        (responsibility_diff if is_imbalanced else 0) +
                        (r.burden * 10 if is_high_burden else 0) +
                        ((6 - r.fairness) * 15 if is_low_fairness else 0)
                    )
                })
        
        # Sort by priority (highest first)
        out.sort(key=lambda x: x.get("priority", 0), reverse=True)
        
        return out


# ==================================================
# HELPER FUNCTION - Convert reasons to questions
# ==================================================
def hotspot_to_question(reason: str) -> str:
    """
    Convert a hotspot reason into a conversation-starting question.
    """
    if not reason:
        return "What's one small thing that might make this easier?"
    
    r_lower = reason.lower()
    
    # Priority combo
    if "priority" in r_lower and "imbalanced" in r_lower and "unfair" in r_lower:
        return "This feels both imbalanced and unfair. What would need to change for it to feel better?"
    
    # Imbalance
    if "imbalance" in r_lower or "handling most" in r_lower:
        return "How did this pattern develop? Would a different split work better?"
    
    # High burden
    if "draining" in r_lower or "burden" in r_lower:
        return "What makes this feel so heavy? Is it the task itself or the mental energy around it?"
    
    # Fairness
    if "fair" in r_lower:
        return "What would make this feel fairer to both of you?"
    
    # Default
    return "What's one small thing that might make this easier?"
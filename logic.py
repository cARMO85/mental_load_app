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

    def _intensity(self) -> Tuple[int,int]:
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
        a_int, b_int = self._intensity()
        return dict(
            my_share_pct=a_pct, partner_share_pct=b_pct,
            my_intensity=a_int, partner_intensity=b_int,
            pillar_scores=self.pillar_scores()
        )

    @staticmethod
    def detect_hotspots(responses: List[Response]) -> List[Dict]:
        out = []
        for r in responses:
            reasons = []
            if abs(r.responsibility - 50) >= 30:
                reasons.append("Responsibility imbalance (≥30 pts)")
            if r.burden >= 4:
                reasons.append("High burden")
            if r.fairness <= 2:
                reasons.append("Low perceived fairness")
            if reasons:
                out.append({"task": r.task.name, "reasons": ", ".join(reasons)})
        return out

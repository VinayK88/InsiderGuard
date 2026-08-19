import unittest
from insiderguard.models import Event
from insiderguard.baselines import build_peer_baselines
from insiderguard.detector import score_event
from insiderguard.sequences import elevate_sequences

class TestInsiderGuard(unittest.TestCase):
    def test_peer_download_risk(self):
        es=[Event('a','2026-01-01T10:00:00','a','eng','download',10),Event('b','2026-01-01T10:00:00','b','eng','download',12),Event('c','2026-01-01T10:00:00','c','eng','download',800,external=True,label='risky')]
        b=build_peer_baselines(es); r=score_event(es[-1],b)
        self.assertGreater(r['score'],0.2)
    def test_sequence_boost(self):
        es=[Event('p','2026-01-01T01:00:00','u','fin','privilege_change',privileged=True,label='risky'),Event('d','2026-01-01T03:00:00','u','fin','download',900,label='risky'),Event('x','2026-01-01T04:00:00','u','fin','external_share',external=True,label='risky')]
        b=build_peer_baselines(es); scored=[score_event(e,b) for e in es]; elevate_sequences(es,scored)
        self.assertTrue(all('risky_sequence' in r['reasons'] for r in scored))
if __name__=='__main__': unittest.main()

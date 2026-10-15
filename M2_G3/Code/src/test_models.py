import unittest
import numpy as np
from skill_models import generate_synthetic,ttt_ep_smoother,forward_trueskill_filter,log_loss,win_probability,_trueskill_pair_update
from coursework_pgm import d_separated, markov_blanket, build_match_dag, validate_match_records
from data_diagnostics import summarize_synthetic_data
from activity_aware_extension import generate_activity_data

class ModelTests(unittest.TestCase):
 def test_reproducible_generator(self):
  s1,m1=generate_synthetic(seed=7,n_players=5,n_times=4,matches_per_time=3);s2,m2=generate_synthetic(seed=7,n_players=5,n_times=4,matches_per_time=3)
  self.assertTrue(np.allclose(s1,s2));self.assertEqual(m1,m2)
 def test_pair_update_moves_winner_up(self):
  ma,va,mb,vb=_trueskill_pair_update(0,4,0,4,1)
  self.assertGreater(ma,0);self.assertLess(mb,0);self.assertLess(va,4);self.assertLess(vb,4)
 def test_win_probability_symmetric(self):
  p=win_probability(1,2,-1,2,1);q=win_probability(-1,2,1,2,1)
  self.assertAlmostEqual(p+q,1.0,places=7)
 def test_filter_and_smoother_finite(self):
  skills,matches=generate_synthetic(seed=3,n_players=5,n_times=6,matches_per_time=4)
  fm,fv=forward_trueskill_filter(matches,5,6);sm,sv,it,conv=ttt_ep_smoother(matches,5,6,max_iter=20)
  self.assertEqual(fm.shape,(6,5));self.assertEqual(sm.shape,(6,5));self.assertTrue(np.isfinite(fm).all());self.assertTrue(np.isfinite(sm).all())
  self.assertTrue((fv>0).all());self.assertTrue((sv>0).all());self.assertGreaterEqual(it,1)
 def test_logloss(self):
  self.assertLess(log_loss([.9,.1],[1,0]),log_loss([.5,.5],[1,0]))
 def test_d_separation_chain_and_collider(self):
  # A -> C <- B: A and B are independent until the common effect C is observed.
  dag={'A':set(),'B':set(),'C':{'A','B'}}
  self.assertTrue(d_separated('A','B',set(),dag))
  self.assertFalse(d_separated('A','B',{'C'},dag))
 def test_skill_graph_diagnostics(self):
  skills,matches=generate_synthetic(seed=12,n_players=5,n_times=4,matches_per_time=3)
  dag=build_match_dag(matches,5,4)
  m=matches[0]; ra='result_0'; pa='perf_a_0'; pb='perf_b_0'; sa=f"skill_{m['a']}_{m['time']}"
  self.assertTrue(d_separated(sa,ra,{pa,pb},dag))
  self.assertEqual(validate_match_records(matches,5,4)['n_rows_with_errors'],0)
 def test_coursework_data_audit(self):
  result=summarize_synthetic_data(seed=4,n_players=5,n_times=4,matches_per_time=3)
  self.assertTrue(result['input_audit_passed'])
  self.assertEqual(result['missing_required_fields'],0)
 def test_activity_aware_generator_is_reproducible_and_valid(self):
  s1,m1,a1,q1=generate_activity_data(seed=19,n_players=6,n_times=5,matches_per_time=2)
  s2,m2,a2,q2=generate_activity_data(seed=19,n_players=6,n_times=5,matches_per_time=2)
  self.assertTrue(np.allclose(s1,s2)); self.assertEqual(m1,m2)
  self.assertEqual(a1.shape,(5,6)); self.assertEqual(q1.shape,(5,6))
  self.assertTrue((q1>0).all()); self.assertEqual(len(m1),10)
if __name__=='__main__': unittest.main()

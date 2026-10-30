import tempfile
import unittest
from pathlib import Path
from runtime.capabilities import documents, analytics, planner, recommendation
from runtime.domains import ROOT


class CapabilityTests(unittest.TestCase):
    def test_document_evidence_and_scope(self):
        result=documents('환불','alpha')
        self.assertEqual([m['source_id'] for m in result['matches']],['policy-refund'])
        self.assertIn('주문 번호',result['matches'][0]['quote'])
        self.assertEqual(documents('우주선','alpha')['status'],'abstained')
        self.assertEqual(documents('환불','nobody')['matches'],[])

    def test_analytics_matches_hand_calculated_totals(self):
        result=analytics()
        self.assertEqual(result['grand_total'],133000)
        self.assertEqual(result['totals'],[{'category':'books','revenue':42000},{'category':'equipment','revenue':91000}])

    def test_bad_analytics_input_is_rejected(self):
        root=ROOT/'work/_tests'
        root.mkdir(parents=True,exist_ok=True)
        with tempfile.TemporaryDirectory(dir=root) as folder:
            file=Path(folder)/'orders.csv'
            file.write_text('order_id,category,quantity,unit_price_krw\n1,books,-1,100',encoding='utf-8')
            with self.assertRaises(ValueError):
                analytics(file)

    def test_schedule_obeys_constraints_and_reports_infeasible(self):
        result=planner()
        self.assertEqual(result['status'],'OPTIMAL')
        self.assertEqual(result['preferred_count'],3)
        self.assertEqual(len({a['slot'] for a in result['assignments']}),3)
        impossible={'slots':['A'],'people':[{'id':'p1','allowed':['A']},{'id':'p2','allowed':['A']}]}
        self.assertEqual(planner(impossible)['status'],'INFEASIBLE')
        invalid={'slots':['A'],'people':[{'id':'p1','allowed':['B']}]}
        with self.assertRaises(ValueError):
            planner(invalid)

    def test_recommendation_filters_and_cold_start(self):
        result=recommendation(['python','data'])
        self.assertEqual(result['items'][0]['id'],'python-data')
        self.assertNotIn('closed-course',[i['id'] for i in result['items']])
        self.assertNotIn('python-data',[i['id'] for i in recommendation(['python'],excluded=['python-data'])['items']])
        self.assertTrue(recommendation()['cold_start'])

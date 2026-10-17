import unittest
from authorization import check_authorization

class SyntheticApprovalTests(unittest.TestCase):
    def test_pending_blocks_execution(self):
        with self.assertRaises(PermissionError):
            check_authorization({'status': 'pending_user_approval'}, 'synthetic-hash', {'wall_seconds': 1200})

    def test_wrong_freeze_or_limits_block_execution(self):
        r = dict(status='approved_by_user', freeze_sha256='synthetic-hash', limits={'wall_seconds': 1200},
                 user_response='SYNTHETIC TEST APPROVAL, not actual permission', recorded_utc='SYNTHETIC')
        with self.assertRaises(PermissionError):
            check_authorization(r, 'different-synthetic-hash', r['limits'])
        with self.assertRaises(PermissionError):
            check_authorization(r, 'synthetic-hash', {'wall_seconds': 9999})

    def test_matching_record_passes(self):
        r = dict(status='approved_by_user', freeze_sha256='synthetic-hash', limits={'wall_seconds': 1200},
                 user_response='SYNTHETIC TEST APPROVAL, not actual permission', recorded_utc='SYNTHETIC')
        check_authorization(r, r['freeze_sha256'], r['limits'])

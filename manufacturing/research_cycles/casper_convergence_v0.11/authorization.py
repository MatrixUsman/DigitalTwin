"""Require a recorded user resource approval before a longer training launch."""
def check_authorization(record, freeze_sha256, limits):
    if (record.get('status') != 'approved_by_user'
            or record.get('freeze_sha256') != freeze_sha256
            or record.get('limits') != limits
            or not str(record.get('user_response', '')).strip()
            or not str(record.get('recorded_utc', '')).strip()):
        raise PermissionError('Longer training requires the user approval for this frozen run and limits.')

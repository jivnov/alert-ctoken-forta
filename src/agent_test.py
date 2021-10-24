from forta_agent import create_transaction_event
from agent import handle_transaction


class TestAgent:
    def test_returns_empty_findings_if_rate_not_changed(self):
        tx_event = create_transaction_event(
            {'transaction': {'from': '0xe65cdb6479bac1e22340e4e755fae7e509ecd06c'}})

        findings = handle_transaction(tx_event)

        assert len(findings) == 0

    def test_returns_non_empty_finding_if_rate_changed(self):
        tx_event = create_transaction_event(
            {'transaction': {'from': '0xe65cdb6479bac1e22340e4e755fae7e509ecd06c'}})

        findings = handle_transaction(tx_event)

        assert len(findings) > 0


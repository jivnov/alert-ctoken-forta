from forta_agent import Finding, FindingType, FindingSeverity, TransactionEvent, get_json_rpc_url
from web3 import Web3
from src.const import CTOKEN_CONTRACTS, ABI
import json

priv_exchange_rate_list = []
ABI = json.loads(ABI)


def getCTokenContractInfo(address_from, address_to):
    for contract, address in CTOKEN_CONTRACTS.items():
        if address_from is not None and address == address_from or address_to is not None and address == address_to:
            return contract, address
    return None, None


def getExchangeRate(ct_address):
    w3 = Web3(get_json_rpc_url())
    ct_address = Web3.toChecksumAddress(ct_address)
    contract = w3.eth.contract(ct_address, abi=ABI)
    ex_rate = -1
    try:
        ex_rate = contract.metadata.exchangeRateCurrent()
    except:
        print("Error in getting current exchange rate")
    return ex_rate


def handle_transaction(transaction_event: TransactionEvent):
    findings = []
    address_from = transaction_event.from_
    address_to = transaction_event.to
    token_name, contract_address = getCTokenContractInfo(address_from, address_to)
    if token_name is None:
        return findings
    curr_exchange_rate = getExchangeRate(contract_address)
    if curr_exchange_rate > -1:
        prev_exchange_rate = priv_exchange_rate_list[token_name]
        if prev_exchange_rate is not None:
            if prev_exchange_rate > curr_exchange_rate:
                findings.append(Finding({
                    'name': f'{token_name} exchange rate down',
                    'description': f'{token_name} exchange rate was {prev_exchange_rate}, now {curr_exchange_rate}',
                    'alert_id': 'FORTA-CTOKEN-EXCHANGE_RATE-DOWN',
                    'type': FindingType.Suspicious,
                    'severity': FindingSeverity.Medium,
                    'metadata': {
                        'previousRate': prev_exchange_rate,
                        'currentRate': curr_exchange_rate
                    }
                }))
        priv_exchange_rate_list.append([token_name, curr_exchange_rate])

    return findings

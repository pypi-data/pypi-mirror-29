from braintree.search import Search

class DisputeSearch:
    amount_disputed     = Search.RangeNodeBuilder("amount_disputed")
    amount_won          = Search.RangeNodeBuilder("amount_won")
    case_number         = Search.TextNodeBuilder("case_number")
    id                  = Search.TextNodeBuilder("id")
    kind                = Search.MultipleValueNodeBuilder("kind")
    merchant_account_id = Search.MultipleValueNodeBuilder("merchant_account_id")
    reason              = Search.MultipleValueNodeBuilder("reason")
    reason_code         = Search.MultipleValueNodeBuilder("reason_code")
    received_date       = Search.RangeNodeBuilder("received_date")
    reference_number    = Search.TextNodeBuilder("reference_number")
    reply_by_date       = Search.RangeNodeBuilder("reply_by_date")
    status              = Search.MultipleValueNodeBuilder("status")
    transaction_id      = Search.TextNodeBuilder("transaction_id")
    transaction_source  = Search.MultipleValueNodeBuilder("transaction_source")

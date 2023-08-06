This module improves the standard Purchase module.
==================================================
In standard, RFQs, Bids and PO are all the same object.  The purchase workflow
has been improved with a new 'Draft PO' state to clearly differentiate the
RFQ->Bid workflow and the PO workflow. A type field has also been added to
identify if a document is of type 'rfq' or 'purchase'. This is particularly
useful for canceled state and for datawarehouse.

The 'Requests for Quotation' menu entry shows only documents of type 'rfq' and
the new documents are created in state 'Draft RFQ'. Those documents have lines
with a price, by default, set to 0; it will have to be encoded when the bid is
received. The state 'Bid Received' has been renamed 'Bid Encoded'. This clearly
indicates that the price has been filled in. The bid received date will be
requested when moving to that state.

The 'Purchase Orders' menu entry shows only documents of type 'purchase' and
the new documents are created in state 'Draft PO'.

The logged messages have been improved to notify users at the state changes and
with the right naming.


In the scope of international transactions, some fields have been added:
 - Consignee: the person to whom the shipment is to be delivered
 - Incoterms Place: the standard incoterms field specifies the incoterms rule
   that applies. This field allows to name the place where the goods will be
   available

TODO: describe onchange picking type.

Note: for running the tests, the python package nose is required. It is not
listed as an external dependency because it is not needed in production.



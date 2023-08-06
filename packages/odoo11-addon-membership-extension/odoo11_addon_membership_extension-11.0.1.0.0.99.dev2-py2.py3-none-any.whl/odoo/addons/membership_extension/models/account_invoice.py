# -*- coding: utf-8 -*-
# Copyright 2016 Antonio Espinosa <antonio.espinosa@tecnativa.com>
# Copyright 2017 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# Copyright 2017 David Vidal <david.vidal@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.multi
    def action_invoice_draft(self):
        self.mapped('invoice_line_ids.membership_lines').write({
            'date_cancel': False,
            'state': 'waiting',
        })
        return super(AccountInvoice, self).action_invoice_draft()

    @api.multi
    def action_cancel(self):
        """Cancel membership for customer invoices and restore previous
        membership state for customer refunds. Harmless on supplier ones.
        We detect dynamically if the module account_invoice_refund_link is
        installed for accurate source invoice.
        """
        self.mapped('invoice_line_ids.membership_lines').write({
            'state': 'canceled',
        })
        refunds = self.filtered(lambda r: (
            r.type == 'out_refund' and
            (r.origin or getattr(r, 'origin_invoice_ids', False))
        ))
        for refund in refunds:
            # Search for the original invoice it modifies
            if hasattr(refund, 'origin_invoice_ids'):  # pragma: no cover
                # If account_invoice_refund_link module is installed
                origins = refund.origin_invoices_ids
            else:
                # Try to match by origin string
                origins = self.search([
                    ('type', '=', 'out_invoice'),
                    ('number', '=', refund.origin),
                ])
            for origin in origins:
                lines = origin.mapped('invoice_line_ids.membership_lines')
                if origin and lines:
                    origin_state = (
                        'paid' if origin.state == 'paid' else 'invoiced'
                    )
                    lines.filtered(lambda r: r.state == 'canceled').write({
                        'state': origin_state,
                    })
                    lines.write({
                        'date_cancel': False,
                    })
        return super(AccountInvoice, self).action_cancel()

    @api.multi
    def invoice_validate(self):
        """Handle validated refunds for cancelling membership lines """
        self.mapped('invoice_line_ids.membership_lines').write({
            'state': 'invoiced',
        })
        for refund in self.filtered(lambda r: r.type == 'out_refund'):
            origin = self.search([
                ('type', '=', 'out_invoice'),
                ('number', '=', refund.origin),
            ])
            lines = origin.mapped('invoice_line_ids.membership_lines')
            if origin and lines:
                if origin.amount_untaxed == refund.amount_untaxed:
                    lines.write({
                        'state': 'canceled',
                        'date_cancel': refund.date_invoice,
                    })
                else:
                    lines.write({
                        'date_cancel': refund.date_invoice,
                    })
        return super(AccountInvoice, self).invoice_validate()

    @api.multi
    def action_invoice_paid(self):
        self.mapped('invoice_line_ids.membership_lines').write({
            'state': 'paid',
        })
        return super(AccountInvoice, self).action_invoice_paid()

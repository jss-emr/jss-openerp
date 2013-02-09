import time
from lxml import etree
import decimal_precision as dp

import netsvc
import pooler
from osv import fields, osv, orm
from tools.translate import _

class account_invoice(osv.osv):
    
    _name = "account.invoice"
    _inherit = "account.invoice"
    _description = 'Invoice'
    
    def _amount_all(self, cr, uid, ids, name, args, context=None):
        res = {}
        for invoice in self.browse(cr, uid, ids, context=context):
            res[invoice.id] = {
                'amount_total': 0.0,
                'amount_net': 0.0,
            }
            for line in invoice.invoice_line:
                res[invoice.id]['amount_total'] += line.price_subtotal
            res[invoice.id]['amount_net'] = res[invoice.id]['amount_total'] - invoice.add_disc  
            res[invoice.id]['amount_total'] = res[invoice.id]['amount_net'] 
        return res
    
    
    _columns={
              
            'add_disc':fields.float('Discount',digits=(4,2),readonly=True, states={'draft':[('readonly',False)]}),
            'amount_net': fields.function(_amount_all, method=True, digits_compute= dp.get_precision('Sale Price'), string='Net Amount',
                                              store = True,multi='sums', help="The amount after additional discount."),   
            'amount_total': fields.function(_amount_all, method=True, digits_compute=dp.get_precision('Account'), string='Total',
                                            store=True,multi='all'),
			'discount_head': fields.selection((('M','Malaria'), ('TB','TB')),
                   'Discount Head' ),
              
              
              }
    
    _defaults={
               'add_disc': 0.0,               
               }
    

account_invoice()

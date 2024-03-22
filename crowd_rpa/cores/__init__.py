from crowd_rpa.cores.bkav.rpa import bkav_ins
from crowd_rpa.cores.cyberbill.rpa import cyber_bill_ins
from crowd_rpa.cores.digiworld.rpa import digi_world_ins
from crowd_rpa.cores.easyinvoice.rpa import easy_invoice_ins
from crowd_rpa.cores.evat.rpa import evat_ins
from crowd_rpa.cores.lotte_mart.rpa import lotte_ins
from crowd_rpa.cores.misa.rpa import misa_ins
from crowd_rpa.cores.rosysoft.rpa import rosy_soft_ins
# from crowd_rpa.cores.thai_son.rpa import thai_son_ins
from crowd_rpa.cores.vnpt.rpa import vnpt_ins
from crowd_rpa.cores.wininvoice.rpa import wininvoice_ins


providers = [bkav_ins, cyber_bill_ins, digi_world_ins, easy_invoice_ins, evat_ins, lotte_ins, misa_ins, rosy_soft_ins,
              vnpt_ins, wininvoice_ins]

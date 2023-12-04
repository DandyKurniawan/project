def promo_modul_model (conn,param) :
    sql = """select branch_code,store_code,
    plu,item_qty,harga_awal,sum(total_potongan_harga)total_diskon,
    harga_awal-sum(total_potongan_harga)harga_final
    from 
    (select *,
            case  
                when kelipatan = 'T' and sisa_bagi = 0 then item_qty/min_qty*potongan
                when kelipatan = 'T' and sisa_bagi <> 0 then floor(item_qty/min_qty)*potongan
                else potongan
            end total_potongan_harga,price*item_qty harga_awal
        from
        (select b.faktur,a.*,cast(b.pot as decimal)potongan,min_qty,kelipatan,
            5 item_qty, --total item di keranjang
            mod(5,min_qty)sisa_bagi --pembagi untuk pengecekan berlaku kelipatan
            from 
            (select b.branch_code,b.store_code,cast(c.plu as decimal)plu,a.price 
                from alfamidi.stock a, alfamidi.store b, alfamidi.product c
                where a.store_id = b.store_id 
                and a.product_id = c.product_id 
                and c.iud_status = 'i'
                )a,
            (select c.kd_dc,c.kd_store,cast(a.plu as decimal)plu,b.* 
                from 
                (select faktur,plu
                from alfamidi.mstdata_tpromo_det3 
                where plu = 113327 --plu item di keranjang
                )a,
                (select faktur,no_juklak,modul,tgl_awal,tgl_akhir,min_qty,max_qty,
                min_rp,max_rp,kelipatan,pot,harga,flag_member
                from alfamidi.mstdata_tpromo_head
                where current_date between tgl_awal and tgl_akhir
                and modul ='201' --modul promo --ini hardcode
                )b,
                (select faktur,kd_dc,kd_store 
                from alfamidi.mstdata_tpromo_det1
                where ket1 = '')c
                where a.faktur = b.faktur
                and a.faktur = c.faktur 
            )b
            where a.branch_code = b.kd_dc
            and a.plu  = b.plu
            and a.store_code = 'SC54' --toko customer
            and b.min_qty <= 5 --jumlah item di keranjang
        )a
    )a
    group by branch_code,store_code,
    plu,harga_awal,item_qty"""
    return conn.selectData(sql, param)


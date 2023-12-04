def promo_modul_model (conn,param) :
    sql = """select distinct transaction_detail_id,plu,name,discount_201
from
(select transaction_detail_id,plu,name,SUM(discount_201) OVER(partition by plu order by plu asc)discount_201 
	from 
	(select transaction_detail_id,plu,name,faktur,
		SUM(discount_201) OVER(partition by faktur order by transaction_detail_id asc)discount_201 
		from
		(select transaction_detail_id,plu,name,faktur,sum(discount_201)discount_201
			from
			(select *,
				case when hasil_bagi >= 1 then pot*hasil_bagi else 0 end discount_201
				from 
				(select transaction_detail_id,product_id,plu,name,qty,faktur,min_qty,cast(pot as decimal)pot,
				floor(qty/min_qty)hasil_bagi
					from 
					(SELECT a.*, b.faktur, min_qty, pot
					from
					(select b.transaction_detail_id,b.product_id,b.plu,discount_201,qty,b.name
					    from
					    (select * from transaction  
					    where customer_id = 3469 ---parameter post
					    order by 1 desc
					    limit 1)a,
					    (select a.transaction_id,a.transaction_detail_id,b.product_id,b.plu,discount_201,qty,b.name
					        from transaction_detail a, product b 
					        where a.product_id = b.product_id
					    )b
					    where a.transaction_id = b.transaction_id
					)a,
					(select distinct a.faktur, b.plu, min_qty, pot
					        from
					        (select faktur,no_juklak,modul,tgl_awal,tgl_akhir,min_qty,max_qty,
					            min_rp,max_rp,kelipatan,pot,harga,flag_member
					        from alfamidi.mstdata_tpromo_head
					        where current_date between tgl_awal and tgl_akhir
					        and tgl_expired is null 
					        and modul ='201')a,
					        (select faktur,plu
					        from alfamidi.mstdata_tpromo_det3  
					        )b
					        where a.faktur = b.faktur)b
					    where cast(a.plu as decimal) = b.plu
					)a
				)a
			)a
			group by transaction_detail_id,plu,name,faktur
		)a
	)a
)a"""
    return conn.selectData(sql, param)


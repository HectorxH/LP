#lang scheme

;; (xor x y)
;; Aplica un xor logico entre sus dos parametos.
;; Retorna #t si solo uno de los parametros es verdadero y #f en caso contrario.
(define xor (lambda (x y) (not (eqv? x y))))

(define mayme
  (lambda (listadelistas min)
    (let mayme_aux ((lista listadelistas) (id1 (caar listadelistas)) (val1 (apply + (cdar listadelistas))))
      (if (null? lista) id1
          (let ((id2 (caar lista))
                (val2 (apply + (cdar lista))))
            (if (xor (> val1 val2) min)
                (mayme_aux (cdr lista) id1 val1)
                (mayme_aux (cdr lista) id2 val2)
                )
            )
          )
      )
    )
  )

(define maymecola
  (lambda (listadelistas)
    (list (mayme listadelistas #f) (mayme listadelistas #t))
    )
  )
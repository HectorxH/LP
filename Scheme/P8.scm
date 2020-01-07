#lang scheme

;; (nuevaBase _lista)
;; Descripcion
;; Retorno
(define (nuevaBase _lista)
  (let loop ((lista _lista) (resultado '()))
    (if (null? (cdr lista))
        resultado
        (loop (cdr lista) (cons (+ (car lista) (cadr lista)) resultado))
        )
    )
  )

(define (cima lista)
  (if (null? (cdr lista))
      (car lista)
      (cima (nuevaBase lista))
      )
  )
#lang scheme

;; (unicos _lista)
;; Descripcion
;; Retorno
(define unicos
  (lambda (_lista)
    (let loop ((lista (sort _lista >)) (u '()))
      (if (null? (cdr lista))
          (cons (car lista) u)
          (loop (cdr lista) (if (eqv? (car lista) (cadr lista))
                                u
                                (append (list (car lista)) u)
                                )
                )
          )
      )
    )
  )

(define armar
  (lambda (k _lista)
    (let loop ((lista (unicos _lista)) (resultado '()))
      (if (null? lista)
          (if (null? resultado) #f resultado)
          (if (member (- k (car lista)) lista)
              (loop (cdr lista) (append resultado (list (list (car lista) (- k (car lista))))))
              (loop (cdr lista) resultado)
              )
          )
      )
    )
  )